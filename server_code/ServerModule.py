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


#Design und variablen und button var ändern


  
  
@anvil.server.callable
def get_user(username, passwort):
  conn = sqlite3.connect(data_files["database.db"])
  cursor =  conn.cursor()
  try:
    res = cursor.execute(f"SELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'")
    result = cursor.fetchone()
    if result:
      res = "Login successful but 'AccountNo' was not passed."
      anvil.server.session["login"] = True
    else:
      raise ValueError("Empty Data")
  except Exception:
    res = f"Login not successful: \nSELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'"
  return res

@anvil.server.callable
def get_query_params(url):
  query = url.split('?')[-1] if '?' in url else ''
  query = urllib.parse.parse_qs(query)
  return query
  
@anvil.server.callable
def get_data_accountno(accountno):
  conn = sqlite3.connect(data_files["database.db"])
  cursor = conn.cursor()
  querybalance = f"SELECT balance FROM Balances WHERE AccountNo = {accountno}"
  queryusername = f"SELECT username FROM Users WHERE AccountNo = {accountno}"
  
  try:
   return list(cursor.execute(queryusername)) + list(cursor.execute(querybalance))
  except:
    return ""
    
@anvil.server.callable
def logout():
  anvil.server.session["login"] = False


@anvil.server.callable
def get_user_safe(username, passwort):
  conn = sqlite3.connect(data_files["database.db"])
  cursor =  conn.cursor()
  try:
    res = cursor.execute("SELECT username FROM Users WHERE username = ? AND password = ?", (username, passwort))
    result = cursor.fetchone()
    if result:
      balance = list(cursor.execute("SELECT Balances.balance FROM Users JOIN Balances ON Users.AccountNo = Balances.AccountNo WHERE Users.username = ? AND Users.password = ?",(username, passwort)))
      res = f"Welcome {username}. Your Balance is {balance}"
      anvil.server.session["login"] = True
    else:
      raise ValueError("Empty Data")
  except Exception:
    res = f"Login not successful: \nSELECT username FROM Users WHERE username = '{username}' AND password = '{passwort}'"
  return res

@anvil.server.callable
def get_data_accountno_safe(accountno):
  conn = sqlite3.connect(data_files["database.db"])
  cursor = conn.cursor()
  querybalance = "SELECT balance FROM Balances WHERE AccountNo = ?"(accountno)
  queryusername = "SELECT username FROM Users WHERE AccountNo = ?"(accountno)
  
  try:
   return list(cursor.execute(queryusername)) + list(cursor.execute(querybalance).fetchone())
  except:
    return ""
    