from scrapy.spider import Spider
from scrapy.selector import Selector
from infomation_crawler.items import StatsMacroDataItem, StatsMacroIndexItem
from time import time
import pymongo
import json

class StatsdataSpider(Spider):
  name = 'statsdata'
  allowed_domains = ['stats.gov.cn']
  ts = str(int(time()))
  urls = []

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tMacroIndex = infoDB.bm_macro_index
  #indexList = tMacroIndex.find({'ifdata':'1','period':'hgjd'})
  indexList = tMacroIndex.find({'ifdata':'1'})
  conn.close()

  for i in indexList:
    startTime = ''
    if i['period'] == 'hgnd':
      startTime = '1949'
    elif i['period'] == 'hgyd': 
      startTime = '194901'
    elif i['period'] == 'hgjd': 
      startTime = '1949A'
    url = 'http://data.stats.gov.cn/workspace/index?a=l&tmp=' + ts + '&m=' + i['period'] + '&index=' + i['code'] + '&region=000000&time=-1%2C' + startTime + '&selectId=000000&third=region'
    urls.append(url)

  start_urls = urls

  def parse(self, response):
    sel = Selector(response)
    period = ''
    if 'hgnd' in response.url:
      period = 'hgnd'
    elif 'hgyd' in response.url:
      period = 'hgyd'
    elif 'hgjd' in response.url:
      period = 'hgjd'

    string = (sel.xpath('//p/text()').extract())[0]
    jsonList = json.loads(string)
    arrTableData = jsonList['tableData']
    arrIndex = jsonList['value']['index'][0]
    arrArea = jsonList['value']['region'][0]

    indexItem = StatsMacroIndexItem()
    indexItem['code'] = arrIndex['id']
    indexItem['unit'] = arrIndex['unit']
    indexItem['note'] = arrIndex['note']
    indexItem['types'] = 'index'
    yield indexItem

    if len(arrTableData) <= 0:
      return

    for key in arrTableData:
      item = StatsMacroDataItem()
      item['key'] = key
      item['code'] = arrIndex['id']
      item['name'] = arrIndex['name']
      item['area'] = arrArea['id']

      arrKey = key.split('_')
      timeStr = arrKey[2]
      if period == 'hgyd':
	item['ydate'] = ''
	item['qdate'] = ''
	item['mdate'] = int(timeStr)
      if period == 'hgnd':
	item['ydate'] = int(timeStr)
	item['qdate'] = ''
	item['mdate'] = ''
      if period == 'hgjd':
	year = timeStr[0:4]
	season = timeStr[4:]
	if season == 'A':
	  qStr = '01'
	elif season == 'B':
	  qStr = '02'
	elif season == 'C':
	  qStr = '03'
	elif season == 'D':
	  qStr = '04'

	item['ydate'] = ''
	item['qdate'] = int(year + qStr)
	item['mdate'] = ''

      value = arrTableData[key].replace(',','')
      if value == '':
	value = 0
      value = float(value)
      item['value'] = value
      item['desc'] = ''
      item['ts'] = int(time())
      item['types'] = 'data'
      yield item

    




