from DB_manager import *

if __name__ == "__main__":
    load_dotenv()
    SERVER = os.getenv('MS_SQL_SERVER')
    DATABASE = os.getenv('MS_SQL_DATABASE')
    USER = os.getenv('MS_SQL_USER')
    PASSWORD = os.getenv('MS_SQL_KEY')
    active_db = "NorthWind"
    customers_data_path = r'..\DB_CSV\north_data\customers_data.csv'
    employees_data_path = r'..\DB_CSV\north_data\employees_data.csv'
    orders_data_path = r'..\DB_CSV\north_data\orders_data.csv'

    my_conn = ConnectDB.connect_to_db(SERVER, DATABASE, USER, PASSWORD)
    my_manager = DBManager(my_conn)

    print(my_manager.fill_table_from_csv(active_db, 'customers_data', customers_data_path,
                                         SQL_Queries.fill_customers_data))
    print(my_manager.fill_table_from_csv(active_db, 'employees_data', employees_data_path,
                                         SQL_Queries.fill_employees_data))
    print(my_manager.fill_table_from_csv(active_db, 'orders_data', orders_data_path, SQL_Queries.fill_orders_data))
