"""Необходимо собрать информацию о вакансиях на вводимую должность (используем input или через аргументы получаем
должность) с сайтов HH(обязательно) и/или Superjob(по желанию). Приложение должно анализировать несколько страниц сайта
(также вводим через input или аргументы). Получившийся список должен содержать в себе минимум:
1. Наименование вакансии.
2. Предлагаемую зарплату (отдельно минимальную и максимальную).
3. Ссылку на саму вакансию.
4. Сайт, откуда собрана вакансия.
По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение). Структура должна быть
одинаковая для вакансий с обоих сайтов. Общий результат можно вывести с помощью dataFrame через pandas. Сохраните в
json либо csv."""

import json
import pandas as pd

import requests
from bs4 import BeautifulSoup as bs


def get_salary(salary):
    min_s, max_s, curr = None, None, None
    job_slices = salary.split()
    if "–" in salary:
        min_s = job_slices[0]
        max_s = job_slices[2]
        curr = job_slices[3]
    else:
        curr = job_slices[2]
        if job_slices[0] == "от":
            min_s = job_slices[1]
        elif job_slices[0] == "до":
            max_s = job_slices[1]
    return min_s, max_s, curr


def hh_job_list(pages, search_text):
    main_url = "https://hh.ru"

    params = {
        "text": search_text
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/92.0.4515.107 Safari/537.36"
    }

    response = requests.get(main_url + "/search/vacancy", params=params, headers=headers)
    soup = bs(response.text, "html.parser")

    jobs = []

    for _ in range(pages):
        jobs_list = soup.find_all('div', {"class": "vacancy-serp-item"})
        for job in jobs_list:
            job_data = {}
            title = job.find('a', {"class": "bloko-link"})
            job_name = title.getText()
            job_link = title["href"]
            try:
                job_salary = job.find("span", {"data-qa": "vacancy-serp__vacancy-compensation"}).getText() \
                    .replace(u"\u202f", "")
                min_salary, max_salary, currency = get_salary(job_salary)
            except:
                max_salary, min_salary, currency = None, None, None

            job_data = {
                "name": job_name,
                "link": job_link,
                "min_salary": min_salary,
                "max_salary": max_salary,
                "currency": currency,
                "source": "hh"
            }
            jobs.append(job_data)

        try:
            next_page = soup.find("a", {"data-qa": "pager-next"})["href"]
            response = requests.get(main_url + next_page, headers=headers)
            soup = bs(response.text, "html.parser")
        except:
            break

    return jobs


result = hh_job_list(2, "python")
#
# df = pd.DataFrame(data=result)
# print(df)

with open('hhInfo.json', 'w') as file:
    json.dump(result, file)
