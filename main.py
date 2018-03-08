#!/usr/bin/env python
# encoding: utf-8
"""
@project:auto_test_api
@author:cloudy
@site:
@file:main.py
@date:2017/9/10 16:28
"""
import requests
import json
import time
from datetime import datetime
from util import login
from local_case import LocalCase
from api_test import CaseRequest
from local_report import LocalReport
import remote_report_conf as report
from remote_report import create_test,create_test_line
from email_send import EmailReport
import sys
import yaml
import os
from test_user import test_user

access_token = ""
global access_token
access_token_list = {}


def main(auto_test=False):
    """
    接口测试启动函数
    :param auto_test:
    :return:
    """
    # 接口测试配置文件
    config_path = os.path.join(os.getcwd(), "config.yml")
    config_file = open(config_path)
    config_yml = yaml.load(config_file)
    config_file.close()
    # 获得基本配置信息
    base_config = config_yml["base"]
    # 获得邮件信息
    email_config = config_yml["email"]
    # 从本地获得用例信息
    case_list = LocalCase().get_case_list()

    # 统计
    failure_count = 0
    skip_count = 0
    success_count = 0
    username = base_config.get("username", "")
    if not username:
        sys.exit(-1)
    # 登录,登录失败将不继续测试
    access_token = login(base_config)
    access_token_list[username] = access_token
    if not access_token:
        # session 为None说明登录失败，用例不继续
        sys.exit(-1)
    local_report_obj = LocalReport()
    # 循环所有测试用例，判断是需要进行测试
    for case_info in case_list:
        # python main.py  [option] 若存在option，则为自动化测试，不存在debug模式
        if not auto_test:
            if not case_info.get("case_debug", "false") == "true":
                skip_count += 1
                continue
        # 获得测试用例中的用户信息(支持多用户测试)
        case_user = case_info.get("case_user", "")
        if not case_user:
            continue
        base_config['username'] = case_user
        # 测试用例对应的用户密码
        base_config['password'] = test_user[case_user]
        # 登录成功，获得用户的token
        access_token_list[case_user] = login(base_config)
        # 测试用例信息给测试请求对象，base_config中包含全局参数，用户请求参数加密，可根据实际情况决定是否需要
        case = CaseRequest(case_info, base_config)

        case.run(access_token_list[case_user])
        local_report_obj.gen_case_line(case)
        if case.result == "success":
            success_count += 1
        elif case.result == "failed":
            failure_count += 1
        elif case.result == "skip":
            skip_count += 1

    total_info = {
        'failure_count': failure_count,
        'skip_count': skip_count,
        'success_count': success_count
    }

    local_report_obj.gen_report_info()
    file_name = "%s" % datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    local_report_obj.save(file_name+".html")
    if auto_test:
        EmailReport(email_config).send_report(total_info, file_name)

    # else:
    #     # 登录,登录失败将不继续测试
    #     access_token = login()
    #     if not access_token:
    #         # session 为None说明登录失败，用例不继续
    #         sys.exit(-1)
    #     try:
    #         session = requests.Session()
    #         response = session.post(report.login_url, json.dumps({'username': report.username,
    #                                                               "password": report.password}))
    #         if response.status_code == 200:
    #             start_time = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    #             end_time = start_time
    #             ok, test_id = create_test(report.server_url, session, report.project_name, report.project_name,
    #                                       start_time, end_time, report.system, report.system_version, report.version)
    #             if ok:
    #                 failure_count = 0
    #                 error_count = 0
    #                 skip_count = 0
    #                 success_count = 0
    #                 for case_info in case_list:
    #                     case = CaseRequest(case_info, base_config)
    #                     case.run(access_token)
    #                     create_test_line(test_id, case, session, report.server_url)
    #                     if case.result == 'success':
    #                         success_count += 1
    #                     elif case.result == "failed":
    #                         failure_count += 1
    #                 end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    #                 data = json.dumps({
    #                     "ID": test_id,
    #                     "SuccessCount": success_count,
    #                     "FailureCount": failure_count,
    #                     "ErrorCount": error_count,
    #                     "SkipCount": skip_count,
    #                     "EndTime": end_time
    #                 })
    #                 response = session.put("%s%s%s" % (report.server_url, "test/", test_id), data)
    #     except Exception, e:
    #         print e

if __name__ == "__main__":
    #  参数为任意值，若带参数则执行测是所用用例的自动化测试，若不带参数则执行单个测试用例(xml中的case_debug为true的用例)
    argv_len = len(sys.argv)
    auto_test = False
    if argv_len > 1:
        auto_test = True
    main(auto_test)
