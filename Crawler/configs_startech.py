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