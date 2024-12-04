from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Login(LoginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        
        self.radio_button_unsafe.selected = True
        self.radio_button_safe.selected = False
   
          
    def button_login_click(self, **event_args):
        username = self.text_box_username.text
        password = self.text_box_password.text
        
        if self.radio_button_unsafe.selected:
            result = anvil.server.call('login_insecure', username, password)
        elif self.radio_button_safe.selected:
            result = anvil.server.call('login_secure', username, password)
        else:
            result = "Bitte wähle einen Typ aus"
        
        if result.startswith("Willkommen"):
            open_form('Home', result=result)
        else:
            self.label_result.text = result
