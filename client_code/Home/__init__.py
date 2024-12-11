from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables



class Home(HomeTemplate):
    def __init__(self, result="Willkommen zurück!", session_id=None, **properties):
      self.init_components(**properties)
      self.label_result.text = result
      
      if session_id:
            self.session_id = session_id

    def button_logout_click_click(self, **event_args):
        anvil.server.call('logout')
        open_form('Login')
