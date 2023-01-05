import time
import bonding_test
import argparse
import sys
import utils

class Arg:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog='argparse')
        self.setup_parse()
        self.test_obj = Test()

    def setup_parse(self):
        sub_parser = self.parser.add_subparsers()

        self.parser.add_argument('-v',
                                 '--version',
                                 dest='version',
                                 help='Show current version',
                                 action='store_true')

        self.parser.set_defaults(func=self.main_usage)

        parser_test01 = sub_parser.add_parser("test01",aliases=['t01'],help='free_login')
        parser_test02 = sub_parser.add_parser("test02",aliases=['t02'],help='free_login')
        parser_test03 = sub_parser.add_parser("test03",aliases=['t03'],help='free_login')
        parser_test04 = sub_parser.add_parser("test04",aliases=['t04'],help='free_login')
        parser_test05 = sub_parser.add_parser("test05",aliases=['t05'],help='free_login')
        parser_test06 = sub_parser.add_parser("test06",aliases=['t06'],help='free_login')
        parser_test07 = sub_parser.add_parser("test07",aliases=['t07'],help='free_login')
        parser_test08 = sub_parser.add_parser("test08",aliases=['t08'],help='free_login')

        parser_test01.set_defaults(func=self.func_test01)
        parser_test02.set_defaults(func=self.func_test02)
        parser_test03.set_defaults(func=self.func_test03)
        parser_test04.set_defaults(func=self.func_test04)
        parser_test05.set_defaults(func=self.func_test05)
        parser_test06.set_defaults(func=self.func_test06)
        parser_test07.set_defaults(func=self.func_test07)
        parser_test08.set_defaults(func=self.func_test08)

    def main_usage(self, args):
        if args.version:
            print(f'Version: ？')
            sys.exit()
        else:
            self.parser.print_help()

    def parser_init(self):
        args = self.parser.parse_args()
        args.func(args)

    def func_test01(self,args):
        self.test_obj.test1()

    def func_test02(self,args):
        self.test_obj.test2()

    def func_test03(self,args):
        self.test_obj.test3()

    def func_test04(self,args):
        self.test_obj.test4()

    def func_test05(self,args):
        self.test_obj.test5()

    def func_test06(self,args):
        self.test_obj.test6()

    def func_test07(self,args):
        self.test_obj.test7()

    def func_test08(self,args):
        self.test_obj.test8()

