from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        url = anvil.js.window.location.href
        queryparams = anvil.server.call('get_query_params', url)
        print(f"Query Params: {queryparams}")  

        accno = queryparams.get('AccountNo', [None])[0]
        print(f"Account Number from URL: {accno}")  

        if accno:
            result = anvil.server.call('get_data_accountno', accno)
            print(f"Account Data: {result}") 
            self.display_user_data(result)
        else:
            self.label_Output.text = "Kein Kontonummer in der URL angegeben."

        if self.is_admin(accno):
            self.show_all_users()

    def display_user_data(self, data):
        print(f"Benutzerdaten anzeigen: {data}")  

        username = data.get("username", "Unbekannt")
        balance = data.get("balance", "Unbekannt")
        self.label_Output.text = f"Willkommen, {username}. Dein Kontostand ist {balance}."

    def show_all_users(self):
        users = anvil.server.call('get_all_users')
        
        if isinstance(users, list):
            all_users_text = ""
            for user in users:
                all_users_text += f"Username: {user['username']}, AccountNo: {user['accountno']}, Balance: {user['balance']}\n"
            
            self.label_Output.text = all_users_text
        else:
            self.label_Output.text = "Fehler beim Abrufen der Benutzerdaten."

    def is_admin(self, accountno):
        return accountno == "1001"  

    def button_back_click(self, **event_args):
        anvil.server.call('logout')
        open_form('Login')
