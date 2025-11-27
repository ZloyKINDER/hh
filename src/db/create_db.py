import psycopg2
from psycopg2 import sql
from .config import get_db_params


class DatabaseManager:
    """Создание таблиц"""

    @staticmethod
    def create_database():
        """Создаёт базу данных, если не существует."""
        conn = psycopg2.connect(
            dbname="postgres",
            user=get_db_params()["user"],
            password=get_db_params()["password"],
            host=get_db_params()["host"]
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(get_db_params()["dbname"])
        ))
        cur.close()
        conn.close()
        print(f"База данных {get_db_params()['dbname']} создана.")

    @staticmethod
    def create_tables():
        """Создаёт таблицы employers и vacancies."""
        conn = psycopg2.connect(**get_db_params())
        cur = conn.cursor()

        # Таблица работодателей
        cur.execute("""
            CREATE TABLE IF NOT EXISTS employers (
                employer_id SERIAL PRIMARY KEY,
                hh_id VARCHAR(50) UNIQUE NOT NULL,
                name VARCHAR(255) NOT NULL,
                url TEXT,
                open_vacancies INTEGER DEFAULT 0
            );
        """)

        # Таблица вакансий
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                vacancy_id SERIAL PRIMARY KEY,
                hh_id VARCHAR(50) UNIQUE NOT NULL,
                title VARCHAR(255) NOT NULL,
                url TEXT NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                employer_id INTEGER REFERENCES employers(employer_id) ON DELETE CASCADE,
                description TEXT
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Таблицы созданы.")
