from abc import ABC
import json
import os
from config import ROOT_DIR
from src.vacancies import Vacancies


class BasesJSONFile(ABC):
    """
    Работа с JSON-файлом
    """
    def save_to_file(self):
        """Сохраняет данные в файл JSON"""
        pass

    @staticmethod
    def read_data_from_file():
        """Читает данные из файла JSON"""
        pass

    @staticmethod
    def del_data_in_file():
        """Удаляет данные в файле JSON"""
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


class JSONFileVacancy(BasesJSONFile):
    """
    Работа с вакансиями в JSON-файле
    """

    def __init__(self, data):
        self.data = data
        self.filter_data = []

    def save_to_file(self) -> None:
        """
        Сохраняет данные в JSON-файл
        """
        with open(os.path.join(ROOT_DIR, "src", "vacancies.json"), "w", encoding="utf-8") as json_file:
            json.dump(self.data, json_file, indent=4, ensure_ascii=False)

    @staticmethod
    def read_data_from_file():
        """
        Чтение информации из файла
        """
        with open(os.path.join(ROOT_DIR, "src", "vacancies.json")) as json_file:
            data_list = json.load(json_file)
            return data_list

    @staticmethod
    def del_data_in_file():
        """
        Удаляет данные в файле JSON
        """
        with open(os.path.join(ROOT_DIR, "src", "vacancies.json"), "w", encoding="utf-8") as json_file:
            json_file.close()

    def sort_vacancies(self):
        """
        Сортирует вакансии по увеличению заработной платы
        """
        data_list = self.read_data_from_file()
        instances_list = []
        for item in data_list:
            vacancy = Vacancies(item["vacancy_name"], item["salary_from"], item["salary_to"],
                                item["town"], item["employer"], item["link_to_ad"], item["responsibility"])
            instances_list.append(vacancy)
            self.filter_data.append(item)
        sorting_vac = sorted(instances_list, key=lambda z: z.salary, reverse=True)
        return sorting_vac

    def get_top_by_salary(self, top: int):
        """
        Выводит ТОП-30 по заработной плате объявлений
        в выбранной пользователем валюте
        """
        sorting_vac = self.sort_vacancies()
        top_vac = sorting_vac[:top]
        print(*top_vac, sep="\n")
        list_vac_dict = []
        for vacancy in top_vac:
            vac_dict = vacancy.__dict__
            list_vac_dict.append(vac_dict)
        if not list_vac_dict:
            print("Нет вакансий, соответствующих заданным критериям.")
        else:
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
                print(f"{count}. {vacancy}")
                count += 1
        if not list_vac_dict:
            print("Нет вакансий, соответствующих заданным критериям.")
        else:
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
                print(f"{count}. {vacancy}")
                count += 1
        if not list_vac_dict:
            print("Нет вакансий, соответствующих заданным критериям.")
        else:
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
                print(f"{count}. {vacancy}")
                count += 1

        if not list_vac_dict:
            print("Нет вакансий, соответствующих заданным критериям.")
        else:
            return list_vac_dict
