from abc import ABC
import os
import requests

"""Создать абстрактный класс для работы с API сайтов с вакансиями. 
Реализовать классы, наследующиеся от абстрактного класса, 
для работы с конкретными платформами. Классы должны уметь подключаться к API 
и получать вакансии."""

SUPER_JOB_API_KEY = os.getenv("SUPER_JOB_API_KEY")


class JobSiteAPI(ABC):

    def get_data(self):
        """Получает данные по вакансиям
        с сайта по поиску работы через API"""
        pass

    def get_vacancies(self):
        """Наполнение списка установленного образца объявлениями"""
        pass

    def __str__(self):
        pass


class HeadHunterAPI(JobSiteAPI):

    def __init__(self, vacancy_name):
        self.vacancy_name = vacancy_name

    def get_data(self):
        """
        Получает данные по вакансиям
        с сайта HH через API (до 600 объявлений)
        """
        count_page = 0
        list_vacancies = []
        while count_page < 6:

            params = {
                "per_page": 100,
                "page": count_page,
                "text": self.vacancy_name,
                "only_with_salary": "true",
                "items": [{}]
            }

            bases_url = 'https://api.hh.ru/'
            method_name = "vacancies"
            response = requests.get(f"{bases_url}{method_name}", params=params)
            # print(response.json(), len(response.json()), count_page)
            # print(response.status_code)
            if response.json():
                list_vacancies.extend(response.json()["items"])
                count_page += 1
            else:
                break
        return list_vacancies

    def get_vacancies(self):
        """
        Наполнение списка установленного образца объявлениями с сайта HH
        """
        list_of_suitable_vacancies = []   # Список подходящих вакансий

        all_ad = self.get_data()
        for item in all_ad:
            if item["type"]["name"] == "Открытая" and item["salary"]["currency"] == "RUR":
                ad = {"job_title": item["name"],                 # Название вакансии
                      "salary_from": item["salary"]["from"],        # Зарплата От...
                      "salary_to": item["salary"]["to"],            # Зарплата До...
                      "employer": item["employer"]["name"],         # Работодатель
                      "town": item["area"]["name"],                 # Город
                      "url": item["alternate_url"],          # Ссылка на объявление
                      "responsibilities": f'{item["snippet"]["responsibility"]}, '
                                          f'{item["snippet"]["requirement"]}',   # Обязанности, требования
                      "job site": "Head Hunter"}                    # Сайт вакансий
                list_of_suitable_vacancies.append(ad)
        return list_of_suitable_vacancies

    def __str__(self):
        pass


class SuperJobAPI(JobSiteAPI):

    def __init__(self, vacancy_name):
        self.vacancy_name = vacancy_name

    def get_data(self):
        """
        Получает данные по вакансиям
        с сайта SJ через API
        """
        count_page = 0
        list_vacancies = []
        while True:
            params = {
                "count": 40,
                "page": count_page,
                "keyword": self.vacancy_name,
                "objects": [{}]
            }

            bases_url = "https://api.superjob.ru/"
            version = "2.0"
            method_name = "vacancies"
            headers = {"X-Api-App-Id": SUPER_JOB_API_KEY}

            response = requests.get(f"{bases_url}{version}/{method_name}/", params=params, headers=headers)
            # print(response.json(), len(response.json()), count_page)
            # print(response.status_code)

            if count_page < 10:
                list_vacancies.extend(response.json()["objects"])
                count_page += 1
            else:
                break
        return list_vacancies

    def get_vacancies(self):
        """
        Наполнение списка установленного образца объявлениями с сайта SJ
        """
        list_of_suitable_vacancies = []

        all_ad = self.get_data()
        for item in all_ad:
            if not item["is_archive"] and item["currency"] == "rub":
                ad = {"job_title": item["profession"],       # Название вакансии
                      "salary_from": item["payment_from"],      # Зарплата От...
                      "salary_to": item["payment_to"],          # Зарплата До...
                      "employer": item["firm_name"],            # Работодатель
                      "town": item["town"]["title"],            # Город
                      "url": item["link"],               # Ссылка на объявление
                      "responsibilities": item["candidat"],       # Обязанности, требования
                      "job site": "Super Job"}                  # Сайт вакансий
                list_of_suitable_vacancies.append(ad)
        return list_of_suitable_vacancies

    def __str__(self):
        pass


# x = HeadHunterAPI("python")
# y = x.get_data()
# z = x.get_vacancies()
# xx = SuperJobAPI("менеджер")
# yy = xx.get_data()
# zz = xx.get_vacancies()
# all_vacancy = zz + z
# print(all_vacancy)
# print(zz, len(zz))
