from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo

class ZolSpider(CrawlSpider):
  name = 'zol'
  allowed_domains = ['cio.zol.com.cn', 'cloud.zol.com.cn']
  start_urls = ['http://cio.zol.com.cn/', 'http://cloud.zol.com.cn/']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'/\d+/\d+\.html'), callback='parse_item', follow=True),
  )

  def parse_item(self, response):
    print "enter Zol_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    i['siteName'] = 'zol'
    i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = (len(sel.xpath('//div[@id="article-content"]').extract())) and sel.xpath('//div[@id="article-content"]').extract()[0] or ''
    i['publishTime'] = ''
    i['keyWords'] = ''
    return i

