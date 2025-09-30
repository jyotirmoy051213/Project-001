import scrapy

class ProductCrawler(scrapy.Spider):
    name = 'product_crawler'
    start_urls = [f'https://computermania.com.bd/page/{i}/?s=e&post_type=product' for i in range(1, 149)]
    
    def parse(self, response):
        product_links = response.xpath('//a[@class="product-image-link"]/@href').getall()
        
        for link in product_links:
            yield {'product_link': link}