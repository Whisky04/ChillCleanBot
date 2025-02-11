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

def create_table_if_not_exists():
    """Create the users table if it does not already exist."""
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            user_id INT PRIMARY KEY,
            user_name VARCHAR(100),
            user_week INT[],
            user_is_admin BOOLEAN
        );
        """
        cursor.execute(create_table_query)
        connection.commit()
        print("Table 'users' has been created or already exists.")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
            
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
            user_name = result[0]
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

def add_new_user(user_id: int, user_name: str) -> bool:
    """Adds a new user to the database."""
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Check if user already exists
        cursor.execute("SELECT user_id FROM users WHERE user_id = %s;", (user_id,))
        if cursor.fetchone():
            print(f"Warning: User {user_id} already exists in the database.")
            return False

        # Insert new user
        insert_query = """
        INSERT INTO users (user_id, user_name, user_week, user_is_admin)
        VALUES (%s, %s, ARRAY[]::INTEGER[], FALSE);
        """
        cursor.execute(insert_query, (user_id, user_name))
        connection.commit()

        print(f"User {user_name} (ID: {user_id}) added successfully.")
        return True

    except Exception as e:
        print(f"Error Database: error while adding user: {e}")
        return False

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

def delete_existing_user(user_id: int) -> tuple[bool, str | None]:
    """Deletes a user from the database and returns the username if successful."""
    try:
        connection = psycopg2.connect(**db_params)
        cursor = connection.cursor()

        # Check if user exists before deleting
        cursor.execute("SELECT user_name FROM users WHERE user_id = %s;", (user_id,))
        result = cursor.fetchone()
        
        if not result:
            print(f"Warning: User {user_id} does not exist in the database.")
            return False, None  # User not found
        
        user_name = result[0]  # Get username
        
        # Delete user
        delete_query = "DELETE FROM users WHERE user_id = %s;"
        cursor.execute(delete_query, (user_id,))
        connection.commit()

        print(f"User '{user_name}' (ID: {user_id}) has been successfully deleted.")
        return True, user_name  # Return success and username

    except Exception as e:
        print(f"Error Database: Error while deleting user: {e}")
        return False, None  # Return failure

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()
