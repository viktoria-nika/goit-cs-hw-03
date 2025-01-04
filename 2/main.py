from pymongo import MongoClient
from pymongo.errors import PyMongoError
from bson import ObjectId

# Підключення до MongoDB
client = mongodb+srv://viktoriamoroz468:<db_password>@cluster0.z7qlg.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0 
db = client['cats_database']  # база даних
collection = db['cats']  # колекція

# Функція для створення нового кота
def create_cat(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    try:
        collection.insert_one(cat)
        print(f"Кіт {name} доданий до бази даних.")
    except PyMongoError as e:
        print(f"Помилка при додаванні кота: {e}")

# Функція для виведення всіх котів
def read_all_cats():
    try:
        cats = collection.find()
        for cat in cats:
            print(f"Ім'я: {cat['name']}, Вік: {cat['age']}, Характеристики: {', '.join(cat['features'])}")
    except PyMongoError as e:
        print(f"Помилка при отриманні даних: {e}")

# Функція для пошуку кота за ім'ям
def read_cat_by_name(name):
    try:
        cat = collection.find_one({"name": name})
        if cat:
            print(f"Ім'я: {cat['name']}, Вік: {cat['age']}, Характеристики: {', '.join(cat['features'])}")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except PyMongoError as e:
        print(f"Помилка при отриманні даних: {e}")

# Функція для оновлення віку кота
def update_cat_age(name, new_age):
    try:
        result = collection.update_one({"name": name}, {"$set": {"age": new_age}})
        if result.modified_count > 0:
            print(f"Вік кота {name} оновлено на {new_age}.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений або вік вже встановлений на {new_age}.")
    except PyMongoError as e:
        print(f"Помилка при оновленні віку кота: {e}")

# Функція для додавання нової характеристики коту
def add_feature_to_cat(name, new_feature):
    try:
        result = collection.update_one(
            {"name": name},
            {"$push": {"features": new_feature}}
        )
        if result.modified_count > 0:
            print(f"Характеристика '{new_feature}' додана коту {name}.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except PyMongoError as e:
        print(f"Помилка при додаванні характеристики коту: {e}")

# Функція для видалення кота за ім'ям
def delete_cat_by_name(name):
    try:
        result = collection.delete_one({"name": name})
        if result.deleted_count > 0:
            print(f"Кіт з ім'ям {name} видалений.")
        else:
            print(f"Кіт з ім'ям {name} не знайдений.")
    except PyMongoError as e:
        print(f"Помилка при видаленні кота: {e}")

# Функція для видалення всіх котів
def delete_all_cats():
    try:
        result = collection.delete_many({})
        print(f"Видалено {result.deleted_count} котів.")
    except PyMongoError as e:
        print(f"Помилка при видаленні котів: {e}")

# Тестування CRUD операцій
if __name__ == "__main__":
    # Створення кількох котів
    create_cat("Barsik", 3, ["ходить в капці", "дає себе гладити", "рудий"])
    create_cat("Tom", 5, ["гарно муркоче", "не любить гуляти"])
    
    # Читання всіх котів
    print("\nУсі коти:")
    read_all_cats()
    
    # Читання кота за ім'ям
    print("\nПошук кота за ім'ям 'Barsik':")
    read_cat_by_name("Barsik")
    
    # Оновлення віку кота
    print("\nОновлення віку кота 'Barsik' на 4:")
    update_cat_age("Barsik", 4)
    
    # Додавання нової характеристики коту
    print("\nДодавання характеристики 'любить гратись' до кота 'Barsik':")
    add_feature_to_cat("Barsik", "любить гратись")
    
    # Видалення кота за ім'ям
    print("\nВидалення кота 'Tom':")
    delete_cat_by_name("Tom")
    
    # Видалення всіх котів
    print("\nВидалення всіх котів:")
    delete_all_cats()
