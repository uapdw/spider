 # -*- coding: utf-8 -*-
import re
from scrapy import Request
import time
from scrapy.contrib.spiders import CrawlSpider
from scrapy.selector import Selector
from spider.db import Session
from sqlalchemy import desc
from spider.models import CurrListedCorp, PeriodList
from spider.items import AsstLiabTableItem

class CnInfoComCnBalanceSpider(CrawlSpider):
    """巨潮资产负债表"""
    name = "cninfo_com_cn_balance"
    allowed_domains = ['cninfo.com.cn']
    monthList = ['-03-31', '-06-30', '-09-30', '-12-31']
    start_urls = (
        'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
        'http://www.cninfo.com.cn/information/sz/sme/szsmelclist.html',
        'http://www.cninfo.com.cn/information/sz/cn/szcnlclist.html',
        'http://www.cninfo.com.cn/information/sh/mb/shmblclist.html',
    )
    # start_urls = [
    #   'http://www.cninfo.com.cn/information/sz/mb/szmblclist.html',
    # ]
    session = Session()
    try: 
        periodlist = session.query(PeriodList).order_by(
             desc(PeriodList.year), desc(PeriodList.period)
            ).all()
        
        stock_cd_market_part_list = session.query(
            CurrListedCorp.stock_cd, CurrListedCorp.market_part
            ).all()
        for stock_cd_market_part in stock_cd_market_part_list:
            stock_cd = stock_cd_market_part[0]
            market_part = stock_cd_market_part[1]
    finally:
        session.close()

  
    balanceSheetColumn = {
    u'货币资金':'curr_fund',
    u'应收票据':'notes_recev',
    u'交易性金融资产':'txn_fin_ast',
    u'应收账款':'reces',
    u'预付款项':'prepay',
    u'其他应收款':'oth_recev',
    u'应收关联公司款':'recev_afflt_account',
    u'应收利息':'recev_intr',
    u'应收股利':'recev_dividn',
    u'存货':'inventy',
    u'其中:消耗性生物资产':'consum_bio_ast',
    u'一年内到期的非流动资产':'oyear_not_current_ast',
    u'其他流动资产':'other_current_ast',
    u'流动资产合计':'current_ast_sum',
    u'可供出售金融资产':'saleable_fin_ast',
    u'持有至到期投资':'hold_investm_due',
    u'长期应收款':'lterm_reces',
    u'长期股权投资':'lterm_equity_investm',
    u'投资性房地产':'real_estate_investm',
    u'固定资产':'fixed_ast',
    u'在建工程':'under_constr_proj',
    u'工程物资':'under_constr_proj',
    u'固定资产清理':'fixed_ast_clean',
    u'生产性生物资产':'prod_bio_ast',
    u'油气资产':'oil_ast',
    u'无形资产':'intang_ast',
    u'开发支出':'develop_costs',
    u'商誉':'goodwill',
    u'长期待摊费用':'deferred_ast',
    u'递延所得税资产':'deferred_tax_ast',
    u'其他非流动资产':'oth_non_current_ast',
    u'非流动资产合计':'non_current_ast_sum',
    u'资产总计':'ast_sum',
    u'短期借款':'sterm_liab',
    u'交易性金融负债':'txn_fin_liab',
    u'应付票据':'notes_payable',
    u'应付帐款':'accounts_payable',
    u'预收款项':'adv_account',
    u'应付职工薪酬':'payroll_payable',
    u'应交税费':'tax_payable',
    u'应付利息':'intr_payable',
    u'应付股利':'dividn_payable',
    u'其他应付款':'oth_payable',
    u'应付关联公司款':'due_related_corp',
    u'一年内到期的非流动负债':'oyear_not_current_liab',
    u'其他流动负债':'oth_current_liab',
    u'流动负债合计':'current_liab_sum',
    u'长期借款':'ltrem_loan',
    u'应付债券':'bonds_payable',
    u'长期应付款':'term_payable',
    u'专项应付款':'spec_payable',
    u'预计负债':'estim_liab',
    u'递延所得税负债':'deferr_inc_tax_liab',
    u'其他非流动负债':'oth_not_current_liab',
    u'非流动负债合计':'not_current_liab_sum',
    u'负债合计':'liab_sum',
    u'实收资本(或股本)':'real_reces_cap',
    u'资本公积':'cap_reserve',
    u'盈余公积':'earned_surplus',
    u'减：库存股':'treas_stock',
    u'未分配利润':'undistr_profit',
    u'少数股东权益':'minority_equity',
    u'外币报表折算价差':'fcurr_trans_spreads',
    u'非正常经营项目收益调整':'abnorm_run_proj_inc_adjust',
    u'所有者权益(或股东权益)合计':'owner_intr_sum',
    u'负债和所有者(或股东权益)合计':'liab_owner_sum'
    }


    def parse(self,response):
        sel = Selector(response)
        onclickList = sel.xpath('//td[@class="zx_data3"]/a/@onclick').extract()
        p = re.compile(r'\d{6}$')
        
        for theStr in onclickList:
            arr = theStr.replace("setLmCode('", '').replace("');", '').split('?')
            code = p.search(arr[1]).group()
            for year in self.periodlist: 
                balanceSheetUrl = 'http://www.cninfo.com.cn/information/stock/balancesheet_.jsp?stockCode='+ code +'&yyyy='+ year.year.encode('utf8') +'&&mm='+ self.monthList[int(year.period.encode('utf8'))] +'&cwzb=balancesheet&button2=%CC%E1%BD%BB'
                #balanceSheetUrl = 'http://www.cninfo.com.cn/information/stock/balancesheet_.jsp?stockCode=002404&yyyy=2015&&mm=-12-31&cwzb=balancesheet&button2=%CC%E1%BD%BB'
                req = Request(balanceSheetUrl, callback=self.parsebalance)
                req.meta['year'] = year.year.encode('utf8')
                req.meta['month'] = year.period.encode('utf8')
                yield req
        

    def parsebalance(self, response):
        sel = Selector(response)
        year = response.meta['year']
        month = response.meta['month']
        tmpStr = sel.xpath('//form[@id="cninfoform"]/table/tr/td/text()').extract()
        if len(tmpStr) < 1:
            return
        stockCode = tmpStr[0].strip()
        stockName = tmpStr[1].strip()
        arrTitle = sel.xpath('//td[@bgcolor="#b8ddf8"]/div/text()').extract()
        arrValue = sel.xpath('//td[@bgcolor="#daf2ff"]/div/text()').extract()
        arrRes = dict([(i.strip(), arrValue[index].strip()) for index, i in enumerate(arrTitle)])

        item = AsstLiabTableItem()
        item['year'] = year
        item['period'] = month
        item['stock_cd'] = stockCode
        item['data_sour'] = '2'
        item['modifytime'] = time.strftime("%Y-%m-%d %H:%M:%S")
        for key in arrRes.keys():
            if key in self.balanceSheetColumn:
                item[self.balanceSheetColumn[key]] = arrRes[key].replace(',','')

        return item
        
