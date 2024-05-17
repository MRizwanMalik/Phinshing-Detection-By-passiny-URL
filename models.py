import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password  # Note: Storing the hashed password directly

    @staticmethod
    def get(user_id):
        connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='fyp'
        )

        cursor = connection.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE id = %s"
        values = (user_id,)

        cursor.execute(query, values)

        user_data = cursor.fetchone()

        cursor.close()
        connection.close()

        if user_data:
            user = User(user_data['id'], user_data['email'], user_data['password'])
            return user
        else:
            return None

def create_user(email, password):
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='fyp'
    )

    cursor = connection.cursor()

    hashed_password = generate_password_hash(password)
    
    query = "INSERT INTO users (email, password) VALUES (%s, %s)"
    values = (email, hashed_password)

    cursor.execute(query, values)

    connection.commit()

    cursor.close()
    connection.close()

def get_user_by_email(email):
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='fyp'
    )

    cursor = connection.cursor(dictionary=True)

    query = "SELECT * FROM users WHERE email = %s"
    values = (email,)

    cursor.execute(query, values)

    user_data = cursor.fetchone()

    cursor.close()
    connection.close()

    if user_data:
        user = User(user_data['id'], user_data['email'], user_data['password'])
        return user
    else:
        return None


