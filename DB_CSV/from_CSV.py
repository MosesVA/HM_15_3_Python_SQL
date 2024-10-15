import csv


class FromCSV:
    """Класс для извлечения данных из файла .csv"""

    @staticmethod
    def get_data(filepath):
        """Метод принимает в качестве аргумента путь к файлу и возвращает список словарей"""
        all_data = []
        with open(filepath, encoding='utf-8') as file:
            data_full = csv.DictReader(file)
            for data in data_full:
                all_data.append(data)
        return all_data
