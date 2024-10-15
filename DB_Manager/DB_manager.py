import os
import json
import pyodbc
from dotenv import load_dotenv
from DB_Operator.DB_operator import ConnectDB
from DB_CSV.from_CSV import FromCSV
import SQL_Queries


class DBManager:
    """Класс для внесения изменений в базу данных"""

    def __init__(self, connector_obj):
        """Инициализация класса в виде подключения к базе данных"""
        self.conn = connector_obj
        self.cursor = self.conn.cursor()

    @staticmethod
    def get_data_from_json(filename):
        """Метод принимает имя файла .json и возвращает данные преобразованные в формат для python"""
        with open(filename, 'r', encoding='utf-8') as file:
            python_data = json.load(file)
            return python_data

    def fill_table(self, database_name, table_name, filename, sql_query):
        """Метод для заполнения таблицы.
        Принимает имя базы данных, имя таблицы, имя файла с данными и SQL запрос"""
        self.cursor.execute(f"USE {database_name}")
        data_to_fill_list = self.get_data_from_json(filename)
        try:
            for data_to_fill in data_to_fill_list:
                self.cursor.execute(sql_query(table_name, data_to_fill))
        except pyodbc.Error as ex:
            return ex
        else:
            return "Данные помещены в таблицу"

        # QUERY = fr"""INSERT INTO {table_name} (employer_id, employer_name, employer_url)
        #                         VALUES
        #                         ('{data_to_fill['id']}',
        #                          '{data_to_fill['name']}',
        #                          '{data_to_fill['alternate_url']}');"""

    def fill_table_from_csv(self, database_name, table_name, filepath, sql_query):
        """Метод для заполнения таблицы данными из .csv файла.
        Принимает имя базы данных, имя таблицы, путь к файлу .csv и SQL запрос"""
        self.cursor.execute(f"USE {database_name}")
        data_to_fill_list = FromCSV.get_data(filepath)
        try:
            if table_name == 'employees_data':
                employee_id = 1
                for data_to_fill in data_to_fill_list:
                    self.cursor.execute(sql_query(table_name, data_to_fill, employee_id))
                    employee_id += 1
            else:
                for data_to_fill in data_to_fill_list:
                    self.cursor.execute(sql_query(table_name, data_to_fill))
        except pyodbc.Error as ex:
            return ex
        else:
            return "Данные помещены в таблицу"
