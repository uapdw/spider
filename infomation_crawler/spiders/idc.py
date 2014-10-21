from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import IndustryReportItem
import datetime
import pymongo

class IDCSpider(CrawlSpider):
  name = 'idc'
  allowed_domains = ['idc.com.cn']
  
  def __init__(self, crawl=None, *args, **kwargs):
    super(IDCSpider, self).__init__(*args, **kwargs)
    if(cmp(crawl, 'all')==0):
      urls = []
      for i in range(6):
        url = 'http://idc.com.cn/about/index.jsp?page=' + str(i+1) + '&thisy=2014'
        urls.append(url)
      self.start_urls = urls    
    else:
      self.start_urls = ['http://idc.com.cn/about/index.jsp?page=1&thisy=2014']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tIndustryReport = infoDB.IndustryReport

  def parse(self, response):
    print "enter idc_parse_item...."
    sel = Selector(response)
    reportContents = sel.xpath('//table/tr[1]/td[1]/table/tr[1]/td[1]/table/tr[2]/td[1]/table/tr[1]/td[1]/p')[0:]
    for report in reportContents:
      reportURL = report.xpath('a/@href').extract()
      i = IndustryReportItem()
      if(len(reportURL)>0):
        i['title'] = report.xpath('text()').extract()[0]
        i['url'] = 'http://idc.com.cn'+report.xpath('a/@href').extract()[0]
        i['publishTime'] = report.xpath('b/text()').extract()[0]
        i['InfSource'] = report.xpath('text()').extract()[1].replace('|','').strip()
        i['addTime'] = datetime.datetime.now()
        i['siteName'] = 'idc'
      else:
        i['url'] = ''
        return
      yield IndustryReportItem(i)
