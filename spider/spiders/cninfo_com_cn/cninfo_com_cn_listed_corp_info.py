# -*- coding: utf-8 -*-

import datetime

from scrapy.http import Request
from scrapy.spider import Spider

from spider.items import ListedCorpInfoItem, CurrListedCorp


class CninfoComCnListedCorpInfo(Spider):
    name = "cninfo_com_cn_listed_corp_info"
    allowed_domains = ['cninfo.com.cn']

    arrStockInfoColumn = {
        u"公司全称：": "corp_name",
        u"英文名称：": "eh_name",
        u"注册地址：": "reg_addr",
        u"公司简称：": "corp_sname",
        u"法定代表人：": "legal_reps",
        u"公司董秘：": "corp_tel",
        u"注册资本(万元)：": "reg_cap",
        u"行业种类：": "indus",
        u"邮政编码：": "post_cd",
        u"公司电话：": "corp_tel",
        u"公司传真：": "corp_fax",
        u"公司网址：": "corp_url",
        u"上市时间：": "listed_time",
        u"招股时间：": "raise_cap",
        u"发行数量（万股）：": "issue_qty",
        u"发行价格（元）：": "issue_price",
        u"发行市盈率（倍）：": "issue_pe_ratio",
        u"发行方式：": "issue_way",
        u"主承销商：": "main_underw",
        u"上市推荐人：": "listed_referr",
        u"保荐机构：": "recomm_org"
    }

    start_urls = (
        'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
        'http://www.cninfo.com.cn/information/sz/sme/szsmelclist.html',
        'http://www.cninfo.com.cn/information/sz/cn/szcnlclist.html',
        'http://www.cninfo.com.cn/information/sh/mb/shmblclist.html',
    )

    information_url_pattern = 'http://www.cninfo.com.cn/information/{}/{}.html'

    def parse(self, response):
        onclickList = response.selector.xpath(
            '//td[@class="zx_data3"]/a/@onclick'
        ).extract()
        for theStr in onclickList:
            arr = theStr.replace(
                "setLmCode('", ''
            ).replace("');", '').split('?')
            companyInfoUrl = self.information_url_pattern.format(
                arr[0], arr[1]
            )
            yield Request(companyInfoUrl, self.parseCompanyInfo)

    def parseCompanyInfo(self, response):
        tmpStr = response.selector.xpath(
            '//table[@class="table"]/tr/td[@style]/text()'
        ).extract()

        stockCode = tmpStr[0].strip()
        stockName = tmpStr[1].strip().replace(' ', '')

        arr_title = response.selector.xpath(
            '//div[@class="zx_left"]/div/table/tr/td[@class="zx_data"]/text()'
        ).extract()
        arr_value = response.selector.xpath(
            '//div[@class="zx_left"]/div/table/tr/td[@class="zx_data2"]/text()'
        ).extract()
        arr_res = dict(zip(arr_title, arr_value))

        item = ListedCorpInfoItem()
        item['stock_cd'] = stockCode
        item['stock_sname'] = stockName
        item['is_crawl'] = '1'
        item['modifytime'] = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )
        item['data_sour'] = '2'
        item['year'] = '2016'
        item['period'] = '0'

        for title, value in arr_res.iteritems():
            if title in self.arrStockInfoColumn:
                item[self.arrStockInfoColumn[title]] = value.strip()
            else:
                return

        return item
