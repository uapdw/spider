from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebBlogItem
import datetime
import pymongo

class IteyeSpider(CrawlSpider):
  name = 'iteye'
  allowed_domains = ['iteye.com']
  start_urls = ['http://www.iteye.com/blogs']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebBlogs = infoDB.web_blogs

  rules = (
    Rule(SgmlLinkExtractor(allow=r'/blogs/')),
    Rule(SgmlLinkExtractor(allow=r'/blog/\d+'), callback='parse_item'),
  )

  def parse_item(self, response):
    sel = Selector(response)
    i = WebBlogItem()
    i['title'] = sel.xpath('//h3/a/text()').extract()[0]
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = sel.xpath('//div[@id="blog_content"]').extract()[0]
    i['siteName'] = 'iteye'
    i['author'] = sel.xpath('//div[@id="blog_owner_name"]/text()').extract()[0]
    return i
