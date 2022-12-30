import time
import timeout_decorator
import utils
import re
import sys
from threading import Thread


def interface_status_check(obj, interface):
    cmd = f"ifconfig {interface}"
    info = utils.exec_cmd(cmd, obj)
    test_info_1 = re.findall(r'(RUNNING)', info)
    if bool(test_info_1):
        print(f"{obj}的网卡：{interface}为正常连接状态")
        return True
    else:
        print(f"{obj}的网卡：{interface}为断开状态")
        return False

class EnvironmentalTesting:
    def __init__(self,test_node_list,other_node_list):
        self.obj_yaml = utils.ConfFile('config.yaml')
        self.yaml_info_list = self.obj_yaml.read_yaml()
        self.test_node_list = test_node_list
        self.other_node_list = other_node_list

    def check_nmcli(self):
        cmd = "nmcli device status"
        for test_node_obj,i in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            print(f"开始{test_node_obj} 的nmcli device status状态检测")
            sub1 = i['sub_bond_name']["sub1"]
            sub2 = i['sub_bond_name']["sub2"]
            info = utils.exec_cmd(cmd,test_node_obj)
            test_info_1 = re.findall(r'\n%s[\s]+[\w]*[\s]*(connected)[\s]+[\w]*\n?' % sub1, info)
            test_info_2 = re.findall(r'\n%s[\s]+[\w]*[\s]*(connected)[\s]+[\w]*\n?' % sub2, info)
            if bool(test_info_1) & bool(test_info_2):
                print(f"{test_node_obj} 的nmcli device status状态检测正常")
            else:
                print(f"{test_node_obj} 的nmcli device status状态检测异常，退出程序")
                sys.exit()

    def check_ifconfig(self):
        for test_node_obj,i in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            print(f"开始{test_node_obj} 的ifconfig状态检测")
            bond_name = i["bond_name"]
            sub1 = i['sub_bond_name']["sub1"]
            sub2 = i['sub_bond_name']["sub2"]
            cmd1 = f"ifconfig {bond_name}"
            cmd2 = f"ifconfig {sub1}"
            cmd3 = f"ifconfig {sub2}"
            info1 = utils.exec_cmd(cmd1,test_node_obj)
            info2 = utils.exec_cmd(cmd2,test_node_obj)
            info3 = utils.exec_cmd(cmd3,test_node_obj)
            test_info_1 = re.findall(r'(RUNNING)', info1)
            test_info_2 = re.findall(r'(RUNNING)', info2)
            test_info_3 = re.findall(r'(RUNNING)', info3)
            if bool(test_info_1) & bool(test_info_2) & bool(test_info_3):
                print(f"{test_node_obj} 的ifconfig状态检测正常")
            else:
                print(f"{test_node_obj} 的ifconfig状态检测异常，退出程序")
                sys.exit()

    def check_ethtool(self):
        for test_node_obj,i in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            print(f"开始{test_node_obj} 的ethtool状态检测")
            bond_name = i["bond_name"]
            cmd = f"ethtool {bond_name}"
            info = utils.exec_cmd(cmd, test_node_obj)
            test_info = re.findall(r'(Speed: 20000Mb/s)',info)
            if bool(test_info):
                print(f"{test_node_obj} 的ethtool状态检测正常")
            else:
                print(f"{test_node_obj} 的ethtool状态检测异常，退出程序")
                sys.exit()

    def check_bonding_config(self):
        for test_node_obj,i in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            print(f"开始{test_node_obj} 的bond配置文件状态检测")
            bond_name = i["bond_name"]
            cmd = f"cat /proc/net/bonding/{bond_name}"
            mode_0 = f"Bonding Mode: load balancing"
            mode_4 = f"Bonding Mode: IEEE 802.3ad"
            info = utils.exec_cmd(cmd, test_node_obj)
            test_info_1 = re.findall(r'(%s)'%mode_0, info)
            test_info_2 = re.findall(r'(%s)'%mode_4, info)
            if bool(test_info_1) is True:
                print(f"{test_node_obj} 为mode0")
            elif bool(test_info_2) is True:
                print(f"{test_node_obj} 为mode4")
            else:
                print(f"{test_node_obj} mode检测异常，退出程序")
                sys.exit()

    def initial_environment_check(self):
        print("--------开始初始环境检测--------")
        self.check_nmcli()
        self.check_ifconfig()
        self.check_ethtool()
        self.check_bonding_config()
        print("--------初始环境检测完成--------")

