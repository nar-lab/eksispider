from subprocess import call
import json
import os

class EksiLinkCrawl(object):

    def __init__(self):
        pass

    def extract_tt(self):
        call("scrapy runspider EksiSpider.py -o solframe.jl")

    def extract_a(self):
        call("scrapy runspider LinkCollector.py")

    def crawl_content(self):
        call("scrapy runspider EntrySpider.py -o icerik.jl")

    def combine_urls(self):
        with open("solframe.jl") as f:
            topics = f.readlines()
        topics_js = [json.loads(topic) for topic in topics]
        urls_sol = [x["link"] for x in topics_js if "link" in x]
        urls_sol = [x for x in urls_sol if x is not None]

        with open("additional_urls.txt") as f:
            urls_content = f.readlines()
        urls_content = [x[:-1] for x in urls_content]
        urls = list(set().union(urls_sol,urls_content))
        urls = ['{"link":"' + x + '"}\n' for x in urls]
        return urls

    def file_ops(self, url_list):
        os.remove("solframe.jl")
        os.remove("additional_urls.txt")
        with open("solframe.jl","a") as f:
            for url in url_list:
                f.writelines(url)
            f.close()

    def follow_links(self):
        self.extract_tt()
        for cnt in range(5):
            self.extract_a()
            urls = self.combine_urls()
            self.file_ops(urls)
        self.crawl_content()

if __name__ == "__main__":
    eksi = EksiLinkCrawl()
    eksi.follow_links()
    
