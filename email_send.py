#!/usr/bin/env python
# encoding: utf-8
"""
@project:artist_api_test
@author:cloudy
@site:
@file:email_send.py
@date:2018/1/22 17:24
@description：邮件发送
"""
import yaml
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailReport(object):
    """
    邮件发送
    """
    def __init__(self, email_config):

        self.email_host = email_config.get("host")
        self.email_user = email_config.get("user")
        self.email_passwd = email_config.get("passwd")
        self.email_receivers = email_config.get("receivers")

    def send_report(self, total_info, file_name):
        """
        发送邮件
        :param report_file:
        :return:
        """
        if not self.email_receivers:
            print "没有邮件接收列表，忽略邮件发送"
            return
        # 创建一个带附件的实例
        msg = MIMEMultipart("related")
        # 添加邮件主体内容
        msg_body = MIMEText("""
        <font color=red>Artist接口自动化测试结果({})</font>
        <table >
            <thead>
                <tr><td>用例总数</td><td>{}</td><tr>
            </thead>
            <tbody>
                <tr><td>成功用例</td><td>{}</td></tr>
                <tr><td>失败用例</td><td>{}</td></tr>
                <tr><td>跳过用例</td><td>{}</td></tr>
            </tbody>
        </table>
        """.format(file_name, sum([total_info['success_count'], total_info['failure_count'], total_info['skip_count']]),total_info['success_count'], total_info['failure_count'], total_info['skip_count']), "html", "utf-8")
        msg.attach(msg_body)
        # 构造附件
        attach = MIMEText(open(os.path.join(os.getcwd(), "local_report", "{}.html".format(file_name)), 'rb').read(), 'base64', 'gb2312')
        attach["Content-Type"] = 'application/octet-stream'
        attach["Content-Disposition"] = 'attachment; filename="{}.html"'.format(file_name)
        msg.attach(attach)

        # 加邮件头
        msg['to'] = ";".join(self.email_receivers)
        msg['from'] = self.email_user
        msg['subject'] = u'Artist接口自动化测试报告({})'.format(file_name)
        # 发送邮件
        try:
            smtpObj = smtplib.SMTP_SSL(self.email_host, 465)
            smtpObj.login(self.email_user, self.email_passwd)
            msg_str = msg.as_string()
            smtpObj.sendmail(self.email_user, self.email_receivers, msg_str)
            smtpObj.quit()
            print u"邮件发送成功"
        except smtplib.SMTPException, e:
            print e


