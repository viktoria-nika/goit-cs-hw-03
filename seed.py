import psycopg2
from psycopg2 import Error
from faker import Faker

# Підключення до бази даних
def create_db():
    """Create a database connection"""
    try:
        conn = psycopg2.connect(
            dbname="your_db", 
            user="your_user", 
            password="your_password", 
            host="localhost"
        )
        return conn
    except Error as e:
        print(f"Error: {e}")
        return None

# Створення користувача
def create_user(conn, user):
    """
    Create a new user in the users table
    :param conn: Database connection
    :param user: Tuple containing (fullname, email)
    :return: user id
    """
    sql = '''
    INSERT INTO users(fullname, email) VALUES(%s, %s) RETURNING id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, user)
        conn.commit()
        user_id = cur.fetchone()[0]
        return user_id
    except Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()

# Створення статусу
def create_status(conn, status):
    """
    Create a new status in the status table
    :param conn: Database connection
    :param status: status name
    :return: status id
    """
    sql = '''
    INSERT INTO status(name) VALUES(%s) RETURNING id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, (status,))
        conn.commit()
        status_id = cur.fetchone()[0]
        return status_id
    except Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()

# Створення завдання
def create_task(conn, task):
    """
    Create a new task in the tasks table
    :param conn: Database connection
    :param task: Tuple containing (title, description, status_id, user_id)
    :return: task id
    """
    sql = '''
    INSERT INTO tasks(title, description, status_id, user_id) VALUES(%s, %s, %s, %s) RETURNING id;
    '''
    cur = conn.cursor()
    try:
        cur.execute(sql, task)
        conn.commit()
        task_id = cur.fetchone()[0]
        return task_id
    except Error as e:
        print(f"Error: {e}")
    finally:
        cur.close()

# Основний блок для заповнення таблиць
if __name__ == '__main__':
    fake = Faker()

    # Підключення до бази даних
    conn = create_db()
    if conn is not None:
        with conn:
            # Створення статусів
            status_new = create_status(conn, 'new')
            status_in_progress = create_status(conn, 'in progress')
            status_completed = create_status(conn, 'completed')

            # Створення користувачів
            user_1 = (fake.name(), fake.email())
            user_2 = (fake.name(), fake.email())
            user_3 = (fake.name(), fake.email())
            
            user_id_1 = create_user(conn, user_1)
            user_id_2 = create_user(conn, user_2)
            user_id_3 = create_user(conn, user_3)

            # Створення завдань для кожного користувача
            task_1 = ('Task 1: Analyze requirements', fake.text(), status_new, user_id_1)
            task_2 = ('Task 2: Design the app', fake.text(), status_in_progress, user_id_2)
            task_3 = ('Task 3: Implement features', fake.text(), status_in_progress, user_id_1)
            task_4 = ('Task 4: Test the app', fake.text(), status_completed, user_id_3)

            task_id_1 = create_task(conn, task_1)
            task_id_2 = create_task(conn, task_2)
            task_id_3 = create_task(conn, task_3)
            task_id_4 = create_task(conn, task_4)

            # Виведення результатів
            print(f"Created user with ID {user_id_1} and task with ID {task_id_1}")
            print(f"Created user with ID {user_id_2} and task with ID {task_id_2}")
            print(f"Created user with ID {user_id_3} and task with ID {task_id_4}")
    else:
        print("Failed to connect to the database")