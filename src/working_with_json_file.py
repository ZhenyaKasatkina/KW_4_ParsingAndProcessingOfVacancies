from abc import ABC
import json
import os
from config import ROOT_DIR


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



    # def add_to_file(self,):
    #     """
    #     Дописывает данные в JSON-файл
    #     """
    #     with open("vacancies.json", "w") as f:
    #         if os.stat("vacancies.json").st_size == 0:  # полный размер файла 0
    #             json.dump([self.data], f)
    #         else:
    #             with open("vacancies.json") as json_file:
    #                 data_list = json.load(json_file)
    #             data_list.append(self.data)
    #             with open("vacancies.json", "w") as json_file:
    #                 json.dump(data_list, json_file)
