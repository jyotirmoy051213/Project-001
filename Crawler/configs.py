"""
This script has all CONFIGURATION SETTINGS TO RUN CRAWLER FROM main.py
Change configuration based on website & crawling strategy
"""

import os, csv, json, asyncio
from pydantic import BaseModel
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, JsonCssExtractionStrategy, CacheMode

## CONTROL VARIABLES
TEST_MODE = False
CRAWL_NUMBER = 16
PAGE_NUMBER = 1
DELAY_TIME = 5


MAIN_FILE= "D:/My Codes/Projects/Project-001/Database/gsmarena_products.csv"
TEST_FILE= "D:/My Codes/Projects/Project-001/Crawler/trials/test_csv.csv"
SESSION_ID = "project-002"



## STRATEGY
CSS_SELECTOR = ".makers"
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
    {"brand": "TCL", "url": "https://www.gsmarena.com/tcl-phones-f-123-0-p.php"}
]

# Handcrafted schema for JsonCssExtractionStrategy by inspecting the webpage
SCHEMA_FOR_EXTRACTION = {
        "name": "Product",
        "baseSelector": ".makers",            
        "fields": [
            {"name": "model", "selector": ".makers li", "type": "list", "fields": [{"name": "model", "type": "text"}]},
            {"name": "model", "selector": ".makers a", "type": "list", "fields": [{"name": "model", "type": "attribute", "attribute": "href"}]}
            ]    
        }

BASE_URL = f"{URLS_TO_CRAWL[CRAWL_NUMBER]['url']}"[:-4]

# PYDANTIC SCHEMA FOR LLM-BASED EXTRACTION STRATEGY
class Products(BaseModel):
    category : str
    name : str
    image_url : str
    description : str
    price : int
    url : str


## CONFIGURATION SETTINGS
def get_browser_config():
    return BrowserConfig(
        browser_type='chromium', # Chrome Browser
        headless=False, # Headless == No GUI
        verbose=True # Verbose logging
    ) 

def get_crawler_config():
    return CrawlerRunConfig(
            css_selector=CSS_SELECTOR,
            extraction_strategy=JsonCssExtractionStrategy(SCHEMA_FOR_EXTRACTION),
            session_id=SESSION_ID,
            cache_mode=CacheMode.BYPASS
        )


# OUTPUT
class Output_Pipeline:
    def __init__(self):
        self.page_number = PAGE_NUMBER
        self.product_count = 0
        self.crawled_page_count = 0
        self.seen_product = set()
        self.delay_time = DELAY_TIME
        self.test_mode = TEST_MODE
        self.main_file = MAIN_FILE
        self.test_file = TEST_FILE
    
    # DYNAMICALLY UPDATE URL
    @property
    def url(self):
        return BASE_URL + f"{self.page_number}.php"
    
    # WRITER METHOD
    def csv_writer(self, file_to_be_written, product_info):
        headers = ["Brand", "Model", "URL"]
        file_exists = os.path.isfile(file_to_be_written)
        with open(file_to_be_written, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

        # Write header only if file is new, otherwise assume, there is already a header
        if not file_exists:
            writer.writerow(headers)
        
        for product in product_info:
            row = [product.get(field, '') for field in headers]
            writer.writerow(row)


    async def __call__(self, crawler):
        ## MODULE 1:: CRAWLING & EXTRACTION
        # RUN THE CRAWLER
        result = await crawler.arun(
            url = self.url,
            config=get_crawler_config()
            )
        # SEE IF THE CRAWLING WAS SUCCESSFUL
        if not result.success:
            print("STATUS: CRAWLING ERROR!!")
            return False
        print("STATUS: CRAWLING SUCCESSFUL. PROCESSING OUTPUT.")
        # SEE IF EXTRACTION WAS SUCCESSFUL
        extracted_data = json.loads(result.extracted_content)
        if not extracted_data:
            print(f"No products found in Page {self.page_number}.")
            return False
        print(f"PAGE NO: {self.page_number}, DATA EXTRACTION COMPLETED.")        
        
        
        
        # MODULE 2 :: ORGANIZE EXTRACTED DATA FOR WRITING (APPEND NEW DATA, CHECK FOR DUPLICATES)
        new_products = []
        model_entries = extracted_data[0].get("model", [])
        for entry in model_entries:
                relative_url = entry.get("model", "")
                if relative_url:
                    model_name = relative_url.split("-")[0].replace("_", " ").title()
                    full_url = f"https://www.gsmarena.com/{relative_url}"
                    new_products.append({"Brand": URLS_TO_CRAWL[CRAWL_NUMBER]['brand'], "Model": model_name, "URL": full_url})
        print(f"Update: Page {self.page_number}: Extracted {len(new_products)} URLs.")


        ## MODULE 3 :: WRITING
        if self.test_mode:
            print("RUNNING ON TEST MODE")
            self.csv_writer(
                file_to_be_written=self.test_file,
                products=new_products
                )
        else:
            self.csv_writer(
                file_to_be_written=self.main_file,
                products=new_products
                )
        
        
        ## MODUEL 4 :: COUNTERS
        self.product_count = self.product_count + len(new_products)
        self.crawled_page_count += 1
        print(f"Update: Page {self.page_number}: Written {len(new_products)} new URLs to database. Total written: {self.product_count}")
        if self.test_mode:
            print(f"TEST MODE SUCCESSFUL. WAIT FOR FINAL LOG")
            return False
        self.page_number += 1
        self.crawled_page_count += 1
        # STOP IF NOTHING FOUND
        if len(new_products) == 0:
            print(f"No Products found in Page{self.page_number}")
            return False            
        # DELAY LOG
        print(f"Proceeding to next page after {self.delay_time} seconds...")
        await asyncio.sleep(self.delay_time) # Be polite and avoid overwhelming the server

        return True