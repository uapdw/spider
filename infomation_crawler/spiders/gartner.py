from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.http import Request
from infomation_crawler.items import IndustryReportItem
import datetime
import pymongo

class GartnerSpider(CrawlSpider):
  name = 'gartner'
  allowed_domains = ['gartner.com']
  SCROLLCOUNT=0
  SCROLLFREE=0
  SCROLLPREMIUM=0
 
  def __init__(self, crawl=None, *args, **kwargs):
    super(GartnerSpider, self).__init__(*args, **kwargs)
    self.start_urls = ['http://www.gartner.com/search/site/freecontent/binSearch?binValue=1', 'http://www.gartner.com/search/site/premiumresearch/sort?sortType=date&sortDir=desc']
    if(cmp(crawl, 'all')==0):
      GartnerSpider.SCROLLCOUNT=5

  conn = pymongo.Connection('localhost',27017)
  infoDB = conn.info
  tIndustryReport = infoDB.IndustryReport

  def parse(self, response):
    print "enter gartner_parse_item...."
    sel = Selector(response)
    reportContents = sel.xpath('//table[@class="table searchResults"]/tbody/tr')[0:]
    for report in reportContents:
      reportURL = report.xpath('td/div/h3/a/@href').extract()
      i = IndustryReportItem()
      if(len(reportURL)>0):
        i['title'] = report.xpath('td/div/h3/a/text()').extract()[0].strip()
        i['url'] = report.xpath('td/div/h3/a/@href').extract()[0]
        i['publishTime'] = report.xpath('td/div/h4/text()').extract()[0].strip()
        analysts = report.xpath('td/div/p[@class="results-analyst"]/a/text()').extract()
        infSource = analysts[0].strip()
        for m in range(len(analysts)-1):
           infSource = infSource + '|' + analysts[m+1].strip()
        i['InfSource'] = infSource 
        i['addTime'] = datetime.datetime.now()
        i['siteName'] = 'gartner'
      else:
        i['url'] = ''
        return
      yield IndustryReportItem(i)
    if GartnerSpider.SCROLLFREE < GartnerSpider.SCROLLCOUNT and 'freecontent' in response.url:
      GartnerSpider.SCROLLFREE += 1
      urlFree = 'http://www.gartner.com/search/site/freecontent/scrollResults?&scrollRequestSuccessCount=' + str(GartnerSpider.SCROLLFREE) 
      yield Request(urlFree, callback=self.parse)
    if GartnerSpider.SCROLLPREMIUM < GartnerSpider.SCROLLCOUNT and 'premiumresearch' in response.url:
      GartnerSpider.SCROLLPREMIUM += 1
      urlPremium = 'http://www.gartner.com/search/site/premiumresearch/scrollResults?&scrollRequestSuccessCount=' + str(GartnerSpider.SCROLLPREMIUM) 
      yield Request(urlPremium, callback=self.parse)
