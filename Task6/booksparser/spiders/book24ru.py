import scrapy
from scrapy.http import HtmlResponse

from Task6.booksparser.items import BooksparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/knigi-bestsellery/']
    # start_urls = ['https://book24.ru/product/rota-virusov-i-batalon-bakteriy-kniga-o-detskikh-infektsiyakh-6016505/']
    page_counter = 1

    def parse(self, response: HtmlResponse):
        if response.status == 200:
            links = response.xpath("//a[contains(@class, 'product-card__name')]/@href")
            self.page_counter += 1
            next_page = f'https://book24.ru/knigi-bestsellery/page-{self.page_counter}/'

            if self.page_counter < 2:
                yield response.follow(next_page, callback=self.parse)

            for link in links:
                yield response.follow(link, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        link_data = response.url
        title_data = response.xpath("//li[contains(@class, '_last-item')]/span/text()").extract_first()
        author_data = response.xpath("//a[contains(@href, 'author') and contains(@class, "
                                     "'product-characteristic-link')]/text()").extract_first()
        author_no_link_data = response.xpath("//span[contains(text(), 'Автор:')]/../"
                                             "following-sibling::div[1]/text()").extract_first()
        main_price_data = response.xpath(
            "//span[@class='app-price product-sidebar-price__price']/text()").extract_first()
        discount_price_data = response.xpath("//span[contains(@class, 'price-old')]/text()").extract_first()
        rating_data = response.xpath("//span[@class='rating-widget__main-text']/text()").extract_first()
        yield BooksparserItem(link=link_data, title=title_data,
                              author=author_data if author_data else author_no_link_data, main_price=main_price_data,
                              discount_price=discount_price_data, rating=rating_data)
