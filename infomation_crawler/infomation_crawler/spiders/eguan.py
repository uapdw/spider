from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from infomation_crawler.items import IndustryReportItem
import time,datetime
import pymongo
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from infomation_crawler.hbase import Hbase
from infomation_crawler.hbase.ttypes import *
class EguanSpider(CrawlSpider):
  name = 'eguan'
  allowed_domains = ['eguan.cn']
  start_urls = ['http://data.eguan.cn/']

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tIndustryReport = infoDB.IndustryReport
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

    content = sel.xpath('//div[@class="article_content"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    pubTime = sel.xpath('//div[@class="article_info"]/text()').extract()
    i['publishTime'] = len(pubTime)>0 and pubTime[0].strip().split()[0] or str(datetime.date.today())

    i['author'] = ''
    i['keyWords'] = ''
    i['siteName'] = 'eguan'
    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter eguan_parse_item...."
    sel = Selector(response)
    items = []
    reportDivs = sel.xpath('//div[@class="data_bottom"]/div')[0:]
    for div in reportDivs:
      reportContents = div.xpath('ul[@class="data"]/li')[0:]
      for report in reportContents:
        i = IndustryReportItem()

        i['url'] = report.xpath('h4/a/@href').extract()[0]

        title = report.xpath('h4/a/text()').extract()
        i['title'] = len(title)>0 and title[0].strip() or ''

        abstract = report.xpath('p/text()').extract()
        i['abstract'] = len(abstract)>0 and abstract[0] or ''
      
        source = report.xpath('p/a/text()').extract()
        i['source'] = len(source)>0 and source[0].strip() or ''

        items.append(i)

    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
