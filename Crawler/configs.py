"""
This script has all CONFIGURATION SETTINGS TO RUN CRAWLER FROM main.py
Change configuration based on website & crawling strategy
"""

import os, csv, json, asyncio, sqlite3
from pydantic import BaseModel
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, JsonCssExtractionStrategy, CacheMode
import pandas as pd

## CONTROL VARIABLES
TEST_MODE = True
MAX_TEST_RUN_COUNT = 3
RETRY_ATTEMPTS = 5
RETRY_DELAY = 7
DELAY_TIME = 18
MAIN_FILE= "D:/My Codes/Projects/Project-001/Database/gsmarena_phones.db"
TEST_FILE= "D:/My Codes/Projects/Project-001/Crawler/trials/test.db"
URLS_TO_CRAWL = [
    {"brand": "Samsung", "url": "https://www.gsmarena.com/samsung-phones-f-9-0-p.php"},
    {"brand": "Apple", "url": "https://www.gsmarena.com/apple-phones-f-48-0-p.php"},
    {"brand": "Huawei", "url": "https://www.gsmarena.com/huawei-phones-f-58-0-p.php"},
    {"brand": "Nokia", "url": "https://www.gsmarena.com/nokia-phones-f-1-0-p.php"},
    {"brand": "Sony", "url": "https://www.gsmarena.com/sony-phones-f-7-0-p.php"},
    {"brand": "LG", "url": "https://www.gsmarena.com/lg-phones-f-20-0-p.php"},
    {"brand": "HTC", "url": "https://www.gsmarena.com/htc-phones-f-45-0-p.php"},
    {"brand": "Motorola", "url": "https://www.gsmarena.com/motorola-phones-f-4-0-p.php"},
    {"brand": "Lenovo", "url": "https://www.gsmarena.com/lenovo-phones-f-73-0-p.php"},
    {"brand": "Xiaomi", "url": "https://www.gsmarena.com/xiaomi-phones-f-80-0-p.php"},
    {"brand": "Google", "url": "https://www.gsmarena.com/google-phones-f-107-0-p.php"},
    {"brand": "Honor", "url": "https://www.gsmarena.com/honor-phones-f-121-0-p.php"},
    {"brand": "Oppo", "url": "https://www.gsmarena.com/oppo-phones-f-82-0-p.php"},
    {"brand": "Realme", "url": "https://www.gsmarena.com/realme-phones-f-118-0-p.php"},
    {"brand": "OnePlus", "url": "https://www.gsmarena.com/oneplus-phones-f-95-0-p.php"},
    {"brand": "Nothing", "url": "https://www.gsmarena.com/nothing-phones-f-128-0-p.php"},
    {"brand": "vivo", "url": "https://www.gsmarena.com/vivo-phones-f-98-0-p.php"},
    {"brand": "Meizu", "url": "https://www.gsmarena.com/meizu-phones-f-74-0-p.php"},
    {"brand": "Asus", "url": "https://www.gsmarena.com/asus-phones-f-46-0-p.php"},
    {"brand": "Alcatel", "url": "https://www.gsmarena.com/alcatel-phones-f-5-0-p.php"},
    {"brand": "ZTE", "url": "https://www.gsmarena.com/zte-phones-f-62-0-p.php"},
    {"brand": "Microsoft", "url": "https://www.gsmarena.com/microsoft-phones-f-64-0-p.php"},
    {"brand": "Umidigi", "url": "https://www.gsmarena.com/umidigi-phones-f-135-0-p.php"},
    {"brand": "Coolpad", "url": "https://www.gsmarena.com/coolpad-phones-f-105-0-p.php"},
    {"brand": "Oscal", "url": "https://www.gsmarena.com/oscal-phones-f-134-0-p.php"},
    {"brand": "Sharp", "url": "https://www.gsmarena.com/sharp-phones-f-23-0-p.php"},
    {"brand": "Micromax", "url": "https://www.gsmarena.com/micromax-phones-f-66-0-p.php"},
    {"brand": "Infinix", "url": "https://www.gsmarena.com/infinix-phones-f-119-0-p.php"},
    {"brand": "Ulefone", "url": "https://www.gsmarena.com/ulefone-phones-f-124-0-p.php"},
    {"brand": "Tecno", "url": "https://www.gsmarena.com/tecno-phones-f-120-0-p.php"},
    {"brand": "Doogee", "url": "https://www.gsmarena.com/doogee-phones-f-129-0-p.php"},
    {"brand": "Blackview", "url": "https://www.gsmarena.com/blackview-phones-f-116-0-p.php"},
    {"brand": "Cubot", "url": "https://www.gsmarena.com/cubot-phones-f-130-0-p.php"},
    {"brand": "Oukitel", "url": "https://www.gsmarena.com/oukitel-phones-f-132-0-p.php"},
    {"brand": "Itel", "url": "https://www.gsmarena.com/itel-phones-f-131-0-p.php"},
    {"brand": "TCL", "url": "https://www.gsmarena.com/tcl-phones-f-123-0-p.php"},  
]




