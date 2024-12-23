from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from anvil.tables import app_tables

class Login(LoginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        state = anvil.server.call('get_login_state')
        if state is True:
            open_form('Home')
        self.check_box_unsafe.selected = True

    def button_login_click(self, **event_args):
        username = self.text_Username.text
        passwort = self.text_Password.text

        if self.check_box_unsafe.selected:
            login_result = anvil.server.call('get_user', username, passwort)
        else:
            login_result = anvil.server.call('get_user_safe', username, passwort)

        if isinstance(login_result, dict) and login_result.get("success"):
            account_no = login_result.get("accountno")
            if account_no:
                anvil.js.window.location.href = f"https://perfumed-red-purple.anvil.app/?AccountNo={account_no}"
            else:
                alert("AccountNo nicht gefunden.")
        else:
            alert(login_result)
