import os
import sys

import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from main import PerformanceReport


class TestSimple:
    def test_process_data_with_real_files(self, temp_csv_file):
        """Тест обработки данных напрямую без файлов"""

        report = PerformanceReport()

        # Задаем тестовые данные
        report.load_data(temp_csv_file)

        result = report.process_data()

        # Проверяем расчеты
        assert len(result) == 8

        dev_data = next(
            item for item in result if item["position"] == "Backend Developer"
        )
        assert dev_data["avg_performance"] == float(4.83)
        assert dev_data["count"] == 3


class TestErrorCases:
    """Тесты обработки ошибок"""

    def test_file_not_found_error(self):
        """Тест ошибки когда файл не найден"""
        report = PerformanceReport()

        with pytest.raises(SystemExit):
            report.load_data(["nonexistent_file.csv"])

    def test_empty_data_error(self, temp_empty_csv_file):
        """Тест ошибки при пустых данных"""
        report = PerformanceReport()

        with pytest.raises(ValueError, match="Нет данных для анализа!"):
            report.load_data([temp_empty_csv_file])

    def test_invalid_performance_values_skipped(self):
        """Тест, что некорректные значения performance пропускаются"""
        report = PerformanceReport()

        # Данные с некорректными значениями
        report.data = [
            {"position": "Developer", "performance": "4.5"},  # валидный
            {"position": "Developer", "performance": "invalid"},  # невалидный
            {"position": "Developer", "performance": "4.8"},  # валидный
            {"position": "Developer", "performance": ""},  # пустой
        ]

        result = report.process_data()
        dev_data = next(item for item in result if item["position"] == "Developer")

        # Должны быть учтены только валидные значения
        assert dev_data["count"] == 2  # Только 4.5 и 4.8
        assert dev_data["avg_performance"] == pytest.approx(4.65)

    def test_missing_performance_field(self):
        """Тест когда у сотрудника нет поля performance"""
        report = PerformanceReport()

        report.data = [
            {"position": "Developer", "performance": "4.5"},
            {"position": "Developer"},  # нет поля performance
            {"position": "Developer", "performance": "4.8"},
        ]

        result = report.process_data()
        dev_data = next(item for item in result if item["position"] == "Developer")

        # Должны быть учтены только сотрудники с performance
        assert dev_data["count"] == 2
        assert dev_data["avg_performance"] == pytest.approx(4.65)


class TestParametrized:
    """Тесты с parametrize"""

    @pytest.mark.parametrize(
        "performances,expected_avg,expected_count",
        [
            # (входные_данные, ожидаемое_среднее, ожидаемое_количество)
            ([4.5, 4.8], 4.65, 2),  # Два нормальных значения
            ([5.0], 5.0, 1),  # Одно значение
            ([3.0, 4.0, 5.0], 4.0, 3),  # Три значения
            ([1.0, 1.0, 1.0, 1.0], 1.0, 4),  # Все одинаковые
        ],
    )
    def test_different_performance_scenarios(
        self, performances, expected_avg, expected_count
    ):
        """Тест расчета среднего для разных сценариев performance"""
        report = PerformanceReport()

        # Создаем тестовые данные на основе параметров
        report.data = [
            {"position": "Tester", "performance": str(perf)} for perf in performances
        ]

        result = report.process_data()
        test_data = next(item for item in result if item["position"] == "Tester")

        assert test_data["avg_performance"] == expected_avg
        assert test_data["count"] == expected_count


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_single_employee(self):
        """Тест когда только один сотрудник"""
        report = PerformanceReport()

        report.data = [{"position": "Developer", "performance": "4.5"}]

        result = report.process_data()

        assert len(result) == 1
        assert result[0]["position"] == "Developer"
        assert result[0]["avg_performance"] == 4.5
        assert result[0]["count"] == 1

    def test_multiple_positions_same_performance(self):
        """Тест когда разные позиции имеют одинаковую эффективность"""
        report = PerformanceReport()

        report.data = [
            {"position": "Backend", "performance": "4.5"},
            {"position": "Frontend", "performance": "4.5"},
            {"position": "Mobile", "performance": "4.5"},
        ]

        result = report.process_data()

        assert len(result) == 3
        for item in result:
            assert item["avg_performance"] == 4.5
            assert item["count"] == 1


def test_output_contains_required_data(temp_csv_file):
    """Тест, что вывод содержит все необходимые данные"""
    report = PerformanceReport()
    report.load_data(temp_csv_file)
    output = report.generate_output(report.process_data())

    # Проверяем что основные элементы присутствуют в выводе
    assert "ОТЧЕТ ПО ЭФФЕКТИВНОСТИ" in output
    assert "Позиция" in output
    assert "Ср. эффективность" in output
    assert "Кол-во сотрудников" in output
    assert "Backend Developer" in output
