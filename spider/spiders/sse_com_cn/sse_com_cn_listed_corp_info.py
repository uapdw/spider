# -*- coding: utf-8 -*-

import json

from scrapy.http import FormRequest
from scrapy.spider import Spider

from spider.items import ListedCorpInfoItem
from spider.db import Session
from spider.models import CurrListedCorp, PeriodList
from spider.loader.processors import text


NO_DATA = '-'


class SseComCnListedCorpInfoSpider(Spider):
    """上交所公司信息"""

    name = "sse_com_cn_listed_corp_info"
    allowed_domains = ['sse.com.cn']

    search_url = 'http://listxbrl.sse.com.cn/companyInfo/showmap.do'

    period_notice_type_dict = {
        '3': '5000',
        '0': '4000',
        '1': '1000',
        '2': '4400'
    }
    value_field_pattern = 'value{}'

    name_list = [
        u"公司法定中文名称",
        u"公司法定代表人",
        u"公司注册地址",
        u"公司办公地址邮政编码",
        u"公司国际互联网网址",
        u"公司董事会秘书姓名",
        u"公司董事会秘书电话",
        u"公司董事会秘书电子信箱",
        u"报告期末股东总数",
        u"每10股送红股数",
        u"每10股派息数（含税）",
        u"每10股转增数",
        u"本期营业收入(元)",
        u"本期营业利润(元)",
        u"利润总额(元)",
        u"归属于上市公司股东的净利润(元)",
        u"归属于上市公司股东的扣除非经常性损益的净利润(元)",
        u"经营活动产生的现金流量净额(元)",
        u"总资产(元)",
        u"所有者权益（或股东权益）(元)",
        u"基本每股收益(元/股)",
        u"稀释每股收益(元/股)",
        u"扣除非经常性损益后的基本每股收益(元/股)",
        u"全面摊薄净资产收益率（%）",
        u"加权平均净资产收益率（%）",
        u"扣除非经常性损益后全面摊薄净资产收益率（%）",
        u"扣除非经常性损益后的加权平均净资产收益率（%）",
        u"每股经营活动产生的现金流量净额(元/股)",
        u"归属于上市公司股东的每股净资产（元/股）"
    ]

    name_row_num_dict = {name: index for index, name in enumerate(name_list)}

    name_field_dict = {
        u"公司法定中文名称": 'corp_name',
        u"公司法定代表人": 'legal_reps',
        u"公司注册地址": 'reg_addr',
        u"公司办公地址邮政编码": 'post_cd',
        u"公司国际互联网网址": 'corp_url',
        u"公司董事会秘书姓名": 'corp_sec',
        u"公司董事会秘书电话": 'corp_tel',
        u"公司董事会秘书电子信箱": 'email'
    }

    def start_requests(self):
        session = Session()
        try:
            year_period_list = session.query(
                PeriodList.year, PeriodList.period
            ).all()

            stock_cd_list = session.query(CurrListedCorp.stock_cd).filter(
                CurrListedCorp.data_sour == '0'
            ).all()
        finally:
            session.close()

        for stock_cd, in stock_cd_list:
            for year_period in year_period_list:
                year = year_period[0]
                period = year_period[1]

                formdata = {
                    'report_year': year,
                    'stock_id': stock_cd,
                    'report_period_id': self.period_notice_type_dict.get(
                        period
                    )
                }

                yield FormRequest(
                    url=self.search_url,
                    formdata=formdata,
                    # headers={
                    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                    #     'Accept-Encoding': 'gzip, deflate',
                    #     'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                    #     'Content-Type': 'application/x-www-form-urlencoded',
                    #     'Host': 'www.cninfo.com.cn',
                    #     'Origin': 'http://www.cninfo.com.cn',
                    #     'Referer': 'http://www.cninfo.com.cn/search/search.jsp'
                    # },
                    meta={
                        'stock_cd': stock_cd,
                        'year': year,
                        'period': period,
                    },
                    callback=self.parse_search
                )

    def parse_search(self, response):
        stock_cd = response.meta['stock_cd']
        year = response.meta['year']
        period = response.meta['period']

        data = json.loads(response.body)

        value_index = None
        for field_year_dict in data['columns'][0]:
            if year == field_year_dict['title']:
                field = field_year_dict['field']
                value_index = int(field[5:])  # value0 -> 0
                break

        if value_index is None:
            return

        rows = data['rows']

        i = ListedCorpInfoItem()
        i['stock_cd'] = stock_cd
        i['year'] = year
        i['period'] = period
        i['data_sour'] = '0'

        for name, field in self.name_field_dict.iteritems():
            row_num = self.name_row_num_dict.get(name)
            value = self._get_value(rows, row_num, value_index)
            i[field] = text(value)

        yield i

    def _get_value(self, rows, row_num, value_index):
        row = rows[row_num]

        current_index = value_index
        value = NO_DATA
        while value == NO_DATA and current_index >= 0:
            value_field = self.value_field_pattern.format(current_index)
            value = row[value_field]
            current_index -= 1

        if value == NO_DATA:
            value = None

        return value
