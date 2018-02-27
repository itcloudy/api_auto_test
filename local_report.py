#!/usr/bin/env python
# encoding: utf-8
"""
@project:auto_test_api
@author:cloudy
@site:
@file:local_report.py
@date:2017/10/16 11:39
"""
import os
from datetime import datetime

REPORT_HEAD_TMPL = """
<!DOCTYPE html>
<html>
<head>
	<title>API测试报告</title>
	<meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 引入 Bootstrap -->
    <link href="https://cdn.bootcss.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">
    <!-- HTML5 Shim 和 Respond.js 用于让 IE8 支持 HTML5元素和媒体查询 -->
    <!-- 注意： 如果通过 file://  引入 Respond.js 文件，则该文件无法起效果 -->
    <!--[if lt IE 9]>
     <script src="https://oss.maxcdn.com/libs/html5shiv/3.7.0/html5shiv.js"></script>
     <script src="https://oss.maxcdn.com/libs/respond.js/1.3.0/respond.min.js"></script>
    <![endif]-->
    <style type="text/css">
        .hidden-detail,.hidden-tr{
            display:none;
        }

    </style>
</head>
<body>

"""
REPORT_HEAD_INFO_TMPL = """
<div class="row">
    <div class="col-md-4 col-md-offset-4">
        <h1 class="text-center">测试报告</h1>

        <table  class="table table-hover table-condensed">
            <tbody>
                <tr>
                    <td>开始时间</td>
                    <td>%(start_time)s</td>
                </tr>
                <tr>
                    <td>结束时间</td>
                    <td>%(end_time)s</td>
                </tr>
                <tr>
                    <td>用例总数</td>
                    <td >%(all_count)s</td>
                </tr>
                <tr>
                    <td>成功数量</td>
                    <td>%(success_count)s</td>
                </tr>
                <tr>
                    <td>跳过数量</td>
                    <td>%(skip_count)s</td>
                </tr>
                <tr>
                    <td>失败数量</td>
                    <td style="color:red">%(failure_count)s</td>
                </tr>
                <tr>
                    <td>成功率</td>
                    <td style="color:red">%(success_percent)s%%</td>
                </tr>
            </tbody>
        </table>
    </div>
</div>
"""
REPORT_MAIN_TMPL = """
<div class="row" style="margin:20px">
    <div >
        <div class="btn-group" role="group" aria-label="...">
            <button type="button" id="check-all" class="btn btn-primary">所有用例</button>
            <button type="button" id="check-success" class="btn btn-success">成功用例</button>
            <button type="button" id="check-danger" class="btn btn-danger">失败用例</button>
            <button type="button" id="check-warning" class="btn btn-warning">跳过用例</button>
        </div>
        <div class="btn-group" role="group" aria-label="...">
            <button type="button" id="check-request" class="btn btn-primary">查看用例请求信息</button>
            <button type="button" id="hidden-request" class="btn btn-success">隐藏用例请求信息</button>
        </div>
        <table  class="table table-hover table-condensed table-bordered" style="word-wrap:break-word; word-break:break-all;">
            <thead>
                <tr>
                    <td>分类</td>
                    <td>功能模块</td>
                    <td>功能点</td>
                    <td>用例名称</td>
                    <td>有效</td>
                    <td>调试</td>
                    <td>地址</td>
                    <td>请求方法</td>
                    <td>数据位置</td>
                    <td>数据类型</td>
                    <td>检查点</td>
                    <td>检查内容</td>
                    <td  width="50%%">请求数据</td>
                    <td>结果</td>
                    <td>操作</td>
                </tr>
            </thead>
            <tbody>
            %(all_lines_str)s
            </tbody>
        </table>
    </div>
</div>
"""
REPORT_CASE_LINE_TMPL = """
<tr class="case-tr %(clazz)s">
    <td>%(category)s</td>
    <td>%(module)s</td>
    <td>%(function)s</td>
    <td>%(case_name)s</td>
    <td>%(active)s</td>
    <td>%(case_debug)s</td>
    <td>%(address)s</td>
    <td>%(request_method)s</td>
    <td>%(data_source)s</td>
    <td>%(data_type)s</td>
    <td>%(check_point)s</td>
    <td>%(check_content)s</td>
    <td  width="30%%">%(request_data)s</td>
    <td>%(result)s</td>
    <td>
        <button type="button"  class="btn btn-primary display-detail btn-sm">查看请求响应信息</button>
    </td>
</tr>
<tr class="request-info hidden-detail"><td>请求：</td><td colspan="14">%(req_data)s</td></tr>
<tr class="request-info hidden-detail"><td>响应：</td><td colspan="14">%(response_text)s</td></tr>


"""
REPORT_FOOTER_TMPL = """
<script src="https://code.jquery.com/jquery.js"></script>
<script src="https://cdn.bootcss.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
<script type="text/javascript">
    $(".display-detail").click(function(e){
        var currentBtn = e.currentTarget;
        var currentTr = currentBtn.parentNode.parentNode;
        if($(currentBtn).text()=="查看请求响应信息"){
            $(currentTr).next("tr").removeClass('hidden-detail');
            $(currentTr).next("tr").next("tr").removeClass('hidden-detail');
            $(currentBtn).text("隐藏请求响应信息");
        }else{
            $(currentTr).next("tr").addClass('hidden-detail');
            $(currentTr).next("tr").next("tr").addClass('hidden-detail');
            $(currentBtn).text("查看请求响应信息");
        };
	});

	$("#check-danger").click(function(e){
	    $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".request-info").addClass("hidden-detail");
	});
	$("#check-warning").click(function(e){
	    $(".case-tr").removeClass("hidden-tr");
        $(".success").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".request-info").addClass("hidden-detail");
	});
	$("#check-success").click(function(e){
	    $(".case-tr").removeClass("hidden-tr");
        $(".warning").addClass("hidden-tr");
        $(".danger").addClass("hidden-tr");
        $(".request-info").addClass("hidden-detail");
	});
	$("#check-all").click(function(e){
	    $(".case-tr").removeClass("hidden-tr");
	    $(".request-info").addClass("hidden-detail");
	});
	$("#check-request").click(function(e){
	    $(".case-tr").each(function(){
            if ($(this).hasClass("hidden-tr") == false){
                $(this).next("tr").removeClass('hidden-detail');
                $(this).next("tr").next("tr").removeClass('hidden-detail');
            }
        });
	});
	$("#hidden-request").click(function(e){
	    $(".request-info").addClass("hidden-detail");
	});
</script>
</body>
</html>
"""


