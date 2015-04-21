from faker import Factory
fake = Factory.create()

BOT_NAME = 'group2'
SPIDER_MODULES = ['group2.spiders']
NEWSPIDER_MODULE = 'group2.spiders'
ITEM_PIPELINES = {
  'group2.pipelines.BaiduNewsPipeline': 1,
  'group2.pipelines.StockCompanyInfoPipeline':2,
  'group2.pipelines.StockBalanceSheetPipeline':3,
  'group2.pipelines.StockIncomeStatementsPipeline':4,
  'group2.pipelines.StockCashFlowPipeline':5,
  'group2.pipelines.StockFinancialReportPipeline':6,
  'group2.pipelines.SteelIndexNumberPipeline':7,
  'group2.pipelines.StatsMacroIndexPipeline':8,
  'group2.pipelines.StatsMacroDataPipeline':9,
  'group2.pipelines.WhpjPipeline':10,
  'group2.pipelines.WebArticlePipeLine':11,
  'group2.pipelines.WebBlogPipeLine':12,
  'group2.pipelines.IndustryReportPipeLine':13,
  'group2.pipelines.WebActivityPipeLine':14,
  'group2.pipelines.DianPingShopPipeLine':15,
  'group2.pipelines.DianPingDishPipeLine':16,
	'group2.pipelines.DaniangNewsPipeLine':17,
	'group2.pipelines.DaniangWeiBoPipeLine':18,
	'group2.pipelines.DaniangWeiXinPipeLine':19,
	'group2.pipelines.GovSubPipeLine':20,
	}
USER_AGENT = fake.internet_explorer()

'''
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_DEBUG = True
'''

DOWNLOAD_DELAY = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1
CONCURRENT_REQUESTS = 1
DOWNLOAD_TIMEOUT = 10

LOG_LEVEL = 'DEBUG'
#LOG_FILE = 'scrapy.log'
