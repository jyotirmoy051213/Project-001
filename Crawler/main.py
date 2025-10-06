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

import asyncio
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
    # Start the crawler, TRY to ensure proper cleanup if crawler fails
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            output_pipeline = configs.Output_Pipeline()
            while True:
                print("STATUS: INITIATING CRAWLING.")
                should_continue = await output_pipeline(crawler=crawler)
                print(should_continue)
                if not should_continue:
                    print("STOPPING OUTPUT PIPELINE.")
                    break
                
    
    finally:
        print("CRAWLING COMPLETE.")
        
        # SHOULD BE TASK-AGNOSTIC ::: Estimated Product Count (CHECK LOG IN CASE OF DISCREPENCY)
        estimated_product_count = (
            "0" if output_pipeline.crawled_page_count == 0
            else "<=50" if output_pipeline.crawled_page_count == 1
            else "50+" if output_pipeline.crawled_page_count == 2
            else f"{(output_pipeline.crawled_page_count - 1) * 20}+"
            )
        print(f"ESTIMATED PRODUCT COUNT: {estimated_product_count}.\nCHECK LOG IN CASE OF DISCREPENCY.")
        
        # FINAL LOG
        print(f"Crawl no: {crawl_number}/{len(urls_to_crawl)-1}, Crawled {output_pipeline.crawled_page_count} Pages.")
        print(f"Total {output_pipeline.product_count} URLs Added to Database.")
        

async def main():
    await crawl_products(test_mode=test_mode)

if __name__ == '__main__':
    asyncio.run(main())