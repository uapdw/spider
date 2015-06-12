from scrapy.http import FormRequest
from scrapy.spider import Spider
from scrapy.selector import Selector
from infomation_crawler.items import WhpjItem
from time import time
import re
import pymongo

class WhpjSpider(Spider):
    name = "whpj"
    allowed_domains = ["boc.cn"]

    conn = pymongo.Connection('172.20.8.3',27017)
    infoDB = conn.info
    tWhpjRate = infoDB.bm_rate

    def start_requests(self):
      reqList = []
      for i in range(1,88484):
	reqList.append(FormRequest('http://srh.bankofchina.com/search/whpj/search.jsp',formdata={'erectDate':'2004-01-01','nothing':'2014-08-01','page':str(i),'pjname':'0'},callback=self.parse_url))

      return reqList

    def parse_url(self, response):
      re_h = re.compile('</?\w+[^>]*>')
      sel = Selector(response)
      trList = sel.xpath('//div[@class="BOC_main publish"]/table/tr')
      for tr in trList:
	tdList = tr.xpath('./td[not(@colspan)]').extract()
	if len(tdList) < 1:
	  continue
	item = WhpjItem()
	item['currentname'] = re_h.sub('',tdList[0].replace(u'\xa0',u'').strip())
	item['price_spot_in'] = re_h.sub('',tdList[1].replace(u'\xa0',u'').strip())
	item['price_cash_in'] = re_h.sub('',tdList[2].replace(u'\xa0',u'').strip())
	item['price_spot_out'] = re_h.sub('',tdList[3].replace(u'\xa0',u'').strip())
	item['price_cash_out'] = re_h.sub('',tdList[4].replace(u'\xa0',u'').strip())
	item['midprice'] = re_h.sub('',tdList[5].replace(u'\xa0',u'').strip())
	item['bocprice'] = re_h.sub('',tdList[6].replace(u'\xa0',u'').strip())
	item['releasetime'] = re_h.sub('',tdList[7].replace(u'\xa0',u'').strip())
	item['note'] = ''
	item['ts'] = int(time())
	yield item

