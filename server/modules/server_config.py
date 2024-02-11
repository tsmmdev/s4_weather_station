# import sys
import os
import json


class Config:
    def __init__(
            self,
            root_folder
    ):
        self.root_folder = root_folder
        self.config_path = os.path.join(root_folder, "server_config.json")
        # with open(self.config_path, "r") as f:
        #     self.config = json.load(f)
        self.load_config()

    def load_config(self):
        with open(self.config_path, "r") as f:
            self.config = json.load(f)

    def get_clients(self) -> dict:
        return self.config.get("clients", {})

    def get_jwt_secret(self) -> str:
        return self.config.get("jwt_secret", "r6Aur&A$nLyf*npUhYvv@i5j*D8$5PKY")

    def get_host(self) -> str:
        return self.config.get("host", "0.0.0.0")

    def get_port(self) -> int:
        return self.config.get("port", 12345)

    def get_db_file(self) -> str:
        db_folder = os.path.join(self.root_folder, "db")
        db_file = os.path.join(db_folder, "weather.db")
        return db_file

    def _get_certificates_files(self) -> {}:
        certificate_config = self.config.get("certificates", {})
        certificate_folder = os.path.join(self.root_folder, 'certs')
        certificate = os.path.join(certificate_folder, certificate_config["certificate"])
        certificate_key = os.path.join(certificate_folder, certificate_config["key"])
        result = {
            "certificate": certificate,
            "key": certificate_key
        }
        return result

    def get_certificate(self) -> str:
        return self._get_certificates_files()["certificate"]

    def get_certificate_key(self) -> str:
        return self._get_certificates_files()["key"]
