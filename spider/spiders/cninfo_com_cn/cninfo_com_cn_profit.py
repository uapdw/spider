# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import datetime
from scrapy.http import Request
from scrapy.spider import Spider

from spider.items import ProfitTableItem
from spider.db import Session
from spider.models import CurrListedCorp, PeriodList

class StockincomeSpider(Spider):
    name = "cninfo_com_cn_profit"
    allowed_domains = ["cninfo.com.cn"]
    
    arrStockProfitColumn = {
		u"一、营业收入": "biz_income",
        u"减:营业成本": "biz_cost",
        u"销售费用": "sell_cost",
        u"管理费用": "manage_cost",
        u"堪探费用": "explor_cost",
        u"财务费用": "fin_cost",
        u"资产减值损失": "ast_devalu_loss",
        u"加:公允价值变动净收益": "fair_value_chng_net_inc",
        u"投资收益": "inv_prft",
        u"其中:对联营企业和合营企业的投资权益": "invest_assoc_joint_comp",
        u"影响营业利润的其他科目": "operat_prft_oth_subj",
        u"二、营业利润": "run_prft",
        u"加:补贴收入": "subs_reven",
        u"营业外收入": "nonbiz_incom",
        u"减:营业外支出": "nonbiz_cost",
        u"其中:非流动资产处置净损失": "ncurrt_ast_dispos_nloss",
        u"加:影响利润总额的其他科目": "oth_subj_affect_total_prft",
        u"三、利润总额": "profit_tamt",
        u"减:所得税": "income_tax",
        u"加:影响净利润的其他科目": "oth_subj_affect_net_prft",
        u"四、净利润": "net_profit",
        u"归属于母公司所有者的净利润": "nprf_attrib_parent_corp",
        u"少数股东损益": "less_intr_income",
    }

    monthList = ['-03-31', '-06-30', '-09-30', '-12-31']

    profit_url_pattern = 'http://www.cninfo.com.cn/information/stock/incomestatements_.jsp?stockCode={}&yyyy={}&mm={}&cwzb=incomestatements&button2=%CC%E1%BD%BB'

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
                        url=self.profit_url_pattern.format(
                        	stock_cd, year, period_season
                    	),
                    	meta={
                            'stock_cd': stock_cd,
                            'year': year,
                            'period': period,
                        },
                        callback=self.parse_profit
                    )                   
        finally:
            session.close()

    def parse_profit(self, response):
        arr_title = response.selector.xpath(
            '//div[@class="zx_left"]/div[2]/table/tr/td[@bgcolor="#b8ddf8"]/text()'
        ).extract()
        arr_value = response.selector.xpath(
            '//div[@class="zx_left"]/div[2]/table/tr/td[@bgcolor="#daf2ff"]/text()'
        ).extract()
        arr_res = dict(zip(arr_title, arr_value))

        # print response.url

        item = ProfitTableItem()
        item['stock_cd'] = response.meta['stock_cd']
        item['year'] = response.meta['year']
        item['period'] = response.meta['period']
        item['data_sour'] = '2'
       	item['modifytime'] = datetime.datetime.now().strftime(
            '%Y-%m-%d %H:%M:%S'
        )

        for title, value in arr_res.iteritems():
            if title in self.arrStockProfitColumn:
                item[self.arrStockProfitColumn[title]] = value.strip()

        return item