## STRATEGY & CONFIGURATION
# Handcrafted schema for JsonCssExtractionStrategy by inspecting the webpage
SCHEMA_FOR_EXTRACTION = {
        "name": "Product",
        "baseSelector": ".makers",            
        "fields": [
            {"name": "old_name", "selector": ".makers a", "type": "list", "fields": [{"name": "old_name", "type": "attribute", "attribute": "href"}]},
            {"name": "new_name", "selector": ".makers span", "type": "list", "fields": [{"name": "new_name", "type": "text"}]},
            {"name": "image", "selector": ".makers img", "type": "list", "fields": [{"name": "image_url", "type": "attribute", "attribute": "src"}]}
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
        proxy_config={"server": "https://152.42.170.187:9090"}
    ) 

def get_crawler_config():
    return CrawlerRunConfig(
            css_selector=".makers",
            session_id="project-002",
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=JsonCssExtractionStrategy(SCHEMA_FOR_EXTRACTION),
        )


## OUTPUT
class Output_Pipeline:
    def __init__(self):
        self.test_mode : bool = TEST_MODE
        self.test_run_count : int = 0
        self.max_test_run_count : int = MAX_TEST_RUN_COUNT
        self.retry_attempts : int = RETRY_ATTEMPTS
        self.retry_delay : int = RETRY_DELAY
        self.delay_time = DELAY_TIME
        self.checkpoint_found = False
        self.filename  = TEST_FILE if TEST_MODE else MAIN_FILE
        self.table_name = "GSMarena Products"
        self.url_list = URLS_TO_CRAWL
        self.current_crawl : int = 0
        self.base_url : str = f"{self.url_list[self.current_crawl]['url']}"[:-4] if self.url_list else ""
        self.page_number : int = 1
        self.write_counter : int = 0
        self.total_counter : int = 0
        

    @property
    def url(self) -> str:
        return self.base_url + f"{self.page_number}.php"

 
    async def __call__(self, crawler : object) -> bool:
        # TRY TO FIND CHECKPOINT TO RESUME CRAWLING
        if not self.checkpoint_found:
            print("Finding Checkpoint to Resume.")
            self.checkpoint_found = self.find_checkpoint()
        

        if self.checkpoint_found and self.current_crawl < len(self.url_list):
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
                return False
            print("STATUS: CRAWLING SUCCESSFUL.")
            extracted_data = json.loads(result.extracted_content)
            
            if not extracted_data:
                print(f"No products found in Page {self.page_number}.")
                self.current_crawl += 1
                self.page_number = 1
                return False
        
            self.organize_result(extracted_data)

            # CONTROL FOR TEST MODE
            if self.test_mode:
                self.test_run_count += 1
                print(f"TEST MODE: TEST RUN NO.{self.test_run_count}/{self.max_test_run_count} SUCCESSFUL.")
                if self.test_run_count == self.max_test_run_count:
                    return False

            await asyncio.sleep(self.delay_time)
            return True
        else:
            print("No URL Left to Crawl.")
            return False
    
    # ACCESS DATABASE (CREATE IF NONE EXISTS), READ THE LAST ROW, SET CURRENT_CRAWL & PAGE_NUMBER 
    # ONLY RUN ONCE WHEN THE PROGRAM STARTS, ALWAYS RETURNS TRUE TO PREVENT FURTHER CALLING
    def find_checkpoint(self) -> True: 
        # CHECK IF THE FILE EXISTS
        if not os.path.exists(self.filename):
            print("No File Exists. Frest Start.")
            self.current_crawl = 0
            self.page_number = 1
            return True
        
        # FETCH LAST INSERTED ROW AS DICTIONARY
        conn = sqlite3.connect(self.filename)
        conn.row_factory = sqlite3.Row  # Makes rows behave like dictionaries
        cur = conn.cursor()
        try:
            query_last_row = f'SELECT * FROM "{self.table_name}" ORDER BY rowid DESC LIMIT 1'
            cur.execute(query_last_row)
            row = cur.fetchone()

            query_row_count = f'SELECT COUNT(*) FROM "{self.table_name}"'
            cur.execute(query_row_count)
            self.total_counter = cur.fetchone()[0]
        except sqlite3.OperationalError as e:
            if "no such table" in str(e):
                print(f"Table '{self.table_name}' not found.")
            else:
                print(f"Operational error: {e}")
            row = None

        finally:    
            conn.close()

        # IF LAST ROW IS FOUND EMPTY, THEN SET INITIALIZING VALUE
        if row is None:
            self.current_crawl = 0
            self.page_number = 1
            print("No Earlier Checkpoint Found. Fresh Start.")
            return True
        
        last_written_phone = dict(row)
                
        # FIND CURRENT_CRAWL & PAGE_NUMBER FROM LAST ROW
        self.page_number = int(last_written_phone['Page_Number']) + 1
        for index, dicts in enumerate(self.url_list):
            if dicts.get("brand") == last_written_phone['Brand']:
                self.current_crawl = index
                break # STOP WHEN FOUND
        
        print(f"Checkpoint Found. Last written: Brand-{last_written_phone['Brand']}, Page-{self.page_number}")
        return True
    

    
    def organize_result(self, extracted_data : list):
        """
        FORMAT OF EXTRACTED DATA : LIST OF A SINGLE DICT WHOSE VALUES ARE LIST OF DICTIONARIES
        extracted_data = [
        {
            "old_name": [
            {"old_name": "samsung_galaxy_m17_5g-14221.php"},
            {"old_name": "samsung_galaxy_f07-14205.php"},
            # ...
            ],
            "new_name": [
            {"new_name": "Galaxy M17"},
            {"new_name": "Galaxy F07"},
            # ...
            ],
            "image": [
            {"image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-a17.jpg"},
            {"image_url": "https://fdn2.gsmarena.com/vv/bigpic/samsung-galaxy-f07.jpg"},
            # ...
            ]
        }
        ]
        """
        new_records : list = []
        # ACCESS THE VALUES (LIST OF DICTS) OF THE OUTER DICTIONARY
        old_name_entries : list[dict] = extracted_data[0].get("old_name", [])
        new_name_entries : list[dict] = extracted_data[0].get("new_name", [])
        image_entries : list[dict] = extracted_data[0].get("image", [])

        # ZIP TO ACCESS ALL 3 LISTS SIMULTANEOUSLY
        for old, new, image in zip(old_name_entries, new_name_entries, image_entries):
            relative_url = old.get("old_name", "")
            new_name = new.get("new_name", "")
            image_url = image.get("image_url", "")

            # CONSTRUCT OLD_NAME AS PREVIOUS
            if relative_url:
                old_name = relative_url.split("-")[0].replace("_", " ").title()
                full_url = f"https://www.gsmarena.com/{relative_url}"

            new_records.append({
                "Page_Number": self.page_number,
                "Brand": self.url_list[self.current_crawl]['brand'],
                "Old_Name": old_name,
                "Model_New": new_name,
                "URL": full_url,
                "Image": image_url
            })

        print(f"Update: Page {self.page_number}: Extracted {len(new_records)} URLs.")

        return self.write_to_SQLite_database(self.filename, new_records)

    # WRITE INTO SQLite DATABASE 
    def write_to_SQLite_database(self, db_file, records : list[dict]):
        if not records:
            return
        
        conn = sqlite3.connect(db_file)
        cur = conn.cursor()
        
        # INFER DATA TYPES
        def get_sqlite_data_type(value):
            if isinstance(value, int): return "INTEGER"
            elif isinstance(value, float): return "REAL"
            elif isinstance(value, (bytes, bytearray)): return "BLOB"
            else: return "TEXT"

        # CREATE COLUMN NAMES FROM KEYS OF THE DICTIONARY 
        sample_record = records[0]
        columns = ', '.join(f'"{k}" {get_sqlite_data_type(v)}' for k, v in sample_record.items())
        cur.execute(
            f'CREATE TABLE IF NOT EXISTS "{self.table_name}" (id INTEGER PRIMARY KEY AUTOINCREMENT, {columns})'
        )

        placeholders = ', '.join('?' for _ in records[0].keys())
        insert_query = f'INSERT INTO "{self.table_name}" ({", ".join(sample_record.keys())}) VALUES ({placeholders})'

        data = [tuple(r.values()) for r in records]
        cur.executemany(insert_query, data)

        conn.commit()
        conn.close()

        self.write_counter = self.write_counter + len(records)
        self.total_counter = self.total_counter + len(records)
        print(f"{len(records)} Phone Information Written in Database.")
        print(f"Total Written: {self.write_counter} in Current Run, {self.total_counter} Overall.")
        self.page_number += 1
        
    """Final Log"""
    def final_log(self):
        print("CRAWLING COMPLETE.")
        print(f"Total {self.total_counter} information added to Database.")