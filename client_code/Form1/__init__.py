from ._anvil_designer import Form1Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from anvil.tables import app_tables

class Form1(Form1Template):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.injection_possible = True
      # Any code you write here will run before the form opens.
      state = anvil.server.call('get_login_state')
      if state is True:
        open_form('Form2')


    def check_box_1_change(self, **event_args):
      """This method is called when this checkbox is checked or unchecked"""

    def button_login_click(self, **event_args):
      username = self.text_Username.text
      passwort = self.text_Password.text
      Resultpage = open_form('Form2')
      Resultpage.label_Output.text =  anvil.server.call("get_user",username, passwort)
      res = anvil.server.call('get_user_safe', username, passwort)
      print(res)
      pass

