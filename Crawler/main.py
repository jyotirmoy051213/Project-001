"""
Crawling project using Crawl4AI with LLM Free Schema-based extraction strategy from ------ (WEBSITE NAME)
Schema is handcrafted after inspecting the webpage structure for specific website.
"""

"""
SCOPE FOR IMPROVEMENTS:
1. Could be automated to loop through all categories in urls_to_crawl list.
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

async def crawl_products(test_mode):
    # CONFIGURATION VARIABLES TO SET UP CRAWLING
    browser_config = configs.get_browser_config()   
    try:
        async with AsyncWebCrawler(config=browser_config) as crawler:
            output_pipeline = configs.Output_Pipeline()
            if test_mode:
                print("RUNNING ON TEST MODE.")
            while True:
                print("STATUS: INITIATING CRAWLING.")
                should_continue = await output_pipeline(crawler=crawler)
                print(should_continue)
                if not should_continue:
                    print("STOPPING OUTPUT PIPELINE.")
                    break
    # FINAL LOG               
    finally:
        print("CRAWLING COMPLETE.")
        print(f"Crawled {output_pipeline.crawled_page_count} Pages.")
        print(f"Total {output_pipeline.product_count} information added to Database.")
        

async def main():
    await crawl_products(test_mode=test_mode)

if __name__ == '__main__':
    asyncio.run(main())