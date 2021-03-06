# -*- coding: utf-8 -*-
from Api import *
from flask import render_template, request
import json
from Config.error_mapping import *
from Api.api_services.api_template import interface_template
from Api.api_services.api_calculate import *
from Common.com_func import is_null
from Common.test_func import is_exist_start_case, is_exist_online_case
from Tools.mongodb import MongoGridFS
from Env import env_config as cfg

"""
api 服务接口
"""


# http://127.0.0.1:8070/api_local/WEB/index
@flask_app.route("/WEB/index", methods=["GET"])
def show_index():
    result_dict = dict()
    result_dict["nginx_api_proxy"] = cfg.NGINX_API_PROXY
    result_dict["api_addr"] = cfg.API_ADDR
    return render_template('index.html', tasks=result_dict)


# http://127.0.0.1:8070/api_local/WEB/get_project_case_list/pro_demo_1
@flask_app.route("/WEB/get_project_case_list/<pro_name>", methods=["GET"])
def get_test_case_list(pro_name):
    result_dict = dict()
    result_dict["nginx_api_proxy"] = cfg.NGINX_API_PROXY
    result_dict["pro_name"] = pro_name
    result_dict["test_case_list"] = get_test_case(pro_name)
    result_dict["current_report_url"] = cfg.BASE_REPORT_PATH + pro_name + "/[WEB_report]" + pro_name + ".html"
    result_dict["history_report_path"] = cfg.BASE_REPORT_PATH + pro_name + "/history/"
    result_dict["is_run"] = is_exist_start_case(pro_name)
    result_dict["progress_info"] = get_progress_info(pro_name)
    return render_template('project.html', tasks=result_dict)


# http://127.0.0.1:8070/api_local/WEB/get_img/5e61152ff0dd77751382563f
@flask_app.route("/WEB/get_img/<file_id>", methods=["GET"])
def get_screenshot_img(file_id):
    """
    获取截屏图片
    :param file_id:
    :return: 1.获取成功、2.找不到该文件、3.mongo连接不上
    """
    if is_null(file_id):
        msg = PARAMS_NOT_NONE
        img_base64 = ""
    else:
        mgf = MongoGridFS()
        img_base64 = mgf.get_base64_by_id(file_id)
        if is_null(img_base64):
            msg = MONGO_CONNECT_FAIL
        elif img_base64 == "no such file":
            msg = NO_SUCH_FILE
        else:
            msg = REQUEST_SUCCESS
            # response = make_response(img_base64)
            # response.headers.set('Content-Type', 'image/png')
            # return response
    re_dict = interface_template(msg, {"file_id": file_id, "img_base64": img_base64})
    return json.dumps(re_dict, ensure_ascii=False)



# http://127.0.0.1:8070/api_local/WEB/set_case_status/pro_demo_1/test_02
@flask_app.route("/WEB/set_case_status/<pro_name>/<test_method_name>", methods=["GET"])
def set_case_status(pro_name, test_method_name):
    """
    设置某个'测试用例'的'状态'(上下线)
    :param pro_name:
    :param test_method_name:
    :return:
    """
    new_case_status = None
    if is_null(pro_name) or is_null(test_method_name):
        msg = PARAMS_NOT_NONE
    else:
        new_case_status = update_case_status(pro_name, test_method_name)
        msg = new_case_status == "mongo error" and MONGO_CONNECT_FAIL or UPDATE_SUCCESS
    re_dict = interface_template(msg, {"pro_name": pro_name, "test_method_name": test_method_name,
                                       "new_case_status": new_case_status})
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/set_case_status_all/pro_demo_1/false
@flask_app.route("/WEB/set_case_status_all/<pro_name>/<case_status>", methods=["GET"])
def set_case_status_all(pro_name, case_status):
    """
    设置整个项目的'测试用例'的'状态'(上下线)
    :param pro_name:
    :param case_status:
    :return:
    """
    test_method_name_list = []
    if is_null(pro_name) or is_null(case_status):
        msg = PARAMS_NOT_NONE
    else:
        if case_status in [True, False, "false", "FALSE", "TRUE", "true"]:
            case_status = case_status in [True, "TRUE", "true"] and True or False
            res = update_case_status_all(pro_name, case_status)
            if res == "mongo error":
                msg = MONGO_CONNECT_FAIL
            else:
                msg = UPDATE_SUCCESS
                test_method_name_list = res
        else:
            msg = REQUEST_ARGS_WRONG
    re_dict = interface_template(msg, {"pro_name": pro_name, "case_status": case_status,
                                       "test_method_name_list": test_method_name_list})
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/stop_run_status/pro_demo_1
@flask_app.route("/WEB/stop_run_status/<pro_name>", methods=["GET"])
def stop_run_status(pro_name):
    """
    强行修改用例运行状态 -> 停止
    :param pro_name:
    :return:
    """
    if is_null(pro_name):
        msg = PARAMS_NOT_NONE
    else:
        insert_result = stop_case_run_status(pro_name)
        if insert_result == "mongo error":
            msg = MONGO_CONNECT_FAIL
        else:
            msg = STOP_SUCCESS
    re_dict = interface_template(msg, {"pro_name": pro_name})
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/refresh_run_progress/pro_demo_1
@flask_app.route("/WEB/refresh_run_progress/<pro_name>", methods=["GET"])
def refresh_run_progress(pro_name):
    """
    刷新执行用例进度
    :param pro_name:
    :return:
    """
    if is_null(pro_name):
        msg = PARAMS_NOT_NONE
    else:
        progress_info = get_progress_info(pro_name)
        if progress_info == "mongo error":
            msg = MONGO_CONNECT_FAIL
        else:
            msg = REQUEST_SUCCESS
    re_dict = interface_template(msg, {"pro_name": pro_name, "progress_info": progress_info})
    return json.dumps(re_dict, ensure_ascii=False)


# http://127.0.0.1:8070/api_local/WEB/refresh_case_run_status/pro_demo_1
@flask_app.route("/WEB/refresh_case_run_status/<pro_name>", methods=["GET"])
def refresh_case_run_status(pro_name):
    """
    刷新用例运行状态
    :param pro_name:
    :return:
    """
    if is_null(pro_name):
        msg = PARAMS_NOT_NONE
    else:
        case_run_status_list = get_case_run_status(pro_name)
        if case_run_status_list == "mongo error":
            msg = MONGO_CONNECT_FAIL
        else:
            msg = REQUEST_SUCCESS
    re_dict = interface_template(msg, {"pro_name": pro_name, "case_run_status_list": case_run_status_list})
    return json.dumps(re_dict, ensure_ascii=False)

