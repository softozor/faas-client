import os.path
import re
from io import StringIO
from os import _Environ

import sh

from faas_client.exception import FaasClientException


class FaasClient:
    def __init__(
        self,
        gateway_url: str,
        gateway_port: int,
        username: str,
        password: str,
        env: _Environ[str] = None,
    ):
        self._cli = sh.Command("faas-cli")
        self.endpoint = f"{gateway_url}:{gateway_port}"
        self._username = username
        self._password = password
        self._env = env

    def login(self):
        result = self._cli(
            "login",
            "-g",
            self.endpoint,
            "--username",
            self._username,
            "--password",
            self._password,
        )
        if result.exit_code != 0:
            raise FaasClientException("unable to log on")

    def build(self, path_to_faas_configuration: str, function_name: str):
        configuration_filename = os.path.basename(path_to_faas_configuration)
        result = self._cli(
            "build",
            "-f",
            configuration_filename,
            "--filter",
            function_name,
            _cwd=os.path.dirname(path_to_faas_configuration),
            _env=self._env,
        )
        if result.exit_code != 0:
            raise FaasClientException(f"unable to build function {function_name}")

    def push(self, path_to_faas_configuration: str, function_name: str):
        configuration_filename = os.path.basename(path_to_faas_configuration)
        result = self._cli(
            "push",
            "-f",
            configuration_filename,
            "--filter",
            function_name,
            _cwd=os.path.dirname(path_to_faas_configuration),
            _env=self._env,
        )
        if result.exit_code != 0:
            raise FaasClientException(f"unable to push function {function_name}")

    def deploy(self, path_to_faas_configuration: str, function_name: str):
        result = self._cli(
            "deploy",
            "-f",
            path_to_faas_configuration,
            "--filter",
            function_name,
            "-g",
            self.endpoint,
            _env=self._env,
        )
        if result.exit_code != 0:
            raise FaasClientException(f"unable to deploy function {function_name}")

    def is_ready(self, function_name: str) -> bool:
        output_buffer = StringIO()
        result = self._cli(
            "describe", function_name, "-g", self.endpoint, _out=output_buffer
        )
        if result.exit_code != 0:
            raise FaasClientException(
                f"unable to assess readiness of function {function_name}"
            )
        description = output_buffer.getvalue()
        m = re.search(r"Status:\s*(.*)\n", description)
        return m.group(1) == "Ready" if m else False


class FaasClientFactory:
    def __init__(self, gateway_port: int, env: _Environ[str] = None):
        self._gateway_port = gateway_port
        self._env = env

    def create(self, gateway_url: str, username: str, password: str):
        return FaasClient(
            gateway_url, self._gateway_port, username, password, self._env
        )
