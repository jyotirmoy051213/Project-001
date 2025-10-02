"""
Crawling project using Crawl4AI with LLM Free Schema-based extraction strategy from Startech.com
This script crawls product data from multiple categories of startech website, handling pagination and saving results to a CSV file.
Right now it is set to use one category at a time. 
Schema is handcrafted after inspecting the webpage structure for this specific site.
"""

"""
SCOPE FOR IMPROVEMENTS:
1. Could be automated to loop through all categories in urls_to_crawl list.
2. CSV is written once after all, could be optimized to write in each page.
3. Some functions can be made to shorten the code.
4. Separate scripts can be made for the code, especially logging, writing files and main logic.
5. Error handling might need improvements.
6. Duplicates are not handled.
7. Logging needs to be improved. Logs needs to be written to a file. Explore logging module.
8. Memory management for large crawls need to be checked.
9. Later maybe build a UI to select website, generate schema using LLM, upload schema, Select crawl number/category/page number, view logs
10. Build in Docker.
11. Explore SQL DB instead of CSV.
12. Need to explore LLM based schema generation.
13. Need to setup a requirements.txt file.
"""

import asyncio
import os
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, JsonCssExtractionStrategy, CacheMode
from dotenv import load_dotenv
import json
import csv
import site_config_startech, configs_startech

load_dotenv()

async def crawl_products():
    # initialize config
    browser_config = configs_startech.get_browser_config()   
    
    session_id = 'product_crawl_session'

    # initialize state variables
    crawl_number = 0 # LENGTH OF urls_to_crawl :: Change this to crawl different categories from urls_to_crawl list
    page_number = 1 # Start from page 1
    all_products = [] # List to hold all scraped products
    seen_names = set() # Set to track unique products
    delay_time = 2 # Delay between requests to avoid overwhelming the server + Rate limiting

    # Website variables from site_configuration: Category of products, URLs & Schema
    urls_to_crawl = site_config_startech.URLS_TO_CRAWL
    schema = site_config_startech.SCHEMA_FOR_EXTRACTION
    css_selector = site_config_startech.CSS_SELECTOR

    # Start the crawler, TRY to ensure proper cleanup if crawler fails
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            while True:
                category = urls_to_crawl[crawl_number]["category"] # Change category as needed by crawl_number
                print(f"\nStatus:Crawling, Crawl No:{crawl_number}/{len(urls_to_crawl)}, Category: {category}, Page: {page_number}") # Log current status
                base_url = f"{urls_to_crawl[crawl_number]['base_url']}?page={page_number}" # URL with pagination copied from site_config

                # Configure Crawler
                crawler_config = configs_startech.get_crawler_config(
                    session_id=session_id,
                    css_selector=css_selector,
                    schema=schema
                )

                # Crawl the page    
                result = await crawler.arun(
                    url=base_url,
                    config=crawler_config    
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
                print(f"Page {page_number}: added {len(extracted_data)} products. \nTotal added including current crawl: {len(all_products)}.")
                
                #break # For testing, comment out to crawl all pages
                page_number += 1

                # Delay Log
                print(f"Proceeding to next page after {delay_time} seconds...")
                await asyncio.sleep(delay_time) # Be polite and avoid overwhelming the server

    # CSV will be saved even if error occurs
    finally: 
        await crawler.close()    

        # Save to CSV once after all pages are crawled
        csv_file = "D:/My Codes/Projects/Project-001/Crawler/Startech_products.csv" # Main file
        #csv_file = "D:/My Codes/Projects/Project-001/Crawler/trial_csv.csv" # Trial file for testing

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
        print(f"Crawling complete. Check log if less than {(page_number-2)*20}+ products added.")

async def main():
    # Entry point
    await crawl_products()

if __name__ == '__main__':
    asyncio.run(main())