# -*- coding: utf-8 -*-

import re
from scrapy.http import Request
from scrapy.spider import Spider

from spider.items import CurrListedCorpItem
from spider.loader.processors import text


class SzseCnCurrListedCorpSpider(Spider):
    name = "szse_cn_curr_listed_corp"
    allowed_domains = ['szse.cn']

    list_url_pattern = 'http://www.szse.cn/szseWeb/ShowReport.szse?CATALOGID=1110&tab1PAGENUM={}&tab1PAGECOUNT={}&tab1RECORDCOUNT={}&TABKEY=tab1'
    page_onclick_re = re.compile(
        "gotoReportPageNo\('1110','tab1',\d+,(\d+),(\d+)\)"
    )

    def start_requests(self):
        yield Request(
            'http://www.szse.cn/szseWeb/ShowReport.szse?CATALOGID=1110&tab1PAGENUM=1&TABKEY=tab1',
            meta={'page': 1}
        )

    def parse(self, response):
        page = response.meta['page']

        page_onclick = response.selector.xpath(
            '//input[contains(@onclick, "goto")][1]/@onclick'
        ).extract()[0]
        match = self.page_onclick_re.match(page_onclick)
        page_count = int(match.group(1))
        record_count = int(match.group(2))

        tr_list = response.selector.xpath(
            '//tr[@class="cls-data-tr"]'
        )

        for tr in tr_list:
            i = CurrListedCorpItem()
            i['stock_cd'] = text(tr.xpath('td[1]').extract()[0])
            i['corp_name'] = text(tr.xpath('td[3]').extract()[0])
            i['indus'] = text(tr.xpath('td[4]').extract()[0])[0]
            i['corp_sname'] = text(tr.xpath('td[2]').extract()[0])
            yield i

        if page >= page_count:
            return

        yield Request(
            self.list_url_pattern.format(page + 1, page_count, record_count),
            meta={'page': page + 1}
        )
