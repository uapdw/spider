# -*- coding: utf-8 -*-

import json
import datetime

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

    name_list = [
        u"货币资金(元)",
        u"结算备付金(元)",
        u"拆出资金(元)",
        u"交易性金融资产(元)",
        u"应收票据(元)",
        u"应收帐款(元)",
        u"预付帐款(元)",
        u"应收保费(元)",
        u"应收分保账款(元)",
        u"应收分保合同准备金(元)",
        u"应收利息(元)",
        u"应收股利(元)",
        u"其他应收款(元)",
        u"买入返售金融资产(元)",
        u"存货(元)",
        u"一年内到期的非流动资产(元)",
        u"其他流动资产(元)",
        u"流动资产合计(元)",
        u"发放贷款和垫款(元)",
        u"可供出售金融资产(元)",
        u"持有至到期投资(元)",
        u"长期应收款(元)",
        u"长期股权投资(元)",
        u"投资性房地产(元)",
        u"固定资产净额(元)",
        u"在建工程(元)",
        u"工程物资(元)",
        u"固定资产清理(元)",
        u"生产性生物资产(元)",
        u"油气资产(元)",
        u"无形资产(元)",
        u"开发支出(元)",
        u"商誉(元)",
        u"长期待摊费用(元)",
        u"递延税款借项合计(元)",
        u"其他长期资产(元)",
        u"非流动资产合计(元)",
        u"资产总计(元)",
        u"短期借款(元)",
        u"向中央银行借款(元)",
        u"吸收存款及同业存放(元)",
        u"拆入资金(元)",
        u"交易性金融负债(元)",
        u"应付票据(元)",
        u"应付帐款(元)",
        u"预收帐款(元)",
        u"卖出回购金融资产款(元)",
        u"应付手续费及佣金(元)",
        u"应付职工薪酬(元)",
        u"应交税金(元)",
        u"应付利息(元)",
        u"应付股利(元)",
        u"其他应付款(元)",
        u"应付分保账款(元)",
        u"保险合同准备金(元)",
        u"代理买卖证券款(元)",
        u"代理承销证券款(元)",
        u"一年内到期的长期负债(元)",
        u"其他流动负债(元)",
        u"流动负债合计(元)",
        u"长期借款(元)",
        u"应付债券(元)",
        u"长期应付款(元)",
        u"专项应付款(元)",
        u"预计负债(元)",
        u"递延税款贷项合计(元)",
        u"其他长期负债(元)",
        u"长期负债合计(元)",
        u"负债合计(元)",
        u"股本(元)",
        u"资本公积(元)",
        u"库存股(元)",
        u"盈余公积(元)",
        u"一般风险准备(元)",
        u"未分配利润(元)",
        u"外币报表折算差额(元)",
        u"归属于母公司所有者权益合计(元)",
        u"少数股东权益(元)",
        u"股东权益合计(元)",
        u"负债和股东权益合计(元)"
    ]

    name_row_num_dict = {name: index for index, name in enumerate(name_list)}

    name_field_dict = {
        u"应付债券(元)": "bonds_payable",
        u"商誉(元)": "goodwill",
        u"应收利息(元)": "recev_intr",
        u"长期借款(元)": "ltrem_loan",
        u"资本公积(元)": "cap_reserve",
        u"流动负债合计(元)": "current_liab_sum",
        u"盈余公积(元)": "earned_surplus",
        u"其他长期负债(元)": "oth_not_current_liab",
        u"应付利息(元)": "intr_payable",
        u"在建工程(元)": "under_constr_proj",
        u"货币资金(元)": "curr_fund",
        u"生产性生物资产(元)": "prod_bio_ast",
        u"预付帐款(元)": "prepay",
        u"工程物资(元)": "proj_goods",
        u"应收票据(元)": "notes_recev",
        u"油气资产(元)": "oil_ast",
        u"应收股利(元)": "recev_dividn",
        u"长期应收款(元)": "lterm_reces",
        u"预计负债(元)": "estim_liab",
        u"未分配利润(元)": "undistr_profit",
        u"资产总计(元)": "ast_sum",
        u"负债和股东权益合计(元)": "liab_owner_sum",
        u"股本(元)": "real_reces_cap",
        u"递延税款借项合计(元)": "deferred_tax_ast",
        u"非流动资产合计(元)": "non_current_ast_sum",
        u"一年内到期的非流动资产(元)": "oyear_not_current_ast",
        u"长期应付款(元)": "term_payable",
        u"股东权益合计(元)": "owner_intr_sum",
        u"存货(元)": "inventy",
        u"其他流动资产(元)": "other_current_ast",
        u"固定资产净额(元)": "fixed_ast",
        u"少数股东权益(元)": "minority_equity",
        u"一年内到期的长期负债(元)": "oyear_not_current_liab",
        u"外币报表折算差额(元)": "fcurr_trans_spreads",
        u"其他应付款(元)": "oth_payable",
        u"无形资产(元)": "intang_ast",
        u"长期负债合计(元)": "not_current_liab_sum",
        u"应付股利(元)": "dividn_payable",
        u"其他长期资产(元)": "oth_non_current_ast",
        u"应付职工薪酬(元)": "payroll_payable",
        u"库存股(元)": "treas_stock",
        u"负债合计(元)": "liab_sum",
        u"交易性金融资产(元)": "txn_fin_ast",
        u"长期股权投资(元)": "lterm_equity_investm",
        u"应交税金(元)": "tax_payable",
        u"专项应付款(元)": "spec_payable",
        u"长期待摊费用(元)": "deferred_ast",
        u"应收帐款(元)": "reces",
        u"固定资产清理(元)": "fixed_ast_clean",
        u"可供出售金融资产(元)": "saleable_fin_ast",
        u"短期借款(元)": "sterm_liab",
        u"其他应收款(元)": "oth_recev",
        u"递延税款贷项合计(元)": "deferr_inc_tax_liab",
        u"开发支出(元)": "develop_costs",
        u"投资性房地产(元)": "real_estate_investm",
        u"其他流动负债(元)": "oth_current_liab",
        u"流动资产合计(元)": "current_ast_sum",
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
