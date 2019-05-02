import scrapy
import json
import time
from bs4 import BeautifulSoup, NavigableString

class LinkCollector(scrapy.Spider):
    name = "linkspider"
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

        entries =  response.xpath("//ul[@id='entry-list']/li")

        for entry in entries:
            content_s = BeautifulSoup(entry.css("div.content").extract_first())

            anc_tags = content_s.select("a")
            if len(anc_tags) > 0:
                additional_urls = ["http://eksisozluk.com" + str(x["href"]) for x in anc_tags if "/?q=" in x["href"]]
                for url in additional_urls:
                    with open("additional_urls.txt","a") as f:
                        try:
                            f.writelines(url + "\n")
                        except:
                            pass
                        finally:
                            f.close()
                            f.flush()
