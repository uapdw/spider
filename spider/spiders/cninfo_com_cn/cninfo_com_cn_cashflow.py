# -*- coding: utf-8 -*-

import datetime
from scrapy.http import Request
from scrapy.spider import Spider

from spider.items import CashFlowTableItem
from spider.db import Session
from spider.models import CurrListedCorp, PeriodList

class CninfoComCnCashFlowSpiderSpider(Spider):
    name = "cninfo_com_cn_cashflow"
    allowed_domains = ["cninfo.com.cn"]
    
    arrStockCashFlowColumn = {
		u"售商品、提供劳务收到的现金": "cash_recev_sell_goods",
		u"收到的税费返还": "refund_taxes",
		u"收到其他与经营活动有关的现金": "cash_recev_oth_run_biz",
		u"经营活动现金流入小计": "operat_activ_cash_inflows",
		u"购买商品、接受劳务支付的现金": "cash_paid_buy_goods",
		u"支付的各项税费": "tax_paym",
		u"支付给职工以及为职工支付的现金": "cash_paid_staff",
		u"支付其他与经营活动有关的现金": "cash_paid_oth_run_biz",
		u"经营活动现金流出小计": "operat_activ_cash_outflow",
		u"经营活动产生的现金流量净额": "operat_activ_cash_flow_net",
		u"收回投资收到的现金": "cash_recev_invests",
		u"取得投资收益收到的现金": "cash_recev_invest_intr",
		u"处置固定资产、无形资产和其他长期资产收回的现金净额": "net_cash_recev_disp_fix_ast",
		u"处置子公司及其他营业单位收到的现金净额": "net_cash_recev_oth_biz",
		u"收到其他与投资活动有关的现金": "recev_oth_invest_activ_cash",
		u"投资活动现金流入小计": "cash_inflow_invest_activ",
		u"购建固定资产、无形资产和其他长期资产支付的现金": "cash_paid_constr_fixed_ast",
		u"投资支付的现金": "inv_payment",
		u"取得子公司及其他营业单位支付的现金净额": "net_cash_acqu_oth_biz_units",
		u"支付其他与投资活动有关的现金": "pay_oth_invest_activ_cash",
		u"投资活动现金流出小计": "cash_outflow_invest_activ",
		u"投资活动产生的现金流量净额": "net_cashflow_make_invest_activ",
		u"吸收投资收到的现金": "cash_recev_invest",
		u"取得借款收到的现金": "cash_recev_debts",
		u"收到其他与筹资活动有关的现金": "oth_fin_activ_recv_cash",
		u"筹资活动现金流入小计": "fina_activ_cash_inflow",
		u"偿还债务支付的现金": "debt_payment",
		u"分配股利、利润或偿还利息支付的现金": "pay_intr_cash",
		u"支付其他与筹资活动有关的现金": "cash_payment_rela_fina_activ",
		u"筹资活动现金流出小计": "cash_outflow_fina_activ",
		u"筹资活动产生的现金流量净额": "ncash_flow_make_fina_activ"
    }

    monthList = ['-03-31', '-06-30', '-09-30', '-12-31']

    cashflow_url_pattern = 'http://www.cninfo.com.cn/information/stock/cashflow_.jsp?stockCode={}&yyyy={}&mm={}&cwzb=cashflow&button2=%CC%E1%BD%BB'

    def start_requests(self):
        session = Session()
        try:
            year_period_list = session.query(
                PeriodList.year, PeriodList.period
            ).all()

            stock_cd_market_part_list = session.query(
                CurrListedCorp.stock_cd
            ).all()
            for stock_cd_market_part in stock_cd_market_part_list:
                stock_cd = stock_cd_market_part[0]
                for year_period in year_period_list:
                    year = int(year_period[0])
                    period = year_period[1]
                    period_season = self.monthList[int(period)]
                    yield Request(
                        url=self.cashflow_url_pattern.format(
                        	stock_cd, year, period_season
                    	),
                    	meta={
                            'stock_cd': stock_cd,
                            'year': year,
                            'period': period,
                        },
                        callback=self.parse_cashflow
                    )                   
        finally:
            session.close()


    def parse_cashflow(self, response):
        arr_title = response.selector.xpath(
            '//td[@bgcolor="#b8ddf8"]/text()'
        ).extract()
        arr_value = response.selector.xpath(
            '//td[@bgcolor="#daf2ff"]/text()'
        ).extract()
        arr_res = dict(zip(arr_title, arr_value))

        # print response.url

        item = CashFlowTableItem()
        item['stock_cd'] = response.meta['stock_cd']
        item['year'] = response.meta['year']
        item['period'] = response.meta['period']
        item['data_sour'] = '2'
       	item['modifytime'] = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        for title, value in arr_res.iteritems():
            if title in self.arrStockCashFlowColumn:
                item[self.arrStockCashFlowColumn[title]] = value.strip().replace(',','')

        return item
