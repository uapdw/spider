# -*- coding: utf-8 -*-

import re
import json
from scrapy import Request

from scrapy.contrib.spiders import CrawlSpider
#from scrapy.linkextractors import LinkExtractor
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.spiders import Rule

from spider.items import CurrListedCorpItem
from spider.loader.processors import DateProcessor


class SseComCnShListedCorpInfoSpider(CrawlSpider):
    """上交所公司信息"""

    name = "sse_com_cn_sh_listed_corp_info"
    allowed_domains = ['sse.com.cn']

    start_urls = ['http://www.sse.com.cn/assortment/stock/areatrade/trade/']
    rules = [
        Rule(SgmlLinkExtractor(allow=('/assortment/stock/areatrade/trade/detail.shtml')),
             callback='parse_sh')
    ]

    def parse_sh(self, response):
        code = response.url.split('=')[1]
        detail_url = 'http://query.sse.com.cn/security/stock/queryIndustryIndex.do?&csrcCode=%s' % code
        yield Request(detail_url, callback=self.parsefare)

    def parsefare(self, response):
        html = response.body
        i = CurrListedCorpItem()
        html_json = json.loads(html)
        info_detail = []
        compinfo = html_json['result']
        for i in range(len(compinfo)):
            item = CurrListedCorpItem()
            item['stock_cd'] = compinfo[i]['companycode']
            item['corp_name'] = compinfo[i]['fullname']
            item['indus'] = html_json['csrcCode']
            item['data_sour'] = 0
            info_detail.append(item)
        return info_detail






