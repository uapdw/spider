# Scrapy settings for infomation_crawler project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#
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
  'infomation_crawler.pipelines.WhpjPipeline':10
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'infomation_crawler (+http://www.kevenking.cn)'
USER_AGENT = fake.user_agent()
DOWNLOAD_DELAY = 2
