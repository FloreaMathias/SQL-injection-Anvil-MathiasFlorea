from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Login(LoginTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        logged_in_user = anvil.server.call('get_logged_in_user')
        if logged_in_user:
            open_form('Home', result=f"Willkommen zurück, {logged_in_user}")

        self.radio_button_unsafe.selected = True
        self.radio_button_safe.selected = False

    def button_login_click(self, **event_args):
        username = self.text_box_username.text
        password = self.text_box_password.text

        if self.radio_button_unsafe.selected:
            result_data = anvil.server.call('login_insecure', username, password)
        elif self.radio_button_safe.selected:
            if any(char in username + password for char in ["'", ";", "--", "/*", "*/"]):
                self.label_result.text = "Ungültige Eingabe erkannt!"
                return

            result_data = anvil.server.call('login_secure', username, password)
        else:
            result_data = {"result": "Bitte wähle einen Typ aus", "session_id": None}

        if result_data["result"].startswith("Willkommen"):
            open_form('Home', result=result_data["result"], session_id=result_data["session_id"])
        else:
            self.label_result.text = result_data["result"]
