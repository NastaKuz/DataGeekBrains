"""Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
Для парсинга использовать XPath. Структура данных должна содержать:
1. название источника;
2. наименование новости;
3. ссылку на новость;
4. дата публикации.
Сложить собранные данные в БД
Минимум один сайт, максимум - все три"""
import datetime
from lxml import html
import requests
import hashlib
import NewsMongo as db


def month_converter(date):
    months = {
      'января': "jan",
      'февраля': "feb",
      'марта': "mar",
      'апреля': "apr",
      'мая': "may",
      'июня': "jun",
      'июля': "jul",
      'августа': "aug",
      'сентября': "sep",
      'октября': "oct",
      'ноября': "nov",
      'декабря': "dec"
    }
    for key, value in months.items():
        date = date.replace(key, str(value))

    return date


def lenta_news():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/92.0.4515.107 Safari/537.36"
    }
    main_link = 'https://lenta.ru'
    response = requests.get(main_link, headers=header)

    dom = html.fromstring(response.text)

    news_block = dom.xpath("//div[@class='span8 js-main__content']")[0]
    items = news_block.xpath(".//div[@class='item' or @class='first-item']")

    news = []

    for item in items:
        news_item = {}
        source = 'lenta.ru'
        xp = ".//a[contains(@href, 'news')]"

        name = item.xpath(xp + "/text()")[0]
        link = main_link + item.xpath(xp + "/@href")[0]
        date = item.xpath(xp + "/time/@datetime")[0].strip()

        news_item["source"] = source
        news_item["name"] = name.replace("\xa0", " ")
        news_item["link"] = link
        news_item["date"] = datetime.datetime.strptime(month_converter(date), "%H:%M, %d %b %Y")
        news_item["_id"] = hashlib.sha1(str(news_item).encode()).hexdigest()

        news.append(news_item)

    return news


def yandex_news():
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/92.0.4515.107 Safari/537.36"
    }
    main_link = "https://yandex.ru/news"
    response = requests.get(main_link, headers=header)

    dom = html.fromstring(response.text)

    items = dom.xpath("//a[contains(@href, 'rubric=politics') and @class='mg-card__link']/ancestor::article")

    news = []

    for item in items:
        news_item = {}
        source = item.xpath(".//a[contains(@class, 'source-link')]/text()")[0]
        name = item.xpath(".//h2/text()")[0]
        link = item.xpath(".//a[@class='mg-card__link']/@href")[0]
        time = datetime.datetime.strptime(item.xpath(".//span[contains(@class, 'time')]/text()")[0], "%H:%M")
        news_item["source"] = source
        news_item["name"] = name.replace("\xa0", " ")
        news_item["link"] = link
        news_item["date"] = datetime.datetime.now().replace(hour=time.hour, minute=time.minute)
        news_item["_id"] = hashlib.sha1(str(news_item).encode()).hexdigest()
        news.append(news_item)

    return news


# db.insert_news(lenta_news())
# db.insert_news(yandex_news())
