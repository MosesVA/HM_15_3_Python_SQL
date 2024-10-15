import os
import pyodbc
from dotenv import load_dotenv
import SQL_Queries


class ConnectDB:
    """Класс для подключения к базе данных"""
    @staticmethod
    def connect_to_db(server, database, user, password):
        """Метод принимает в качестве аргументов
        Сервер(server), Базу Данных(database), Имя Пользователя(user), Пароль(password).
        Возвращает Ошибку, если что-то пошло не так, либо сам коннектор"""
        ConnectionString = f'''DRIVER={{ODBC Driver 17 for SQL Server}};
                               SERVER={server};
                               DATABASE={database};
                               UID={user};
                               PWD={password}'''
        try:
            conn = pyodbc.connect(ConnectionString)
            conn.autocommit = True
        except pyodbc.ProgrammingError as ex:
            return ex
        else:
            return conn


class MSSQLOperator:
    """Класс для создания/удаления базы данных и таблиц"""

    def __init__(self, connector_obj):
        self.conn = connector_obj

    def create_database(self, database_name, size=None, maxsize=None, filegrowth=None):
        """Метод для создания базы данных с параметрами
        Имя(name), Нач.Размер(size), Макс.Размер(maxsize) и Шаг Увеличения(filegrowth).
        Возвращает Ошибку, если что-то пошло не так, либо сообщает о том, что база данных успешно создана"""
        SQL_COMMAND = SQL_Queries.create_database(database_name, size, maxsize, filegrowth)
        try:
            self.conn.execute(SQL_COMMAND)
        except pyodbc.ProgrammingError as ex:
            print(ex)
        else:
            return f"База данных {database_name} успешно создана"

    def create_table(self, database_name, table_name, sql_query):
        """Метод для создания таблицы.
        Принимает название базы данных, название таблицы и SQL запрос.
        Возвращает Ошибку, если что-то пошло не так, либо сообщает о том, что таблица успешно создана"""
        cursor = self.conn.cursor()
        cursor.execute(f'USE {database_name}')
        SQL_Query = sql_query(table_name)
        try:
            cursor.execute(SQL_Query)
        except pyodbc.ProgrammingError as ex:
            return ex
        else:
            return f"Таблица: {table_name} успешно создана"

    def drop_table(self, database_name, table_name, sql_query):
        """Метод для удаления таблицы.
        Принимает имя базы данных, имя таблицы и SQL запрос.
        Возвращает Ошибку, если что-то пошло не так, либо сообщает о том, что таблица успешно удалена"""
        cursor = self.conn.cursor()
        cursor.execute(f'USE {database_name}')
        SQL_Query = sql_query(table_name)
        try:
            cursor.execute(SQL_Query)
        except pyodbc.Error as ex:
            return ex
        else:
            return f"Таблица: {table_name} успешно удалена!"


if __name__ == "__main__":
    load_dotenv()
    SERVER = os.getenv('MS_SQL_SERVER')
    DATABASE = os.getenv('MS_SQL_DATABASE')
    USER = os.getenv('MS_SQL_USER')
    PASSWORD = os.getenv('MS_SQL_KEY')
    new_db = "EmployersVacancies"

    my_conn = ConnectDB.connect_to_db(SERVER, DATABASE, USER, PASSWORD)
    my_db_operator = MSSQLOperator(my_conn)
    print(my_db_operator.create_database(new_db, "10", "20", "5%"))
    print(my_db_operator.drop_table(new_db, "Vacancies", SQL_Queries.drop_table))
    print(my_db_operator.drop_table(new_db, "Employers", SQL_Queries.drop_table))
    print(my_db_operator.create_table(new_db, "Employers", SQL_Queries.create_employers))
    print(my_db_operator.create_table(new_db, "Vacancies", SQL_Queries.create_vacancies))
