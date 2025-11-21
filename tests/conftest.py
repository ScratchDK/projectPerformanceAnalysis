import os
import tempfile

import pytest


@pytest.fixture
def employees1_test_csv():
    """Фикстура с содержимым CSV файла"""
    return """name,position,completed_tasks,performance,skills,team,experience_years
David Chen,Mobile Developer,36,4.6,"Swift, Kotlin, React Native, iOS",Mobile Team,3
Elena Popova,Backend Developer,43,4.8,"Java, Spring Boot, MySQL, Redis",API Team,4
Chris Wilson,DevOps Engineer,39,4.7,"Docker, Jenkins, GitLab CI, AWS",Infrastructure Team,5
Olga Kuznetsova,Frontend Developer,42,4.6,"Vue.js, JavaScript, Webpack, Sass",Web Team,3
Robert Kim,Data Engineer,34,4.7,"Python, Apache Spark, Airflow, Kafka",Data Team,4
Julia Martin,QA Engineer,38,4.5,"Playwright, Jest, API Testing",Testing Team,3
Tom Anderson,Backend Developer,49,4.9,"Go, Microservices, gRPC, PostgreSQL",API Team,7
Lisa Wang,Mobile Developer,33,4.6,"Flutter, Dart, Android, Firebase",Mobile Team,2
Mark Thompson,Data Scientist,31,4.7,"R, Python, TensorFlow, SQL",AI Team,4"""


@pytest.fixture
def employees2_test_csv():
    """Фикстура с содержимым CSV файла"""
    return """name,position,completed_tasks,performance,skills,team,experience_years
Alex Ivanov,Backend Developer,45,4.8,"Python, Django, PostgreSQL, Docker",API Team,5
Maria Petrova,Frontend Developer,38,4.7,"React, TypeScript, Redux, CSS",Web Team,4
John Smith,Data Scientist,29,4.6,"Python, ML, SQL, Pandas",AI Team,3
Anna Lee,DevOps Engineer,52,4.9,"AWS, Kubernetes, Terraform, Ansible",Infrastructure Team,6
Mike Brown,QA Engineer,41,4.5,"Selenium, Jest, Cypress, Postman",Testing Team,4
Sarah Johnson,Fullstack Developer,47,4.7,"JavaScript, Node.js, React, MongoDB",Web Team,5"""


@pytest.fixture
def temp_csv_file(employees1_test_csv, employees2_test_csv):
    """Фикстура создающая временный CSV файл с тестовыми данными"""

    list_csv_files = []

    # Создаем временный файл
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".csv", delete=False
    ) as f:  # Создаем временный файл с уникальным именем
        f.write(employees1_test_csv)
        list_csv_files.append(f.name)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write(employees2_test_csv)
        list_csv_files.append(f.name)

    # Возвращаем путь к файлу тесту
    yield list_csv_files

    # Удаляем файлы после завершения теста
    for file in list_csv_files:
        try:
            os.unlink(file)
        except OSError:
            pass


@pytest.fixture
def temp_empty_csv_file():
    """Фикстура с пустым CSV файлом (только заголовки)"""
    csv_content = "name,position,performance\n"  # Только заголовки

    with tempfile.NamedTemporaryFile(mode="w", suffix="_empty.csv", delete=False) as f:
        f.write(csv_content)
        temp_path = f.name

    yield temp_path
    os.unlink(temp_path)
