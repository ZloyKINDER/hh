from http.client import responses
from symtable import Class
from typing import Dict, List

import requests

from .abstract_api import AbstractAPI


class HeadHunter(AbstractAPI):
    base_url = "https://api.hh.ru"

    def __init__(self):
        self.headers = {"User-Agent": "HH-Vacancies-DB/1.0"}

    def get_employer(self, employer_id: str) -> Dict:
        url = f"{self.base_url}/employers/{employer_id}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_vacancies(self, employer_id: str) -> List[Dict]:
        url = f"{self.base_url}/vacancies"
        parameters = {"employer_id": employer_id, "per_page": 100, "area": 113, "only_with_salary": False}
        response = requests.get(url, headers=self.headers, params=parameters)
        response.raise_for_status()
        return response.json().get("items", [])