class FaultSimulation:
    def __init__(self,test_node_list,other_node_list):
        self.obj_yaml = utils.ConfFile('config.yaml')
        self.yaml_info_list = self.obj_yaml.read_yaml()
        self.test_node_list = test_node_list
        self.other_node_list = other_node_list

    def interface_down(self):
        for test_node_obj,i in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            sub1 = i['sub_bond_name']["sub1"]
            cmd = f"ifconfig {sub1} down"
            utils.exec_cmd(cmd,test_node_obj)
            time.sleep(5)
            status = interface_status_check(test_node_obj,sub1)
            if not status:
                print(f"{test_node_obj}的网卡{sub1}关闭成功")
            else:
                print(f"{test_node_obj}的网卡{sub1}关闭失败，退出程序")
                sys.exit()

    def port_down(self):
        telnet_obj = utils.Telnetconn(self.yaml_info_list["switch_node"]["ip"])
        cmd1 = "configure terminal"
        telnet_obj.exec_cmd(cmd1)
        for i in self.yaml_info_list["test_node"]:
            port = i["port_name"]
            cmd2 = f"interface {port}"
            cmd3 = "shutdown"
            telnet_obj.exec_cmd(cmd2)
            telnet_obj.exec_cmd(cmd3)

    @timeout_decorator.timeout(600)
    def network_cable_down(self):
        a = False
        while a is False:
            status_list = []
            time.sleep(5)
            for test_node_obj, i in zip(self.test_node_list, self.yaml_info_list["test_node"]):
                sub1 = i['sub_bond_name']["sub1"]
                status = interface_status_check(test_node_obj,sub1)
                status_list.append(status)

            test_list = []
            for z in status_list:
                if not z:
                    pass
                else:
                    test_list.append(False)

            if not bool(test_list):
                print("拔网线成功")
                break
            else:
                print("拔网线检测中")

class FaultRecovery:
    def __init__(self, test_node_list, other_node_list):
        self.obj_yaml = utils.ConfFile('config.yaml')
        self.yaml_info_list = self.obj_yaml.read_yaml()
        self.test_node_list = test_node_list
        self.other_node_list = other_node_list

    def interface_up(self):
        for test_node_obj in self.test_node_list:
            for i in self.yaml_info_list["test_node"]:
                sub1 = i['sub_bond_name']["sub1"]
                cmd = f"ifconfig {sub1} up"
                utils.exec_cmd(cmd,test_node_obj)
                time.sleep(5)
                status = interface_status_check(test_node_obj,sub1)
                if not status:
                    print(f"{test_node_obj}的网卡{sub1}开启成功")
                else:
                    print(f"{test_node_obj}的网卡{sub1}开启失败，退出程序")
                    sys.exit()

    def port_up(self):
        telnet_obj = utils.Telnetconn(self.yaml_info_list["switch_node"]["ip"])
        cmd1 = "configure terminal"
        telnet_obj.exec_cmd(cmd1)
        for i in self.yaml_info_list["test_node"]:
            port = i["port_name"]
            cmd2 = f"interface {port}"
            cmd3 = "no shutdown"
            telnet_obj.exec_cmd(cmd2)
            telnet_obj.exec_cmd(cmd3)

    @timeout_decorator.timeout(600)
    def network_cable_up(self):
        a = False
        while a is False:
            status_list = []
            time.sleep(5)
            for test_node_obj in self.test_node_list:
                for i in self.yaml_info_list["test_node"]:
                    sub1 = i['sub_bond_name']["sub1"]
                    status = interface_status_check(test_node_obj,sub1)
                    status_list.append(status)

            test_list = []
            for z in status_list:
                if z:
                    pass
                else:
                    test_list.append(False)

            if not bool(test_list):
                print("拔网线成功")
                break
            else:
                print("拔网线检测中")

class Ping:
    def __init__(self,test_node_list,other_node_list):
        self.obj_yaml = utils.ConfFile('config.yaml')
        self.yaml_info_list = self.obj_yaml.read_yaml()
        self.test_node_list = test_node_list
        self.other_node_list = other_node_list

    def start_test_node_ping(self,obj):
            other_node_ip = self.yaml_info_list["other_node"][0]["ip"]
            cmd = f"ping {other_node_ip}"
            obj.invoke_conn.send(cmd+"\r")
            time.sleep(2)


    def thread_start_test_node_ping(self):
        for test_node_obj in self.test_node_list:
            state1 = Thread(target=self.start_test_node_ping,args=(test_node_obj,))
            state1.setDaemon(True)
            state1.start()

    def end_test_node_ping(self):
        cmd = "\003"+"\r"
        ping_info_list = []
        for test_node_obj in self.test_node_list:
            test_node_obj.invoke_conn.send(cmd)
            time.sleep(1)
            stdout = test_node_obj.invoke_conn.recv(9999)
            info = stdout.decode()
            ping_info_list.append(info)

        return ping_info_list
