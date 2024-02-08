from abc import ABC
import json
import csv
import os
from config import ROOT_DIR
from src.vacancies import Vacancies

DIR = "src"
JSONFILE = 'vacancies.json'
CSVFILE = 'vacancies.csv'


class BasesFileVacancy(ABC):
    """
    Работа с файлом
    """
    def save_to_file(self):
        """Сохраняет данные в файл"""
        pass

    @staticmethod
    def read_data_from_file():
        """Читает данные из файла"""
        pass

    @staticmethod
    def del_data_in_file():
        """Удаляет данные в файле"""
        pass

    def sort_vacancies(self):
        """Сортирует вакансии по увеличению заработной платы"""
        pass

    def get_top_by_salary(self, top: int):
        """Выводит ТОП-30 по заработной плате объявлений
        в выбранной пользователем валюте"""
        pass

    def get_user_salary_ad(self, user_salary_from: int, user_salary_to: int):
        """Выводит объявления по заработной плате, указанной пользователем"""
        pass

    def get_ad_by_keyword(self, keyword: str):
        """Выводит объявления по ключевому слову в описании, указанному пользователем"""
        pass

    def get_ad_by_name_town(self, town: str):
        """Выводит объявления по определенному городу"""
        pass

    def __str__(self):
        pass


class JSONFileVacancy(BasesFileVacancy):
    """
    Работа с вакансиями в JSON-файле
    """

    def __init__(self, data):
        self.data = data

    def save_to_file(self) -> None:
        """
        Сохраняет данные в JSON-файл
        """
        with open(os.path.join(ROOT_DIR, DIR, JSONFILE), "w", encoding="utf-8") as json_file:
            json.dump(self.data, json_file, indent=4, ensure_ascii=False)

    @staticmethod
    def read_data_from_file():
        """
        Чтение информации из JSON-файла
        """
        with open(os.path.join(ROOT_DIR, DIR, JSONFILE)) as json_file:
            data_list = json.load(json_file)
            return data_list

    @staticmethod
    def del_data_in_file():
        """
        Удаляет данные в файле JSON
        """
        with open(os.path.join(ROOT_DIR, DIR, JSONFILE), "w", encoding="utf-8") as json_file:
            json_file.close()

    def sort_vacancies(self):
        """
        Сортирует вакансии по увеличению заработной платы
        """
        data_list = self.read_data_from_file()
        instances_list = []
        for item in data_list:
            vacancy = Vacancies(item["job_title"], item["salary_from"], item["salary_to"],
                                item["town"], item["employer"], item["url"], item["responsibilities"])
            instances_list.append(vacancy)
            self.data.append(item)
        sorting_vac = sorted(instances_list, key=lambda z: z.salary, reverse=True)
        return sorting_vac

    def get_top_by_salary(self, top: int):
        """
        Выводит ТОП-30 по заработной плате объявлений
        в выбранной пользователем валюте
        """
        sorting_vac = self.sort_vacancies()
        top_vac = sorting_vac[:top]
        list_vac_dict = []
        for vacancy in top_vac:
            vac_dict = vacancy.__dict__
            list_vac_dict.append(vac_dict)
        return list_vac_dict

    def get_user_salary_ad(self, user_salary_from: int, user_salary_to: int):
        """
        Выводит объявления по заработной плате, указанной пользователем
        """
        sorting_vac = self.sort_vacancies()
        list_vac_dict = []
        count = 1
        for vacancy in sorting_vac:
            if vacancy.salary_from >= user_salary_from and vacancy.salary_to <= user_salary_to:
                vac_dict = vacancy.__dict__
                list_vac_dict.append(vac_dict)
                count += 1
        return list_vac_dict

    def get_ad_by_keyword(self, keyword: str):
        """
        Выводит объявления по ключевому слову в описании,
        указанному пользователем
        """
        sorting_vac = self.sort_vacancies()
        list_vac_dict = []
        count = 1
        for vacancy in sorting_vac:
            if keyword in vacancy.responsibilities:
                vac_dict = vacancy.__dict__
                list_vac_dict.append(vac_dict)
                count += 1
        return list_vac_dict

    def get_ad_by_name_town(self, town: str):
        """
        Выводит объявления по определенному городу
        """
        sorting_vac = self.sort_vacancies()
        list_vac_dict = []
        count = 1
        for vacancy in sorting_vac:
            if town == vacancy.town:
                vac_dict = vacancy.__dict__
                list_vac_dict.append(vac_dict)
                count += 1
        return list_vac_dict

    def __str__(self):
        data = ""
        for item in self.data:
            str_data = f'{item["job_title"]}, {item["salary_from"]}-{item["salary_to"]} '\
                       f'{item["town"]}, {item["employer"]}, {item["url"]}\n'
            data += str_data
        return data


