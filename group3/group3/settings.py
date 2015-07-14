from faker import Factory
fake = Factory.create()

BOT_NAME = 'group3'
SPIDER_MODULES = ['group3.spiders']
NEWSPIDER_MODULE = 'group3.spiders'
ITEM_PIPELINES = {
  'group3.pipelines.BaiduNewsPipeline': 1,
  'group3.pipelines.StockCompanyInfoPipeline':2,
  'group3.pipelines.StockBalanceSheetPipeline':3,
  'group3.pipelines.StockIncomeStatementsPipeline':4,
  'group3.pipelines.StockCashFlowPipeline':5,
  'group3.pipelines.StockFinancialReportPipeline':6,
  'group3.pipelines.SteelIndexNumberPipeline':7,
  'group3.pipelines.StatsMacroIndexPipeline':8,
  'group3.pipelines.StatsMacroDataPipeline':9,
  'group3.pipelines.WhpjPipeline':10,
  'group3.pipelines.WebArticlePipeLine':11,
  'group3.pipelines.WebBlogPipeLine':12,
  'group3.pipelines.IndustryReportPipeLine':13,
  'group3.pipelines.WebActivityPipeLine':14,
  'group3.pipelines.DianPingShopPipeLine':15,
  'group3.pipelines.DianPingDishPipeLine':16,
	'group3.pipelines.DaniangNewsPipeLine':17,
	'group3.pipelines.DaniangWeiBoPipeLine':18,
	'group3.pipelines.DaniangWeiXinPipeLine':19,
	'group3.pipelines.GovSubPipeLine':20,
	'group3.pipelines.PublicDemoArticlePipeLine':21,
	'group3.pipelines.PublicDemoBBSPipeLine':22,
	}
USER_AGENT = fake.internet_explorer()

'''
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_DEBUG = True
'''

DOWNLOAD_DELAY = 0
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS = 16
DOWNLOAD_TIMEOUT = 10

COMMANDS_MODULE = 'group3.commands'

LOG_LEVEL = 'DEBUG'
#LOG_FILE = 'scrapy.log'
