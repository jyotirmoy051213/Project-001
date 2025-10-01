"""
Crawling project using Crawl4AI with LLM Free Schema-based extraction strategy from ryanscomputerbd
This script crawls product data from multiple categories on ryanscomputerbd, handling pagination and saving results to a CSV file.
Right now it is set to use one category at a time. 
Category and the url need to be changed manually in the code.
Schema is handcrafted after inspecting the webpage structure for this specific site.
Code need to be modularized.
"""

"""
SCOPE FOR IMPROVEMENTS:
1. Could be automated to loop through all categories in base_urls list.
2. CSV is written once after all, could be optimized to write in each page.
3. Some functions can be made to shorten the code.
4. Separate scripts can be made for the code, especially Schema (as it is website-specific) & Configs.
5. Error handling might need improvements.
6. Duplicates are not handled.
7. Logging needs to be improved.
8. Memory management for large crawls need to be checked.
"""



import asyncio, os
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, JsonCssExtractionStrategy,  CacheMode
from dotenv import load_dotenv
import json
import csv

load_dotenv()

async def crawl_products():
    # initialize config
    browser_config = BrowserConfig(
        browser_type='chromium', # Chrome Browser
        headless=False, # Headless == No GUI
        verbose=True # Verbose logging
    )    
    
    session_id = 'product_crawl_session'

    # initialize state variables
    crawl_number = 14 # Change this to crawl different categories from base_urls list
    page_number = 1 # Start from page 1
    all_products = [] # List to hold all scraped products
    seen_names = set() # Set to track unique products
    delay_time = 2 # Delay between requests to avoid overwhelming the server + Rate limiting

    # URLS of ryanscomputerbd
    base_urls = [
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

    # Start the crawler, TRY to ensure proper cleanup if crawler fails
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            while True:
                category = base_urls[crawl_number]["category"] # Change category as needed by crawl_number
                print(f"\nStatus: Crawling. Crawl Number: {crawl_number}. Category: {category}. Page: {page_number}") # Log current status
                url = f"{base_urls[crawl_number]["base_url"]}?page={page_number}" # URL with pagination
                css_selector= ".card.h-100" # Only select where class contains this string

                

                # Build schema for JsonCssExtractionStrategy by inspecting the webpage
                schema = {
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
                
                # Configure Crawler
                config=CrawlerRunConfig(
                    session_id=session_id, # Unique session ID for the crawl
                    extraction_strategy=JsonCssExtractionStrategy(schema=schema),
                    css_selector=css_selector,
                    cache_mode=CacheMode.BYPASS
                    )

                # Crawl the page    
                result = await crawler.arun(
                    url=url,
                    config=config    
                )
                

                # Parse results safely, skip if JSON is invalid
                try:
                    extracted_data = json.loads(result.extracted_content)

                # If encountered json decode error, skip this page
                except json.JSONDecodeError:
                    print(f"Error decoding JSON in Page {page_number}, skipping.")
                    page_number += 1
                    continue 

                # Stop if no products found
                if not extracted_data:
                    print(f"No products found in Page {page_number}.")
                    break 
                
                # Append new unique products
                for item in extracted_data:
                    item['category'] = category # Add category field
                    all_products.append(item)
                print(f"Page {page_number}: added {len(extracted_data)} products. \nTotal added in current crawl: {len(all_products)}.")
                #break # For testing, comment out to crawl all pages
                page_number +=1
            
                # Delay Log
                print(f"Proceeding to next page after {delay_time} seconds...")
                await asyncio.sleep(delay_time) # Be polite and avoid overwhelming the server

    # CSV will be saved even if error occurs
    finally: 
        await crawler.close()    
        
        # Save to CSV once after all pages are crawled
        csv_file = "D:/My Codes/Projects/scraping/MyDeepSeekCrawlProject/Ryans_products.csv" # Main file
        #csv_file = "D:/My Codes/Projects/scraping/MyDeepSeekCrawlProject/trial_Ryans_products.csv" # Trial file for testing
        
        headers = ['category'] + [field['name'] for field in schema['fields']]
        # Check if file already exists to write header only once
        file_exists = os.path.isfile(csv_file)

        # Write to CSV
        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write header only if file is new
            if not file_exists:
                writer.writerow(headers)
            
            # Write product rows with category as the first column
            for product in all_products:
                row = [product.get('category', '')] + [product.get(field, '') for field in headers[1:]]
                writer.writerow(row)

        
        # Final Log
        print(f"Added {len(all_products)} new products to database.")


        

async def main():
    # Entry point
    await crawl_products()

if __name__ == '__main__':
    asyncio.run(main())