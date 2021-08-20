"""1) Написать программу, которая собирает входящие письма из своего или тестового почтового ящика и сложить данные о
письмах в базу данных (от кого, дата отправки, тема письма, текст письма полный)
Логин тестового ящика: study.ai_172@mail.ru
Пароль тестового ящика: NextPassword172!!!"""
import hashlib

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
from pymongo import MongoClient, errors
import datetime

chrome_options = Options()
chrome_options.add_argument("start-maximized")

driver = webdriver.Chrome(executable_path="./chromedriver.exe", options=chrome_options)

driver.get("https://mail.ru/")


def month_converter(d):
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
        d = d.replace(key, str(value))

    return d


def date_format(date_str):
    date = date_str.split()
    day = datetime.date.today().day
    month = datetime.date.today().month
    year = datetime.date.today().year
    time = datetime.datetime.strptime(date[1], "%H:%M")

    if date[0] == "Вчера,":
        yesterday = (datetime.date.today() - datetime.timedelta(days=1))
        day = yesterday.day
        month = yesterday.month
        year = yesterday.year
    elif date[0] != "Сегодня,":
        day = date[0]
        month = month_converter(date[1][:-1])
        year = datetime.date.today().year
        time = datetime.datetime.strptime(date[2], "%H:%M")

    date = datetime.datetime(year, month, day, time.hour, time.minute)
    return date


def mail_login(mail, password):
    login = driver.find_element_by_class_name("email-input")
    login.send_keys(mail)

    passw_button = driver.find_element_by_xpath("//button[contains(text(), 'Ввести пароль')]")
    passw_button.click()

    sleep(0.2)
    passw = driver.find_element_by_class_name("password-input")
    passw.send_keys(password)

    login_button = driver.find_element_by_class_name("second-button")
    login_button.click()


def get_all_mail():
    mail = []
    while True:
        sleep(1)
        info = get_mail_info()
        mail.append(info)
        next_mail = driver.find_element_by_class_name("button2_arrow-down")
        if 'disabled' in next_mail.get_attribute('class').split():
            break
        else:
            next_mail.click()
    return mail


def get_mail_info():
    mail_item = {}
    sender = driver.find_element_by_class_name('letter-contact').text
    date = date_format(driver.find_element_by_class_name('letter__date').text)
    subject = driver.find_element_by_tag_name('h2').text
    text = driver.find_element_by_class_name('letter__body').text

    mail_item["sender"] = sender
    mail_item["date"] = date
    mail_item["subject"] = subject
    mail_item["text"] = text
    mail_item["_id"] = hashlib.sha1(str(mail_item).encode()).hexdigest()

    return mail_item


def insert_mail(result):
    client = MongoClient('127.0.0.1', 27017)
    db = client['mail']
    for item in result:
        try:
            db.mail.insert_one(item)
        except errors.DuplicateKeyError:
            print("Письмо уже есть в базе")


mail_login("study.ai_172", "NextPassword172!!!")

sleep(5)
first_mail = driver.find_element_by_class_name("js-letter-list-item")
first_mail.click()
get_all_mail()


insert_mail(get_all_mail())
driver.close()
