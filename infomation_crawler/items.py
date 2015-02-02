# -*- coding: utf-8 -*-
# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class BaiduNewsItem(Item):
    title = Field()
    sitename = Field()
    url = Field()
    publishtime = Field()
    keywords = Field()
    content = Field()
    addtime = Field()


class StockCompanyInfoItem(Item):
  stockCode = Field() #股票代码
  stockName = Field() #股票名称
  gsqc = Field() #公司全称
  ywmc = Field() #英文名称
  zcdz = Field()#注册地址
  gsjc = Field() #公司简称
  fddbr = Field() #法定代表人
  gsdm = Field() #公司董秘
  zczb = Field() #注册资本（万元）
  hyzl = Field() #行业种类
  yzbm = Field() #邮政编码
  gsdh = Field() #公司电话
  gscz = Field() #公司传真
  gswz = Field() #公司网址
  sssj = Field() #上市时间
  zgsj = Field() #招股时间
  fxsl = Field() #发行数量（万股）
  fxjg = Field() #发行价格（元）
  fxsyl = Field() #发行市盈率（倍）per=price earning ratio
  fxfs = Field() #发行方式
  zcxs = Field() #主承销商
  shtjr = Field() #上市推荐人
  bjjg = Field() #保荐机构

class StockBalanceSheetItem(Item):
  stockCode = Field() #股票代码
  stockName = Field() #股票名称
  pubtime = Field() #发布时间
  km = Field() #科目
  hbzj = Field() #货币资金
  dqjk = Field() #短期借款
  jyxjrzc = Field() #交易性金融资产
  jyxjrfz = Field() #交易性金融负债
  yspj = Field() #应收票据
  yfpj = Field() #应付票据
  yszk = Field() #应收账款
  yfzk = Field() #应付账款
  yfkx = Field() #预付款项
  yskx = Field() #预收款项
  qtysk = Field() #其他应收款
  yfzgxc = Field() #应付职工薪酬
  ysglgsk = Field() #应收关联公司款
  yjsf = Field() #应交税费
  yslx = Field() #应收利息
  yflx = Field() #应付利息
  ysgl = Field() #应收股利
  yfgl = Field() #应付股利
  ch = Field() #存货
  qtyfk = Field() #其他应付款
  xhxswzc = Field() #其中:消耗性生物资产
  yfglgsk = Field() #应付关联公司款
  ynndqdfldzc = Field() #一年内到期的非流动资产
  ynndqdfldfz = Field() #一年内到期的非流动负债
  qtldzc = Field() #其他流动资产
  qtldfz = Field() #其他流动负债
  ldzchj = Field() #流动资产合计
  ldfzhj = Field() #流动负债合计
  kgcsjrzc = Field() #可供出售金融资产
  cqjk = Field() #长期借款
  cyzdqtz = Field() #持有至到期投资
  yfzq = Field() #应付债券
  cqysk = Field() #长期应收款
  cqyfk = Field() #长期应付款
  cqgqtz = Field() #长期股权投资
  zxyfk = Field() #专项应付款
  tzxfdc = Field() #投资性房地产
  yjfz = Field() #预计负债
  gdzc = Field() #固定资产
  dysdsfz = Field() #递延所得税负债
  zjgc = Field() #在建工程
  qtfldfz = Field() #其他非流动负债
  gcwz = Field() #工程物资
  fldfzhj = Field() #非流动负债合计
  gdzcql = Field() #固定资产清理
  fzhj = Field() #负债合计
  scxswzc = Field() #生产性生物资产
  shzb = Field() #实收资本(或股本)
  yqzc = Field() #油气资产
  zbgj = Field() #资本公积
  wxzc = Field() #无形资产
  yygj = Field() #盈余公积
  kfzc = Field() #开发支出
  jkcg = Field() #减:库存股
  sy = Field() #商誉
  wfplr = Field() #未分配利润
  cqdtfy = Field() #长期待摊费用
  ssgdqy = Field() #少数股东权益
  dysdszc = Field() #递延所得税资产
  wbbbzsjc = Field() #外币报表折算价差
  qtfldzc = Field() #其他非流动资产
  fzcjyxmsytz = Field() #非正常经营项目收益调整
  fldzchj = Field() #非流动资产合计
  syzqy = Field() #所有者权益(或股东权益)合计
  zczj = Field() #资产总计
  fzhsyz = Field() #负债和所有者(或股东权益)合计


