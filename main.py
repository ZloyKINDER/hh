from src.db.create_db import DatabaseManager
from src.db.data_load_in_db import DataLoader
from src.db.db_manager import DBManager

# Список из 10 компаний (найдите ID на hh.ru → "О компании" → URL)
EMPLOYER_IDS = [
    "3529",  # Сбер
    "15478",  # ВКонтакте
    "39305",  # Тинькофф
    "4181",  # Яндекс
    "87021",  # Ozon
    "2180",  # МТС
    "4219",  # Ростелеком
    "3776",  # Kaspersky
    "78638",  # Т-Банк
    "4934"  # Avito
]


def main():
    print("Создание базы данных и таблиц...")
    try:
        DatabaseManager.create_database()
    except:
        print("БД уже существует или ошибка.")

    DatabaseManager.create_tables()

    print("Загрузка данных...")
    loader = DataLoader()
    loader.load_employers(EMPLOYER_IDS)
    loader.load_vacancies(EMPLOYER_IDS)

    print("\n" + "=" * 60)
    print("РАБОТА С БАЗОЙ ДАННЫХ")
    print("=" * 60)

    db = DBManager()

    print("\n1. Компании и количество вакансий:")
    for item in db.get_companies_and_vacancies_count():
        print(f"   • {item['company']}: {item['vacancies']} вакансий")

    print(f"\n2. Средняя зарплата: {db.get_avg_salary():,.0f} ₽")

    print("\n3. Вакансии с зарплатой выше средней:")
    for v in db.get_vacancies_with_higher_salary()[:5]:
        print(f"   • {v['title']} | {v['company']} | от {v['salary']:,.0f} ₽")

    keyword = input("\nВведите слово для поиска в названии вакансий (например, python): ").strip()
    if keyword:
        print(f"\nВакансии с ключевым словом '{keyword}':")
        results = db.get_vacancies_with_keyword(keyword)
        for v in results[:5]:
            print(f"   • {v['title']} | {v['company']} | {v['url']}")


if __name__ == "__main__":
    main()