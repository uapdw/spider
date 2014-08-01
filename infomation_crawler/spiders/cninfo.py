# -*- coding: utf-8 -*-
import re
from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from infomation_crawler.items import StockCompanyInfoItem, StockBalanceSheetItem, StockIncomeStatementsItem, StockCashFlowItem, StockFinancialReportItem

class CninfoStockSpider(Spider):
  name = "cninfo"
  allowed_domains = ['cninfo.com.cn']

  # start_urls = [
  #   'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
  #   'http://www.cninfo.com.cn/information/sz/sme/szsmelclist.html',
  #   'http://www.cninfo.com.cn/information/sz/cn/szcnlclist.html',
  #   'http://www.cninfo.com.cn/information/sh/mb/shmblclist.html',
  # ]
  start_urls = [
    'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
  ]

  monthList = ['-03-31','-06-30','-09-30','-12-31']

  arrBalanceSheetColumn = {
    u'科目':'km',
    u'货币资金':'hbzj',
    u'短期借款':'dqjk',
    u'交易性金融资产':'jyxjrzc',
    u'交易性金融负债':'jyxjrfz',
    u'应收票据':'yspj',
    u'应付票据':'yfpj',
    u'应收账款':'yszk',
    u'应付账款':'yfzk',
    u'预付款项':'yfkx',
    u'预收款项':'yskx',
    u'其他应收款':'qtysk',
    u'应付职工薪酬':'yfzgxc',
    u'应收关联公司款':'ysglgsk',
    u'应交税费':'yjsf',
    u'应收利息':'yslx',
    u'应付利息':'yflx',
    u'应收股利':'ysgl',
    u'应付股利':'yfgl',
    u'存货':'ch',
    u'其他应付款':'qtyfk',
    u'其中:消耗性生物资产':'xhxswzc',
    u'应付关联公司款':'yfglgsk',
    u'一年内到期的非流动资产':'ynndqdfldzc',
    u'一年内到期的非流动负债':'ynndqdfldfz',
    u'其他流动资产':'qtldzc',
    u'其他流动负债':'qtldfz',
    u'流动资产合计':'ldzchj',
    u'流动负债合计':'ldfzhj',
    u'可供出售金融资产':'kgcsjrzc',
    u'长期借款':'cqjk',
    u'持有至到期投资':'cyzdqtz',
    u'应付债券':'yfzq',
    u'长期应收款':'cqysk',
    u'长期应付款':'cqyfk',
    u'长期股权投资':'cqgqtz',
    u'专项应付款':'zxyfk',
    u'投资性房地产':'tzxfdc',
    u'预计负债':'yjfz',
    u'固定资产':'gdzc',
    u'递延所得税负债':'dysdsfz',
    u'在建工程':'zjgc',
    u'其他非流动负债':'qtfldfz',
    u'工程物资':'gcwz',
    u'非流动负债合计':'fldfzhj',
    u'固定资产清理':'gdzcql',
    u'负债合计':'fzhj',
    u'生产性生物资产':'scxswzc',
    u'实收资本(或股本)':'shzb',
    u'油气资产':'yqzc',
    u'资本公积':'zbgj',
    u'无形资产':'wxzc',
    u'盈余公积':'yygj',
    u'开发支出':'kfzc',
    u'减:库存股':'jkcg',
    u'商誉':'sy',
    u'未分配利润':'wfplr',
    u'长期待摊费用':'cqdtfy',
    u'少数股东权益':'ssgdqy',
    u'递延所得税资产':'dysdszc',
    u'外币报表折算价差':'wbbbzsjc',
    u'其他非流动资产':'qtfldzc',
    u'非正常经营项目收益调整':'fzcjyxmsytz',
    u'非流动资产合计':'fldzchj',
    u'所有者权益(或股东权益)合计':'syzqy',
    u'资产总计':'zczj',
    u'负债和所有者(或股东权益)合计':'fzhsyz'
  }

  def parse(self, response):
    sel = Selector(response)
    onclickList = sel.xpath('//td[@class="zx_data3"]/a/@onclick').extract()
    p = re.compile(r'\d{6}$')
    for theStr in onclickList:
      arr = theStr.replace("setLmCode('",'').replace("');",'').split('?')
      code = p.search(arr[1]).group()
      companyInfoUrl = 'http://www.cninfo.com.cn/information/' + arr[0] + '/' + arr[1] + '.html'
      balanceSheetUrl = 'http://www.cninfo.com.cn/information/stock/balancesheet_.jsp?stockCode=' + code
      incomeStatementsUrl = 'http://www.cninfo.com.cn/information/stock/incomestatements_.jsp?stockCode=' + code
      cashFlowUrl = 'http://www.cninfo.com.cn/information/stock/cashflow_.jsp?stockCode=' + code
      financialReportUrl = 'http://www.cninfo.com.cn/information/stock/financialreport_.jsp?stockCode=' + code
      for yyyy in range(2000,2015):
	for mm in self.monthList:
	  #yield Request(companyInfoUrl, self.parseCompanyInfo)
	  yield Request(url=balanceSheetUrl, callback=self.parseBalanceSheet, method='GET',meta={'mm':mm,'yyyy':yyyy})
	  '''
	  yield Request(incomeStatementsUrl, self.parseIncomeStatements)
	  yield Request(cashFlowUrl, self.parseCashFlow)
	  yield Request(financialReportUrl, self.parseFinancialReport)
	  '''

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
    item['iType'] = 'companyInfo'

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
    sel = Selector(response)
    print response.url

    # from scrapy.shell import inspect_response
    # inspect_response(response)

    '''
    tmpStr = sel.xpath('//form[@id="cninfoform"]/table/tr/td/text()').extract()
    stockCode = tmpStr[0].strip()
    stockName = tmpStr[1].strip()

    arrTitle = sel.xpath('//td[@bgcolor="#b8ddf8"]/div/text()').extract()
    arrValue = sel.xpath('//td[@bgcolor="#daf2ff"]/div/text()').extract()
    arrRes = dict([(i.strip(),arrValue[index].strip()) for index,i in enumerate(arrTitle)])

    item = StockBalanceSheetItem()
    item['stockCode'] = stockCode
    item['stockName'] = stockName
    item['iType'] = 'balanceSheet'

    for key in arrRes.keys():
      if key == u'科目':
	item['subject'] = arrRes[key]

    print item
    '''
    #return item

  def parseIncomeStatements(self, response):
    print 'Method => incomeStatements'
    item = StockIncomeStatementsItem()
    item['iType'] = 'incomeStatements'
    return item

  def parseCashFlow(self, response):
    print 'Method => cashFlow'
    item = StockCashFlowItem()
    item['iType'] = 'cashFlow'
    return item

  def parseFinancialReport(self, response):
    print 'Method => financialReport'
    item = StockFinancialReportItem()
    item['iType'] = 'financialReport'
    return item

