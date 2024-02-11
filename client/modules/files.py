# import sys
import os
import random
from .client_config import Config
from .server import ServerConnect
from .helpers import log_time_zone


def _rewrite_file(filepath, max_lines, buffer, just_return=False):
    # Check if file exists
    if not os.path.exists(filepath):
        return f"Error: file '{filepath}' does not exist"

    # Check if file is not binary
    if not os.path.isfile(filepath):
        return f"Error: '{filepath}' is not a file"

    # Check if max_lines is valid
    if max_lines < 1:
        return "Error: max_lines must be greater than or equal to 1"

    # Check if buffer is smaller than max_lines
    if buffer >= max_lines:
        return "Error: buffer must be less than buffer"

    # Read the lines in the file
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Check if the file has enough lines
    if len(lines) <= max_lines:
        return f"Error: file '{filepath}' has less than {max_lines} lines"

    # Get the header line and last max_lines lines
    header_line = lines[0]
    # buffer gives us more time. we don`t want everytime to rewrite file
    last_lines = lines[-(max_lines - buffer):]

    if just_return:
        return [header_line] + last_lines
    else:
        # Truncate the file and write the new data
        with open(filepath, 'w') as f:
            f.write(header_line)
            f.writelines(last_lines)

    return f"File '{filepath}' rewritten with {max_lines} lines"


class Files:
    def __init__(self, root_folder):
        self.config = Config(root_folder)

    def parse_logs(self):
        logs_dir = self.config.get_log_directory()
        if not os.path.isdir(logs_dir):
            print(f"Error: {logs_dir} does not exist.")
            exit(1)
        # SEE client/modules/client_config.py foe config explanation
        read_lines = self.config.get_read_lines()
        store_max_lines = self.config.get_store_max_lines()
        buffer_store_max_lines = self.config.get_buffer_store_max_lines()

        data = {}
        ignore_logs = self.config.get_ignore_logs()
        for filename in os.listdir(logs_dir):
            filepath = os.path.join(logs_dir, filename)
            if os.path.isfile(filepath) and filename.endswith("_log.txt"):
                temp_filename = filename
                temp_filename = temp_filename.split('_')[0]
                if temp_filename not in ignore_logs:
                    if f"{filename}" not in data:
                        data[f"{filename}"] = {
                            "header": [],
                            "data": []
                        }
                    with open(filepath, "r") as f:
                        all_lines = f.readlines()
                        header = all_lines[:1]
                        data[f"{filename}"]["header"] = header[0].strip().split("\t")
                        # throw some random value that we are going to ignore in server for security reasons
                        lines = all_lines[-read_lines:]
                        for i, line in enumerate(lines[1:]):
                            values = line.strip().split("\t")
                            data[f"{filename}"]["data"].append(values)

                    # trim file
                    _rewrite_file(filepath=filepath, max_lines=store_max_lines, buffer=buffer_store_max_lines)

        server = ServerConnect(config=self.config)
        response = server.send_data_to_server(data=data)
        print(f"{log_time_zone()}: " + response)
