# import sys
import os
from modules.config import Config
from modules.server import WeatherServer

ROOT_FOLDER = os.path.abspath(os.path.dirname(__file__))
config = Config(ROOT_FOLDER)
server = WeatherServer(config=config)
server.start()
