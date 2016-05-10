# -*- coding: utf-8 -*-

import re

from scrapy.spider import Spider
from spider.items import CninfoCurrListedCorpItem


class CninfoComCnListedCorpInfo(Spider):
    """巨潮网公司列表"""

    name = "cninfo_com_cn_curr_listed_corp"
    allowed_domains = ['cninfo.com.cn']

    start_urls = (
        'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
        'http://www.cninfo.com.cn/information/sz/sme/szsmelclist.html',
        'http://www.cninfo.com.cn/information/sz/cn/szcnlclist.html',
        'http://www.cninfo.com.cn/information/sh/mb/shmblclist.html',
    )

    information_url_pattern = 'http://www.cninfo.com.cn/information/{}/{}.html'

    market_part_code_re = re.compile('.*?\?([a-zA-Z]+)(\d+).*')

    def parse(self, response):
        onclickList = response.selector.xpath(
            '//td[@class="zx_data3"]/a/@onclick'
        ).extract()

        for theStr in onclickList:
            match = self.market_part_code_re.match(theStr)
            i = CninfoCurrListedCorpItem()
            i['stock_cd'] = match.group(2)
            i['market_part'] = match.group(1)
            yield i
