"""1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию, записывающую собранные
вакансии в созданную БД.
2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше введённой суммы.
3. Написать функцию, которая будет добавлять в вашу базу данных только новые вакансии с сайта."""
from pymongo import MongoClient
import JobInfo as jobI

client = MongoClient('127.0.0.1', 27017)
db = client['jobs']

job_collection = db.jobs


def insert_jobs(pages, keyword, jobs):  # задания 1 и 3
    result = jobI.hh_job_list(pages, keyword)
    for item in result:
        job_check = jobs.find({"_id": item["_id"]})
        try:
            job_check.next()
        except:
            jobs.insert_one(item)
    print(result)


def salary_sort(jobs, salary):  # задание 2
    for job in jobs.find({"$or": [{"min_salary": {"$gt": salary}}, {"max_salary": {"$gt": salary}}]}, {'_id': 0}):
        print(job)


# insert_jobs(2, "python", job_collection)
# salary_sort(job_collection, 40000)
