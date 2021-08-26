from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from Task6.booksparser import settings
from Task6.booksparser.spiders.book24ru import Book24Spider

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    crawler_process = CrawlerProcess(settings=crawler_settings)
    crawler_process.crawl(Book24Spider)

    crawler_process.start()
