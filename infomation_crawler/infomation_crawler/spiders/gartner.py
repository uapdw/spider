from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from infomation_crawler.items import IndustryReportItem
import time,datetime
import pymongo

class GartnerSpider(CrawlSpider):
  name = 'gartner'
  allowed_domains = ['gartner.com']
  SCROLLCOUNT=0
  SCROLLFREE=0
  SCROLLPREMIUM=0
 
  def __init__(self, crawl=None, *args, **kwargs):
    super(GartnerSpider, self).__init__(*args, **kwargs)
    self.start_urls = ['http://www.gartner.com/search/site/freecontent/simple', 'http://www.gartner.com/search/site/premiumresearch/sort?sortType=date&sortDir=desc']
    if(cmp(crawl, 'all')==0):
      GartnerSpider.SCROLLCOUNT=5

  conn = pymongo.Connection('172.20.8.3',27017)
  infoDB = conn.info
  tIndustryReport = infoDB.IndustryReport

  def parse_item(self, response):
    sel = Selector(response)
    i = response.meta['item']

    content = sel.xpath('//div[@id="doc-body"]').extract()
    i['content'] = len(content)>0 and content[0] or ''

    i['siteName'] = 'gartner'
    i['source'] = ''
    i['addTime'] = datetime.datetime.now()
    
    return i

  def parse(self, response):
    print "enter gartner_parse_item...."
    sel = Selector(response)
    items = []
    reportContents = sel.xpath('//table[@class="table searchResults"]/tbody/tr')[0:]
    for report in reportContents:
      i = IndustryReportItem()
      
      i['url'] = report.xpath('td/div/h3/a/@href').extract()[0]
 
      title = report.xpath('td/div/h3/a/text()').extract()
      i['title'] = len(title)>0 and title[0].strip() or ''
      
      authorList = report.xpath('td/div/p[@class="results-analyst"]/a/text()').extract()
      authors = len(authorList)>0 and authorList[0].strip() or ''
      for aut in range(len(authorList)-1):
        authors = authors + '|' + authorList[aut+1].strip()
      i['author'] = authors

      abstract = report.xpath('td/div/p[@class="arial result-summary"]/text()').extract()
      i['abstract'] = len(abstract)>0 and abstract[0] or ''

      i['keyWords'] = ''

      pubTime = report.xpath('td/div/h4/text()').extract()
      if len(pubTime)>0:
        t = time.strptime(pubTime[0].strip(), "%d %B %Y")
        y,m,d = t[0:3]
        i['publishTime'] = str(datetime.date(y,m,d))
      else:
        i['publishTime'] = str(datetime.date.today())
      items.append(i)

    for item in items:
      yield Request(item['url'],meta={'item':item},callback=self.parse_item)
    
    if GartnerSpider.SCROLLFREE < GartnerSpider.SCROLLCOUNT and 'freecontent' in response.url:
      GartnerSpider.SCROLLFREE += 1
      urlFree = 'http://www.gartner.com/search/site/freecontent/scrollResults?&scrollRequestSuccessCount=' + str(GartnerSpider.SCROLLFREE) 
      yield Request(urlFree, callback=self.parse)
    
    if GartnerSpider.SCROLLPREMIUM < GartnerSpider.SCROLLCOUNT and 'premiumresearch' in response.url:
      GartnerSpider.SCROLLPREMIUM += 1
      urlPremium = 'http://www.gartner.com/search/site/premiumresearch/scrollResults?&scrollRequestSuccessCount=' + str(GartnerSpider.SCROLLPREMIUM) 
      yield Request(urlPremium, callback=self.parse)
