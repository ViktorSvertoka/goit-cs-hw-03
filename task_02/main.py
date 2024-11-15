from dotenv import load_dotenv
import os
from pymongo import MongoClient
from colorama import init, Fore
from bson import ObjectId
from data import cats

# Ініціалізація colorama для кольорового виводу
init(autoreset=True)

# Завантажуємо змінні середовища з .env файлу
load_dotenv()

# Отримуємо пароль з змінної середовища
mongo_password = os.getenv("MONGO_PASSWORD")

# Підключення до MongoDB
client = MongoClient(
    f"mongodb+srv://data_md:{mongo_password}@cluster777.ax8qp.mongodb.net/?retryWrites=true&w=majority&appName=Cluster777"
)

db = client["cats_db"]
cats_collection = db["cats"]


# Функція для додавання котів до бази даних
def add_sample_cats():
    """Функція для додавання згенерованих котів до бази даних"""
    try:
        cats_collection.insert_many(cats)
        print(Fore.GREEN + "Коти успішно додані.")
    except Exception as e:
        print(Fore.RED + f"Помилка при додаванні котів: {e}")


# Операції CRUD
def get_all_cats():
    """Функція для виведення всіх котів з колекції."""
    try:
        cats = cats_collection.find()
        if cats_collection.count_documents({}) == 0:
            print(Fore.YELLOW + "Колекція пуста.")
        else:
            for cat in cats:
                print(Fore.CYAN + str(cat))
    except Exception as e:
        print(Fore.RED + f"Помилка при отриманні котів: {e}")


def get_cat_by_name(name):
    """Функція для виведення кота за ім'ям."""
    try:
        cat = cats_collection.find_one({"name": name})
        if cat:
            print(Fore.GREEN + str(cat))
        else:
            print(Fore.YELLOW + f"Кота з ім'ям {name} не знайдено.")
    except Exception as e:
        print(Fore.RED + f"Помилка при отриманні кота: {e}")


def update_cat_age(name, new_age):
    """Функція для оновлення віку кота."""
    try:
        result = cats_collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(Fore.GREEN + f"Вік кота {name} оновлено на {new_age}.")
        else:
            print(Fore.YELLOW + f"Не знайдено кота з ім'ям {name}.")
    except Exception as e:
        print(Fore.RED + f"Помилка при оновленні віку кота: {e}")


def add_feature_to_cat(name, new_feature):
    """Функція для додавання нової характеристики до кота."""
    try:
        result = cats_collection.update_one(
            {"name": name},
            {"$addToSet": {"features": new_feature}},  # Додає елемент, якщо його немає
        )
        if result.modified_count > 0:
            print(Fore.GREEN + f"Характеристика '{new_feature}' додана до кота {name}.")
        else:
            print(Fore.YELLOW + f"Не знайдено кота з ім'ям {name}.")
    except Exception as e:
        print(Fore.RED + f"Помилка при додаванні характеристики: {e}")


def delete_cat_by_name(name):
    """Функція для видалення кота за ім'ям."""
    try:
        result = cats_collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(Fore.GREEN + f"Кота з ім'ям {name} видалено.")
        else:
            print(Fore.YELLOW + f"Не знайдено кота з ім'ям {name}.")
    except Exception as e:
        print(Fore.RED + f"Помилка при видаленні кота: {e}")


def delete_all_cats():
    """Функція для видалення всіх котів з колекції."""
    try:
        result = cats_collection.delete_many({})
        print(Fore.GREEN + f"{result.deleted_count} котів було видалено.")
    except Exception as e:
        print(Fore.RED + f"Помилка при видаленні котів: {e}")


if __name__ == "__main__":
    # Додати котів до бази даних перед тестуванням інших операцій
    add_sample_cats()

    # Тестування операцій
    print(Fore.MAGENTA + "Отримання всіх котів:")
    get_all_cats()

    print(Fore.BLUE + "\nОтримання кота за ім'ям 'Barsik':")
    get_cat_by_name("Barsik")

    print(Fore.BLUE + "\nОновлення віку кота 'Barsik' на 4 роки:")
    update_cat_age("Barsik", 4)

    print(Fore.BLUE + "\nДодавання характеристики до кота 'Barsik':")
    add_feature_to_cat("Barsik", "любить лазити по деревах")

    print(Fore.BLUE + "\nОтримання оновлених даних кота 'Barsik':")
    get_cat_by_name("Barsik")

    print(Fore.BLUE + "\nВидалення кота 'Barsik':")
    delete_cat_by_name("Barsik")

    print(Fore.BLUE + "\nВидалення всіх котів:")
    delete_all_cats()
