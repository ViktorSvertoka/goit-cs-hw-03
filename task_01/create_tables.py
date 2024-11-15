import psycopg2
from psycopg2 import Error
from contextlib import contextmanager
from colorama import init, Fore, Style
from config import DB_CONFIG

# Ініціалізація colorama
init(autoreset=True)


@contextmanager
def create_connection():
    """Створення з'єднання з PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"{Fore.RED}Помилка підключення: {e}")
    finally:
        if conn:
            conn.close()


def create_table(conn, create_table_sql):
    """Створення таблиці на основі переданого SQL-запиту."""
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_sql)
        print(f"{Fore.GREEN}Таблиця успішно створена.")
    except Error as e:
        print(f"{Fore.RED}Помилка створення таблиці: {e}")


if __name__ == "__main__":
    # SQL-запити для створення таблиць
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE
    );
    """
    sql_create_statuses_table = """
    CREATE TABLE IF NOT EXISTS statuses (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
    """
    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER REFERENCES statuses(id),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
    """

    # Підключення до бази даних і створення таблиць
    with create_connection() as conn:
        if conn:
            print(f"{Fore.BLUE}Підключення до бази даних успішне.")

            print(f"{Fore.YELLOW}Створення таблиці 'users'...")
            create_table(conn, sql_create_users_table)

            print(f"{Fore.YELLOW}Створення таблиці 'statuses'...")
            create_table(conn, sql_create_statuses_table)

            print(f"{Fore.YELLOW}Створення таблиці 'tasks'...")
            create_table(conn, sql_create_tasks_table)

            print(f"{Fore.MAGENTA}Всі таблиці створені успішно!")
        else:
            print(f"{Fore.RED}Не вдалося створити з'єднання з базою даних.")
