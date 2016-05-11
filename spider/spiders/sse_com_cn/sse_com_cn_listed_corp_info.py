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

    row_num_field_dict = {
        0: 'corp_name',
        1: 'legal_reps',
        2: 'reg_addr',
        3: 'post_cd',
        4: 'corp_url',
        5: 'corp_sec',
        6: 'corp_tel',
        7: 'email'
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

        for row_num, field in self.row_num_field_dict.iteritems():
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
