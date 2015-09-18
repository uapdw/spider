# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'zhangxin'

from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
from scrapy.exceptions import DropItem

from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *
class CcidnetSpider(CrawlSpider):
  name = 'ccidnet'
  allowed_domains = ['ccidnet.com']
  start_urls = [
    'http://www.ccidnet.com/news/',
    'http://www.ccidnet.com/internet/',
    'http://www.ccidnet.com/product/',
    'http://www.ccidnet.com/security/',
    'http://www.ccidnet.com/information/',
    'http://www.ccidnet.com/smartindustry/',
    'http://www.ccidnet.com/smartcity/',
    'http://www.ccidnet.com/smartlife/',
    
  ]

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  time_range = [today, yesterday]

  rules = (
    Rule(SgmlLinkExtractor(allow=r'www\.ccidnet\.com/\d{4}/\d{4}/\d+\.shtml'), callback='parse_item'),
    Rule(SgmlLinkExtractor(allow=r'www\.ccidnet\.com/[A-Za-z]+/[A-Za-z]+/$'), callback='parse_list'),
    Rule(SgmlLinkExtractor(allow=r'www\.ccidnet\.com/[A-Za-z]+/[A-Za-z]+/\d+\.shtml$'), callback='parse_list'),
  )


  def __init__(self,**kw):
    super(CcidnetSpider,self).__init__(**kw)
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)


  def __del__(self):
    self.transport.close()


  def parse_list(self, response):
    print "enter parse_list...."

    xpath = XPath(Selector(response))

    urlList = [url for url in (xpath.list('//div[@class="nr_cont1 F_Left"]//div[@class="plist1 "]/div[@class="plist1_p F_Right"]/h2/a/@href') if len(xpath.list('//div[@class="nr_cont1 F_Left"]//div[@class="plist1 "]/div[@class="plist1_p F_Right"]/h2/a/@href'))>0 else xpath.list('//div[@class="nr_cont1 F_Left"]//div[@class="plist11 "]/div[@class="plist11_p F_Left"]/h2/a/@href'))]
    for url in urlList:
      yield Request(url, callback=self.parse_item)

    pageList = xpath.list('//div[@class="fy"]/li/a/@href')
    # print pageList

    if len(pageList) > 0:
      for url in pageList:
        if 'javascript' in url:
          continue
        else:
          yield Request(url, callback=self.parse_list)
    # print pageList
    # pageList = [url for url in xpath.list('//div[@class="fy"]/')]


  def parse_item(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()

    authorStrList = xpath.first('//div[@class="nr_cont1 F_Left"]/div[@class="tittle_j"]/text()').split()
    publishTime = authorStrList[0].split('：')[1]
    pubTime = datetime.datetime.strptime(publishTime,'%Y-%m-%d')

    try:
      if pubTime and pubTime.date() not in self.time_range:
        raise DropItem('publishTime is out of the time range: %s' % publishTime)
    except:
      i['title'] = ''
      i['url'] = response.url
      return i

    i['title'] = xpath.first('//div[@class="nr_cont1 F_Left"]/h2/text()')
    i['url'] = response.url
    i['source'] = authorStrList[2].split('：')[1]
    i['author'] = authorStrList[3].split('：')[1]
    i['publishTime'] = publishTime
    i['abstract'] = xpath.first('//div[@class="nr_cont1 F_Left"]/div[@class="p_jd"]/text()')
    i['keyWords'] = ' '.join([w for w in xpath.list('//div[@class="cont2_tittle"]/div[@class="gjc F_Left"]/a/text()')])
    i['content'] = xpath.first('//div[@class="main_content"]')
    i['siteName'] = 'www.ccidnet.com'
    i['addTime'] = datetime.datetime.now()

    return i


class XPath():

  _selecter = None

  def __init__(self, selector):
    self._selecter = selector

  def selector(self, xpath = None):
    if xpath:
      return self._selecter.xpath(xpath)
    else:
      return self._selecter

  def list(self, path):
    return [s.strip() for s in self._selecter.xpath(path).extract() if s.strip()]

  def first(self, path):
    l = self.list(path)
    if l:
      return l[0].strip()
    else:
      return ''
