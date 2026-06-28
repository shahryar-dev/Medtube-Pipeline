import scrapy

class ResearchSpider(scrapy.Spider):
    name = "research_spider"
    
    # 1. The Target: Pure Scrapy needs a direct, static starting URL
    allowed_domains = ["arxiv.org"]
    start_urls = ["https://arxiv.org/list/cond-mat.mtrl-sci/recent"]

    def parse(self, response):
        self.logger.info(f"📄 Connected to: {response.url}")
        
        # 2. The Extraction: We isolate the HTML block containing the paper details
        papers = response.css('div#dlpage dl dd')
        
        for paper in papers:
            # Clean up the raw text extracted from the HTML tags
            raw_title = paper.css('div.list-title ::text').getall()
            title = "".join(raw_title).replace('Title:', '').strip()
            
            raw_subjects = paper.css('div.list-subjects ::text').getall()
            subjects = "".join(raw_subjects).replace('Subjects:', '').strip()
            
            authors = paper.css('div.list-authors a::text').getall()

            # 3. The Yield: Send the structured data to the output file
            yield {
                "title": title,
                "authors": authors,
                "subjects": subjects
            }
