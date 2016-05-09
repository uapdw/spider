# # -*- coding: utf-8 -*-
# import re
# from scrapy.http import Request
# from scrapy.spider import Spider
# from scrapy.selector import Selector
#
# from spider.items import StockFlexibleItem as FlexibleItem
#
#
# class StockbalanceSpider(Spider):
#     name = "stockbalance"
#     allowed_domains = ['cninfo.com.cn']
#     monthList = ['-03-31', '-06-30', '-09-30', '-12-31']
#
#     start_urls = (
#         'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
#         'http://www.cninfo.com.cn/information/sz/sme/szsmelclist.html',
#         'http://www.cninfo.com.cn/information/sz/cn/szcnlclist.html',
#         'http://www.cninfo.com.cn/information/sh/mb/shmblclist.html',
#     )
#     # start_urls = [
#     #   'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
#     # ]
#
#     def parse(self, response):
#         sel = Selector(response)
#         onclickList = sel.xpath('//td[@class="zx_data3"]/a/@onclick').extract()
#         p = re.compile(r'\d{6}$')
#         for theStr in onclickList:
#             arr = theStr.replace("setLmCode('", '').replace("');", '').split('?')
#             code = p.search(arr[1]).group()
#             for year in range(2000, 2015):
#                 for month in self.monthList:
#                     balanceSheetUrl = 'http://www.cninfo.com.cn/information/stock/balancesheet_.jsp?stockCode=' + code + '&yyyy=' + str(year) + '&mm=' + month + '&cwzb=balancesheet&button2=%CC%E1%BD%BB'
#                     req = Request(balanceSheetUrl, self.parseBalanceSheet)
#                     req.meta['year'] = str(year)
#                     req.meta['month'] = month
#                     yield req
#
#     def parseBalanceSheet(self, response):
#         sel = Selector(response)
#         year = response.meta['year']
#         month = response.meta['month']
#         tmpStr = sel.xpath('//form[@id="cninfoform"]/table/tr/td/text()').extract()
#         if len(tmpStr) < 1:
#             return
#         stockCode = tmpStr[0].strip()
#         stockName = tmpStr[1].strip()
#
#         arrTitle = sel.xpath('//td[@bgcolor="#b8ddf8"]/div/text()').extract()
#         arrValue = sel.xpath('//td[@bgcolor="#daf2ff"]/div/text()').extract()
#         arrRes = dict([(i.strip(), arrValue[index].strip()) for index, i in enumerate(arrTitle)])
#
#         item = FlexibleItem()
#         row = {}
#         row['stockCode'] = stockCode
#         row['stockName'] = stockName
#         row['pubtime'] = year + month
#
#         for key in arrRes.keys():
#             row[key.encode('utf8')] = arrRes[key]
#
#         item['row'] = row
#         return item
