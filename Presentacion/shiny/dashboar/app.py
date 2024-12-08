from shiny import App
from components.ui import app_ui
from components.server import server

app = App(app_ui, server).run()
