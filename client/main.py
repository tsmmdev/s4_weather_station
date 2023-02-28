import os
# import sys
from modules.config import Config
from modules.files import Files

ROOT_FOLDER = os.path.abspath(os.path.dirname(__file__))
config = Config(ROOT_FOLDER)

parser = Files(config=config)
parser.parse_logs()
