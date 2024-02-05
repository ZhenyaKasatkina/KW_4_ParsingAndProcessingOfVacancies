from src.job_site_api import HeadHunterAPI
from src.job_site_api import SuperJobAPI


def check_range_and_num(name_user, range_from: int, range_to: int):
    """
    Проверка введенных данных на значение - число и диапазон
    """
    while True:
        number = input("Введи номер(число) своего выбора:  ")
        if not number.isdigit():
            print(f"Должно быть число. {name_user}, попробуй еще раз")

        elif int(number) < range_from or int(number) > range_to:
            print(f"Такого числа в диапазоне нет. {name_user}, попробуй еще раз")
        else:
            break
    return number


def choose_job_site(site, vacancy):
    """Выбираем сайт поиска вакансий"""
    if site == 1:
        sj_api = SuperJobAPI(vacancy)
        return sj_api.get_vacancies()
    elif site == 2:
        hh_api = HeadHunterAPI(vacancy)
        return hh_api.get_vacancies()
    else:

        sj_api = SuperJobAPI(vacancy)
        hh_api = HeadHunterAPI(vacancy)
        return hh_api.get_vacancies() + sj_api.get_vacancies()


def work_with_the_user():
    print("Привет!\nЯ 'Поиск работы'")
    print("Если хочешь чтобы помог тебе найти работу\nнапиши свое имя:")
    name_user = input().capitalize()
    print(f"Теперь, {name_user}, я знаю твое имя и предлагаю тебе начать поиск работы")

    print("\nШаг №1: выбираем сайт на котором будем рассматривать вакансии:\n"
          "1. Super Job\n2. Head Hunter\n3. На всех указанных сайтах по поиску работы\n")
    site_choice = ["1. Super Job", "2. Head Hunter", "3. На всех указанных сайтах по поиску работы"]
    number_site = int(check_range_and_num(name_user, 1, 3))
    print(f"Отлично! {name_user}, твой выбор {site_choice[int(number_site) - 1]}")


if __name__ == "__main__":
    work_with_the_user()


