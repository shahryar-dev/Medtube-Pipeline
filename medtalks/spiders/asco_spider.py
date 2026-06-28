import scrapy
import json
import os
from urllib.parse import urlencode

class AscoSpiderSpider(scrapy.Spider):
    name = "asco_spider"
    
    # We use a dummy URL to kick off the spider engine natively
    start_urls = ["https://httpbin.org/get"]

    def parse(self, response):
        """
        Instead of relying on start_requests, Scrapy opens this default parse method.
        From here, we dynamically hand over to SerpApi.
        """
        serpapi_key = os.environ.get("SERPAPI_KEY")
        
        if not serpapi_key or "YOUR_SECRET" in serpapi_key:
            self.logger.error("❌ ERROR: SERPAPI_KEY env variable is empty or using placeholder!")
            return

        query = "site:conferences.asco.org/am/abstracts video presentation"
        params = {
            "engine": "google",
            "q": query,
            "api_key": serpapi_key,
            "num": 5
        }
        
        serpapi_url = f"https://serpapi.com/search.json?{urlencode(params)}"
        self.logger.info(f"🚀 ENGINE ACTIVE: Swapping to SerpApi -> {serpapi_url}")
        
        yield scrapy.Request(url=serpapi_url, callback=self.parse_serpapi, dont_filter=True)

    def parse_serpapi(self, response):
        self.logger.info("✅ SUCCESS: Received response from SerpApi.")
        data = json.loads(response.body)
        organic_results = data.get("organic_results", [])
        
        if not organic_results:
            self.logger.warning("⚠️ SerpApi returned zero organic results. Check query limits or key parameters.")
        
        for result in organic_results:
            link = result.get("link")
            if link:
                self.logger.info(f"🔗 Crawling discovered medical abstract: {link}")
                yield scrapy.Request(url=link, callback=self.parse_conference_page, dont_filter=True)

    def parse_conference_page(self, response):
        self.logger.info(f"📄 Extracting data from: {response.url}")
        yield {
            "title": response.css('h1::text').get(default='No Title').strip(),
            "source_url": response.url
        }
