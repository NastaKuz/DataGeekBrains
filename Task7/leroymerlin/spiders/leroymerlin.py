import scrapy
from scrapy.http import HtmlResponse
from Task7.leroymerlin.items import LeroymerlinItem
from scrapy.loader import ItemLoader

class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, search):
        super().__init__()
        if len(search):
            self.start_urls = [f'https://leroymerlin.ru/search/?q={search}']
        else:
            self.start_urls = ['https://leroymerlin.ru/search/?q=люстры']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@data-qa-pagination-item="right"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

        product_links = response.xpath('//a[@data-qa="product-name"]')
        for link in product_links:
            yield response.follow(link, callback=self.parse_product)

    def parse_product(self, response: HtmlResponse):
        item_loader = ItemLoader(item=LeroymerlinItem(), response=response)
        item_loader.add_value("link", response.url)
        item_loader.add_xpath("title", "//h1/text()")
        item_loader.add_xpath("photos", "//picture/img[@alt='product image']/@src")
        item_loader.add_xpath("params", "//div[@class='def-list__group']/dt/text() | "
                                        "//div[@class='def-list__group']/dd/text()")
        item_loader.add_xpath("price", "//span[@slot='price']/text()")

        yield item_loader.load_item()
