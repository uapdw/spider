from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo

class It168Spider(CrawlSpider):
  name = 'it168'
  allowed_domains = ['it168.com']
  
  today = datetime.date.today()
  year = today.year
  safeURL = 'http://archive.it168.com/100002/' + str(year) + '/' + str(today) + '.shtml'
  cloudURL = 'http://archive.it168.com/100043/' + str(year) + '/' + str(today) + '.shtml'
  urls = []
  urls.append(safeURL)
  urls.append(cloudURL)
  start_urls = urls

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'(safe|cloud)\.it168\.com/a\d+'), callback='parse_item'),
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
    i['publishTime'] = str(It168Spider.today)
    tagWords = sel.xpath('//div[@class="biaoq"]/a/text()').extract()
    if len(tagWords)>0:
      keyWords = tagWords[0].strip()
      for m in range(len(tagWords)-1):
        keyWords = keyWords + '|' + tagWords[m+1].strip()
      i['keyWords'] = keyWords
    else:
      i['keyWords'] = ''
    return i
