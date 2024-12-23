from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form2(Form2Template):
    def __init__(self, **properties):
        self.init_components(**properties)

    def display_user_data(self, data):
        username = data.get("username", "Unknown")
        balance = data.get("balance", "Unknown")
        self.label_Output.text = f"Welcome, {username}. Your balance is {balance}."

    def button_back_click(self, **event_args):
        anvil.server.call('logout')
        open_form('Form1')
