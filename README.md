# MEDtube-Pipeline
An asynchronous web scraping pipeline built with Scrapy, designed to aggregate medical literature and video metadata.

## Features
- **Asynchronous Crawling:** Uses Scrapy’s engine to navigate high-volume data sources efficiently.
- **Resilient Extraction:** Implements wildcard DOM selectors to handle UI layout updates.
- **Automated Pagination:** Automatically traverses multi-page search results.
- **Data Pipeline:** Includes a custom pipeline to clean and structure messy HTML text into a clean CSV format.

## Challenges Overcome
- **WAF Bypass:** Encountered and analyzed TLS-based blocking mechanisms from enterprise firewalls.
- **Data Normalization:** Built a custom pipeline to clean unstructured medical text (removing Unicode characters and excess whitespace).

## How to Run
1. Install requirements: `pip install scrapy`
2. Run the crawler: `scrapy crawl medvideo_spider -o pubmed_data.csv`