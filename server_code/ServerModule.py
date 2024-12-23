import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
import urllib.parse


@anvil.server.callable
def get_login_state():
  if "login" not in anvil.server.session:
    anvil.server.session["login"] = False
  return anvil.server.session["login"]


@anvil.server.callable
def get_query_params(url):
    query = url.split('?')[-1] if '?' in url else ''
    query = urllib.parse.parse_qs(query)
    return query


@anvil.server.callable
def get_data_accountno(accountno):
    conn = sqlite3.connect(data_files["database.db"])
    cursor = conn.cursor()
    
    print(f"Received AccountNo: {accountno}") 
    
    querybalance = f"SELECT balance FROM Balances WHERE AccountNo = {accountno}"
    queryusername = f"SELECT username FROM Users WHERE AccountNo = {accountno}"
    
    try:
        username_result = cursor.execute(queryusername).fetchone()
        balance_result = cursor.execute(querybalance).fetchone()
        
        print(f"Username Query Result: {username_result}") 
        print(f"Balance Query Result: {balance_result}") 
        
        if username_result and balance_result:
            username = username_result[0] if username_result else "Unknown"
            balance = balance_result[0] if balance_result else "Unknown"
            return {"username": username, "balance": balance}
        else:
            return {"username": "Unknown", "balance": "Unknown"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}


    
@anvil.server.callable
def logout():
  anvil.server.session["login"] = False

@anvil.server.callable
def get_user(username, passwort):
    conn = sqlite3.connect(data_files["database.db"])
    cursor = conn.cursor()
    
    print(f"Unsicherer Login Versuch für: {username}")
    
    try:

        cursor.execute(f"SELECT username, AccountNo FROM Users WHERE username = '{username}' AND password = '{passwort}'")
        user = cursor.fetchone()
        
        print(f"Abfrageergebnis: {user}") 
        
        if user:
            username, accountno = user
            cursor.execute(f"SELECT balance FROM Balances WHERE AccountNo = {accountno}")
            balance = cursor.fetchone()
            balance = balance[0] if balance else "Unknown"
            anvil.server.session["login"] = True
            return {"success": True, "username": username, "balance": balance, "accountno": accountno}
        else:
            return "Login nicht erfolgreich. Bitte überprüfe deine Anmeldedaten."
    except Exception as e:
        return f"Fehler beim Login: {str(e)}"


@anvil.server.callable
def get_user_safe(username, passwort):
    conn = sqlite3.connect(data_files["database.db"])
    cursor = conn.cursor()
    
    print(f"Sicherer Login Versuch für: {username}")  
    try:
        cursor.execute("SELECT username, AccountNo FROM Users WHERE username = ? AND password = ?", (username, passwort))
        user = cursor.fetchone()
        
        print(f"Abfrageergebnis: {user}")  
        
        if user:
            username, accountno = user
            cursor.execute("SELECT balance FROM Balances WHERE AccountNo = ?", (accountno,))
            balance = cursor.fetchone()
            balance = balance[0] if balance else "Unknown"
            anvil.server.session["login"] = True
            return {"success": True, "username": username, "balance": balance, "accountno": accountno}
        else:
            return "Login nicht erfolgreich. Bitte überprüfe deine Anmeldedaten."
    except Exception as e:
        return f"Fehler beim Login: {str(e)}"


@anvil.server.callable
def get_data_accountno_safe(accountno):
  conn = sqlite3.connect(data_files["database.db"])
  cursor = conn.cursor()
  querybalance = "SELECT balance FROM Balances WHERE AccountNo = ?"(accountno)
  queryusername = "SELECT username FROM Users WHERE AccountNo = ?"(accountno)
  
  try:
   return list(cursor.execute(queryusername)) + list(cursor.execute(querybalance).fetchone())
  except Exception as e:
    return f"Error: {str(e)}"
    