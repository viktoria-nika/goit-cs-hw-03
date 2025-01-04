import psycopg2
from faker import Faker
import random

# Підключення до бази даних PostgreSQL
conn = psycopg2.connect(
    dbname="salary.db", 
    user="your_user", 
    password="your_password", 
    host="localhost", 
    port="5432"
)
cur = conn.cursor()

fake = Faker()

# Створення статусів
statuses = ['new', 'in progress', 'completed']
for status in statuses:
    cur.execute("INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;", (status,))

# Створення користувачів
users = []
for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    cur.execute("INSERT INTO users (fullname, email) VALUES (%s, %s) RETURNING id;", (fullname, email))
    user_id = cur.fetchone()[0]
    users.append(user_id)

# Створення завдань
for _ in range(20):
    title = fake.sentence()
    description = fake.text()
    status_id = random.choice([1, 2, 3])  # Вибір випадкового статусу
    user_id = random.choice(users)
    cur.execute(
        "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s);", 
        (title, description, status_id, user_id)
    )

# Збереження змін і закриття з'єднання
conn.commit()
cur.close()
conn.close()