#!/usr/bin/env python3
# Main entry point for Online Schools Parser

import logging
import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import (
    SCHOOLS_URLS,
    EXCEL_OUTPUT,
    LOG_LEVEL,
    LOG_FORMAT
)
from src.parser import SchoolParser
from src.exporter import ExcelExporter

# Setup logging
logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)
logger = logging.getLogger(__name__)

def main():
    """Main function to run the parser"""
    
    print("\n" + "="*60)
    print("🚀 Запуск парсера онлайн-школ...")
    print("="*60)
    print(f"⏰ Время начала: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
    print("-" * 60)
    
    try:
        # Initialize parser
        parser = SchoolParser()
        
        # Parse schools
        logger.info(f"📍 Обработано примеров: {len(SCHOOLS_URLS)}")
        schools_data = parser.parse_multiple(SCHOOLS_URLS)
        
        if not schools_data:
            logger.error("❌ Не удалось получить данные о школах")
            return False
        
        print("-" * 60)
        
        # Print statistics
        print("\n📊 Статистика:")
        print(f"   Всего школ: {len(schools_data)}")
        schools_with_url = sum(1 for s in schools_data if s.get('url'))
        print(f"   С сайтом: {schools_with_url}")
        schools_with_contacts = sum(1 for s in schools_data if s.get('contacts', {}).get('email') or s.get('contacts', {}).get('phone'))
        print(f"   С контактами: {schools_with_contacts}")
        schools_with_socials = sum(1 for s in schools_data if any(s.get('social_media', {}).values()))
        print(f"   С соцсетями: {schools_with_socials}")
        schools_with_courses = sum(1 for s in schools_data if s.get('courses'))
        print(f"   С курсами: {schools_with_courses}")
        
        # Export to Excel
        print("\n💾 Экспорт в Excel...")
        exporter = ExcelExporter(str(EXCEL_OUTPUT))
        exporter.export(schools_data)
        
        print("\n" + "="*60)
        print("✨ Парсинг успешно завершён!")
        print("="*60)
        print(f"📁 Файл сохранён: {EXCEL_OUTPUT}")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {str(e)}", exc_info=True)
        print("\n" + "="*60)
        print("❌ Ошибка при запуске парсера!")
        print("="*60 + "\n")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
