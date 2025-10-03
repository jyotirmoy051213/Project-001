"""
This script has all CONFIGURATION SETTINGS TO RUN CRAWLER FROM main.py
Change configuration based on website & crawling strategy
"""
import os, csv
from pydantic import BaseModel
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, JsonCssExtractionStrategy, CacheMode

TEST_MODE = False
MAIN_FILE= "D:/My Codes/Projects/Project-001/Crawler/Database/Vertech_products.csv"
TEST_FILE= "D:/My Codes/Projects/Project-001/Crawler/test_csv.csv"
CSS_SELECTOR = r".grid.grid-cols-2"
URLS_TO_CRAWL = [
    {"category": "Laptop", "base_url": "https://www.vertech.com.bd/category/laptop"},
    {"category": "iMac & iMac Mini", "base_url": "https://www.vertech.com.bd/category/laptop/imac-and-mac-mini"},
    {"category": "ipad", "base_url": "https://www.vertech.com.bd/category/ipad"},
]


## CONFIGURATION SETTINGS
def get_browser_config():
    return BrowserConfig(
        browser_type='chromium', # Chrome Browser
        headless=True, # Headless == No GUI
        verbose=True # Verbose logging
    ) 

def get_crawler_config(session_id, css_selector, schema): # ARGUMENTS THAT NEED TO BE PASSED FROM THE MAIN SCRIPT, MUST BE DEFINED BEFORE EXECUTING THIS FUNCTION
    return CrawlerRunConfig(
        session_id=session_id, # Unique session ID for the crawl
        extraction_strategy=JsonCssExtractionStrategy(schema=schema),
        css_selector=css_selector,  # Decides what part of an encountered webpage crawler will crawl through
        cache_mode=CacheMode.BYPASS
    )

## SCHEMA FOR EXTRACTION
# Schema for JsonCssExtractionStrategy by inspecting the webpage
SCHEMA_FOR_EXTRACTION = {
        "name": "Product",
        "baseSelector": r".relative.group\/root",  # A Selector which is repeated, and contains information of a single product
        "fields": [
            {"name": "name", "selector": r".p-md", "type": "text"},
            {"name": "image_url", "selector": r".flex.justify-center.border-b.border-gray-100.w-full img", "type": "attribute", "attribute": "src"},
            {"name": "description", "selector": r".short-description li", "type": "text"},
            {"name": "price", "selector": r".text-primary.font-medium.text-title_3", "type": "text"},
            {"name": "url", "selector": r".p-md a", "type": "attribute", "attribute": "href"}
            ] 
        }

# Pydantic Basemodel for LLM-based Extraction Strategy
class Products(BaseModel):
    # Data structure for extracted product information
    category : str
    name : str
    image_url : str
    description : str
    price : int
    url : str


## WRITING
HEADERS = ['category'] + [field['name'] for field in SCHEMA_FOR_EXTRACTION['fields']]

def custom_csv_writer(file_to_be_written, headers, products):    
    file_exists = os.path.isfile(file_to_be_written)            # Write to CSV
    with open(file_to_be_written, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write header only if file is new, otherwise assume, there is already a header
        if not file_exists:
            writer.writerow(headers)
        
        # THIS SECTION IS EXTRACTION SPECIFIC::: Write as per extracted data
        for product in products:
            if "url" in product and not product["url"].startswith("http"):
                product["url"] = "https://www.vertech.com.bd/" + product["url"]

            row = [product.get('category', '')] + [product.get(field, '') for field in headers[1:]]
            writer.writerow(row)