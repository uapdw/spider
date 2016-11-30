# -*- coding: utf-8 -*-

import datetime

from decimal import Decimal
from scrapy.item import Item, Field
from scrapy.exceptions import DropItem
from sqlalchemy import DECIMAL, Integer
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError

from spider.models import (CurrListedCorp, PeriodList)
from spider.db import Session


class RequiredFieldItem(Item):
    def validate(self):
        for required_field in self.required_fields:
            if required_field not in self or self[required_field] is None:
                raise DropItem('not field %s' % required_field)


class HBaseItem(RequiredFieldItem):

    # hbase 表名
    table_name = None

    # hbase 列族
    column_family = 'column'

    # md5后作为主键的列
    row_key_field = None

    def get_row_key(self):
        return self[self.row_key_field]


class PM25ChinaItem(HBaseItem):
    table_name = 'dw_weather'
    column_family = 'info'
    required_fields = ['monitor_code', 'publishtime']

    areacode = Field()
    areaname = Field()
    publishtime = Field()
    index_value = Field()
    monitor_code = Field()
    monitor_name = Field()
    monitor_aqi = Field()
    monitor_pm25 = Field()
    monitor_pm10 = Field()
    monitor_key = Field()
    crawltime = Field()

    def get_row_key(self):
        return self['monitor_code'] + self['publishtime']


class SqlalchemyItem(RequiredFieldItem):

    model = None

    def save(self):
        self.validate()

        ModelClass = self.model
        session = Session()
        try:
            row = ModelClass()
            for key in self.fields.keys():
                value = self.get(key)
                if (
                    getattr(
                        ModelClass, key
                    ).property.columns[0].type.__class__ == DECIMAL
                ) and (isinstance(value, str) or isinstance(value, unicode)):
                    if not value:
                        value = None
                    else:
                        value = Decimal(value.replace(',', ''))
                elif (
                    getattr(
                        ModelClass, key
                    ).property.columns[0].type.__class__ == Integer
                ) and (isinstance(value, str) or isinstance(value, unicode)):
                    if not value:
                        value = None
                    else:
                        value = int(value.replace(',', ''))
                setattr(row, key, value)
            session.add(row)
            session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError) as e:
            session.rollback()
            raise DropItem(e.message)
        # except Exception as e:
        #     session.rollback()
        #     raise DropItem(e.message)
        finally:
            session.close()


class CurrListedCorpItem(SqlalchemyItem):
    required_fields = ['stock_cd', 'corp_name', 'indus']
    model = CurrListedCorp

    stock_cd = Field()
    corp_name = Field()
    indus = Field()
    data_sour = Field()

    stock_sname = Field()
    corp_sname = Field()
    market_part = Field()


class CninfoCurrListedCorpItem(SqlalchemyItem):
    required_fields = ['stock_cd', 'market_part']

    stock_cd = Field()
    market_part = Field()

    def save(self):
        self.validate()

        session = Session()
        try:
            session.query(CurrListedCorp).filter(
                CurrListedCorp.stock_cd == self['stock_cd']
            ).update({
                CurrListedCorp.market_part: self['market_part']
            })
            session.commit()
        except (SqlalchemyIntegrityError, PymysqlIntegrityError) as e:
            session.rollback()
            raise DropItem(e.message)
        # except Exception as e:
        #     session.rollback()
        #     raise DropItem(e.message)
        finally:
            session.close()


class PeriodListItem(SqlalchemyItem):
    required_fields = ['year', 'period']
    model = PeriodList

    year = Field()
    period = Field()


class ListedCorpInfoItem(HBaseItem):
    required_fields = ['stock_cd']
    table_name = 'dw_company'
    column_family = 'info'

    stock_cd = Field()
    stock_sname = Field()
    corp_sname = Field()
    corp_name = Field()
    eh_name = Field()
    indus = Field()
    reg_addr = Field()
    corp_url = Field()
    legal_reps = Field()
    corp_sec = Field()
    reg_cap = Field()
    post_cd = Field()
    corp_tel = Field()
    corp_fax = Field()
    email = Field()
    listed_time = Field()
    raise_cap = Field()
    issue_qty = Field()
    issue_price = Field()
    issue_pe_ratio = Field()
    issue_way = Field()
    main_underw = Field()
    listed_referr = Field()
    recomm_org = Field()
    modifytime = Field()

    def get_row_key(self):
        return self['stock_cd']


