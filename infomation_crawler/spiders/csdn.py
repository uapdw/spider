from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo

class CsdnSpider(CrawlSpider):
  name = 'csdn'
  allowed_domains = ['csdn.net']
  start_urls = ['http://www.csdn.net/']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'/article/',deny=r'(download|passport|bbs|blog|subject|g|share|newsletter|student|huiyi|hero|msdn|tingyun|ibm|baidu|intel|ibmuniversity|api|geek|club|ask|read|code|yuntongxun|qcloud|qualcomm|m)\.csdn\.net'), callback='parse_item', follow=True),
    #Rule(SgmlLinkExtractor(allow=r'www\.csdn\.net/article/'), callback='parse_item'),
    #Rule(SgmlLinkExtractor(allow=r'http://www\.csdn\.net/article/'), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter Csdn_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    i['siteName'] = 'csdn'
    i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = (len(sel.xpath('//div[@class="con news_content"]').extract())) and sel.xpath('//div[@class="con news_content"]').extract()[0] or ''
    return i

