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
class DataguruSpider(CrawlSpider):
  name = 'dataguru'
  allowed_domains = ['dataguru.cn']
  start_urls = ['http://it.dataguru.cn/','http://bi.dataguru.cn/','http://byod.dataguru.cn/']

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

    pubTime = sel.xpath('//div[@class="h hm"]/p/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].strip().split()[0] or str(datetime.date.today())
    author = sel.xpath('//div[@class="h hm"]/p/a/text()').extract()
    i['author'] = len(author)>0 and author[0].strip() or ''

    content = sel.xpath('//table[@class="vwtb"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'dataguru'

    #source = sel.xpath('//ul[@class="article-meta"]/li[3]/a/text()').extract()
    i['source'] = ''
    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter dataguru_parse_item...."
    sel = Selector(response)
    items = []
    newsLists = sel.xpath('//div[@class="bm_c xld"]/dl[@class="bbda cl"]')[0:]
    keyWord = sel.xpath('//div[@class="bm_h cl"]/h1/text()').extract()
    for news in newsLists:
      i = WebArticleItem()
      i['url'] = news.xpath('dt/a/@href').extract()[0]
      
      title = news.xpath('dt/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      abstract = news.xpath('dd/text()').extract()
      i['abstract'] = len(abstract)>1 and abstract[1].strip() or ''

      i['keyWords'] = len(keyWord)>0 and keyWord[0].strip() or ''

      items.append(i)

    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
