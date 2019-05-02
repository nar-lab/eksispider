import scrapy
import json
import time
from bs4 import BeautifulSoup, NavigableString

class EntrySpider(scrapy.Spider):
    name = "entryspider"
    def start_requests(self):
        with open("solframe.jl","r") as f:
            topics = f.readlines()
            topic_list = [json.loads(topic) for topic in topics]
            urls = [topic["link"] for topic in topic_list if "link" in topic]
            for url in urls:
                yield scrapy.Request(url = url, callback = self.pager)


    def pager(self,response):
        pager =  int(response.css("div.pager").xpath("@data-pagecount").extract_first())
        base_link = response.url
        for i in range(pager):
            page_url = str(base_link) + "&p=" + str(i)
            yield scrapy.Request(url = page_url, callback = self.parse)

    def parse(self, response):
        req_url = response.url

        baslik = response.xpath("//h1[@id='title']/a/span/text()").extract_first()
        entries =  response.xpath("//ul[@id='entry-list']/li")

        for entry in entries:
            content_s = BeautifulSoup(entry.css("div.content").extract_first())

            strip_text = content_s.findAll(text=lambda text:isinstance(text, NavigableString))
            content = u" ".join(strip_text)

            yield{
                "id": entry.xpath("@data-id").extract(),
                "author": entry.xpath("@data-author").extract(),
                "header":baslik,
                "content": content,
                "url": req_url,
            }
