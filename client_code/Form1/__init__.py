from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from anvil.tables import app_tables

class Form1(Form1Template):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.injection_possible = True
        state = anvil.server.call('get_login_state')
        if state is True:
            open_form('Form2')

    def button_login_click(self, **event_args):
        username = self.text_Username.text
        passwort = self.text_Password.text

        if self.check_box_safe.selected:
            login_result = anvil.server.call('get_user_safe', username, passwort)
        else:
            login_result = anvil.server.call('get_user', username, passwort)

        if isinstance(login_result, dict) and login_result.get("success"):
            Resultpage = open_form('Form2')
            Resultpage.display_user_data(login_result)
        else:
            alert(login_result)

    

