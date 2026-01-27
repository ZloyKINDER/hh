from abc import ABC, abstractmethod
from typing import Dict, List


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API."""

    @abstractmethod
    def get_employer(self, employer_id: str) -> Dict:
        pass

    @abstractmethod
    def get_vacancies(self, employer_id: str) -> List[Dict]:
        pass
