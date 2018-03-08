#!/usr/bin/env python
# encoding: utf-8
"""
@project:auto_test_api
@author:cloudy
@site:
@file:local_case.py
@date:2017/9/25 15:54
"""
import os
from xml.dom.minidom import parse
import xml.dom.minidom


class LocalCase(object):
    """本地获得测试用例信息"""

    @staticmethod
    def get_all_xml_file():
        """
        获得所有的xml文件
        :return:
        """
        file_list = []
        all_cases = []
        # 获得测试用例文件路径
        case_dir = os.path.join(os.getcwd(), "test_case")
        # 获得xml测试用例路径
        case_xml = os.path.join(case_dir, "xml")
        # 获得xml文件夹下的所有xml文件，并解析其中的测试用例信息
        for root, dirs, files in os.walk(case_xml):
            for fp_st in files:
                if fp_st.endswith(".xml"):
                    file_list.append(os.path.join(case_xml, fp_st))
        # 循环所有xml文件，解析其中的测试用例信息
        for file_xml in file_list:
            tree = xml.dom.minidom.parse(file_xml)
            data = tree.documentElement
            case_apis = data.getElementsByTagName("case_api")
            for case_api in case_apis:
                case_name = case_api.getElementsByTagName("case_name")[0].childNodes[0].data
                case_category = case_api.getElementsByTagName("case_category")[0].childNodes[0].data
                case_module = case_api.getElementsByTagName("case_module")[0].childNodes[0].data
                case_function = case_api.getElementsByTagName("case_function")[0].childNodes[0].data
                case_active = case_api.getElementsByTagName("case_active")[0].childNodes[0].data
                case_debug = case_api.getElementsByTagName("case_debug")[0].childNodes[0].data
                case_address = case_api.getElementsByTagName("case_address")[0].childNodes[0].data
                case_data_location = case_api.getElementsByTagName("case_data_location")[0].childNodes[0].data
                case_method = case_api.getElementsByTagName("case_method")[0].childNodes[0].data
                case_data_type = case_api.getElementsByTagName("case_data_type")[0].childNodes[0].data
                case_check_point = case_api.getElementsByTagName("case_check_point")[0].childNodes[0].data
                case_check_content = case_api.getElementsByTagName("case_check_content")[0].childNodes[0].data
                case_request_data = case_api.getElementsByTagName("case_request_data")[0].childNodes[0].data
                case_comment = case_api.getElementsByTagName("case_comment")[0].childNodes[0].data
                case_user = case_api.getElementsByTagName("case_user")[0].childNodes[0].data

                all_cases.append({
                    'case_name': case_name,
                    'case_category': case_category,
                    'case_module': case_module,
                    'case_function': case_function,
                    'case_active': case_active,
                    'case_address': case_address,
                    'case_data_location': case_data_location,
                    'case_method': case_method,
                    'case_data_type': case_data_type,
                    'case_check_point': case_check_point,
                    'case_check_content': case_check_content,
                    'case_request_data': case_request_data,
                    'case_comment': case_comment,
                    'case_debug': case_debug,
                    "case_user": case_user,
                })
        return all_cases

    def get_case_list(self):
        """获得所有的测试用例信息"""
        all_cases = self.get_all_xml_file()
        return all_cases

