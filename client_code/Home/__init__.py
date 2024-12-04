from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Home(HomeTemplate):
    def __init__(self, result, **properties):
        self.init_components(**properties)
        self.label_result.text = result

    def button_logout_click_click(self, **event_args):
      open_form('Login')
    