# -*- coding: utf-8 -*-

import datetime

from scrapy.http import Request
from scrapy.spider import Spider
from sqlalchemy import desc
# from sqlalchemy.orm.exc import NoResultFound

from spider.items import ListedCorpInfoItem
from spider.db import Session
from spider.models import CurrListedCorp, PeriodList


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

    information_url_pattern = 'http://www.cninfo.com.cn/information/brief/{}{}.html'

    def start_requests(self):
        session = Session()
        try:
            stock_cd_market_part_list = session.query(
                CurrListedCorp.stock_cd, CurrListedCorp.market_part
            ).all()

            for stock_cd_market_part in stock_cd_market_part_list:
                stock_cd = stock_cd_market_part[0]
                market_part = stock_cd_market_part[1]
                yield Request(
                    self.information_url_pattern.format(
                        market_part, stock_cd
                    )
                )
        finally:
            session.close()

    def parse(self, response):
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
        item['modifytime'] = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        for title, value in arr_res.iteritems():
            if title in self.arrStockInfoColumn:
                item[self.arrStockInfoColumn[title]] = value.strip()
            else:
                return

        return item
