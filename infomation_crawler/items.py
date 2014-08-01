# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BaiduNewsItem(Item):
    title = Field()
    sitename = Field()
    href = Field()
    posttime = Field()
    keyword = Field()

class StockCompanyInfoItem(Item):
  #股票代码
  stockCode = Field()
  #股票名称
  stockName = Field() 
  #item类型
  iType = Field()
  #公司全称
  fullName = Field() 
  #英文名称
  englishName = Field() 
  #注册地址
  regAddress = Field()
  #公司简称
  shortName = Field() 
  #法人代表
  legalPerson = Field() 
  #公司董秘
  secretary = Field() 
  #注册资本（万元）
  regCapital = Field() 
  industry = Field() #行业种类
  postCode = Field() #邮政编码
  phone = Field() #公司电话
  fax = Field() #公司传真
  website = Field() #公司网址
  listTime = Field() #上市时间
  ipoTime = Field() #招股时间
  issueAmount = Field() #发行数量（万股）
  issuePrice = Field() #发行价格（元）
  issuePer = Field() #发行市盈率（倍）per=price earning ratio
  issueMode = Field() #发行方式
  underWriter = Field() #主承销商
  listSponsor = Field() #上市推荐人
  recomInstitution = Field() #保荐机构

class StockBalanceSheetItem(Item):
  #股票代码
  stockCode = Field()
  #股票名称
  stockName = Field() 
  #item类型
  iType = Field()

class StockIncomeStatementsItem(Item):
  #股票代码
  stockCode = Field()
  #股票名称
  stockName = Field() 
  #item类型
  iType = Field()

class StockCashFlowItem(Item):
  #股票代码
  stockCode = Field()
  #股票名称
  stockName = Field() 
  #item类型
  iType = Field()

class StockFinancialReportItem(Item):
  #股票代码
  stockCode = Field()
  #股票名称
  stockName = Field() 
  #item类型
  iType = Field()

class SteelIndexNumberItem(Item):
  #发布日期
  pubDate = Field()
  #钢材综合指数
  indexNumber = Field()

class StatsMacroIndexItem(Item):
  code = Field()
  name = Field()
  parentCode = Field()
  period = Field()
  ifData = Field()
  unit = Field()
  note = Field()
  ts = Field()
  types = Field()

class StatsMacroDataItem(Item):
  key = Field()
  code = Field()
  name = Field()
  area = Field()
  ydate = Field()
  qdate = Field()
  mdate = Field()
  value = Field()
  desc = Field()
  ts = Field()
  types = Field()

class InfomationCrawlerItem(Item):
  pass
