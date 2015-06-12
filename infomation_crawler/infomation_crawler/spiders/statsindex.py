from scrapy.http import Request
from scrapy.spider import Spider
from scrapy.selector import Selector
from infomation_crawler.items import StatsMacroIndexItem
from time import time
import json
import pymongo

class StatsindexSpider(Spider):
  name = "statsindex"
  allowed_domains = ["stats.gov.cn"]
  ts = str(int(time()))

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tMacroIndex = infoDB.bm_macro_index

  start_urls = (
      'http://data.stats.gov.cn/quotas/init?t=' + ts + '&dbcode=hgjd&dimension=zb&selectedCodeId=',
      'http://data.stats.gov.cn/quotas/init?t=' + ts + '&dbcode=hgyd&dimension=zb&selectedCodeId=',
      'http://data.stats.gov.cn/quotas/init?t=' + ts + '&dbcode=hgnd&dimension=zb&selectedCodeId=',
      )

  def parse(self, response):
    sel = Selector(response)
    string = (sel.xpath('//p/text()').extract())[0]
    jsonList = json.loads(string)
    period = ''

    if 'hgnd' in response.url:
      period = 'hgnd'
    elif 'hgyd' in response.url:
      period = 'hgyd'
    elif 'hgjd' in response.url:
      period = 'hgjd'

    for i in jsonList:
      if i['pId'] == '1':
	item = StatsMacroIndexItem()

	item['code'] = i['id']
	item['name'] = i['name']
	item['parentCode'] = i['pId']
	item['period'] = period
	item['ifData'] = i['ifData']
	item['unit'] = ''
	item['note'] = ''
	item['ts'] = int(time())

	yield item
	yield Request('http://data.stats.gov.cn/quotas/getchildren?code=' + i['id'] + '&dbcode=' + period + '&dimension=zb', self.parse_item)

  def parse_item(self,response):
    if response.body.strip() == '':
      return
    sel = Selector(response)
    string = (sel.xpath('//p/text()').extract())[0]
    if string == '[]':
      return
    jsonList = json.loads(string)
    period = ''

    if 'hgnd' in response.url:
      period = 'hgnd'
    elif 'hgyd' in response.url:
      period = 'hgyd'
    elif 'hgjd' in response.url:
      period = 'hgjd'

    for i in jsonList:
      item = StatsMacroIndexItem()

      item['code'] = i['id']
      item['name'] = i['name']
      item['parentCode'] = i['pId']
      item['period'] = period
      item['ifData'] = i['ifData']
      item['unit'] = ''
      item['note'] = ''
      item['ts'] = int(time())

      yield item
      yield Request('http://data.stats.gov.cn/quotas/getchildren?code=' + i['id'] + '&dbcode=' + period + '&dimension=zb', self.parse_item)


