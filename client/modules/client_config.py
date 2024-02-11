# import sys
import os
import json


class Config:
    def __init__(
            self,
            root_folder: str
    ):
        self.root_folder = root_folder
        config_path = os.path.join(root_folder, "client_config.json")
        with open(config_path, "r") as f:
            self.config = json.load(f)

    # TODO: add description in json
    def get_log_directory(self) -> str:
        return self.config.get("log_directory", "/data/data/com.termux/files/home/storage/shared/weather_station")

    # TODO: add description in json
    def get_read_lines(self) -> int:
        # around 96 records is one day every ~ 15min is one record. (24*60)/15 = 96 -> 100
        # default is 200 (2 days)
        return self.config.get("read_lines", 200)

    # TODO: add description in json
    # This also trims data from device
    def get_store_max_lines(self) -> int:
        # above how many lines is log file will trigger file to be truncated
        # store_max_lines - buffer_store_max_lines = how many lines will be left in log after truncate
        return self.config.get("store_max_lines", 1000)

    # TODO: add description in json
    # This also trims data from device
    def get_buffer_store_max_lines(self) -> int:
        # store_max_lines - buffer_store_max_lines = how many lines will be left in log after truncate
        return self.config.get("buffer_store_max_lines", 200)

    # TODO: add description here and in json
    def get_host(self) -> str:
        return self.config.get("host", "0.0.0.0")

    # TODO: add description here and in json
    def get_port(self) -> int:
        return self.config.get("port", 12345)

    # TODO: add description here and in json
    def get_device(self) -> str:
        return self.config.get("device", "home")

    # TODO: add description here and in json
    def get_jwt_secret(self) -> str:
        return self.config.get("jwt_secret", "r6Aur&A$nLyf*npUhYvv@i5j*D8$5PKY")

    # TODO: add description here and in json
    # TODO: good idea to trim this files also
    def get_ignore_logs(self) -> str:
        return self.config.get("ignore_logs", [])