#!/usr/bin/env python
# encoding: utf-8
"""
@project:auto_test_api
@author:cloudy
@site:
@file:local_case.py
@date:2017/9/25 15:54
"""
import xlrd
import os
from xml.dom.minidom import parse
import xml.dom.minidom


class LocalCase(object):
    """本地获得测试用例信息"""

    @staticmethod
    def get_all_excel_file():
        """
        获得所有的excel文件
        :return:
        """
        file_list = []
        all_cases = []
        case_dir = os.path.join(os.getcwd(), "test_case")
        case_excel = os.path.join(case_dir, "excel")
        for root, dirs, files in os.walk(case_excel):
            for fp_st in files:
                if fp_st.endswith(".xlsx"):
                    file_list.append(os.path.join(case_excel,fp_st))
        for fp_name in file_list:
            case_file = xlrd.open_workbook(filename=fp_name)
            sheet = case_file.sheet_by_index(0)
            title_line = sheet.row_values(0)
            titles = []
            for v in title_line:
                titles.append(v.strip())
            for line in range(1, sheet.nrows):
                all_cases.append(dict(zip(titles, sheet.row_values(line))))
        return all_cases

    @staticmethod
    def get_all_xml_file():
        """
        获得所有的xml文件
        :return:
        """
        file_list = []
        all_cases = []
        case_dir = os.path.join(os.getcwd(), "test_case")
        case_xml = os.path.join(case_dir, "xml")
        for root, dirs, files in os.walk(case_xml):
            for fp_st in files:
                if fp_st.endswith(".xml"):
                    file_list.append(os.path.join(case_xml, fp_st))
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

    def get_case_list(self,case_types="xml"):
        """获得所有的测试用例信息"""
        all_cases = []
        if case_types:
            case_type_list = case_types.split(",")
            for case_type in case_type_list:
                if "xml" == case_type:
                    all_cases += self.get_all_xml_file()
                elif "excel" == case_type:
                    all_cases += self.get_all_excel_file()
                elif "yml" == case_type:
                    all_cases += self.get_all_yml_file()
        return all_cases

