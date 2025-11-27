import os
from typing import Dict

def get_db_params() -> Dict[str, str]:
    """Конфиг подключения к бд."""
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "dbname": os.getenv("DB_NAME", "hh_vacancies"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "Stalker9823!"),
    }