class StockIncomeStatementsItem(Item):
  stockCode = Field() #股票代码
  stockName = Field() #股票名称
  pubtime = Field() #发布时间
  km = Field() #科目
  yesr = Field() #一、营业收入
  yelr = Field() #二、营业利润
  yecb = Field() #减:营业成本
  btsr = Field() #加:补贴收入
  yesjjfj = Field() #营业税金及附加
  yywsr = Field() #营业外收入
  xsfy = Field() #销售费用
  yywzc = Field() #减:营业外支出
  glfy = Field() #管理费用
  fldzcczjss = Field() #其中:非流动资产处置净损失
  ktfy = Field() #堪探费用
  yxlrzedqtkm = Field() #加:影响利润总额的其他科目
  cwfy = Field() #财务费用
  lrze = Field() #三、利润总额
  zcjzss = Field() #资产减值损失
  sds = Field() #减:所得税
  gyjzbdjsy = Field() #加:公允价值变动净收益
  yxjlrdqtkm = Field() #加:影响净利润的其他科目
  tzsy = Field() #投资收益
  jlr = Field() #四、净利润
  dlyqyhhyqydtzqy = Field() #其中:对联营企业和合营企业的投资权益
  gsymgssyzdjlr = Field() #归属于母公司所有者的净利润
  yxyelrdqtkm = Field() #影响营业利润的其他科目
  ssgdsy = Field() #少数股东损益

class StockCashFlowItem(Item):
  stockCode = Field() #股票代码
  stockName = Field() #股票名称
  pubtime = Field() #发布时间

class StockFinancialReportItem(Item):
  stockCode = Field() #股票代码
  stockName = Field() #股票名称
  pubtime = Field() #发布时间

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

class WhpjItem(Item):
  key = Field()
  currentname = Field()
  price_spot_in = Field()
  price_cash_in = Field()
  price_spot_out = Field()
  price_cash_out = Field()
  midprice = Field()
  bocprice = Field()
  releasetime = Field()
  note = Field()
  ts = Field()

class WebArticleItem(Item):
  title = Field()
  url = Field()
  author = Field()
  abstract = Field()
  keyWords = Field()
  publishTime = Field()
  content = Field()
  siteName = Field()
  source = Field()
  addTime = Field()

class WebBlogItem(Item):
  title = Field()
  url = Field()
  author = Field()
  abstract = Field()
  keyWords = Field()
  publishTime = Field()
  content = Field()
  siteName = Field()
  source = Field()
  addTime = Field()

class WebBBSItem(Item):
  title = Field()
  url = Field()
  author = Field()
  abstract = Field()
  keyWords = Field()
  publishTime = Field()
  content = Field()
  siteName = Field()
  source = Field()
  addTime = Field()

class IndustryReportItem(Item):
  title = Field()
  url = Field()
  author = Field()
  abstract = Field()
  keyWords = Field()
  publishTime = Field()
  content = Field()
  siteName = Field()
  source = Field()
  addTime = Field()

class WebActivityItem(Item):
  title = Field()
  url = Field()
  trad = Field()
  time = Field()
  location = Field()
  keyWords = Field()
  activityID = Field()
  siteName = Field()
  addTime = Field()
class DianPingShopItem(Item):
  shopid = Field()
  level = Field()
  consume = Field()
  comment = Field()
  taste = Field()
  environment = Field()
  service = Field()
  #recommend = Field()
  #rnumber = Field()
  shopname = Field()
  city = Field()
  address = Field()
  business = Field()

class DianPingDishItem(Item):
	shopid = Field()
	arrDish = Field()
class DemoItem(Item):
	title = Field()
	url = Field()
	time = Field()
	siteName = Field()

class WeiBoItem(Item):
	image = Field()
	username = Field()
	content = Field()
	source = Field()
	time = Field()
	weibourl = Field()
	userurl = Field()

class WeiXinItem(Item):
	image = Field()
	title = Field()
	url = Field()
	time = Field()
	content = Field()
	source = Field()
class InfomationCrawlerItem(Item):
  pass
