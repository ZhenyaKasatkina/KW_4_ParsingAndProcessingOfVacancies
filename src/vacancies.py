
class Vacancies:

    def __init__(self, job_title: str, salary_from: int | None, salary_to: int | None,
                 town: str, employer: str, url: str, responsibilities: str) -> None:

        self.job_title = job_title                              # должность
        self.salary_from = self._is_valid_salary(salary_from)   # зарплата ОТ
        self.salary_to = self._is_valid_salary(salary_to)       # зарплата ДО
        self.salary = self.compare_salary()                     # максимальная ЗП из указанной в объявлении
        self.employer = self._is_valid_employer(employer)       # работодатель
        self.town = self._is_valid_town(town)                   # город
        self.url = self._is_valid_url(url)                      # ссылка на объявление
        self.responsibilities = self._is_valid_responsibilities(responsibilities)     # обязанности/требования

    @staticmethod
    def _is_valid_salary(salary):
        """Проверка заработной платы на предмет указания ее размера"""
        if not salary:
            salary = 0
        return int(salary)

    @staticmethod
    def _is_valid_employer(employer):
        """Проверка работодателя на предмет указания его наименования"""
        if not employer:
            employer = "Работодатель не указан"
        return employer

    @staticmethod
    def _is_valid_town(town):
        """Проверка города на предмет его указания"""
        if not town:
            town = "Город не указан"
        return town

    @staticmethod
    def _is_valid_url(url):
        """Проверка ссылки на объявление на предмет её указания"""
        if not url:
            url = "Ссылка на объявление не указана"
        return url

    @staticmethod
    def _is_valid_responsibilities(responsibilities):
        """Проверка наличия указания в объявлении обязанностей и требований к кандидату"""
        if not responsibilities:
            responsibilities = "Обязанности и требования к кандидату не  указаны"
        return responsibilities

    def compare_salary(self):
        """Сравниваем указанную в одном объявлении заработную плату
        от ... с до ..., например:
        от 50000 до "не указано", или от 50000 до 100000,
        и выводим большую по значению ЗП"""
        if self.salary_from > self.salary_to:
            return self.salary_from
        else:
            return self.salary_to

    def __ge__(self, other):
        return (self.salary_from >= other.salary_from
                or self.salary >= other.salary)

    def __le__(self, other):
        return self.salary_to <= other.salary_to

    def __str__(self):
        return (f"{self.job_title} {self.salary_from}-{self.salary_to}, {self.town}, "
                f"{self.employer}, {self.url}, {self.responsibilities}\n")

    def __repr__(self):
        return (f"{self.job_title} {self.salary_from}-{self.salary_to} ({self.salary}), "
                f"{self.town}, {self.employer}, "
                f"{self.url}, {self.responsibilities}\n")
