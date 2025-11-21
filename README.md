# Анализ эффективности разработчиков

Скрипт для генерации отчетов по эффективности сотрудников на основе CSV файлов.

## Как добавить новый отчет:

1. Создать класс унаследованный от `ReportTemplate`
2. Реализовать `process_data()` - логика обработки
3. Реализовать `generate_output()` - формат вывода
4. Добавить в `report_classes` в `main()`

Пример:
```python
class TechnologyReport(ReportTemplate):
    def process_data(self):
        # логика анализа технологий
        pass
    def generate_output(self, processed_data):
        # форматирование вывода
        pass
```

## Запуск тестов
```bash
pytest tests/ -v
```

## Примеры использования:
```bash
python main.py --files employees1.csv --report performance
python main.py --files employees1.csv employees2.csv --report performance
```