# -*- coding:utf-8 -*-
import unittest
from Common.com_func import log
from Config import global_var as gv
from Tools.mongodb import MongodbUtils
from Env import env_config as cfg
from Common.test_func import mongo_exception_send_DD
from TestBase.app_action import get_driver, get_desired_caps


class ParaCase(unittest.TestCase):

    def __init__(self, pro_name, test_method="test_", connected_android_device_list=[]):
        """
        【 用 例 对 象 初 始 化 】
        :param pro_name :
        :param test_method : 这个参数必须是测试类中存在的以'test_'开头的方法
        :param connected_android_device_list : 已连接设备信息列表
        """
        super(ParaCase, self).__init__(test_method)
        self.log = log
        self.pro_name = pro_name
        self.test_method = test_method
        self.connected_android_device_list = connected_android_device_list
        self.screen_shot_id_list = []  # 截图ID列表
        self.screen_shot_id_list_name = self.__class__.__name__ + "." + test_method  # 截图ID列表名称
        self.class_method_path = self.__class__.__name__ + "/" + test_method + "/"  # 获取当前的'类名/方法名/'(提供截屏路径)
        self.current_thread_name_index = 0  # 记录当前线程名的索引（目的：不同线程使用不同的登录账号）

    def setUp(self):
        """
        【 每个用例对象执行前，需要进行如下配置 】
        :return:
        """
        from Config.pro_config import get_login_accout
        # 通过线程名的索引 获取登录账号
        self.user, self.passwd = get_login_accout(self.current_thread_name_index)

        # 通过线程名的索引和项目名称 获取启动设备信息(指定设备，指定应用)
        self.desired_caps, self.device_name = get_desired_caps(self.pro_name, self.current_thread_name_index,
                                                               self.connected_android_device_list)
        # 启动设备中的应用
        self.driver = get_driver(pro_name=self.pro_name, desired_caps=self.desired_caps, device_name=self.device_name)

        # 隐式等待时间
        self.driver.implicitly_wait(gv.IMPLICITY_WAIT)

    def tearDown(self):
        """
        【 每个用例对象执行后，需要进行如下配置 】
        :return:
        """
        # 关闭应用
        self.driver.quit()

    @staticmethod
    def get_online_case_to_suite(pro_name, connected_android_device_list=[]):
        """
        将'测试类'列表中的'上线'的'测试方法'添加入 suite 实例对象中
        :param pro_name:
        :param connected_android_device_list: 已连接设备信息列表
        [ { "thread_index": 1, "device_name": "小米5S", "platform_version": "7.0", "device_udid": "192.168.31.136:5555" } } ,
          { "thread_index": 2, "device_name": "坚果Pro", "platform_version": "7.1.1", "device_udid": "15a6c95a" } } ]
        :return:
        【 添 加 步 骤 】
        1.从mongo中获取'上线'状态的'测试用例'列表
        2.重置 上线用例的'运行状态：pending、开始时间：----、运行时间：----'
        3.通过'项目名称'获取'测试类'列表
        4.循环获取'测试类'列表中的所有'测试方法名称'
        5.将这些'测试方法名称'与mongo中'上线'的'测试方法名称'作比较
        6.匹配成功的，则实例化'测试类'时，并添加入'suite'实例对象中
        【 备 注 】
          实例化'测试类'时，必须带上该类中存在的以'test_'开头的方法名
        """
        with MongodbUtils(ip=cfg.MONGODB_ADDR, database=cfg.MONGODB_DATABASE, collection=pro_name) as pro_db:
            try:
                # 获取上线用例列表
                query_dict = {"case_status": True}
                results = pro_db.find(query_dict, {"_id": 0})
                on_line_test_method_name_list = [result.get("test_method_name") for result in results]
                # 重置 上线用例的'运行状态：pending、开始时间：----、运行时间：----'
                update_dict = {"$set": {"run_status": "pending", "start_time": "----", "run_time": "----"}}
                pro_db.update(query_dict, update_dict, multi=True)
            except Exception as e:
                on_line_test_method_name_list = []
                mongo_exception_send_DD(e=e, msg="获取'" + pro_name + "'项目'上线'测试用例数据")
                return "mongo error", on_line_test_method_name_list

        from Config.pro_config import get_test_class_list
        test_class_list = get_test_class_list(pro_name)
        test_loader = unittest.TestLoader()
        suite = unittest.TestSuite()
        for test_class in test_class_list:
            test_methods_name = test_loader.getTestCaseNames(test_class)
            for test_method_name in test_methods_name:
                if test_method_name in on_line_test_method_name_list:  # 匹配'测试方法'名称
                    test_instance = test_class(pro_name=pro_name, test_method=test_method_name,
                                               connected_android_device_list=connected_android_device_list)
                    suite.addTest(test_instance)
        return suite, on_line_test_method_name_list

