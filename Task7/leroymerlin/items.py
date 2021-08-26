# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy
from itemloaders.processors import MapCompose, TakeFirst


def get_number(value):
    try:
        return float(value)
    except:
        return value


def get_params(value):
    result = value.replace("\n", "").strip()
    return get_number(result)


def get_price(value):
    result = value.replace(" ", "")
    return get_number(result)


class LeroymerlinItem(scrapy.Item):
    _id = scrapy.Field()
    link = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    params = scrapy.Field(input_processor=MapCompose(get_params))
    price = scrapy.Field(input_processor=MapCompose(get_price),
                         output_processor=TakeFirst())
    print()
