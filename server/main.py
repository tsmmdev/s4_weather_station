# import sys
import os
# from modules.config import Config
from modules.server import WeatherServer


ROOT_FOLDER = os.path.abspath(os.path.dirname(__file__))
# config = Config(ROOT_FOLDER)
server = WeatherServer(root_folder=ROOT_FOLDER)
server.start()
