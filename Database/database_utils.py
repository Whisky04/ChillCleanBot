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
    """Check if a user exists in the database by their ID and log the result."""
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Check if the user exists and retrieve their name if they do
        query = """
        SELECT user_name 
        FROM users 
        WHERE user_id = %s;
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result is not None:  # Check if fetchone returned a result
            user_name = result[0]  # Assuming user_name is in the first column
            print(f"User with ID {user_id} and name {user_name} has started the bot usage.")
            return True
        else:
            print(f"User with ID {user_id} is not authorized to use the bot.")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def is_user_admin(user_id: int) -> bool:
    """Check if a user has admin privileges and log the result."""
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Check if the user is an admin and retrieve their name if they are
        query = """
        SELECT user_name, user_is_admin 
        FROM users 
        WHERE user_id = %s;
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()

        if result is not None:
            user_name, user_is_admin = result
            if user_is_admin:
                print(f"User with ID {user_id} and name {user_name} is logged as administrator.")
                print("-----------------------------------------------------------------------------")
                return True
            else:
                print(f"User with ID {user_id} and name {user_name} is not an administrator.")
                print("-----------------------------------------------------------------------------")
                return False
        else:
            print(f"User with ID {user_id} is not found in the database.")
            print("-----------------------------------------------------------------------------")
            return False

    except Exception as e:
        print(f"An error occurred: {e}")
        print("-----------------------------------------------------------------------------")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
