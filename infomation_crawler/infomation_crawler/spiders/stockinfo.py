# -*- coding: utf-8 -*-
import pymongo
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from infomation_crawler.items import StockCompanyInfoItem

class StockinfoSpider(Spider):
  name = "stockinfo"
  allowed_domains = ['cninfo.com.cn']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tCompanyInfo = infoDB.stock_companyinfo

  arrStockInfoColumn = {
    u"公司全称：":"gsqc",
    u"英文名称：":"ywmc",
    u"注册地址：":"zcdz",
    u"公司简称：":"gsjc",
    u"法定代表人：":"fddbr",
    u"公司董秘：":"gsdm",
    u"注册资本(万元)：":"zczb",
    u"行业种类：":"hyzl",
    u"邮政编码：":"yzbm",
    u"公司电话：":"gsdh",
    u"公司传真：":"gscz",
    u"公司网址：":"gswz",
    u"上市时间：":"sssj",
    u"招股时间：":"zgsj",
    u"发行数量（万股）：":"fxsl",
    u"发行价格（元）：":"fxjg",
    u"发行市盈率（倍）：":"fxsyl",
    u"发行方式：":"fxfs",
    u"主承销商：":"zcxs",
    u"上市推荐人：":"shtjr",
    u"保荐机构：":"bjjg"
  }

  start_urls = (
     'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
     'http://www.cninfo.com.cn/information/sz/sme/szsmelclist.html',
     'http://www.cninfo.com.cn/information/sz/cn/szcnlclist.html',
     'http://www.cninfo.com.cn/information/sh/mb/shmblclist.html',
   )
  #start_urls = [
  #  'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
  #]

  def parse(self, response):
    sel = Selector(response)
    onclickList = sel.xpath('//td[@class="zx_data3"]/a/@onclick').extract()
    for theStr in onclickList:
      arr = theStr.replace("setLmCode('",'').replace("');",'').split('?')
      companyInfoUrl = 'http://www.cninfo.com.cn/information/' + arr[0] + '/' + arr[1] + '.html'
      yield Request(companyInfoUrl, self.parseCompanyInfo)

  def parseCompanyInfo(self, response):
    sel = Selector(response)
    tmpStr = sel.xpath('//table[@class="table"]/tr/td[@style]/text()').extract()
    stockCode = tmpStr[0].strip()
    stockName = tmpStr[1].strip().replace(' ','')
    arrTitle = sel.xpath('//div[@class="zx_left"]/div/table/tr/td[@class="zx_data"]/text()').extract()
    arrValue = sel.xpath('//div[@class="zx_left"]/div/table/tr/td[@class="zx_data2"]/text()').extract()
    arrRes = dict([(i,arrValue[index]) for index,i in enumerate(arrTitle)])

    item = StockCompanyInfoItem()
    item['stockCode'] = stockCode
    item['stockName'] = stockName

    for key in arrRes.keys():
      if key in self.arrStockInfoColumn:
	item[self.arrStockInfoColumn[key]] = arrRes[key].strip()
      else:
	return

    return item