class CSVFileVacancy(BasesFileVacancy):
    """
    Работа с вакансиями в JSON-файле
    """

    def __init__(self, data):
        self.data = data

    def save_to_file(self) -> None:
        """
        Сохраняет данные в CSV-файл
        """
        with open(os.path.join(ROOT_DIR, DIR, CSVFILE), 'w', newline='', encoding="utf-8") as csvfile:
            fieldnames = ["job_title", "salary_from", "salary_to", "salary", "town",
                          "employer", "url", "responsibilities", "job site"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
            writer.writeheader()
            writer.writerows(self.data)

    @staticmethod
    def read_data_from_file():
        """
        Чтение информации из файла
        """
        data_list = []
        with (open(os.path.join(ROOT_DIR, DIR, CSVFILE), encoding="utf-8", newline='') as csvfile):
            reader = csv.DictReader(csvfile)
            for row in reader:
                # print(row)
                data_list.append(row)
        return data_list

    @staticmethod
    def del_data_in_file():
        """
        Удаляет данные в файле CSV
        """
        csvfile = open(os.path.join(ROOT_DIR, DIR, CSVFILE), "w+")
        csvfile.close()

    def sort_vacancies(self):
        """
        Сортирует вакансии по заработной плате
        """
        data_list = self.read_data_from_file()
        instances_list = []
        for item in data_list:
            vacancy = Vacancies(item["job_title"], item["salary_from"], item["salary_to"],
                                item["town"], item["employer"], item["url"], item["responsibilities"])
            instances_list.append(vacancy)
            self.data.append(item)
        sorting_vac = sorted(instances_list, key=lambda z: z.salary, reverse=True)
        return sorting_vac

    def get_top_by_salary(self, top: int):
        """
        Выводит ТОП объявления по заработной плате
        """
        sorting_vac = self.sort_vacancies()
        top_vac = sorting_vac[:top]
        list_vac_dict = []
        for vacancy in top_vac:
            vac_dict = vacancy.__dict__
            list_vac_dict.append(vac_dict)
        return list_vac_dict

    def get_user_salary_ad(self, user_salary_from: int, user_salary_to: int):
        """
        Выводит объявления по заработной плате, указанной пользователем
        """
        sorting_vac = self.sort_vacancies()
        list_vac_dict = []
        count = 1
        for vacancy in sorting_vac:
            if vacancy.salary_from >= user_salary_from and vacancy.salary_to <= user_salary_to:
                vac_dict = vacancy.__dict__
                list_vac_dict.append(vac_dict)
                count += 1
        return list_vac_dict

    def get_ad_by_keyword(self, keyword: str):
        """
        Выводит объявления по ключевому слову в описании,
        указанному пользователем
        """
        sorting_vac = self.sort_vacancies()
        list_vac_dict = []
        count = 1
        for vacancy in sorting_vac:
            if keyword in vacancy.responsibilities:
                vac_dict = vacancy.__dict__
                list_vac_dict.append(vac_dict)
                count += 1
        return list_vac_dict

    def get_ad_by_name_town(self, town: str):
        """
        Выводит объявления по определенному городу
        """
        sorting_vac = self.sort_vacancies()
        list_vac_dict = []
        count = 1
        for vacancy in sorting_vac:
            if town == vacancy.town:
                vac_dict = vacancy.__dict__
                list_vac_dict.append(vac_dict)
                count += 1
        return list_vac_dict

    def __str__(self):
        data = ""
        for item in self.data:
            str_data = f'{item["job_title"]}, {item["salary_from"]}-{item["salary_to"]} '\
                       f'{item["town"]}, {item["employer"]}, {item["url"]}\n'
            data += str_data
        return data
