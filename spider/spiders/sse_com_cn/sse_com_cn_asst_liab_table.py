# -*- coding: utf-8 -*-

import json

from scrapy.http import FormRequest
from scrapy.spider import Spider

from spider.items import AsstLiabTableItem
from spider.db import Session
from spider.models import CurrListedCorp, PeriodList
from spider.loader.processors import text


NO_DATA = '-'


class SseComCnAsstLiabTableSpider(Spider):
    """上交所资产负债表"""

    name = "sse_com_cn_asst_liab_table"
    allowed_domains = ['sse.com.cn']

    search_url = 'http://listxbrl.sse.com.cn/companyInfo/showBalance.do'

    period_notice_type_dict = {
        '3': '5000',
        '0': '4000',
        '1': '1000',
        '2': '4400'
    }
    value_field_pattern = 'value{}'

    row_num_field_dict = {
        0: 'curr_fund',  # 货币资金(元)
        3: 'txn_fin_ast',  # 交易性金融资产(元)
        4: 'notes_recev',  # 应收票据(元)
        5: 'reces',  # 应收帐款(元)
        6: 'prepay',  # 预付帐款(元)
        10: 'recev_intr',  # 应收利息(元)
        11: 'recev_dividn',  # 应收股利(元)
        12: 'oth_recev',  # 其他应收款(元)
        14: 'inventy',  # 存货(元)
        15: 'oyear_not_current_ast',  # 一年内到期的非流动资产(元)
        16: 'other_current_ast',  # 其他流动资产(元)
        17: 'current_ast_sum',  # 流动资产合计(元)
        19: 'saleable_fin_ast',  # 可供出售金融资产(元)
        21: 'lterm_reces',  # 长期应收款(元)
        22: 'lterm_equity_investm',  # 长期股权投资(元)
        23: 'real_estate_investm',  # 投资性房地产(元)
        24: 'fixed_ast',  # 固定资产净额(元)
        25: 'under_constr_proj',  # 在建工程(元)
        26: 'proj_goods',  # 工程物资(元)
        27: 'fixed_ast_clean',  # 固定资产清理(元)
        28: 'prod_bio_ast',  # 生产性生物资产(元)
        29: 'oil_ast',  # 油气资产(元)
        30: 'intang_ast',  # 无形资产(元)
        31: 'develop_costs',  # 开发支出(元)
        32: 'goodwill',  # 商誉(元)
        33: 'deferred_ast',  # 长期待摊费用(元)
        34: 'deferred_tax_ast',  # 递延税款借项合计(元)
        35: 'oth_non_current_ast',  # 其他长期资产(元)
        36: 'non_current_ast_sum',  # 非流动资产合计(元)
        37: 'ast_sum',  # 资产总计(元)
        38: 'sterm_liab',  # 短期借款(元)
        48: 'payroll_payable',  # 应付职工薪酬(元)
        49: 'tax_payable',  # 应交税金(元)
        50: 'intr_payable',  # 应付利息(元)
        51: 'dividn_payable',  # 应付股利(元)
        52: 'oth_payable',  # 其他应付款(元)
        57: 'oyear_not_current_liab',  # 一年内到期的长期负债(元)
        58: 'oth_current_liab',  # 其他流动负债(元)
        59: 'current_liab_sum',  # 流动负债合计(元)
        60: 'lterm_loan',  # 长期借款(元)
        61: 'bonds_payable',  # 应付债券(元)
        62: 'term_payable',  # 长期应付款(元)
        63: 'spec_payable',  # 专项应付款(元)
        64: 'estim_liab',  # 预计负债(元)
        65: 'deferr_inc_tax_liab',  # 递延税款贷项合计(元)
        66: 'oth_not_current_liab',  # 其他长期负债(元)
        67: 'not_current_liab_sum',  # 长期负债合计(元)
        68: 'liab_sum',  # 负债合计(元)
        69: 'real_reces_cap',  # 股本(元)
        70: 'cap_reserve',  # 资本公积(元)
        71: 'treas_stock',  # 库存股(元)
        72: 'earned_surplus',  # 盈余公积(元)
        74: 'undistr_profit',  # 未分配利润(元)
        75: 'fcurr_trans_spreads',  # 外币报表折算差额(元)
        77: 'minority_equity',  # 少数股东权益(元)
        78: 'owner_intr_sum',  # 股东权益合计(元)
        79: 'liab_owner_sum'  # 负债和股东权益合计(元)
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

        i = AsstLiabTableItem()
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
