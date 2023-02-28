# import sys
import os
import json


class Config:
    def __init__(
            self,
            root_folder: str
    ):
        self.root_folder = root_folder
        config_path = os.path.join(root_folder, "config.json")
        with open(config_path, "r") as f:
            self.config = json.load(f)

    def get_log_directory(self) -> str:
        return self.config.get("log_directory", "/data/data/com.termux/files/home/storage/shared/weather_station")

    def get_read_lines(self) -> int:
        # around 96 records is one day every ~ 15min is one record. (24*60)/15 = 96 -> 100
        return self.config.get("read_lines", 100)

    def get_store_max_lines(self) -> int:
        # above how many lines is log file will trigger file to be truncated
        # store_max_lines - buffer_store_max_lines = how many lines will be left in log after truncate
        return self.config.get("store_max_lines", 800)

    def get_buffer_store_max_lines(self) -> int:
        # store_max_lines - buffer_store_max_lines = how many lines will be left in log after truncate
        return self.config.get("buffer_store_max_lines", 100)

    def get_host(self) -> str:
        return self.config.get("host", "0.0.0.0")

    def get_port(self) -> int:
        return self.config.get("port", 12345)

    def get_device(self) -> str:
        return self.config.get("device", "home")

    def get_jwt_secret(self) -> str:
        return self.config.get("jwt_secret", "r6Aur&A$nLyf*npUhYvv@i5j*D8$5PKY")

    def get_certificate(self) -> {}:
        certificate_config = self.config.get("certificates", {})
        certificate_folder = os.path.join(self.root_folder, certificate_config["folder"])
        certificate = os.path.join(certificate_folder, certificate_config["certificate"])
        return certificate
