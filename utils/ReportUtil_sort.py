#! /usr/bin/python3
# -*- coding: utf8 -*-

# 生成详细报告模板
class ReportUtil_sort():
    TOP_TMPL = """<?xml version="1.0" encoding="UTF-8"?>
        <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head>
        <title>搜索效果测试报告</title>
        <meta http-equiv="Content-Type" content="charset=UTF-8"/>
        <link href="http://libs.baidu.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">
        <style type="text/css" media="screen">
        body { font-family: Microsoft YaHei,Tahoma,arial,helvetica,sans-serif;padding: 20px}
        /* -- heading ---------------------------------------------------------------------- */
            .heading {
                margin-top: 0ex;
                margin-bottom: 1ex;
            }
            .heading .description {
                margin-top: 4ex;
                margin-bottom: 6ex;
            }
        </style>
        </head>
        <body >
        <div class='heading'>
        <h3 style="font-family: Microsoft YaHei" align=center>搜索效果详细测试报告</h3>
        <p class='attribute'><strong>测试人员 : </strong> 测试机器人</p>
        <p class='attribute'><strong>开始时间 : </strong> %(starttime)s</p>
        <p class='attribute'><strong>合计耗时 : </strong> %(duration)s</p>

    <table id='result_table' class="table table-condensed table-bordered table-hover">
    <tr id='header_row' class="text-center success" style="font-weight: bold;font-size: 14px;">
        <td>ID</td>
        <td>搜索词</td>
        <td>排序类型</td>
        <td>排序测试结果</td>
        <td>详细信息</td>
    </tr>
    """
    TR_TMPL = r"""
        <tr class='passClass warning'>
        <td style="vertical-align:middle; text-align:center">%(id)s</td>
        <td style="vertical-align:middle; text-align:center"; width="300px">%(kw)s</td>
        <td style="vertical-align:middle; text-align:center">%(sort_type)s</td>
        <td style="vertical-align:middle; text-align:center"><img width="20" height="20" src="../img/%(sort_result)s.jpg"></td>
        <td style="vertical-align:middle; text-align:center">%(detail)s</td>
        </tr>
        """
    BOTTOM_TMPL = r"""
        </table>
        <div id='ending'>&nbsp;</div>
        <div style=" position:fixed;right:50px; bottom:30px; width:20px; height:20px;cursor:pointer">
        <a href="#"><span class="glyphicon glyphicon-eject" style = "font-size:30px;" aria-hidden="true">
        </span></a></div>
        </body>
        </html>
        """

    def generateReport(self, StartTime, Duration, searchresults):
        starttime = StartTime.replace(" ", "-").replace(":", "_")
        ENCODE_UTF = "utf-"

        top = self.TOP_TMPL % dict(starttime=StartTime, duration=Duration)

        tr = ""
        search_id = 0
        for searchresult in searchresults:
            search_id += 1
            keyword = searchresult.getKeyword()
            sort_type = searchresult.get_sort_type()
            sort_result = searchresult.get_sort_result()
            detail = searchresult.get_sort_result_detail()
            tr += self.TR_TMPL % dict(id=search_id, kw=keyword, sort_type=sort_type, sort_result=sort_result, detail=detail)

        bottom = self.BOTTOM_TMPL
        with open("reports\\detailed_" + starttime + ".html", 'wb') as f:
            f.write(top.encode(ENCODE_UTF))
            f.write(tr.encode(ENCODE_UTF))
            f.write(bottom.encode(ENCODE_UTF))