"""
This script contains configuration settings for the main script. 
Alter/Set configuration here to try Crawl/Extraction techniques.  
"""
from crawl4ai import BrowserConfig, CrawlerRunConfig, LLMConfig, LLMExtractionStrategy, JsonCssExtractionStrategy, CacheMode



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

# List of product categories and their URLs
URLS_TO_CRAWL = [
        {"category": "laptop", "base_url": "https://www.ryans.com/category/laptop"}, #0
        {"category": "desktop_and_server", "base_url": "https://www.ryans.com/category/desktop-and-server"}, #1
        {"category": "gaming", "base_url": "https://www.ryans.com/category/gaming"}, #2
        {"category": "monitor", "base_url": "https://www.ryans.com/category/monitor"}, #3
        {"category": "tablet_pc", "base_url": "https://www.ryans.com/category/tablet"}, #4
        {"category": "printer", "base_url": "https://www.ryans.com/category/printer"}, #5
        {"category": "camera", "base_url": "https://www.ryans.com/category/camera"}, #6
        {"category": "security", "base_url": "https://www.ryans.com/category/security-system"}, #7
        {"category": "network", "base_url": "https://www.ryans.com/category/network"}, #8
        {"category": "sound", "base_url": "https://www.ryans.com/category/sound-system"}, #9
        {"category": "office_items", "base_url": "https://www.ryans.com/category/office-items"}, #10
        {"category": "accessories", "base_url": "https://www.ryans.com/category/accessories"}, #11
        {"category": "software", "base_url": "https://www.ryans.com/category/software"}, #12
        {"category": "gadget", "base_url": "https://www.ryans.com/category/gadget"}, #13
        {"category": "store", "base_url": "https://www.ryans.com/category/store"} #14
    ]

# Handcrafted schema for JsonCssExtractionStrategy by inspecting the webpage
SCHEMA_FOR_EXTRACTION = {
        "name": "Product",
        "baseSelector": ".card.h-100",            
        "fields": [
            {"name": "name", "selector": ".card-text.p-0.m-0.list-view-text a", "type": "attribute", "attribute": "data-bs-original-title"},
            {"name": "image_url", "selector": ".image-box img", "type": "attribute", "attribute": "src"},
            {"name": "description", "selector": ".short-desc-attr li", "type": "list", "fields": [{"name": "feature","type": "text"}]},
            {"name": "price", "selector": ".pr-text.cat-sp-text.pb-1.text-dark.text-decoration-none", "type": "text"},
            {"name": "url", "selector": ".card-text.p-0.m-0.list-view-text a", "type": "attribute", "attribute": "href"}
            ] 
        }

# base_url_format:: Copy and paste as "base_url" variable for ryans website
# base_url = f"{urls_to_crawl[crawl_number]["base_url"]}?page={page_number}"


# CSS Selector for crawler
CSS_SELECTOR = ".card.h-100"