import os
# import sys
from modules.client_config import Config
from modules.files import Files

ROOT_FOLDER = os.path.abspath(os.path.dirname(__file__))
# config = Config(ROOT_FOLDER)

parser = Files(root_folder=ROOT_FOLDER)
parser.parse_logs()
