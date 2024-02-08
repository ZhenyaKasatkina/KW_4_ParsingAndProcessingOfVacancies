from src.job_site_api import HeadHunterAPI
from src.job_site_api import SuperJobAPI
from src.working_with_file_of_vacancies import JSONFileVacancy, CSVFileVacancy


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

    print("\nШаг №2: выбираем вакансию (должность), какую ищешь")
    name_vacancy = str((input())).lower()

    all_vacancies = choose_job_site(number_site, name_vacancy)
    if not all_vacancies:
        print("Нет вакансий, соответствующих заданным критериям.\n"
              "Программа завершена")
    else:
        json_file_vacancy = JSONFileVacancy(all_vacancies)
        csv_file_vacancy = CSVFileVacancy(all_vacancies)
        json_file_vacancy.save_to_file()
        csv_file_vacancy.save_to_file()

        while True:
            print("\nПредлагаю несколько вариантов фильтра:\n"
                  "1. ТОП вакансий по заработной плате\n"
                  "2. выбрать все объявления с установленной тобой диапазоном заработной платы\n"
                  "3. найти все вакансии с ключевым словом в описании\n"
                  "4. выбрать все объявления в определенном городе\n"
                  "Либо просто выйти из программы нажав цифру 5.")
            salary_choice = ["1. ТОП вакансий по заработной плате",
                             "2. выбрать все объявления с установленной минимальной заработной платой",
                             "3. вакансии с ключевым словом в описании",
                             "4. выбрать все объявления в определенном городе",
                             "5. выйти из программы"]
            number_choice = int(check_range_and_num(name_user, 1, 5))
            print(f"\nОтлично! {name_user}, твой выбор {salary_choice[int(number_choice) - 1]}")
            if number_choice == 1:
                try:
                    quantity_top_vacancies = int(input("Введите количество(число) вакансий для вывода в топ: "))
                    json_file_vacancy.data = json_file_vacancy.get_top_by_salary(quantity_top_vacancies)
                    csv_file_vacancy.data = csv_file_vacancy.get_top_by_salary(quantity_top_vacancies)
                except ValueError:
                    print("При указании количества ТОП вакансий, количество должно быть целым числом")
                else:
                    # print(json_file_vacancy)
                    print(csv_file_vacancy)

            elif number_choice == 2:
                try:
                    user_salary_size_from = int(input("Введите размер желаемой заработной платы: от "))
                    user_salary_size_to = int(input("до "))
                    json_file_vacancy.data = json_file_vacancy.get_user_salary_ad(user_salary_size_from,
                                                                                  user_salary_size_to)
                    csv_file_vacancy.data = csv_file_vacancy.get_user_salary_ad(user_salary_size_from,
                                                                                user_salary_size_to)
                    if not json_file_vacancy.data:
                        print("Нет вакансий, соответствующих заданным критериям")
                    else:
                        # print(json_file_vacancy)
                        print(csv_file_vacancy)
                except ValueError:
                    print("При указании диапазона заработной платы необходимо ввести целое число")

            elif number_choice == 3:
                word_user = str(input("Введите ключевое слово для фильтрации: "))
                json_file_vacancy.data = json_file_vacancy.get_ad_by_keyword(word_user)
                csv_file_vacancy.data = csv_file_vacancy.get_ad_by_keyword(word_user)
                if not json_file_vacancy.data:
                    print("Нет вакансий, соответствующих заданным критериям")
                else:
                    # print(json_file_vacancy)
                    print(csv_file_vacancy)

            elif number_choice == 4:
                town_user = str(input("Введите название города для фильтрации: ").capitalize())
                json_file_vacancy.data = json_file_vacancy.get_ad_by_name_town(town_user)
                csv_file_vacancy.data = csv_file_vacancy.get_ad_by_name_town(town_user)
                if not json_file_vacancy.data:
                    print("Нет вакансий, соответствующих заданным критериям")
                else:
                    # print(json_file_vacancy)
                    print(csv_file_vacancy)

            else:
                print("Завершить программу и удалить все данные - нажми 0.\n"
                      "Завершить программу и записать данные фильтрации в файл 'vacancies.json(.csv)' - нажми 1")
                completion_choice = ["Программа завершена, данные удалены",
                                     "Программа завершена, данные записаны"]
                number_choice = int(check_range_and_num(name_user, 0, 1))
                print(f"\n{name_user}, {completion_choice[int(number_choice)]}")
                if number_choice == 0:
                    json_file_vacancy.del_data_in_file()
                    csv_file_vacancy.del_data_in_file()
                    break
                else:
                    json_file_vacancy.save_to_file()
                    csv_file_vacancy.save_to_file()
                    break
