# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
__author__ = 'zhangxin'

from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
import re
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *

class ArticleSPNNews(CrawlSpider):
  name = 'article_spn_news'
  allowed_domains = ['spn.com.cn']
  start_urls = ['http://www.spn.com.cn/news/']

  for i in range(2,6):
    url = 'http://www.spn.com.cn/news/'+str(i)+'.html'
    start_urls.append(url)

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  today = datetime.date.today()
  yesterday = (datetime.date.today() - datetime.timedelta(days=1))
  time_range = [today, yesterday]

  rules = (
    Rule(SgmlLinkExtractor(allow=r'www\.spn\.com\.cn/news/\d{8}/\d+.html'), callback='parse_item'),
  )

  def __init__(self,**kw):
    super(ArticleSPNNews,self).__init__(**kw)
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)


  def __del__(self):
    self.transport.close()

  def parse_item(self, response):
    xpath = XPath(Selector(response))
    i = WebArticleItem()
    
    authorStrList = (xpath.first('//table[@width="604"]/tr[3]/td/text()')).split(' ')
    publishTime = authorStrList[0]
    pubTime = datetime.datetime.strptime(publishTime,'%Y年%m月%d日')

    try:
      if pubTime and pubTime.date() not in self.time_range:
        raise DropItem('publishTime is out of the time range: %s' % publishTime)
    except:
      return i

    i['title'] = xpath.first('/html/body/div[3]/div[5]/div/table/tbody/tr[2]/td[1]/table/tbody/tr[2]/td/text()')
    i['url'] = response.url
    i['source'] = authorStrList[1]
    i['author'] = ''
    i['publishTime'] = pubTime.strftime('%Y-%m-%d')
    i['abstract'] = xpath.first('/html/body/div[3]/div[5]/div/table/tbody/tr[2]/td[1]/table/tbody/tr[6]/td/text()')
    i['keyWords'] = ''
    i['content'] = xpath.first('/html/body/div[3]/div[5]/div/table/tbody/tr[2]/td[1]/table/tbody/tr[8]/td')
    i['siteName'] = 'www.spn.com.cn'
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

