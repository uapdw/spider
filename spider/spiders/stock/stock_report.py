# # -*- coding: utf-8 -*-
#
# import re
# import json
#
# from scrapy import Spider
#
# from spider.items import StockReportItem
# from spider.loader.processors import DateProcessor
#
#
# class StockYearReportSpider(Spider):
#
#     name = "stockreport"
#     allowed_domains = ['cninfo.com.cn']
#
#     start_urls = [
#         'http://www.cninfo.com.cn/disclosure/annualreport/plate/shmbar.js',
#         'http://www.cninfo.com.cn/disclosure/seannualreport/plate/shmbsar.js',
#         'http://www.cninfo.com.cn/disclosure/1qreport/plate/shmbq1.js',
#         'http://www.cninfo.com.cn/disclosure/3qreport/plate/shmbq3.js'
#     ]
#
#     process_date = DateProcessor('%Y-%m-%d %H:%M')
#
#     def parse(self, response):
#         html = response.body.decode('gbk')
#         m = re.match('.*?(\[\[.*\]\]);.*', html, re.DOTALL)
#         json_str = m.group(1)
#
#         report_list = json.loads(json_str)
#         for index, report in enumerate(report_list):
#             i = StockReportItem()
#             i['stock_code'] = report[0]
#             i['publish_time'] = StockYearReportSpider.process_date(report[6])
#             i['report_name'] = report[2]
#             i['file_urls'] = [{
#                 'file_url': 'http://www.cninfo.com.cn/' + report[1],
#                 'file_name': i['stock_code'] + '_' + i['report_name'] + '.pdf'
#             }]
#             yield i
