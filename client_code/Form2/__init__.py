from ._anvil_designer import Form2Template
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Form2(Form2Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    url = anvil.js.window.location.href
    queryparams = anvil.server.call('get_query_params', url)
    accno = queryparams.get('AccountNo', [None])[0]
    self.label_Output.text = anvil.server.call('get_data_accountno', accno)

    # Any code you write here will run before the form opens.

  def outlined_button_back_click(self, **event_args):
    anvil.server.call('logout')
    open_form('Form1')