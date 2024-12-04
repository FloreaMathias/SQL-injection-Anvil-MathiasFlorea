import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3

db_path = data_files['database.db']
@anvil.server.callable
def login_secure(username, password):
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            
            query = """
                SELECT Users.username, Balances.balance 
                FROM Users 
                JOIN Balances ON Users.AccountNo = Balances.AccountNo 
                WHERE Users.username = ? AND Users.password = ?
            """
            user = cursor.execute(query, (username, password)).fetchone()

            if user:
                return f"Willkommen {user[0]}! Dein Kontostand beträgt {user[1]}€"
            else:
                return "Login fehlgeschlagen!"
    except Exception as e:
        return f"Fehler: {str(e)}"


@anvil.server.callable
def login_insecure(username, password):
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            
            query = f"""
                SELECT Users.username, Balances.balance 
                FROM Users 
                JOIN Balances ON Users.AccountNo = Balances.AccountNo 
                WHERE Users.username = '{username}' AND Users.password = '{password}'
            """
            
            user = cursor.execute(query).fetchone()

            if user:
                return f"Willkommen {user[0]}! Dein Kontostand beträgt {user[1]} Euro."
            else:
                return f"Login fehlgeschlagen! Query: {query}"
    except Exception as e:
        return f"Fehler: {str(e)}"
