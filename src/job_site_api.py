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
        """Возвращает объект для работы
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
        Возвращает объект для работы с сайта HH через API (до 600 объявлений)
        """
        count_page = 0
        list_vacancies = []
        while count_page < 6:

            params = {
                # "found": 1,
                "per_page": 100,
                # "pages": 1,
                "page": count_page,
                "text": self.vacancy_name,
                # "salary": "RUR",
                "only_with_salary": "true",
                "items": [{}]
            }

            bases_url = 'https://api.hh.ru/'
            method_name = "vacancies"
            response = requests.get(f"{bases_url}{method_name}", params=params)
            # print(response.json(), len(response.json()), count_page)
            # print(response.text)
            # print(response.url)
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
                ad = {"vacancy_name": item["name"],                 # Название вакансии
                      "salary_from": item["salary"]["from"],        # Зарплата От...
                      "salary_to": item["salary"]["to"],            # Зарплата До...
                      "employer": item["employer"]["name"],         # Работодатель
                      "town": item["area"]["name"],                 # Город
                      "link_to_ad": item["alternate_url"],          # Ссылка на объявление
                      "responsibility": f'{item["snippet"]["responsibility"]}, '
                                        f'{item["snippet"]["requirement"]}',   # Обязанности, требования
                      "job site": "Head Hunter"}                    # Сайт вакансий

                # print(item['name'])
                list_of_suitable_vacancies.append(ad)

        return list_of_suitable_vacancies

    def __str__(self):
        pass
        # list_of_suitable_vacancies = self.get_vacancies()
        # return (f"Получено {len(list_of_suitable_vacancies)} вакансий,"
        #         f"вот их список: {list_of_suitable_vacancies}")
        #  ПРОПИСАТЬ КЛЮЧ / ЗЗНАЧЕНИЕ


class SuperJobAPI(JobSiteAPI):

    def __init__(self, vacancy_name):
        self.vacancy_name = vacancy_name

    def get_data(self):
        """
        Возвращает объект для работы с сайта SJ через API
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

            # print(count_page)  #response.json(), len(response.json()), count_page)
            # print(response.text)
            # print(response.url)
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
                ad = {"vacancy_name": item["profession"],       # Название вакансии
                      "salary_from": item["payment_from"],      # Зарплата От...
                      "salary_to": item["payment_to"],          # Зарплата До...
                      "employer": item["firm_name"],            # Работодатель
                      "town": item["town"]["title"],            # Город
                      "link_to_ad": item["link"],               # Ссылка на объявление
                      "responsibility": item["candidat"],       # Обязанности, требования
                      "job site": "Super Job"}                  # Сайт вакансий

                # print(item["profession"])
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
