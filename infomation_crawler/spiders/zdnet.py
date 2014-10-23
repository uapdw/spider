from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from infomation_crawler.items import WebArticleItem
import datetime
import pymongo
import re

class ZdnetSpider(CrawlSpider):
  name = 'zdnet'
  allowed_domains = ['zdnet.com.cn']
  
  start_urls = ['http://security.zdnet.com.cn','http://cloud.zdnet.com.cn','http://cio.zdnet.com.cn','http://big-data.zdnet.com.cn']
  
  today = str(datetime.date.today())
  WHICHURL=today[:4]+'/'+today[5:7]+today[8:]+'/\d+\.shtml'
  #WHICHURL='\d{4}/\d{4}/\d+.shtml'

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'(security|cloud|cio|soft|stor-age)\.zdnet\.com\.cn/(.*)' + str(WHICHURL)), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter zdnet_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()
    i['siteName'] = 'zdnet'
    i['title'] = (len(sel.xpath('//h1/text()').extract())>0) and sel.xpath('//h1/text()').extract()[0] or ''
    i['url'] = response.url
    i['addTime'] = datetime.datetime.now()
    i['content'] = (len(sel.xpath('//div[@class="qu_ocn"]').extract())) and sel.xpath('//div[@class="qu_ocn"]').extract()[0] or ''
    publishTime = re.findall(r'\d{4}/\d{4}', response.url, re.M)
    if len(publishTime)>0:
      i['publishTime'] = publishTime[0][:4]+'-'+publishTime[0][5:7]+'-'+publishTime[0][7:]
    else:
      i['publishTime'] = ''
    tagWords = sel.xpath('//div[@class="qu_zuo"]/p[@class="guzhu"]/a/text()').extract()
    keyWords = len(tagWords)>0 and tagWords[0].strip() or ''
    for m in range(len(tagWords)-1):
      keyWords = keyWords + '|' + tagWords[m+1].strip()
    i['keyWords'] = keyWords
    return i
