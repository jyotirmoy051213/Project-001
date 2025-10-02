"""
This script has Website variables for startech.com
urls_to_crawl --> Categories of products and URLs to go through in the website 
schema --> Handcrafted JSON Schema of Startech website (Upto 01/10/2025) to extract from crawled content - LLM-free extraction strategy
"""

# List of product categories and their URLs
URLS_TO_CRAWL = [
    {"category": "Desktop", "base_url": "https://www.startech.com.bd/desktops"},
    {"category": "Laptop", "base_url": "https://www.startech.com.bd/laptop-notebook"},
    {"category": "Component", "base_url": "https://www.startech.com.bd/component"},
    {"category": "Monitor", "base_url": "https://www.startech.com.bd/monitor"},
    {"category": "Power", "base_url": "https://www.startech.com.bd/power"},
    {"category": "Phone", "base_url": "https://www.startech.com.bd/mobile-phone"},
    {"category": "Tablet", "base_url": "https://www.startech.com.bd/tablet-pc"},
    {"category": "Office Equipment", "base_url": "https://www.startech.com.bd/office-equipment"},
    {"category": "Camera", "base_url": "https://www.startech.com.bd/camera"},
    {"category": "Security", "base_url": "https://www.startech.com.bd/Security-Camera"},
    {"category": "Networking", "base_url": "https://www.startech.com.bd/networking"},
    {"category": "Software", "base_url": "https://www.startech.com.bd/software"},
    {"category": "Server & Storage", "base_url": "https://www.startech.com.bd/server-networking"},
    {"category": "Accessories", "base_url": "https://www.startech.com.bd/accessories"},
    {"category": "Gadget", "base_url": "https://www.startech.com.bd/gadget"},
    {"category": "Gaming", "base_url": "https://www.startech.com.bd/gaming"},
    {"category": "TV", "base_url": "https://www.startech.com.bd/television-shop"},
    {"category": "Appliance", "base_url": "https://www.startech.com.bd/appliance"},
]


# Handcrafted schema for JsonCssExtractionStrategy by inspecting the webpage
SCHEMA_FOR_EXTRACTION = {
        "name": "Product",
        "baseSelector": ".p-item-inner",            
        "fields": [
            {"name": "name", "selector": ".p-item-name a", "type": "text"},
            {"name": "image_url", "selector": ".p-item-img img", "type": "attribute", "attribute": "src"},
            {"name": "description", "selector": ".short-description li", "type": "list", "fields": [{"name": "feature","type": "text"}]},
            {"name": "price", "selector": ".p-item-price span", "type": "text"},
            {"name": "url", "selector": ".p-item-tag a", "type": "attribute", "attribute": "href"}
            ] 
        }

# base_url_format:: Copy and paste as "base_url" variable for startech website


# CSS Selector for crawler
CSS_SELECTOR = ".main-content.p-items-wrap"