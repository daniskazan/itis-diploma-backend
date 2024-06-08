from abc import ABC
from typing import TypedDict
import paramiko
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from sqlalchemy.engine import create_engine

from core.models import Grant, Application


class ResourceConnector(ABC):

    def execute(self) -> None:
        raise NotImplementedError


class ServerSSHConnectionParams(TypedDict):
    username: str
    password: str


class CreateNewSSHConnectionServerConnector(ResourceConnector):
    def __init__(
            self,
            server_ip: str,
            connection_params: ServerSSHConnectionParams,
            running_script: str,
            grant: Grant
    ):
        self.server_ip = server_ip
        self.connection_params = connection_params
        self.grant = grant
        self.running_script = running_script

    def __connect_to_server(self) -> paramiko.SSHClient | None:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(
                hostname=self.server_ip,
                username=self.connection_params.get("username"),
            )
            return ssh
        except Exception as exc:
            return

    def execute(self) -> str:
        ssh_client = self.__connect_to_server()
        username = self.grant.application.user.email
        ssh_public_key = self.grant.application.payload["ssh"]
        # Добавляем нового пользователя
        command = f"sudo adduser --disabled-password --gecos '' {username}"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdout.channel.recv_exit_status()  # Ждем завершения команды

        # Создаем каталог .ssh для нового пользователя
        command = f"sudo -u {username} mkdir -p /home/{username}/.ssh"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdout.channel.recv_exit_status()

        # Добавляем открытый ключ в файл authorized_keys нового пользователя
        command = f"echo '{ssh_public_key}' | sudo -u {username} tee -a /home/{username}/.ssh/authorized_keys"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdout.channel.recv_exit_status()

        # Устанавливаем правильные права доступа
        command = f"sudo -u {username} chmod 700 /home/{username}/.ssh"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdout.channel.recv_exit_status()

        command = f"sudo -u {username} chmod 600 /home/{username}/.ssh/authorized_keys"
        stdin, stdout, stderr = ssh_client.exec_command(command)
        stdout.channel.recv_exit_status()

        # Закрываем соединение
        ssh_client.close()
        res = stdout.read().decode()
        return res

class DatabaseCommandExecutor(ResourceConnector):
    def __init__(self, db_url: str, running_script: str, grant: Grant):
        self.db_url = db_url
        self.running_script = running_script
        self.grant = grant

    def __fill_user_parameters(self):
        user_data = self.grant.application.payload
        self.running_script = self.running_script.format(**user_data)

    def execute(self):
        engine = create_engine(url=self.db_url)
        Session = sessionmaker(engine)

        self.__fill_user_parameters()
        with Session() as session:
            res = session.execute(text(self.running_script))
            return res
