from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebBlogItem
from scrapy.http import Request
import datetime
import pymongo

class IteyeSpider(CrawlSpider):
  name = 'iteye'
  allowed_domains = ['iteye.com']
  start_urls = ['http://wwwa.iteye.com/blogs', 'http://www.iteye.com/blogs?page=2', 'http://www.iteye.com/blogs?page=3']

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebBlogs = infoDB.web_blogs

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']
    i['title'] = sel.xpath('//h3/a/text()').extract()[0]
    i['content'] = sel.xpath('//div[@id="blog_content"]').extract()[0]
    i['addTime'] = datetime.datetime.now()
    i['siteName'] = 'iteye'
    i['author'] = sel.xpath('//div[@id="blog_owner_name"]/text()').extract()[0]
    tagWords = sel.xpath('//div[@class="news_tag"]/a/text()').extract()
    keyWords = len(tagWords)>0 and tagWords[0].strip() or ''
    for m in range(len(tagWords)-1):
      keyWords = keyWords + '|' + tagWords[m+1].strip()
    i['keyWords'] = keyWords
    return i

  def parse(self, response):
    sel = Selector(response)
    items = []
    indexBlogs = sel.xpath('//div[@id="index_main"]/div[@class="blog clearfix"]')[0:]
    for blog in indexBlogs:
      i = WebBlogItem()
      i['url'] = blog.xpath('div/h3/a/@href').extract()[0]
      i['publishTime'] = blog.xpath('div/div[@class="blog_info"]/span[@class="date"]/text()').extract()[0][:10]
      items.append(i)
    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
