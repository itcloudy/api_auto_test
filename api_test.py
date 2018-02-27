#!/usr/bin/env python
# encoding: utf-8
"""
@project:auto_test_api
@author:cloudy
@site:
@file:api_test.py
@date:2017/9/25 16:52
"""
from util import get_sign_key
import json
import os
import urllib
import requests


class CaseRequest(object):
    """
    api请求和结果判断
    """
    def __init__(self, case_info={}, base_config={}):
        """
        :param case_info: 用例信息
        :param session: request session
        """

        self.case_info = case_info
        self.base_config = base_config
        self.base_url = self.base_config.get("base_url")
        self.response = None
        self.get_sign_key = get_sign_key
        self.result = "failed"
        self.req_data = ''
        self.app_id = self.base_config.get("app_id")
        self.app_secret = self.base_config.get("app_secret")

    def request(self, access_token=""):
        """
        发送请求
        :return: response
        """

        if not self.case_info.get("case_active", True):
            return False, {}
        address = self.case_info.get('case_address', "")
        method = self.case_info.get('case_method', "POST")
        data_type = self.case_info.get("case_data_type", "Form")
        self.check_point = self.case_info.get("case_check_point", u"包含")
        self.check_msg = self.case_info.get("case_check_content", '')

        self.data_location = self.case_info.get("case_data_location", u"本地")
        request_data = self.case_info.get("case_request_data", "")
        headers = {}
        headers["User-Agent"] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36"
        # 表单数据
        if data_type == "Form":
            # 数据来源为文件的话，读取文件的内容
            if self.data_location == u"文件":
                data_dir = os.path.join(os.getcwd(), "test_data")
                data_file = os.path.join(data_dir,  request_data)
                fopen = open(data_file, encoding="utf-8")
                lines = fopen.readlines()
                request_data = ""
                for line in lines:
                    request_data += line
                request_data.replace("\n", "", 0)

            request_data = json.loads(request_data)
            print self.case_info.get('case_name', ""), " 请求数据： {}".format(request_data)
            headers['Content-Type'] = 'application/json;charset=UTF-8'
        elif data_type == "Data":
            data_dir = os.path.join(os.getcwd(), "test_data")
            data_file = os.path.join(data_dir, request_data)
            fopen = open(data_file, encoding="utf-8")
            lines = fopen.readlines()
            request_data = ""
            for line in lines:
                request_data += line
            request_data.replace("\n", "", 0)
            request_data = request_data.encode("utf-8")
            headers['Content-Type'] = 'text/plain; charset=UTF-8'
        elif data_type == "File":
            data_dir = os.path.join(os.getcwd(), "test_media")
            data_file = os.path.join(data_dir, request_data)
            fopen = open(data_file, 'rb')
            data = fopen.read()
            fopen.close()
            request_data = '''
            ------WebKitFormBoundaryDf9uRfwb8uzv1eNe
            Content-Disposition:form-data;name="file";filename="%s"
            Content-Type:
            Content-Transfer-Encoding:binary

            %s
            ------WebKitFormBoundaryDf9uRfwb8uzv1eNe--
                ''' % (os.path.basename(data_file), data)
            headers['Content-Type'] = 'multipart/form-data;boundary=----WebKitFormBoundaryDf9uRfwb8uzv1eNe;charset=UTF-8'
        print "request address: ", self.base_url+address
        if method.upper() == "POST":

            data = json.dumps(self.get_sign_key(request_data,"POST",address,access_token,self.app_id,self.app_secret))
            self.response = requests.post(self.base_url+address, data=data,headers=headers)
            self.req_data = data
        elif method.upper() == "GET":
            data = json.dumps(self.get_sign_key(request_data,"GET",address,access_token,self.app_id,self.app_secret))
            self.response = requests.get(self.base_url+address, data=data,headers=headers)
            self.req_data = data
        elif method.upper() == "PUT":
            data = json.dumps(self.get_sign_key(request_data, "PUT", address, access_token,self.app_id,self.app_secret))
            self.response = requests.put(self.base_url + address, data=data, headers=headers)
            self.req_data = data
        elif method.upper() == "DELETE":
            data = json.dumps(self.get_sign_key(request_data, "DELETE", address, access_token,self.app_id,self.app_secret))
            self.response = requests.delete(self.base_url + address, data=data, headers=headers)
            self.req_data = data

    def run(self, access_token=""):
        """
        返回测试结果
        :return: Ture/False
        """
        self.request(access_token)
        print "response code: ", self.response or self.response.status_code, "text: ", self.response.text
        if self.response and self.response.status_code:
            status_code = self.response.status_code
            response_text = self.response.text
            if status_code == 200:
                if self.check_point == u"包含":
                    if response_text.find(self.check_msg) >= 0:
                        self.result = "success"
                elif self.check_point == u"等于":
                    if response_text == self.check_msg:
                        self.result = "success"




