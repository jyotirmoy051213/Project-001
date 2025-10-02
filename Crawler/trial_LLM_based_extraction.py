"""Crawling project using Crawl4AI with LLM based extraction strategy
from ryanscomputerbd
"""

import asyncio, os
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, BrowserConfig, LLMExtractionStrategy, LLMConfig,  CacheMode
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import json
import csv

load_dotenv()


class Products(BaseModel):
    # Data structure for extracted product information
    category : str
    name : str
    image_url : str
    description : str
    price : int
    url : str


async def crawl_products():
    # initialize config
    browser_config = BrowserConfig(
        browser_type='chromium', # Chrome Browser
        headless=False, # Headless == No GUI
        verbose=True # Verbose logging
    )
    
    llm_extraction_strategy = LLMExtractionStrategy(
        llm_config = LLMConfig(provider="groq/meta-llama/llama-4-maverick-17b-128e-instruct", api_token=os.getenv("GROQ_API_KEY")),
        schema=Products.model_json_schema(),
        extraction_type='schema',
        instruction="Extract all product object with 'category', 'name', 'image url', 'description', 'price', and 'url' from the content.",
        input_format='markdown',
        verbose=True 
    )
    
    session_id = 'product_crawl_session'

    # initialize state variables
    page_number = 1 # Start from page 1
    all_products = [] # List to hold all scraped products
    seen_names = set() # Set to track unique products
    delay_time = 60 # Delay between requests to avoid overwhelming the server + Rate limiting

    # Start the crawler, TRY to ensure proper cleanup if crawler fails
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            while True:
                url = f"https://www.ryans.com/category/laptop?page={page_number}" # URL with pagination
                css_selector= "[class*='cus-col-2 cus-col-3 cus-col-4 cus-col-5 category-single-product mb-2 context1']" # Only select where class contains this string

                # Crawl the page    
                result = await crawler.arun(
                    url=url,
                    config=CrawlerRunConfig(
                    session_id=session_id, # Unique session ID for the crawl
                    extraction_strategy=llm_extraction_strategy,
                    css_selector=css_selector,
                    cache_mode=CacheMode.BYPASS
                    )
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


    finally: # CSV will be saved even if error occurs
        await crawler.close()    
        # Save to CSV once after all pages are crawled
        csv_file = "D:/My Codes/Projects/scraping/MyDeepSeekCrawlProject/products.csv"
        with open (csv_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            headers = list(Products.model_json_schema()["properties"].keys())
            writer.writerow(headers)
            for product in all_products:
                writer.writerow([product.get(field, "") for field in headers])

        
        print(f"Saved {len(all_products)} unique products to {csv_file}.")
        print(f"Tokens used: {llm_extraction_strategy.show_usage()}")


        

async def main():
    # Entry point
    await crawl_products()

if __name__ == '__main__':
    asyncio.run(main())