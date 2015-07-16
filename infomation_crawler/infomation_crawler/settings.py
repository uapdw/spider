from faker import Factory
fake = Factory.create()

BOT_NAME = 'infomation_crawler'
SPIDER_MODULES = ['infomation_crawler.spiders']
NEWSPIDER_MODULE = 'infomation_crawler.spiders'
ITEM_PIPELINES = {
  'infomation_crawler.pipelines.BaiduNewsPipeline': 1,
  'infomation_crawler.pipelines.StockCompanyInfoPipeline':2,
  'infomation_crawler.pipelines.StockBalanceSheetPipeline':3,
  'infomation_crawler.pipelines.StockIncomeStatementsPipeline':4,
  'infomation_crawler.pipelines.StockCashFlowPipeline':5,
  'infomation_crawler.pipelines.StockFinancialReportPipeline':6,
  'infomation_crawler.pipelines.SteelIndexNumberPipeline':7,
  'infomation_crawler.pipelines.StatsMacroIndexPipeline':8,
  'infomation_crawler.pipelines.StatsMacroDataPipeline':9,
  'infomation_crawler.pipelines.WhpjPipeline':10,
  'infomation_crawler.pipelines.WebArticlePipeLine':11,
  'infomation_crawler.pipelines.WebBlogPipeLine':12,
  'infomation_crawler.pipelines.IndustryReportPipeLine':13,
  'infomation_crawler.pipelines.WebActivityPipeLine':14,
  'infomation_crawler.pipelines.DianPingShopPipeLine':15,
  'infomation_crawler.pipelines.DianPingDishPipeLine':16,
	'infomation_crawler.pipelines.DaniangNewsPipeLine':17,
	'infomation_crawler.pipelines.DaniangWeiBoPipeLine':18,
	'infomation_crawler.pipelines.DaniangWeiXinPipeLine':19,
	'infomation_crawler.pipelines.GovSubPipeLine':20,
	'infomation_crawler.pipelines.JDBaseInfoPipeLine':21,
	'infomation_crawler.pipelines.JDCommDetailPipeLine':22,
	'infomation_crawler.pipelines.JDWaresInfoPipeLine':23,
	'infomation_crawler.pipelines.JDSummaryCommPipeLine':24,
	'infomation_crawler.pipelines.JDDpInfoTestPipeLine':25,
	'infomation_crawler.pipelines.HRDataPipeLine':26,
	'infomation_crawler.pipelines.PM25ChinaPipeLine':27,
	}
USER_AGENT = fake.internet_explorer()
#USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.54 Safari/536.5'
'''
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 10
AUTOTHROTTLE_DEBUG = True
'''

DOWNLOADER_MIDDLEWARES = {
		    'scrapyjs.SplashMiddleware': 725,
				}
SPLASH_URL = 'http://172.20.8.3:8050/'
DOWNLOAD_DELAY = 0.5
DUPEFILTER_CLASS = 'scrapyjs.SplashAwareDupeFilter'
CONCURRENT_REQUESTS_PER_DOMAIN = 8
CONCURRENT_REQUESTS = 16
DOWNLOAD_TIMEOUT = 30

LOG_LEVEL = 'DEBUG'
#LOG_FILE = 'scrapy.log'