class AsstLiabTableItem(HBaseItem):
    required_fields = ['stock_cd', 'year', 'period']

    table_name = 'dw_balance'
    column_family = 'balance'

    year = Field()
    period = Field()
    stock_cd = Field()
    curr_fund = Field()
    notes_recev = Field()
    txn_fin_ast = Field()
    reces = Field()
    prepay = Field()
    oth_recev = Field()
    recev_afflt_account = Field()
    recev_intr = Field()
    recev_dividn = Field()
    inventy = Field()
    consum_bio_ast = Field()
    oyear_not_current_ast = Field()
    other_current_ast = Field()
    current_ast_sum = Field()
    saleable_fin_ast = Field()
    hold_investm_due = Field()
    lterm_reces = Field()
    lterm_equity_investm = Field()
    real_estate_investm = Field()
    fixed_ast = Field()
    under_constr_proj = Field()
    proj_goods = Field()
    fixed_ast_clean = Field()
    prod_bio_ast = Field()
    oil_ast = Field()
    intang_ast = Field()
    develop_costs = Field()
    goodwill = Field()
    deferred_ast = Field()
    deferred_tax_ast = Field()
    oth_non_current_ast = Field()
    non_current_ast_sum = Field()
    ast_sum = Field()
    sterm_liab = Field()
    txn_fin_liab = Field()
    notes_payable = Field()
    accounts_payable = Field()
    adv_account = Field()
    payroll_payable = Field()
    tax_payable = Field()
    intr_payable = Field()
    dividn_payable = Field()
    oth_payable = Field()
    due_related_corp = Field()
    oyear_not_current_liab = Field()
    oth_current_liab = Field()
    current_liab_sum = Field()
    ltrem_loan = Field()
    bonds_payable = Field()
    term_payable = Field()
    spec_payable = Field()
    estim_liab = Field()
    deferr_inc_tax_liab = Field()
    oth_not_current_liab = Field()
    not_current_liab_sum = Field()
    liab_sum = Field()
    real_reces_cap = Field()
    cap_reserve = Field()
    earned_surplus = Field()
    treas_stock = Field()
    undistr_profit = Field()
    minority_equity = Field()
    fcurr_trans_spreads = Field()
    abnorm_run_proj_inc_adjust = Field()
    owner_intr_sum = Field()
    liab_owner_sum = Field()
    modifytime = Field()

    def get_row_key(self):
        return '%s_%s_%s' % (
            self['stock_cd'],
            self['year'],
            self['period']
        )


class ProfitTableItem(HBaseItem):
    required_fields = ['stock_cd', 'year', 'period']
    table_name = 'dw_profit'
    column_family = 'profit'

    year = Field()
    period = Field()
    stock_cd = Field()
    data_sour = Field()
    biz_income = Field()
    biz_cost = Field()
    sell_cost = Field()
    manage_cost = Field()
    explor_cost = Field()
    fin_cost = Field()
    ast_devalu_loss = Field()
    fair_value_chng_net_inc = Field()
    inv_prft = Field()
    invest_assoc_joint_comp = Field()
    operat_prft_oth_subj = Field()
    run_prft = Field()
    subs_reven = Field()
    nonbiz_incom = Field()
    nonbiz_cost = Field()
    ncurrt_ast_dispos_nloss = Field()
    oth_subj_affect_total_prft = Field()
    profit_tamt = Field()
    income_tax = Field()
    oth_subj_affect_net_prft = Field()
    net_profit = Field()
    nprf_attrib_parent_corp = Field()
    less_intr_income = Field()
    modifytime = Field()

    def get_row_key(self):
        return '%s_%s_%s' % (
            self['stock_cd'],
            self['year'],
            self['period']
        )


class CashFlowTableItem(HBaseItem):
    required_fields = ['stock_cd', 'year', 'period']
    table_name = 'dw_cashflow'
    column_family = 'cash'

    year = Field()
    period = Field()
    stock_cd = Field()
    data_sour = Field()
    cash_recev_sell_goods = Field()
    refund_taxes = Field()
    cash_recev_oth_run_biz = Field()
    operat_activ_cash_inflows = Field()
    cash_paid_buy_goods = Field()
    tax_paym = Field()
    cash_paid_staff = Field()
    cash_paid_oth_run_biz = Field()
    operat_activ_cash_outflow = Field()
    operat_activ_cash_flow_net = Field()
    cash_recev_invests = Field()
    cash_recev_invest_intr = Field()
    net_cash_recev_disp_fix_ast = Field()
    net_cash_recev_oth_biz = Field()
    recev_oth_invest_activ_cash = Field()
    cash_inflow_invest_activ = Field()
    cash_paid_constr_fixed_ast = Field()
    inv_payment = Field()
    net_cash_acqu_oth_biz_units = Field()
    pay_oth_invest_activ_cash = Field()
    cash_outflow_invest_activ = Field()
    net_cashflow_make_invest_activ = Field()
    cash_recev_invest = Field()
    cash_recev_debts = Field()
    oth_fin_activ_recv_cash = Field()
    fina_activ_cash_inflow = Field()
    debt_payment = Field()
    pay_intr_cash = Field()
    cash_payment_rela_fina_activ = Field()
    cash_outflow_fina_activ = Field()
    ncash_flow_make_fina_activ = Field()
    modifytime = Field()

    def get_row_key(self):
        return '%s_%s_%s' % (
            self['stock_cd'],
            self['year'],
            self['period']
        )