class Test:
    def __init__(self):
        self.obj_yaml = utils.ConfFile('config.yaml')
        self.yaml_info_list = self.obj_yaml.read_yaml()
        self.test_node_list, self.other_node_list = init()

    def test1(self):
        init_env_obj = bonding_test.EnvironmentalTesting(self.test_node_list,self.other_node_list)
        init_env_obj.initial_environment_check()

        test_node_ip_list = []
        re_other_node_obj_list = []
        for i in self.yaml_info_list["test_node"]:
            test_node_ip_list.append(i["ip"])
            other_node_obj = utils.SSHconn(host=self.yaml_info_list["other_node"]["ip"]
                                           ,password=self.yaml_info_list["other_node"]["password"])
            re_other_node_obj_list.append(other_node_obj)

        ping_obj = bonding_test.Ping(self.test_node_list,self.other_node_list)
        ping_obj.thread_start_other_node_ping(test_node_ip_list=test_node_ip_list,re_other_node_obj_list=re_other_node_obj_list)
        time.sleep(100)
        ping_info_list = ping_obj.end_other_node_ping(re_other_node_obj_list=re_other_node_obj_list)

    def test2(self):
        init_env_obj = bonding_test.EnvironmentalTesting(self.test_node_list, self.other_node_list)
        init_env_obj.initial_environment_check()

        test_node_ip_list = []
        re_other_node_obj_list = []
        for i in self.yaml_info_list["test_node"]:
            test_node_ip_list.append(i["ip"])
            other_node_obj = utils.SSHconn(host=self.yaml_info_list["other_node"]["ip"]
                                           , password=self.yaml_info_list["other_node"]["password"])
            re_other_node_obj_list.append(other_node_obj)

        ping_obj = bonding_test.Ping(self.test_node_list,self.other_node_list)
        ping_obj.thread_start_other_node_ping(test_node_ip_list=test_node_ip_list,re_other_node_obj_list=re_other_node_obj_list)

        fault_sim_obj = bonding_test.FaultSimulation(self.test_node_list,self.other_node_list)
        fault_sim_obj.interface_down()

        for i,z in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            status = bonding_test.interface_status_check(i,z['sub_bond_name']["sub1"])
            if not status:
                pass
            else:
                sys.exit()

        time.sleep(20)

        ping_info_list = ping_obj.end_other_node_ping(re_other_node_obj_list)

        ping_obj.thread_start_other_node_ping(re_other_node_obj_list=re_other_node_obj_list,test_node_ip_list=test_node_ip_list)
        fault_rec_obj = bonding_test.FaultRecovery(self.test_node_list,self.other_node_list)
        fault_rec_obj.interface_up()

        for i,z in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            status = bonding_test.interface_status_check(i,z['sub_bond_name']["sub1"])
            if status:
                pass
            else:
                sys.exit()

        time.sleep(20)

        ping_info_list2 = ping_obj.end_other_node_ping(re_other_node_obj_list)

    def test3(self):
        init_env_obj = bonding_test.EnvironmentalTesting(self.test_node_list, self.other_node_list)
        init_env_obj.initial_environment_check()

        test_node_ip_list = []
        re_other_node_obj_list = []
        for i in self.yaml_info_list["test_node"]:
            test_node_ip_list.append(i["ip"])
            other_node_obj = utils.SSHconn(host=self.yaml_info_list["other_node"]["ip"]
                                           , password=self.yaml_info_list["other_node"]["password"])
            re_other_node_obj_list.append(other_node_obj)

        ping_obj = bonding_test.Ping(self.test_node_list,self.other_node_list)
        ping_obj.thread_start_other_node_ping(test_node_ip_list=test_node_ip_list,re_other_node_obj_list=re_other_node_obj_list)

        fault_sim_obj = bonding_test.FaultSimulation(self.test_node_list,self.other_node_list)
        fault_sim_obj.network_cable_down()

        for i,z in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            status = bonding_test.interface_status_check(i,z['sub_bond_name']["sub1"])
            if not status:
                pass
            else:
                sys.exit()

        time.sleep(20)

        ping_info_list = ping_obj.end_other_node_ping(re_other_node_obj_list)

        ping_obj.thread_start_other_node_ping(re_other_node_obj_list=re_other_node_obj_list,test_node_ip_list=test_node_ip_list)
        fault_rec_obj = bonding_test.FaultRecovery(self.test_node_list,self.other_node_list)
        fault_rec_obj.network_cable_up()

        for i,z in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            status = bonding_test.interface_status_check(i,z['sub_bond_name']["sub1"])
            if status:
                pass
            else:
                sys.exit()

        time.sleep(20)

        ping_info_list2 = ping_obj.end_other_node_ping(re_other_node_obj_list)

    def test4(self):
        init_env_obj = bonding_test.EnvironmentalTesting(self.test_node_list, self.other_node_list)
        init_env_obj.initial_environment_check()

        test_node_ip_list = []
        re_other_node_obj_list = []
        for i in self.yaml_info_list["test_node"]:
            test_node_ip_list.append(i["ip"])
            other_node_obj = utils.SSHconn(host=self.yaml_info_list["other_node"]["ip"]
                                           , password=self.yaml_info_list["other_node"]["password"])
            re_other_node_obj_list.append(other_node_obj)

        ping_obj = bonding_test.Ping(self.test_node_list,self.other_node_list)
        ping_obj.thread_start_other_node_ping(test_node_ip_list=test_node_ip_list,re_other_node_obj_list=re_other_node_obj_list)

        fault_sim_obj = bonding_test.FaultSimulation(self.test_node_list,self.other_node_list)
        fault_sim_obj.port_down()

        for i,z in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            status = bonding_test.interface_status_check(i,z['sub_bond_name']["sub1"])
            if not status:
                pass
            else:
                sys.exit()

        time.sleep(20)

        ping_info_list = ping_obj.end_other_node_ping(re_other_node_obj_list)

        ping_obj.thread_start_other_node_ping(re_other_node_obj_list=re_other_node_obj_list,test_node_ip_list=test_node_ip_list)
        fault_rec_obj = bonding_test.FaultRecovery(self.test_node_list,self.other_node_list)
        fault_rec_obj.port_up()

        for i,z in zip(self.test_node_list,self.yaml_info_list["test_node"]):
            status = bonding_test.interface_status_check(i,z['sub_bond_name']["sub1"])
            if status:
                pass
            else:
                sys.exit()

        time.sleep(20)

        ping_info_list2 = ping_obj.end_other_node_ping(re_other_node_obj_list)

    def test5(self):
        init_env_obj = bonding_test.EnvironmentalTesting(self.test_node_list, self.other_node_list)
        init_env_obj.initial_environment_check()

        ping_obj = bonding_test.Ping(self.test_node_list,self.other_node_list)
        ping_obj.thread_start_test_node_ping()

        time.sleep(100)

        ping_info_list = ping_obj.end_test_node_ping()



    def test6(self):
        init_env_obj = bonding_test.EnvironmentalTesting(self.test_node_list, self.other_node_list)
        init_env_obj.initial_environment_check()

        ping_obj = bonding_test.Ping(self.test_node_list, self.other_node_list)
        ping_obj.thread_start_test_node_ping()

        fault_sim_obj = bonding_test.FaultSimulation(self.test_node_list, self.other_node_list)
        fault_sim_obj.interface_down()

        time.sleep(20)

        ping_info_list = ping_obj.end_test_node_ping()

        ping_obj.thread_start_test_node_ping()
        fault_rec_obj = bonding_test.FaultRecovery(self.test_node_list, self.other_node_list)
        fault_rec_obj.interface_up()

        time.sleep(20)

        ping_info_list2 = ping_obj.end_test_node_ping()

    def test7(self):
        init_env_obj = bonding_test.EnvironmentalTesting(self.test_node_list, self.other_node_list)
        init_env_obj.initial_environment_check()

        ping_obj = bonding_test.Ping(self.test_node_list, self.other_node_list)
        ping_obj.thread_start_test_node_ping()

        fault_sim_obj = bonding_test.FaultSimulation(self.test_node_list, self.other_node_list)
        fault_sim_obj.network_cable_down()

        time.sleep(20)

        ping_info_list = ping_obj.end_test_node_ping()

        ping_obj.thread_start_test_node_ping()
        fault_rec_obj = bonding_test.FaultRecovery(self.test_node_list, self.other_node_list)
        fault_rec_obj.network_cable_up()

        time.sleep(20)

        ping_info_list2 = ping_obj.end_test_node_ping()

    def test8(self):
        init_env_obj = bonding_test.EnvironmentalTesting(self.test_node_list, self.other_node_list)
        init_env_obj.initial_environment_check()

        ping_obj = bonding_test.Ping(self.test_node_list, self.other_node_list)
        ping_obj.thread_start_test_node_ping()

        fault_sim_obj = bonding_test.FaultSimulation(self.test_node_list, self.other_node_list)
        fault_sim_obj.port_down()

        time.sleep(20)

        ping_info_list = ping_obj.end_test_node_ping()

        ping_obj.thread_start_test_node_ping()
        fault_rec_obj = bonding_test.FaultRecovery(self.test_node_list, self.other_node_list)
        fault_rec_obj.port_up()

        time.sleep(20)

        ping_info_list2 = ping_obj.end_test_node_ping()

def init():
    obj_yaml = utils.ConfFile('config.yaml')
    yaml_info_list = obj_yaml.read_yaml()

    test_node_ip_list = []
    test_node_passwd_list = []
    test_node_list = []
    other_node_ip_list = []
    other_node_passwd_list = []
    other_node_list = []

    for i in yaml_info_list["test_node"]:
        test_node_ip_list.append(i["ip"])
        test_node_passwd_list.append(i["password"])

    for i,z in zip(test_node_ip_list,test_node_passwd_list):
        obj = utils.SSHconn(host=i,password=z)
        test_node_list.append(obj)

    for i in yaml_info_list["other_node"]:
        other_node_ip_list.append(i["ip"])
        other_node_passwd_list.append(i["password"])

    for i,z in zip(other_node_ip_list,other_node_passwd_list):
        obj = utils.SSHconn(host=i,password=z)
        other_node_list.append(obj)

    return test_node_list, other_node_list

if __name__ == '__main__':
    cmd = Arg()
    cmd.parser_init()
    # test = Test()
    # test.test1()


