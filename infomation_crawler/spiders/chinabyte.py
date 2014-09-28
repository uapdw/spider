from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo

class ChinaByteSpider(CrawlSpider):
  name = 'chinabyte'
  allowed_domains = ['chinabyte.com']
  start_urls = ['http://www.chinabyte.com/']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'/(\D*/)?\d+/\d+\.shtml',deny=r'(bbs|blog|cmo|com|device|edu|jifen|labs|nb|nbpc|pc|passport|product|shang|solution|tech|video|view|win8)\.chinabyte\.com'), callback='parse_item', follow=True),
  )

  def parse_item(self, response):
    print "enter chinabyte_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    i['siteName'] = 'chinabyte'
    i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = (len(sel.xpath('//div[@id="logincontent"]').extract())) and sel.xpath('//div[@id="logincontent"]').extract()[0] or ''
    return i
