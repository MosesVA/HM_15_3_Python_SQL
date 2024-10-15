from DB_operator import *

if __name__ == '__main__':
    load_dotenv()
    SERVER = os.getenv('MS_SQL_SERVER')
    DATABASE = os.getenv('MS_SQL_DATABASE')
    USER = os.getenv('MS_SQL_USER')
    PASSWORD = os.getenv('MS_SQL_KEY')

    my_conn = ConnectDB.connect_to_db(SERVER, DATABASE, USER, PASSWORD)
    my_db_operator = MSSQLOperator(my_conn)
    my_db = 'NorthWind'

    my_db_operator.create_database(my_db, '10',  '20', '5%')
    print(my_db_operator.create_table(my_db, 'customers_data', SQL_Queries.create_customers_data))
    print(my_db_operator.create_table(my_db, 'employees_data', SQL_Queries.create_employees_data))
    print(my_db_operator.create_table(my_db, 'orders_data', SQL_Queries.create_orders_data))


