import src.vacancies
import pytest


@pytest.fixture
def data_vacancy():
    test_vacancy = src.vacancies.Vacancies("Chief Technology Officer/CTO",
                                           800000, 1200000,
                                           "Москва", "HR СНАЙПЕР",
                                           "https://hh.ru/vacancy/78157311",
                                           "Руководство подразделением (100 чел). Организация процессов."
                                           "Контроль сроков и качества выполненных работ. Образование – высшее."
                                           "Опыт работы в крупнейших мировых IT компаниях"
                                           "(Google, Facebook, Microsoft, Amazon, Авито, Озон)."
                                           "Опыт работы в должности – более 7 лет")
    return test_vacancy


def test__init__(data_vacancy):
    assert data_vacancy.job_title == "Chief Technology Officer/CTO"
    assert data_vacancy.salary_from == 800000
    assert data_vacancy.salary_to == 1200000
    assert data_vacancy.salary == 1200000
    assert data_vacancy.employer == "HR СНАЙПЕР"
    assert data_vacancy.town == "Москва"
    assert data_vacancy.url == "https://hh.ru/vacancy/78157311"
    assert data_vacancy.responsibilities == ("Руководство подразделением (100 чел). Организация процессов."
                                             "Контроль сроков и качества выполненных работ. Образование – высшее."
                                             "Опыт работы в крупнейших мировых IT компаниях"
                                             "(Google, Facebook, Microsoft, Amazon, Авито, Озон)."
                                             "Опыт работы в должности – более 7 лет")


def test_is_valid_salary(data_vacancy):
    assert data_vacancy._is_valid_salary(5000) == 5000
    assert data_vacancy._is_valid_salary(None) == 0


def test_is_valid_employer(data_vacancy):
    assert data_vacancy._is_valid_employer("HR СНАЙПЕР") == "HR СНАЙПЕР"
    assert data_vacancy._is_valid_employer(None) == "Работодатель не указан"


def test_is_valid_town(data_vacancy):
    assert data_vacancy._is_valid_town("Москва") == "Москва"
    assert data_vacancy._is_valid_town(None) == "Город не указан"


def test_is_valid_url(data_vacancy):
    assert data_vacancy._is_valid_url("https://hh.ru/vacancy/78157311") == "https://hh.ru/vacancy/78157311"
    assert data_vacancy._is_valid_url(None) == "Ссылка на объявление не указана"


def test_is_valid_responsibilities(data_vacancy):
    assert (data_vacancy._is_valid_responsibilities("Руководство подразделением (100 чел). Организация процессов.") ==
            "Руководство подразделением (100 чел). Организация процессов.")
    assert data_vacancy._is_valid_responsibilities(None) == "Обязанности и требования к кандидату не  указаны"


def test_compare_salary(data_vacancy):
    assert data_vacancy.compare_salary() == 1200000
    data_vacancy.salary_to = 0
    assert data_vacancy.compare_salary() == 800000


def test__ge__(data_vacancy):
    test_2_vacancy = src.vacancies.Vacancies("Technology Officer",
                                             900000, None,
                                             "Москва", "HR THO",
                                             "https://hh.ru/vacancy/78157000",
                                             "Контроль сроков и качества выполненных работ.")

    assert (sorted([test_2_vacancy, data_vacancy], key=lambda z: z.salary, reverse=True) ==
            [data_vacancy, test_2_vacancy])
    assert (sorted([test_2_vacancy, data_vacancy], key=lambda z: z.salary_from, reverse=True) ==
            [test_2_vacancy, data_vacancy])


def test__le__(data_vacancy):
    test_2_vacancy = src.vacancies.Vacancies("Technology Officer",
                                             900000, None,
                                             "Москва", "HR THO",
                                             "https://hh.ru/vacancy/78157000",
                                             "Контроль сроков и качества выполненных работ.")
    assert (sorted([test_2_vacancy, data_vacancy], key=lambda z: z.salary_to, reverse=True) ==
            [data_vacancy, test_2_vacancy])


def test__str__(data_vacancy):
    assert data_vacancy.__str__() == ("Chief Technology Officer/CTO "
                                      "800000-1200000, Москва, HR СНАЙПЕР, "
                                      "https://hh.ru/vacancy/78157311, "
                                      "Руководство подразделением (100 чел). Организация процессов."
                                      "Контроль сроков и качества выполненных работ. Образование – высшее."
                                      "Опыт работы в крупнейших мировых IT компаниях"
                                      "(Google, Facebook, Microsoft, Amazon, Авито, Озон)."
                                      "Опыт работы в должности – более 7 лет\n")


def test__repr__(data_vacancy):
    assert data_vacancy.__repr__() == ("Chief Technology Officer/CTO "
                                       "800000-1200000 (1200000), Москва, HR СНАЙПЕР, "
                                       "https://hh.ru/vacancy/78157311, "
                                       "Руководство подразделением (100 чел). Организация процессов."
                                       "Контроль сроков и качества выполненных работ. Образование – высшее."
                                       "Опыт работы в крупнейших мировых IT компаниях"
                                       "(Google, Facebook, Microsoft, Amazon, Авито, Озон)."
                                       "Опыт работы в должности – более 7 лет\n")
