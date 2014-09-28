from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo

class CsdnSpider(CrawlSpider):
  name = 'it168'
  allowed_domains = ['cio.it168.com']
  start_urls = ['http://cio.it168.com/']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'/a\d+'), callback='parse_item', follow=True),
  )

  def parse_item(self, response):
    print "enter it168_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    i['siteName'] = 'it168'
    i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = (len(sel.xpath('//div[@id="detailWord"]').extract())) and sel.xpath('//div[@id="detailWord"]').extract()[0] or ''
    return i
