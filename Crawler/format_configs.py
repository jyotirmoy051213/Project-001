"""
This script has all CONFIGURATION SETTINGS TO RUN CRAWLER FROM main.py
Change configuration based on website & crawling strategy
"""
import os, csv
from pydantic import BaseModel
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, JsonCssExtractionStrategy, CacheMode

TEST_MODE = False
MAIN_FILE= "D:/My Codes/Projects/Project-001/Crawler/Database/products.csv"
TEST_FILE= "D:/My Codes/Projects/Project-001/Crawler/test_csv.csv"
CSS_SELECTOR = ".main-content.p-items-wrap"
URLS_TO_CRAWL = [
    {"category": "Desktop", "base_url": "https://www.startech.com.bd/desktops"},
    {"category": "Laptop", "base_url": "https://www.startech.com.bd/laptop-notebook"},
    {"category": "Component", "base_url": "https://www.startech.com.bd/component"},
    {"category": "Monitor", "base_url": "https://www.startech.com.bd/monitor"},
    {"category": "Power", "base_url": "https://www.startech.com.bd/power"},
    {"category": "Phone", "base_url": "https://www.startech.com.bd/mobile-phone"},
    {"category": "Tablet", "base_url": "https://www.startech.com.bd/tablet-pc"},
    {"category": "Office Equipment", "base_url": "https://www.startech.com.bd/office-equipment"},
    {"category": "Camera", "base_url": "https://www.startech.com.bd/camera"},
    {"category": "Security", "base_url": "https://www.startech.com.bd/Security-Camera"},
    {"category": "Networking", "base_url": "https://www.startech.com.bd/networking"},
    {"category": "Software", "base_url": "https://www.startech.com.bd/software"},
    {"category": "Server & Storage", "base_url": "https://www.startech.com.bd/server-networking"},
    {"category": "Accessories", "base_url": "https://www.startech.com.bd/accessories"},
    {"category": "Gadget", "base_url": "https://www.startech.com.bd/gadget"},
    {"category": "Gaming", "base_url": "https://www.startech.com.bd/gaming"},
    {"category": "TV", "base_url": "https://www.startech.com.bd/television-shop"},
    {"category": "Appliance", "base_url": "https://www.startech.com.bd/appliance"},
]


## CONFIGURATION SETTINGS
def get_browser_config():
    return BrowserConfig(
        browser_type='chromium', # Chrome Browser
        headless=False, # Headless == No GUI
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
        "baseSelector": ".p-item-inner",            
        "fields": [
            {"name": "name", "selector": ".p-item-name a", "type": "text"},
            {"name": "image_url", "selector": ".p-item-img img", "type": "attribute", "attribute": "src"},
            {"name": "description", "selector": ".short-description li", "type": "list", "fields": [{"name": "feature","type": "text"}]},
            {"name": "price", "selector": ".p-item-price span", "type": "text"},
            {"name": "url", "selector": ".p-item-img a", "type": "attribute", "attribute": "href"}
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
            row = [product.get('category', '')] + [product.get(field, '') for field in headers[1:]]
            writer.writerow(row)