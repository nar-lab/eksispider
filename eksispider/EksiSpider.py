import scrapy
class EksiSpider(scrapy.Spider):
    name = "eksispider"
    start_urls = ["http://eksisozluk.com",]
    
    def parse(self,response):
        entries = response.css("ul.topic-list li")
        for entry in entries:
            yield{
                #"text": entry.xpath("a/text()").extract_first(),
                "link": "http://eksisozluk.com" + str(entry.css("a::attr(href)").extract_first())
            }
