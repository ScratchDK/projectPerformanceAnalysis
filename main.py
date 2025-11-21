import argparse
import csv
import sys
from abc import ABC, abstractmethod
from collections import defaultdict


class ReportTemplate(ABC):
    """Абстрактный класс-шаблон для генерации отчетов"""

    def __init__(self):
        self.data = []

    def load_data(self, filenames: list[str]):
        """Загрузка данных из CSV файлов (общая для всех отчетов)"""
        all_data = []

        for filename in filenames:
            try:
                with open(filename, "r", encoding="utf-8") as file:
                    reader = csv.DictReader(file)
                    all_data.extend(reader)
                    print(f"Загружен файл: {filename}")
            except FileNotFoundError as e:
                sys.exit(f"Файл {e.filename}, не найден!")
            except Exception as e:
                sys.exit(f"Ошибка {e}!")

        if not all_data:
            raise ValueError("Нет данных для анализа!")

        self.data = all_data
        return all_data

    @abstractmethod
    def process_data(self):
        """ОБЯЗАТЕЛЬНО к переопределению: обработка данных для отчета"""
        pass

    @abstractmethod
    def generate_output(self, processed_data):
        """ОБЯЗАТЕЛЬНО к переопределению: генерация вывода"""
        pass

    def generate_report(self, filenames):
        """
        Общий алгоритм генерации отчета (шаблонный метод)

        Шаги:
        1. Загрузка данных из CSV
        2. Обработка данных (реализуется в подклассах)
        3. Генерация вывода (реализуется в подклассах)
        """
        # 1. Загрузка данных
        self.load_data(filenames)

        # 2. Обработка данных (абстрактный метод)
        processed_data = self.process_data()

        # 3. Генерация вывода (абстрактный метод)
        result = self.generate_output(processed_data)

        return result


class PerformanceReport(ReportTemplate):
    """Конкретная реализация отчета по эффективности"""

    def process_data(self):
        """Обработка данных для отчета по эффективности"""
        position_stats = defaultdict(list)

        for employee in self.data:
            position = employee["position"]
            try:
                performance = float(employee["performance"])
                position_stats[position].append(performance)
            except (ValueError, KeyError):
                continue

        report_data = []
        for position, performances in position_stats.items():
            avg_performance = round(
                sum(performances) / len(performances), 2
            )  # Округляем до 2 знаков для читаемости
            report_data.append(
                {
                    "position": position,
                    "avg_performance": avg_performance,
                    "count": len(performances),
                }
            )

        # Сортировка по убыванию эффективности
        report_data.sort(key=lambda x: x["avg_performance"], reverse=True)
        return report_data

    def generate_output(self, processed_data):
        """Генерация красивого вывода для отчета по эффективности"""
        output_lines = [
            "\n" + "=" * 60,
            "ОТЧЕТ ПО ЭФФЕКТИВНОСТИ",
            "=" * 60,
            f"{'Позиция':<25} {'Ср. эффективность':<18} {'Кол-во сотрудников':<15}",
            "-" * 60,
        ]

        for item in processed_data:
            line = f"{item['position']:<25} {item['avg_performance']:<18.2f} {item['count']:<15}"
            output_lines.append(line)

        output_lines.append("=" * 60)
        return "\n".join(output_lines)


def main():
    parser = argparse.ArgumentParser(description="Генерация отчетов по сотрудникам")
    parser.add_argument("--files", nargs="+", required=True, help="Список CSV файлов")
    parser.add_argument(
        "--report", choices=["performance"], default="performance", help="Тип отчета"
    )

    # Читаем пользовательский ввод
    args = parser.parse_args()

    # Выбор реализации в зависимости от типа отчета
    report_classes = {"performance": PerformanceReport}

    report_class = report_classes[args.report]  # Получаем класс PerformanceReport
    report_generator = report_class()  # Создаем объект этого класса

    try:
        result = report_generator.generate_report(args.files)
        print(result)  # Выводим результат пользователю
    except ValueError as e:
        sys.exit(f"Ошибка: {e}")
    except Exception as e:
        sys.exit(f"Неожиданная ошибка: {e}")


if __name__ == "__main__":
    main()