class LocalReport(object):
    """
    生成本地报告
    """
    def __init__(self):

        self.report_path = os.path.join(os.getcwd() , "local_report")
        if not os.path.exists(self.report_path):
            os.makedirs(self.report_path)
        self.success_count = 0
        self.skip_count = 0
        self.failure_count = 0
        self.success_percent = 0
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.all_lines_trs = ""
        self.report_head_info = ""

    def gen_case_line(self, line={}):
        """
        根据用例明细生成html用例结果信息
        :param line:
        :return:
        """
        case_info = line.case_info
        if line.result == "success":
            self.success_count += 1
            clazz = "success"
        elif line.result == "skip":
            self.skip_count += 1
            clazz = "warning"
        else:
            self.failure_count += 1
            clazz = "danger"
        self.success_percent = self.success_count*100 / (self.success_count + self.failure_count + self.skip_count)
        response_text = line.response.text
        try:
            req_data = line.req_data.encode('utf-8').decode('unicode_escape')
        except:
            req_data = line.req_data
        self.all_lines_trs += REPORT_CASE_LINE_TMPL % dict(
            category=case_info.get('case_category', ""),
            module=case_info.get('case_module', ""),
            function=case_info.get('case_function', ""),
            address=case_info.get("case_address", ""),
            data_source=case_info.get("case_data_location"),
            data_type=case_info.get("case_data_type"),
            active=case_info.get("case_active", u"未知"),
            check_content=case_info.get("case_check_content", ""),
            check_point=case_info.get("case_check_point", ""),
            case_name=case_info.get('case_name', ""),
            case_debug=case_info.get("case_debug", u"未知"),
            request_method=case_info.get("case_method", u"未知"),
            request_data=case_info.get("case_request_data", ""),
            result=line.result,
            clazz=clazz,
            response_text=response_text,
            req_data=req_data,
        )

    def gen_case_lines(self, lines=[]):
        """
        根据用例明细生成html用例结果信息
        :param lines:
        :return:
        """
        for line in lines:
            self.all_lines_trs += REPORT_CASE_LINE_TMPL % dict(
                category=line.category,
                module=line.module,
                function=line.function,
                case_name=line.case_name,
                condition=line.condition,
                step=line.step,
                result=line.result,
            )
            if line.result == "success":
                self.success_count += 1
            elif line.result == "skip":
                self.skip_count += 1
            else:
                self.failure_count += 1

    def gen_report_info(self):
        """
        报告头部生成
        :return:
        """
        self.report_head_info = REPORT_HEAD_INFO_TMPL % dict(
            success_count=self.success_count,
            skip_count=self.skip_count,
            failure_count=self.failure_count,
            success_percent=self.success_percent,
            start_time=self.start_time,
            end_time=self.end_time,
            all_count=self.failure_count+self.success_count+self.skip_count
        )

    def save(self, file_name):
        """
        保存文件
        :return:
        """
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        report = os.path.join(self.report_path, file_name)
        print  report
        fp = open(report, "w")
        fp.write(REPORT_HEAD_TMPL)
        fp.write(self.report_head_info)
        fp.write(REPORT_MAIN_TMPL % dict(all_lines_str=self.all_lines_trs))
        fp.write(REPORT_FOOTER_TMPL)
        fp.close()






