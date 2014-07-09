# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from infomation_crawler.items import StockCompanyInfoItem

class CninfoStockSpider(Spider):
  name = "cninfo"
  allowed_domains = ['cninfo.com.cn']

  # start_urls = [
  #   'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
  #   'http://www.cninfo.com.cn/information/sz/sme/szsmelclist.html',
  #   'http://www.cninfo.com.cn/information/sz/cn/szcnlclist.html',
  #   'http://www.cninfo.com.cn/information/sh/mb/shmblclist.html',
  #   'http://www.cninfo.com.cn/information/hk/mb/hkmblclist.html',
  #   'http://www.cninfo.com.cn/information/hk/gem/hkgemlclist.html'
  # ]
  start_urls = [
    'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
  ]

  def parse(self, response):
    sel = Selector(response)
    onclickList = sel.xpath('//td[@class="zx_data3"]/a/@onclick').extract()
    for theStr in onclickList:
      arr = theStr.replace("setLmCode('",'').replace("');",'').split('?')
      companyInfoUrl = 'http://www.cninfo.com.cn/information/' + arr[0] + '/' + arr[1] + '.html'
      balanceSheetUrl = 'http://www.cninfo.com.cn/information/balancesheet/' + arr[1] + '.html'
      incomeStatementsUrl = 'http://www.cninfo.com.cn/information/incomestatements/' + arr[1] + '.html'
      cashFlowUrl = 'http://www.cninfo.com.cn/information/cashflow/' + arr[1] + '.html'
      financialReportUrl = 'http://www.cninfo.com.cn/information/financialreport/' + arr[1] + '.html'
      yield Request(companyInfoUrl, self.parseCompanyInfo)
      yield Request(balanceSheetUrl, self.parseBalanceSheet)
      yield Request(incomeStatementsUrl, self.parseIncomeStatements)
      yield Request(cashFlowUrl, self.parseCashFlow)
      yield Request(financialReportUrl, self.parseFinancialReport)

  def parseCompanyInfo(self, response):
    print 'Method => companyInfo'
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
      if key == u'\u516c\u53f8\u5168\u79f0\uff1a':
	item['fullName'] = arrRes[key].strip()
      elif key == u'\u82f1\u6587\u540d\u79f0\uff1a':
	item['englishName'] = arrRes[key].strip()
      elif key == u'\u6ce8\u518c\u5730\u5740\uff1a':
	item['regAddress'] = arrRes[key].strip()
      elif key == u'\u516c\u53f8\u7b80\u79f0\uff1a':
	item['shortName'] = arrRes[key].strip()
      elif key == u'\u6cd5\u5b9a\u4ee3\u8868\u4eba\uff1a':
	item['legalPerson'] = arrRes[key].strip()
      elif key == u'\u516c\u53f8\u8463\u79d8\uff1a':
	item['secretary'] = arrRes[key].strip()
      elif key == u'\u6ce8\u518c\u8d44\u672c(\u4e07\u5143)\uff1a':
	item['regCapital'] = arrRes[key].strip()
      elif key == u'\u884c\u4e1a\u79cd\u7c7b\uff1a':
	item['industry'] = arrRes[key].strip()
      elif key == u'\u90ae\u653f\u7f16\u7801\uff1a':
	item['postCode'] = arrRes[key].strip()
      elif key == u'\u516c\u53f8\u7535\u8bdd\uff1a':
	item['phone'] = arrRes[key].strip()
      elif key == u'\u516c\u53f8\u4f20\u771f\uff1a':
	item['fax'] = arrRes[key].strip()
      elif key == u'\u516c\u53f8\u7f51\u5740\uff1a':
	item['website'] = arrRes[key].strip()
      elif key == u'\u4e0a\u5e02\u65f6\u95f4\uff1a':
	item['listTime'] = arrRes[key].strip()
      elif key == u'\u62db\u80a1\u65f6\u95f4\uff1a':
	item['ipoTime'] = arrRes[key].strip()
      elif key == u'\u53d1\u884c\u6570\u91cf\uff08\u4e07\u80a1\uff09\uff1a':
	item['issueAmount'] = arrRes[key].strip()
      elif key == u'\u53d1\u884c\u4ef7\u683c\uff08\u5143\uff09\uff1a':
	item['issuePrice'] = arrRes[key].strip()
      elif key == u'\u53d1\u884c\u5e02\u76c8\u7387\uff08\u500d\uff09\uff1a':
	item['issuePer'] = arrRes[key].strip()
      elif key == u'\u53d1\u884c\u65b9\u5f0f\uff1a':
	item['issueMode'] = arrRes[key].strip()
      elif key == u'\u4e3b\u627f\u9500\u5546\uff1a':
	item['underWriter'] = arrRes[key].strip()
      elif key == u'\u4e0a\u5e02\u63a8\u8350\u4eba\uff1a':
	item['listSponsor'] = arrRes[key].strip()
      elif key == u'\u4fdd\u8350\u673a\u6784\uff1a':
	item['recomInstitution'] = arrRes[key].strip()
     
    #print "short: %s,full: %s,amount: %s" % (item['stockName'],item['fullName'],item['issueAmount'])
    return item

  def parseBalanceSheet(self, response):
    print 'Method => balanceSheet'

  def parseIncomeStatements(self, response):
    print 'Method => incomeStatements'

  def parseCashFlow(self, response):
    print 'Method => cashFlow'

  def parseFinancialReport(self, response):
    print 'Method => financialReport'

