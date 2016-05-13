# -*- coding: utf-8 -*-

import json
import datetime

from scrapy.http import FormRequest
from scrapy.spider import Spider

from spider.items import ProfitTableItem
from spider.db import Session
from spider.models import CurrListedCorp, PeriodList
from spider.loader.processors import text


NO_DATA = '-'


class SseComCnProfitTableSpider(Spider):
    """上交所利润表"""

    name = "sse_com_cn_profit_table"
    allowed_domains = ['sse.com.cn']

    search_url = 'http://listxbrl.sse.com.cn/profit/showmap.do'

    period_notice_type_dict = {
        '3': '5000',
        '0': '4000',
        '1': '1000',
        '2': '4400'
    }
    value_field_pattern = 'value{}'

    name_list = [
        u"营业总收入(元)",
        u"营业收入(元)",
        u"金融资产利息收入(元)",
        u"已赚保费(元)",
        u"手续费及佣金收入(元)",
        u"营业总成本(元)",
        u"营业成本(元)",
        u"金融资产利息支出(元)",
        u"手续费及佣金支出(元)",
        u"退保金(元)",
        u"赔付支出净额(元)",
        u"提取保险合同准备金净额(元)",
        u"保单红利支出(元)",
        u"分保费用(元)",
        u"营业税金及附加(元)",
        u"销售费用(元)",
        u"管理费用(元)",
        u"财务费用(元)",
        u"资产减值损失(元)",
        u"公允价值变动收益(元)",
        u"投资收益(元)",
        u"对联营企业和合营企业的投资收益(元)",
        u"汇兑收益(元)",
        u"营业利润(元)",
        u"营业外收入(元)",
        u"营业外支出(元)",
        u"非流动资产处置净损失(元)",
        u"利润总额(元)",
        u"所得税(元)",
        u"净利润(元)",
        u"归属于母公司所有者的净利润(元)",
        u"少数股东损益(元)",
        u"基本每股收益(元)",
        u"稀释每股收益(元)"
    ]

    name_row_num_dict = {name: index for index, name in enumerate(name_list)}

    name_field_dict = {
        u'营业收入(元)': 'biz_income',
        u'营业成本(元)': 'biz_cost',
        u'销售费用(元)': 'sell_cost',
        u'管理费用(元)': 'manage_cost',
        u'财务费用(元)': 'fin_cost',
        u'资产减值损失(元)': 'ast_devalu_loss',
        u'公允价值变动收益(元)': 'fair_value_chng_net_inc',
        u'投资收益(元)': 'inv_prft',
        u'对联营企业和合营企业的投资收益(元)': 'invest_assoc_joint_comp',
        u'营业利润(元)': 'run_prft',
        u'营业外收入(元)': 'nonbiz_incom',
        u'营业外支出(元)': 'nonbiz_cost',
        u'非流动资产处置净损失(元)': 'ncurrt_ast_dispos_nloss',
        u'利润总额(元)': 'profit_tamt',
        u'所得税(元)': 'income_tax',
        u'净利润(元)': 'net_profit',
        u'归属于母公司所有者的净利润(元)': 'nprf_attrib_parent_corp',
        u'少数股东损益(元)': 'less_intr_income'
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

        i = ProfitTableItem()
        i['stock_cd'] = stock_cd
        i['year'] = year
        i['period'] = period
        i['data_sour'] = '0'

        for name, field in self.name_field_dict.iteritems():
            row_num = self.name_row_num_dict.get(name)
            value = self._get_value(rows, row_num, value_index)
            i[field] = text(value)

        i['modifytime'] = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

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
