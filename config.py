# Configuration for Online Schools Parser
import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Output directory
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

# Excel output file
EXCEL_OUTPUT = OUTPUT_DIR / "schools_database.xlsx"

# URLs to parse
SCHOOLS_URLS = [
    "https://lyceum.yandex.ru/",
    "https://skillbox.ru/",
    "https://foxford.ru/",
    "https://netology.ru/",
    "https://www.udemy.com/",
]

# Parser settings
TIMEOUT = 10  # seconds
MAX_RETRIES = 3
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# HH.ru API settings
HH_API_BASE = "https://api.hh.ru"
HH_VACANCIES_ENDPOINT = "/vacancies"

# Logging
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
