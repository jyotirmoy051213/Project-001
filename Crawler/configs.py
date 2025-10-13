"""
This script has all CONFIGURATION SETTINGS TO RUN CRAWLER FROM main.py
Change configuration based on website & crawling strategy
"""

import os, csv, json, asyncio
from pydantic import BaseModel
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, JsonCssExtractionStrategy, CacheMode
import pandas as pd

## CONTROL VARIABLES
TEST_MODE = False
RETRY_ATTEMPTS = 5
RETRY_DELAY = 7
BATCH_SIZE = 100
DELAY_TIME = 18
START_FROM_PHONE = 6785
MAIN_FILE= "D:/My Codes/Projects/Project-001/Database/gsmarena_phonespecs.csv"
TEST_FILE= "D:/My Codes/Projects/Project-001/Crawler/trials/test_csv.csv"
PHONE_LIST_FILE = "D:/My Codes/Projects/Project-001/Database/gsmarena_products.csv"



## STRATEGY & CONFIGURATION
# Handcrafted schema for JsonCssExtractionStrategy by inspecting the webpage
SCHEMA_FOR_EXTRACTION = {
        "name": "Product",
        "baseSelector": ".makers",            
        "fields": [
            {"name": "model", "selector": ".makers li", "type": "list", "fields": [{"name": "model", "type": "text"}]},
            {"name": "model", "selector": ".makers a", "type": "list", "fields": [{"name": "model", "type": "attribute", "attribute": "href"}]}
            ]    
        }

# PYDANTIC SCHEMA FOR LLM-BASED EXTRACTION STRATEGY
class Products(BaseModel):
    category : str
    name : str
    image_url : str
    description : str
    price : int
    url : str

def get_browser_config():
    return BrowserConfig(
        browser_type='chromium',
        headless=False,
        verbose=True,
        proxy_config={"server": "socks5://104.248.197.67:1080"}
    ) 

def get_crawler_config():
    return CrawlerRunConfig(
            session_id="project-002",
            cache_mode=CacheMode.BYPASS,
            table_score_threshold=5
        )


## OUTPUT
class Output_Pipeline:
    def __init__(self):
        self.test_mode : bool = TEST_MODE
        self.retry_attempts : int = RETRY_ATTEMPTS
        self.retry_delay : int = RETRY_DELAY
        self.current_counter : int = 0
        self.total_counter : int = 0
        self.batch_size : int = BATCH_SIZE
        self.filename  = TEST_FILE if TEST_MODE else MAIN_FILE
        self.phone_list_file = PHONE_LIST_FILE
        self.phone_list : list[dict] = []
        self.start_from_phone : int = START_FROM_PHONE
        self.buffer : list[dict] = []
        self.master_columns : list[str] = []
        self.delay_time = DELAY_TIME

    @property
    def url(self):
        return self.phone_list[self.current_counter]['URL']

    
    async def __call__(self, crawler):
        """Construct list of phones from file"""
        if not self.phone_list or self.current_counter >= len(self.phone_list):
            print("FETCHING NEW BATCH.") 
            self.phone_list_reader(self.batch_size)
            self.current_counter = 0
            
            if not self.phone_list:
                print("NO MORE PHONES TO SCRAPE.")
                self.flush()
                return False
 
        for attempt in range(self.retry_attempts):
            print(f"Accessing URL. Attempt: {attempt + 1}")
            result = await crawler.arun(
                url = self.url,
                config=get_crawler_config()
                )
            if result.success:
                print("URL Accessed.")
                break
            print(f"Can't Access URL. Waiting {self.retry_delay} seconds for next attempt.")
            await asyncio.sleep(self.retry_delay)

        if not result.success:
            print("STATUS: CRAWLING ERROR!!")
            self.flush()
            return False
        print("STATUS: CRAWLING SUCCESSFUL.")
        if not result.tables:
            print(f"No Data Found.")
            self.flush()
            return False
        print(f"DATA EXTRACTION COMPLETED.")
        self.organize_result(result.tables)
        await asyncio.sleep(self.delay_time)
        return True
    
    def phone_list_reader(self, batch_size):
        self.phone_list.clear()
        self.current_counter = 0
        
        with open(self.phone_list_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for _ in range(self.start_from_phone - 1): ## AS DICTREADER BY DEFAULT SKIPS A ROW IF NO FIELDNAME IS GIVEN
                next(reader, None) # SKIPPING

            for _ in range(batch_size):
                try:
                    phone_data = next(reader)
                    if not phone_data.get('URL'):
                        break
                    self.phone_list.append(phone_data)
                    self.start_from_phone += 1
                except StopIteration:
                    break
            if self.phone_list:
                print(f"{len(self.phone_list)} PHONE LINKS LOADED IN MEMORY FOR CRAWLING.")
    
    def organize_result(self, tables):
        brand = self.phone_list[self.current_counter]['Brand']
        model = self.phone_list[self.current_counter]['Model']
        flat_dict = {"Brand": brand, "Model": model}
        for table in tables:
            section = table['headers'][0]
            for row in table['rows']:
                if not row[0]:  # skip empty keys
                    continue
                key = f"{section}_{row[0]}".strip()
                value = row[1].strip()
                flat_dict[key] = value
        print(f"STORING IN MEMORY: Brand-{brand}, Model-{model}")
        return self.store_in_memory(flat_dict)
        
    def store_in_memory(self, flat_dict : dict):
        """Add a scraped record"""
        self.buffer.append(flat_dict)

        """Add new keys in the master column"""
        for key in flat_dict.keys():
            if key not in self.master_columns:
                """key alone is just a 'string',
                {key} is a set containing that string: {'string'}"""
                self.master_columns = sorted(
                    set(self.master_columns) | {key}
                    )
        self.current_counter += 1
        self.total_counter += 1
        print(f"CURRENT BUFFER: {self.current_counter} PHONE SPECS STORED IN MEMORY.")
        print(f"TOTAL {self.total_counter} PHONE SPECS WRITTEN SO FAR.")
        if len(self.buffer) == self.batch_size or self.test_mode:
            self.flush()
    
    def flush(self):
        self.phone_list.clear()
        self.current_counter = 0
        """write buffers to csv"""
        if not self.buffer:
            print("NO PHONE SPECS IN MEMORY TO WRITE.")
            return
        print(f"WRITING {len(self.buffer)} PHONE SPECS FROM MEMORY.")
        """Create a new dataframe first with buffered data"""
        df_new = pd.DataFrame(self.buffer)

        try:
            """check for existing file to resume writing"""
            df_existing = pd.read_csv(self.filename)
            all_columns = list(
                set(df_existing.columns) | set(df_new.columns)
            )
            
            """Putting Brand and Model as Column No 1 & 2"""
            PRIORITY = ['Brand', 'Model']
            priority_columns = [col for col in PRIORITY]
            remaining_columns = sorted([col for col in all_columns if col not in priority_columns])
            reordered_columns = (priority_columns + remaining_columns)
            
            """Reindex both dataframes to ensure same columns"""
            df_existing = df_existing.reindex(columns=reordered_columns)
            df_new = df_new.reindex(columns=reordered_columns)

            """Concatenate and save"""
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(self.filename, index=False)

        except FileNotFoundError:
            """First time writing: Save new data"""
            df_new = df_new.reindex(columns=self.master_columns)
            df_new.to_csv(self.filename, index=False)
        print(f"{len(self.buffer)} PHONE SPECS WRITTEN IN DATABASE.")
        self.buffer.clear()

        
    """Final Log"""
    def final_log(self):
        print("CRAWLING COMPLETE.")
        print(f"Total {self.total_counter} information added to Database.")