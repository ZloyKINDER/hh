from typing import Optional, Dict, List

class Vacancy:
    def __init__(self, title: str, url: str, salary_from: Optional[int],
                 salary_to: Optional[int], employer: str, description: str = "",):
        self.title = title
        self.url = url
        self.salary_from = salary_from or 0
        self.salary_to = salary_to
        self.employer = employer
        self.description = description or ""

    @staticmethod
    def from_hh_data(data: Dict) -> 'Vacancy':
        salary = data.get("salary") or {}
        return Vacancy(
            title=data.get("name", "Без названия"),
            url=data.get("alternate_url", ""),
            salary_from=salary.get("from"),
            salary_to=salary.get("to"),
            employer=data.get("employer", {}).get("name", "Неизвестно"),
            description=(data.get("snippet") or {}).get("responsibility", "") or ""
        )

    def __str__(self):
        salary = f"от {self.salary_from}" if self.salary_from else ""
        if self.salary_to:
            salary += f" до {self.salary_to}"
        return f"{self.title} ({self.employer})\nЗарплата: {salary or 'Не указана'}\n{self.url}"
