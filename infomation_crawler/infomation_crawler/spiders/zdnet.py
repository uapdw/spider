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
  
  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tWebArticles = infoDB.web_articles

  rules = (
    Rule(SgmlLinkExtractor(allow=r'(security|cloud|cio|soft|stor-age)\.zdnet\.com\.cn/(.*)\d{4}/\d{4}/\d+.shtml'), callback='parse_item'),
  )

  def parse_item(self, response):
    print "enter zdnet_parse_item...."
    sel = Selector(response)
    i = WebArticleItem()

    title = sel.xpath('//h1/text()').extract()
    i['title'] = len(title)>0 and title[0].strip() or ''

    i['url'] = response.url

    author = sel.xpath('//div[@class="qu_zuo"]/p[1]/a/text()').extract()
    i['author'] = len(author)>0 and author[0] or ''

    info = sel.xpath('//div[@class="qu_zuo"]/p[1]/text()').extract()
    _info = len(info)>0 and info[len(info)-1].split('|') or ''
    
    source = len(_info)>0 and _info[0].strip().replace(u'\u4f5c\u8005\uff1a','@').replace(u'\u6765\u6e90\uff1a','@').split('@') or ''
    i['source'] = len(source)>1 and source[-1] or ''
    if i['author'] == '':
      i['author'] = len(source)>2 and source[-2] or ''
    
    pubTime = len(_info)>1 and _info[1].strip().split()[0] or str(datetime.date.today())
    i['publishTime'] = pubTime.replace(u'\u5e74','-').replace(u'\u6708','-').replace(u'\u65e5','')
    
    abstract = sel.xpath('//p[@class="zhai"]/text()').extract()
    i['abstract'] = len(abstract)>0 and abstract[0] or ''

    keyWordList = sel.xpath('//div[@class="qu_zuo"]/p[@class="guzhu"]/a/text()').extract()
    keyWords = len(keyWordList)>0 and keyWordList[0].strip() or ''
    for key in range(len(keyWordList)-1):
      keyWords = keyWords + '|' + keyWordList[key+1].strip()
    i['keyWords'] = keyWords

    content = sel.xpath('//div[@class="qu_ocn"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'zdnet'

    i['addTime'] = datetime.datetime.now()   

    return i
