"""
This script has all CONFIGURATION SETTINGS TO RUN CRAWLER FROM main.py
Change configuration based on website & crawling strategy
"""
import os, csv
from pydantic import BaseModel
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, JsonCssExtractionStrategy, CacheMode

TEST_MODE = True
MAIN_FILE= "D:/My Codes/Projects/Project-001/Crawler/Database/Computer-village_products.csv"
TEST_FILE= "D:/My Codes/Projects/Project-001/Crawler/test_csv.csv"
CSS_SELECTOR = ".main-products.product-grid"
URLS_TO_CRAWL = [
  { "category": "Laptop", "base_url": "https://www.computervillage.com.bd/laptop-notebook" },
  { "category": "Tablet", "base_url": "https://www.computervillage.com.bd/tablet" },
  { "category": "Desktop", "base_url": "https://www.computervillage.com.bd/desktop-pc" },
  { "category": "Apple", "base_url": "https://www.computervillage.com.bd/laptop-apple" },
  { "category": "Gaming", "base_url": "https://www.computervillage.com.bd/gaming-peripherals" },
  { "category": "Component", "base_url": "https://www.computervillage.com.bd/component" },
  { "category": "Monitor", "base_url": "https://www.computervillage.com.bd/monitor" },
  { "category": "Accessories", "base_url": "https://www.computervillage.com.bd/accessories" },
  { "category": "Gadget", "base_url": "https://www.computervillage.com.bd/gadget" },
  { "category": "Photography", "base_url": "https://www.computervillage.com.bd/photography" },
  { "category": "Office Equipment", "base_url": "https://www.computervillage.com.bd/office-equipments" },
  { "category": "Security & Software", "base_url": "https://www.computervillage.com.bd/security-solution" },
  { "category": "Networking", "base_url": "https://www.computervillage.com.bd/networking-product" },
  { "category": "Enterprise Solution", "base_url": "https://www.computervillage.com.bd/enterprise-solution" },
  { "category": "Server & Storage", "base_url": "https://www.computervillage.com.bd/server-and-storage" },
  { "category": "Pre Owned", "base_url": "https://www.computervillage.com.bd/pre-owned" }
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
        "baseSelector": ".product-thumb",  # A Selector which is repeated, and contains information of a single product
        "fields": [
            {"name": "name", "selector": ".name", "type": "text"},
            {"name": "image_url", "selector": ".img-responsive.img-first", "type": "attribute", "attribute": "src"},
            {"name": "description", "selector": ".module-features-description li", "type": "list", "fields": [{"name": "feature", "type": "text"}]}, #???
            {"name": "price", "selector": ".price-tax", "type": "text"}, #???
            {"name": "url", "selector": ".name a", "type": "attribute", "attribute": "href"} #???
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
            price = product.get("price", "")
            if price and price.startswith("Ex Tax:"):
                product["price"] = price.replace("Ex Tax:", "").strip()

            row = [product.get('category', '')] + [product.get(field, '') for field in headers[1:]]
            writer.writerow(row)