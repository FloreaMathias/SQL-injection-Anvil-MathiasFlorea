import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
from urllib.parse import urlparse, parse_qs
import uuid


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
                anvil.server.session["username"] = user[0]
                return {"result": f"Willkommen {user[0]}! Dein Kontostand beträgt {user[1]}€", "session_id": anvil.server.session.session_id}
            else:
                return {"result": "Login fehlgeschlagen!", "session_id": None}
    except Exception as e:
        return {"result": f"Fehler: {str(e)}", "session_id": None}

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
                anvil.server.session["username"] = user[0]
                return {"result": f"Willkommen {user[0]}! Dein Kontostand beträgt {user[1]} Euro.", "session_id": anvil.server.session.session_id}
            else:
                return {"result": "Login fehlgeschlagen!", "session_id": None}
    except Exception as e:
        return {"result": f"Fehler: {str(e)}", "session_id": None}


@anvil.server.callable
def get_logged_in_user_from_session(session_id):
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            query = "SELECT username FROM sessions WHERE session_id = ?"
            user = cursor.execute(query, (session_id,)).fetchone()
            return user[0] if user else None
    except Exception:
        return None



  
@anvil.server.callable
def get_logged_in_user():
    return anvil.server.session.get("username", None)

@anvil.server.callable
def logout():
    if "username" in anvil.server.session:
        del anvil.server.session["username"]
    return "Logout erfolgreich!"


@anvil.server.callable
def get_username_from_id(account_no):
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            
            query = f"SELECT username FROM Users WHERE AccountNo = {account_no}"
            user = cursor.execute(query).fetchone()

            if user:
                return f"Benutzername: {user[0]}"
            else:
                return "Kein Benutzer mit dieser AccountNo gefunden!"
    except Exception as e:
        return f"Fehler: {str(e)}"

@anvil.server.callable
def get_account_balance():
    full_url = anvil.server.request.url  
    
    parsed_url = urlparse(full_url)
    query_params = parse_qs(parsed_url.query)
    
    account_no = query_params.get('AccountNo', [''])[0] 
    
    print(f"AccountNo-Eingabe: {account_no}")
    
    try:
        with sqlite3.connect(db_path) as connection:
            cursor = connection.cursor()
            
            query = f"""
                SELECT Users.username, Balances.balance 
                FROM Users 
                JOIN Balances ON Users.AccountNo = Balances.AccountNo 
                WHERE Users.AccountNo = {account_no}
            """
           
            
            user = cursor.execute(query).fetchall()

            if user:
                return f"Gefundene Benutzer: {user}"
            else:
                return "Kein Benutzer mit dieser AccountNo gefunden!"
    except Exception as e:
        return f"Fehler bei der Abfrage: {str(e)}"