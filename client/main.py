import os
import sys
import json

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


# # Check if the LOGS_DIR exists
# if not os.path.isdir(LOGS_DIR):
#     print(f"Error: {LOGS_DIR} does not exist.")
#     exit(1)
#
# data = {}
# # Read the last 100 lines of text files in the LOGS_DIR
# for filename in os.listdir(LOGS_DIR):
#     filepath = os.path.join(LOGS_DIR, filename)
#     if os.path.isfile(filepath) and filename.endswith(".txt"):
#         if f"{filename}" not in data:
#             data[f"{filename}"] = {
#                 "header": [],
#                 "data": []
#             }
#         with open(filepath, "r") as f:
#             all_lines = f.readlines()
#
#             header = all_lines[:1]
#             data[f"{filename}"]["header"] = header[0].strip().split("\t")
#             # throw some random value that we are going to ignore in server
#             data[f"{filename}"]["header"].append("junk")
#             lines = all_lines[-READ_LINES:]
#             for i, line in enumerate(lines[1:]):
#                 # throw some random value that we are going to ignore in server
#                 junk = random.randint(99999, 99999999999)
#                 values = line.strip().split("\t")
#                 values.append(junk)
#                 data[f"{filename}"]["data"].append(values)
#
#         #trim file
#         result = files.rewrite_file(filepath, STORE_MAX_LINES, BUFFER_STORE_MAX_LINES)
#
# response = server.send_data_to_server(HOST, PORT, DEVICE_ID, JWT_SECRET, data, SERVER_CERTIFICATE)
# print(response)




# # Convert the dictionary to JSON
# json_str = json.dumps(data)
#
# # Print the JSON
# # print(json_str)
#
# json_str_prety = json.dumps(data, indent=4)
# print(json_str_prety)
