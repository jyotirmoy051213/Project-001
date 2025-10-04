"""
Crawling project using Crawl4AI with LLM Free Schema-based extraction strategy from ------ (WEBSITE NAME)
This script crawls product data from multiple categories of startech website, handling pagination and saving results to a CSV file.
Right now it is set to use one category at a time. 
Schema is handcrafted after inspecting the webpage structure for specific website.
"""

"""
SCOPE FOR IMPROVEMENTS:
1. Could be automated to loop through all categories in urls_to_crawl list.
4. Separate scripts can be made for the code, especially logging, writing files and main logic.
5. Error handling might need improvements.
6. Duplicates are not handled.
7. Logging needs to be improved. Logs needs to be written to a file. Explore logging module.
8. Memory management for large crawls need to be checked.
9. Later maybe build a UI to select website, generate schema using LLM, upload schema, Select crawl number/category/page number, view logs
10. Build in Docker.
11. Explore SQL DB instead of CSV.
12. Need to explore LLM based schema generation.
"""

import asyncio, json
from crawl4ai import AsyncWebCrawler
from dotenv import load_dotenv
import configs

load_dotenv()
test_mode = configs.TEST_MODE

async def crawl_products(test_mode=False):
    # CONFIGURATION VARIABLES TO SET UP CRAWLING
    urls_to_crawl = configs.URLS_TO_CRAWL 
    browser_config = configs.get_browser_config()   
    

    # VARIABLES TO DICTATE CRAWLING
    crawl_number = configs.CRAWL_NUMBER # Change this to crawl different categories from urls_to_crawl list
    page_number = configs.PAGE_NUMBER # Start from page 1 
    delay_time = configs.DELAY_TIME # Delay between requests to avoid overwhelming the server + Rate limiting
    main_file = configs.MAIN_FILE
    test_file = configs.TEST_FILE

    # Start the crawler, TRY to ensure proper cleanup if crawler fails
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            product_count = 0
            crawled_page_count = 0
            seen_products = set()
            while True:
                ## URL should be made Task Agnostic
                url = f"{urls_to_crawl[crawl_number]['base_url']}?page={page_number}" # URL with pagination copied from site_config
                # Log current status
                print("STATUS: INITIATING CRAWLING.")
                
                result = await configs.crawl_and_extract_from_page(url=url, crawler=crawler)
                
                if not result.success:
                    print("STATUS: CRAWLING ERROR!!")
                    break
                else:
                    print("STATUS: CRAWLING SUCCESSFUL. PROCESSING OUTPUT.")
                    
                    ## OUTPUT PIPELINE SHOULD BE MADE TASK AGNOSTIC. OUTPUT FUNCTION WILL TAKE THE RESULT AND DO THE REST.
                    extracted_data = json.loads(result.extracted_content)
                    # Stop if no products found
                    if not extracted_data:
                        print(f"No products found in Page {page_number}.")
                        break 
                
                    # Append new unique products
                    new_products = [] 
                    for item in extracted_data:
                        new_products.append(item)
                        print(f"Update: Page {page_number}: Extracted {len(extracted_data)} products.")
                
                        # Add products in CSV file
                        if test_mode:
                            configs.custom_csv_writer(
                            file_to_be_written=test_file,
                            products=new_products
                            )
                            product_count = product_count + len(new_products)
                            crawled_page_count += 1
                            print(f"Update: Page {page_number}: Written {len(new_products)} new products to database. Total written: {product_count}")
                            print(f"TEST MODE SUCCESSFUL. WAIT FOR FINAL LOG")
                            break
                
                        else:
                            configs.custom_csv_writer(
                            file_to_be_written=main_file,
                            products=new_products
                            )
                            # Count of total products extracted & written
                            product_count = product_count + len(new_products)
                            print(f"Update: Page {page_number}: Written {len(new_products)} new products to database. Total written: {product_count}")
                
                            # Proceed to next page
                            page_number += 1
                            crawled_page_count += 1
                            # Delay Log
                            print(f"Proceeding to next page after {delay_time} seconds...")
                            await asyncio.sleep(delay_time) # Be polite and avoid overwhelming the server

    
    finally:
        print("CRAWLING COMPLETE.")
        # SHOULD BE TASK-AGNOSTIC ::: Estimated Product Count (CHECK LOG IN CASE OF DISCREPENCY)
        estimated_product_count = (
            "0" if crawled_page_count == 0
            else "<=20" if crawled_page_count == 1
            else "20+" if crawled_page_count == 2
            else f"{(crawled_page_count - 1) * 20}+"
            )
        print(f"ESTIMATED PRODUCT COUNT: {estimated_product_count}.\nCHECK LOG IN CASE OF DISCREPENCY.")
        
        # FINAL LOG
        print(f"Crawl no: {crawl_number}/{len(urls_to_crawl)-1}, Category: {configs.CATEGORY}. Crawled {crawled_page_count} Pages.")
        print(f"Total {product_count} Products Added to Database.")
        

async def main():
    await crawl_products(test_mode=test_mode)

if __name__ == '__main__':
    asyncio.run(main())