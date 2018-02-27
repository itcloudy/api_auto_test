#!/usr/bin/env python
# encoding: utf-8
"""
@project:appium_test
@author:cloudy
@site:
@file:result_operation.py
@date:2017/8/25 16:44
"""
import unittest
import requests
import json
import time
import StringIO
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def create_test(base_url, session, project_name, test_name, start_time, end_time, system, system_version, version):
    """
    创建测试
    :param base_url: 测试上报基地址
    :param session: request session
    :param project_name: 项目名称
    :param test_name: 测试名称
    :param start_time: 开始时间
    :param end_time: 结束时间
    :param system: 系统
    :param system_version:系统版本
    :param version: 被测版本
    :return:
    """
    test_url = base_url + "test"
    data = json.dumps({
        "Name": test_name,
        "StartTime": start_time,
        "EndTime": end_time,
        "ProjectName": project_name,
        "System": system,
        "SystemVersion": system_version,
        "Version": version,
        "SuccessCount": 0,
        "FailureCount": 0,
        "ErrorCount": 0,
        "SkipCount": 0
    })
    response = session.post(test_url, data)
    # 查看返回信息，debug时使用，或者查看错误
    if response.status_code == 200:
        data = json.loads(response.text)
        if data['code'] == 'success':
            return True, data['test']

    return False, 0


def create_test_line(test, case, session, base_url):
    """

    :param test:上报测试id
    :param case:测试对象
    :param session:请求session
    :param base_url:请求地址
    :return:
    """
    if not (test and case and session):
        return
    data = {
        "Category": case.case_info.get("case_category", ""),
        "Module": case.case_info.get("case_module", ""),
        "Function": case.case_info.get("case_function", ""),
        "Name": case.case_info.get("case_name", ""),
        "ResultInfo": (case.response and case.response.text) or "",
        "Result": case.result,
        "Test": test

    }
    upload_case_info(base_url, session, data)


def upload_case_info(base_url, session, data={}):
    """
    上报测试用例信息
    :param base_url:
    :param session:
    :param data:
    :return:
    """
    server_url = base_url + "test/line"
    session.post(server_url, json.dumps(data))
