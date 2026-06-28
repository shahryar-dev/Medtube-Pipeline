# medtalks/spiders/medvideo_spider.py
import scrapy

class PubMedSpider(scrapy.Spider):
    name = "medvideo_spider"
    current_page = 1
    base_url = "https://pmc.ncbi.nlm.nih.gov/search/?term=urology&page="
    start_urls = [f"{base_url}1"]

    def parse(self, response):
        self.logger.info(f"📚 Crawling Page {self.current_page}...")
        
        # Bulletproof link extraction
        article_links = list(set(response.css('a[href*="/articles/PMC"]::attr(href)').getall()))
        
        for link in article_links:
            yield response.follow(link, callback=self.parse_article)

        # Pagination: Loop up to page 5
        if self.current_page < 5:
            self.current_page += 1
            yield scrapy.Request(f"{self.base_url}{self.current_page}", callback=self.parse)

    def parse_article(self, response):
        yield {
            "title": response.css('h1::text, h1.content-title::text').get(default='N/A').strip(),
            "authors": [a.strip() for a in response.css('.contrib-group a::text').getall() if a.strip()],
            "doi": response.css('span.doi a::text, a[href*="doi.org"]::text').get(default='N/A'),
            "abstract": " ".join([p.strip() for p in response.css('.abstract p::text').getall() if p.strip()]),
            "source_url": response.url
        }