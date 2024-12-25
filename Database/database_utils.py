import psycopg2
from dotenv import load_dotenv
import os

# Database connection parameters
load_dotenv('.env')
db_params = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

def is_user_in_database(user_id: int) -> bool:
    """Check if a user exists in the database by their ID."""
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        query = "SELECT EXISTS(SELECT 1 FROM users WHERE user_id = %s);"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()[0]

        return result  # Returns True if user exists, False otherwise

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def is_user_admin(user_id: int) -> bool:
    """Check if a user has admin privileges."""
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        query = "SELECT user_is_admin FROM users WHERE user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        return result[0] if result else False  # Returns True if user_is_admin is True, False otherwise

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
