from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Task7.leroymerlin import settings
from Task7.leroymerlin.spiders.leroymerlin import LeroymerlinSpider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(LeroymerlinSpider, search="краска")
    # crawler_process.crawl(LeroymerlinSpider, '')

    crawler_process.start()
