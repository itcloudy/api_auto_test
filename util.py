#!/usr/bin/env python
# encoding: utf-8
"""
@project:auto_test_api
@author:cloudy
@site:
@file:util.py
@date:2017/9/25 17:02
"""
import ConfigParser
import os
import requests
import urllib
import json
import base64
import hashlib



def login(base_config):
    """
    返回登录后的
    :return:
    """
    username = base_config.get("username")
    password = base_config.get("password")
    base_url = base_config.get("base_url")
    company_id = base_config.get("company_id")
    app_id = base_config.get("app_id")
    app_secret = base_config.get("app_secret")
    login_url = base_url + "/" + base_config.get("login_url")
    username = username.strip()
    password = password.strip()
    login_values = {'accountName': username, "password": password, "companyId": company_id}

    login_values = get_sign_key(login_values, "POST", login_url, "", app_id, app_secret)
    headers = {'content-type': 'application/json'}
    response = requests.post(login_url, data=json.dumps(login_values), headers=headers)

    if response.status_code == 200:
        response_data = json.loads(response.text)
        print response.text
        access_token = response_data["data"]['token']["accessToken"]
        return access_token
    else:
        print "login failed code: {} , response text: {}".format(response.status_code, response.text)
        print "login_values: {}".format(login_values)
        return ""


def get_sign_key(data={}, method="GET", url="", access_token="", app_id="", app_secret=""):
    """

    :param data: 请求数据
    :param method: 请求方法
    :param url:请求地址
    :param access_token: token
    :param app_id:  app id
    :param app_secret:  app secret
    :return:
    """
    if access_token:
        data["accessToken"] = access_token
    data["appId"] = app_id
    keys = data.keys()
    keys.sort()
    string = "%s%s" % (method, url)
    data_el_str = ""
    for key in keys:
        if isinstance(data[key], list):
            for item in data[key]:
                data_el_str += "&{0}={1}".format(key, item)
        elif isinstance(data[key], dict):
            data_el_str += "&{0}={1}".format(key, json.dumps(data[key]))
        else:
            data_el_str += "&{0}={1}".format(key, data[key])
    string += data_el_str
    string += "&%s" % app_secret
    print string
    string_base64 = base64.b64encode(string)
    m = hashlib.md5()
    m.update(string_base64)
    data["signKey"] = m.hexdigest()

    return data
    


