import os
import sys
import json
# from modules.config import Config


# ROOT_FOLDER = os.path.abspath(os.path.dirname(__file__))
# config = Config(ROOT_FOLDER)


ROOT_FOLDER = os.path.abspath(os.path.dirname(__file__))
MODULES_DIRECTORY = os.path.join(ROOT_FOLDER, "modules")
CONFIG_PATH = os.path.join(ROOT_FOLDER, "config.json")
sys.path.append(MODULES_DIRECTORY)
import files

# Read the config file
with open(CONFIG_PATH, "r") as f:
    CONFIG = json.load(f)

JWT_SECRET = CONFIG.get("jwt_secret", "r6Aur&A$nLyf*npUhYvv@i5j*D8$5PKY")
HOST = CONFIG.get("host", "0.0.0.0")
PORT = CONFIG.get("port", 12345)
DEVICE_ID = CONFIG.get("device_id", "home")

CERT_CONFIG = CONFIG.get("certificates", {})
CERT_FOLDER = os.path.join(ROOT_FOLDER, CERT_CONFIG["folder"])
SERVER_CERTIFICATE = os.path.join(CERT_FOLDER, CERT_CONFIG["certificate"])

LOGS_DIR = CONFIG.get("log_directory", os.path.expanduser("~/storage/shared/weather_station"))
READ_LINES = CONFIG.get("read_lines", 100)

# one day
BUFFER_STORE_MAX_LINES = CONFIG.get("buffer_store_max_lines", 96)
# one week
STORE_MAX_LINES = CONFIG.get("store_max_lines", 672)

files.parse_logs(
    LOGS_DIR,
    READ_LINES,
    STORE_MAX_LINES,
    BUFFER_STORE_MAX_LINES,
    HOST,
    PORT,
    DEVICE_ID,
    JWT_SECRET,
    SERVER_CERTIFICATE
)
