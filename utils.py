from prettytable import PrettyTable
import subprocess
import sys
import yaml
import paramiko
import telnetlib
from DALAvailability import exec_command
import logging
import logging.handlers
import datetime
import sys
import socket

class Telnetconn:
    def __init__(self,ip):
        self.ip = ip
        self.tn = telnetlib.Telnet(f"{self.ip}")

    def exec_cmd(self,cmd):
        self.tn.write(f"{cmd}".encode('utf-8') + b'\n')
        res = self.tn.read_very_eager().decode('utf-8')


class SSHconn(object):
    def __init__(self, host, port=22, username="root", password=None, timeout=8):
        self._host = host
        self._port = port
        self._username = username
        self._password = password
        self.timeout = timeout
        self.sshconnection = None
        self.ssh_conn()
        self.invoke_conn = self.sshconnection.invoke_shell()
        self.invoke_conn.keep_this = self.sshconnection

    def __str__(self):
        return f"node:{self._host}"

    def ssh_conn(self):
        """
        SSH连接
        """
        try:
            conn = paramiko.SSHClient()
            conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            conn.connect(hostname=self._host,
                         username=self._username,
                         port=self._port,
                         password=self._password,
                         timeout=self.timeout,
                         look_for_keys=False,
                         allow_agent=False)
            self.sshconnection = conn
        except paramiko.AuthenticationException:
            print(f" Error SSH connection message of {self._host}")
        except Exception as e:
            print(f" Failed to connect {self._host}")

    def exec_cmd(self, command):
        """
        命令执行
        """
        if self.sshconnection:
            stdin, stdout, stderr = self.sshconnection.exec_command(command)
            result = stdout.read()
            result = result.decode() if isinstance(result, bytes) else result
            if result is not None:
                return {"st": True, "rt": result}

            err = stderr.read()
            if err is not None:
                return {"st": False, "rt": err}

def get_host_ip():
    """
    查询本机ip地址
    """
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

def exec_cmd(cmd, conn=None):
    local_obj = exec_command.LocalProcess()
    if conn:
        result = conn.exec_cmd(cmd)
    else:
        result = local_obj.exec_cmd(cmd)
    result = result.decode() if isinstance(result, bytes) else result
    log_data = f'{get_host_ip()} - {cmd} - {result}'
    Log().logger.info(log_data)
    if result['st']:
        pass
        # f_result = result['rt'].rstrip('\n')
    if result['st'] is False:
        sys.exit()
    return result['rt']

class ConfFile(object):
    def __init__(self,file_path):
        self.file_path = file_path
        self.config = self.read_yaml()

    def read_yaml(self):
        """
        读yaml文件
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                yaml_file = yaml.load(f,Loader=yaml.FullLoader)
            return yaml_file
        except FileNotFoundError:
            print("File not found")
        except TypeError:
            print("Error in the type of file .")

    def update_yaml(self,yaml_dict):
        """
        更新yaml文件
        """
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_dict, f, default_flow_style=False)
        except FileNotFoundError:
            print("File not found")
        except TypeError:
            print("Error in the type of file .")

class Log(object):
    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            Log._instance = super().__new__(cls)
            Log._instance.logger = logging.getLogger()
            Log._instance.logger.setLevel(logging.INFO)
            Log.set_handler(Log._instance.logger)
        return Log._instance

    @staticmethod
    def set_handler(logger):
        now_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        file_name = str(now_time) + '.log'
        fh = logging.FileHandler(file_name, mode='a')
        fh.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        logger.addHandler(fh)