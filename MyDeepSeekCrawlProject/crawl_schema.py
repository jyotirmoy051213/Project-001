"""Crawling project using Crawl4AI with LLM Free Schema based extraction strategy
from ryanscomputerbd
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
    page_number = 1 # Start from page 1
    all_products = [] # List to hold all scraped products
    seen_names = set() # Set to track unique products
    delay_time = 5 # Delay between requests to avoid overwhelming the server + Rate limiting

    # Start the crawler, TRY to ensure proper cleanup if crawler fails
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            while True:
                url = f"https://www.ryans.com/category/desktop-and-server?page={page_number}" # URL with pagination
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
                    all_products.append(item)
                print(f"Page {page_number}: added {len(extracted_data)} products, Total so far: {len(all_products)}.")

                """# Filter for duplicates
                new_products = []
                for item in extracted_data:
                    if item['name'] not in seen_names:
                        seen_names.add(item['name'])
                        all_products.append(item)
                        new_products.append(item)

                print(f"Page {page_number}: Found {len(new_products)} new products.")"""

                page_number +=1
                
                print(f"Proceeding to Page after {delay_time} seconds...")
                await asyncio.sleep(delay_time) # Be polite and avoid overwhelming the server
                break


    finally: # CSV will be saved even if error occurs
        await crawler.close()    
        # Save to CSV once after all pages are crawled
        

        csv_file = "D:/My Codes/Projects/scraping/MyDeepSeekCrawlProject/Ryans_products.csv"
        headers = [field['name'] for field in schema['fields']]
        # Check if file already exists to write header only once
        file_exists = os.path.isfile(csv_file)

        with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Write header only if file is new
            if not file_exists:
                writer.writerow(headers)
            
            for product in all_products:
                writer.writerow([product.get(field, "") for field in headers])


        
        print(f"Saved {len(all_products)} unique products to {csv_file}.")


        

async def main():
    # Entry point
    await crawl_products()

if __name__ == '__main__':
    asyncio.run(main())