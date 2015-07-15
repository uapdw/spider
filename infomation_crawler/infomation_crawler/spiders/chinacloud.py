from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
from scrapy.http import Request
import datetime
import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *
class chinaCloudSpider(CrawlSpider):
  name = 'chinacloud'
  allowed_domains = ['china-cloud.com']
  start_urls = ['http://www.china-cloud.com/yunzixun/list_3_1.html','http://www.china-cloud.com/yunzixun/list_3_2.html','http://www.china-cloud.com/yunzixun/list_3_3.html']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles
  def __init__(self):
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    title = sel.xpath('//div[@class="wenzhang_top"]/h2/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''

    info = sel.xpath('//div[@class="sm_arcinfo"]/span/text()').extract()[0:]
    i['publishTime'] = len(info)>0 and info[0].split()[0].strip() or str(datetime.date.today())
    i['source'] = len(info)>1 and info[1].strip() or ''
    i['author'] = len(info)>2 and info[2].strip() or ''

    content = sel.xpath('//div[@class="zhengwen"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'china-cloud'

    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter china-cloud_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="sm_yxz_listbox"]/ul/li/div[@class="sm_info"]')[0:]
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = 'http://www.china-cloud.com'+news.xpath('a/@href').extract()[0]
      
      abstract = news.xpath('div[@class="sm_yxz_intro"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0].strip() or ''
      
      keyWord = news.xpath('span[@class="sm_tag"]/a/text()').extract()
      i['keyWords'] = len(keyWord)>0 and keyWord[0].strip() or ''

      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
