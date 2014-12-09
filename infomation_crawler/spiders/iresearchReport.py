from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from infomation_crawler.items import IndustryReportItem
import time,datetime
import pymongo

class IresearchReportSpider(CrawlSpider):
  name = 'iresearchReport'
  allowed_domains = ['iresearch.cn']
  start_urls = ['http://report.iresearch.cn/research/','http://report.iresearch.cn/reports/com-iResearch/','http://report.iresearch.cn/data/com-iResearch/']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tIndustryReport = infoDB.IndustryReport
  
  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    content1 = sel.xpath('//div[@class="content_Article a_width"]').extract()
    content2 = sel.xpath('//div[@class="content_Article a_width bd_1px"]').extract()
    i['content'] = len(content1)>0 and content1[0] or ''
    if i['content'] == '':
      i['content'] = len(content2)>0 and content2[0] or ''
    if i['content'] == '':
      i['content'] = i['abstract']

    i['author'] = ''
    i['siteName'] = 'iresearch'
    i['addTime'] = datetime.datetime.now()

    return i

  def parse(self, response):
    print "enter iresearchReport_parse_item...."
    sel = Selector(response)
    items = []
    reportContents = sel.xpath('//div[@class="box_style_content"]/dl')[0:]
    for report in reportContents:
      i = IndustryReportItem()

      url = report.xpath('dd/a/@href').extract()[0] 
      if url.find('http://')==-1:
        i['url'] = 'http://report.iresearch.cn'+url
      else:
        i['url'] = url

      title = report.xpath('dd/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''

      abstract = report.xpath('dd/p[@class="font_p"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0] or ''
      
      keyWords = report.xpath('dd/div[@class="newsinfo"]/span[2]/a/text()').extract()
      i['keyWords'] = len(keyWords)>0 and keyWords[0] or ''

      pubTime = report.xpath('dd/div[@class="newsinfo"]/span[1]/text()').extract()
      i['publishTime'] = len(pubTime)>0 and pubTime[0].split(u'\uff1a')[1].strip() or str(datetime.date.today())

      source = report.xpath('//div[@class="title"]/h3/text()').extract()
      i['source'] = len(source)>0 and source[0].strip() or ''

      items.append(i)

    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
