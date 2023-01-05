import utils
import time

#112 ping 113
class Ping_test:
    def __init__(self,test_node,other_node):
        self.obj_yaml = utils.ConfFile('config.yaml')
        self.yaml_info_list = self.obj_yaml.read_yaml()
        self.test_node_list = test_node
        self.other_node_list = other_node

    def start_test_node_ping(self):
            other_node_ip = "10.203.1.113"
            cmd = f"ping {other_node_ip}"
            self.test_node_list.invoke_conn.send(cmd+"\r")
            time.sleep(2)

    def end_test_node_ping(self):
        cmd = "\003"+"\r"
        ping_info_list = []
        self.test_node_list.invoke_conn.send(cmd)
        time.sleep(1)
        stdout = self.test_node_list.invoke_conn.recv(9999)
        info = stdout.decode()
        ping_info_list.append(info)

        return ping_info_list


if __name__ == '__main__':
    test_node = utils.SSHconn(host="10.203.1.112",password="password")
    other_node = utils.SSHconn(host="10.203.1.113",password="password")

    test_obj = Ping_test(test_node,other_node)
    test_obj.start_test_node_ping()
    time.sleep(5)
    list = test_obj.end_test_node_ping()
    print(list)

