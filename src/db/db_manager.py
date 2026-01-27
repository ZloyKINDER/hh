from typing import Any, Dict, List

import psycopg2

from .config import get_db_params


class DBManager:
    def __init__(self):
        self.params = get_db_params()

    def get_companies_and_vacancies_count(self) -> List[Dict]:
        """Получает список всех компаний и количество вакансий у каждой компании."""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT e.name, COUNT(v.vacancy_id) as vacancy_count
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
            ORDER BY vacancy_count DESC;
            """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"company": r[0], "vacancies": r[1]} for r in rows]

    def get_all_vacancies(self) -> List[Dict]:
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            ORDER BY v.salary_from DESC NULLS LAST;
            """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [
            {"company": r[0], "title": r[1], "salary": f"{r[2] or 0} - {r[3] or ''}".strip(" -"), "url": r[4]}
            for r in rows
        ]

    def get_avg_salary(self) -> float:
        """получает среднюю зарплату по вакансиям"""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute("SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL;")
        avg = cur.fetchone()[0]
        cur.close()
        conn.close()
        return round(avg or 0, 2)

    def get_vacancies_with_higher_salary(self) -> List[Dict]:
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT e.name, v.title, v.salary_from, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE v.salary_from > (SELECT AVG(salary_from) FROM vacancies WHERE salary_from IS NOT NULL)
            ORDER BY v.salary_from DESC;
            """
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"company": r[0], "title": r[1], "salary": r[2], "url": r[3]} for r in rows]

    def get_vacancies_with_keyword(self, keyword: str) -> List[Dict]:
        """получает список всех вакансий, в названии которых содержатся переданные в метод слова"""
        conn = psycopg2.connect(**self.params)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT e.name, v.title, v.salary_from, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE LOWER(v.title) LIKE LOWER(%s)
            ORDER BY v.salary_from DESC NULLS LAST;
            """,
            (f"%{keyword}%",),
        )
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return [{"company": r[0], "title": r[1], "salary": r[2], "url": r[3]} for r in rows]
