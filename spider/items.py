# -*- coding: utf-8 -*-

import datetime

from decimal import Decimal
from scrapy.item import Item, Field
from scrapy.exceptions import DropItem
from sqlalchemy import DECIMAL, Integer
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError

from spider.models import (CurrListedCorp, PeriodList, SpiderProcessInfo,
                           ListedCorpInfo, AsstLiabTable, ProfitTable,
                           CashFlowTable)
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


class PublishItem(HBaseItem):
    def validate(self):
        super(HBaseItem, self).validate()

        publish_time = getattr(self, 'publish_time', None)
        if isinstance(publish_time, datetime.datetime) and \
                publish_time > datetime.datetime.now():
            raise DropItem('invalid publish_time %s' % publish_time)


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


class SpiderProcessInfoItem(SqlalchemyItem):
    required_fields = ['corp_stock_cd', 'year', 'period']
    model = SpiderProcessInfo

    corp_stock_cd = Field()
    year = Field()
    period = Field()
    data_sour = Field()


class ListedCorpInfoItem(SqlalchemyItem, HBaseItem):
    required_fields = ['stock_cd', 'year', 'period', 'data_sour']
    model = ListedCorpInfo

    data_sour = Field()
    year = Field()
    period = Field()
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
    is_crawl = Field()
    modifytime = Field()

    def get_row_key(self):
        return '%s_%s_%s_%s' % (
            self['data_sour'],
            self['year'],
            self['period'],
            self['stock_cd']
        )


class AsstLiabTableItem(SqlalchemyItem, HBaseItem):
    required_fields = ['stock_cd', 'year', 'period', 'data_sour']
    model = AsstLiabTable

    year = Field()
    period = Field()
    stock_cd = Field()
    data_sour = Field()
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
        return '%s_%s_%s_%s' % (
            self['data_sour'],
            self['year'],
            self['period'],
            self['stock_cd']
        )


class ProfitTableItem(SqlalchemyItem, HBaseItem):
    required_fields = ['stock_cd', 'year', 'period', 'data_sour']
    model = ProfitTable

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
        return '%s_%s_%s_%s' % (
            self['data_sour'],
            self['year'],
            self['period'],
            self['stock_cd']
        )


class CashFlowTableItem(SqlalchemyItem, HBaseItem):
    required_fields = ['stock_cd', 'year', 'period', 'data_sour']
    model = CashFlowTable

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
        return '%s_%s_%s_%s' % (
            self['data_sour'],
            self['year'],
            self['period'],
            self['stock_cd']
        )


class PdfItem(Item):
    stock_cd = Field()
    year = Field()
    period = Field()
    title = Field()

    file_urls = Field()
    files = Field()


class UradarWeiboItem(PublishItem):
    table_name = 'uradar_weibo'

    required_fields = ['weibo_id', 'weibo_url', 'content', 'created_at']

    weibo_id = Field()
    weibo_url = Field()
    content = Field()
    created_at = Field()

    user_url = Field()
    screen_name = Field()
    user_pic = Field()

    comment_count = Field()
    repost_count = Field()

    def get_row_key(self):
        return self['weibo_url']


class UradarBBSItem(PublishItem):
    table_name = 'uradar_bbs'
    required_fields = ['thread_id', 'post_id', 'url', 'title', 'content',
                       'publish_time']

    thread_id = Field()
    post_id = Field()

    url = Field()
    title = Field()
    abstract = Field()
    keywords = Field()
    content = Field()
    author = Field()
    publish_time = Field()

    source = Field()

    site_domain = Field()
    site_name = Field()

    sentiment = Field()

    def get_row_key(self):
        return '%s_%s_%s' % (self['site_domain'], self['thread_id'],
                             self['post_id'])


class UradarArticleItem(PublishItem):

    table_name = 'uradar_article'
    row_key_field = 'url'
    required_fields = ['url', 'title', 'content', 'publish_time']

    url = Field()
    title = Field()
    author = Field()
    abstract = Field()
    content = Field()
    publish_time = Field()
    source = Field()  # 文章来源
    keywords = Field()

    article_type = Field()  # 文章类型
    site_domain = Field()
    site_name = Field()

    add_time = Field()
    sentiment = Field()


class UradarNewsItem(UradarArticleItem):

    def __init__(self):
        super(UradarNewsItem, self).__init__(article_type='1')


class UradarBlogItem(UradarArticleItem):

    def __init__(self):
        super(UradarBlogItem, self).__init__(article_type='3')


class UradarWeixinItem(UradarArticleItem):

    def __init__(self):
        super(UradarWeixinItem, self).__init__(article_type='2')


class UradarReportItem(UradarArticleItem):

    def __init__(self):
        super(UradarReportItem, self).__init__(article_type='4')


class UradarActivityItem(HBaseItem):

    table_name = 'uradar_activity'
    row_key_field = 'url'
    required_fields = ['url', 'title', 'start_time', 'end_time']

    url = Field()
    title = Field()
    start_time = Field()
    end_time = Field()
    location = Field()
    trad = Field()
    content = Field()
    keywords = Field()

    source_domain = Field()
    source_name = Field()
    add_time = Field()


class CarComDetailItem(PublishItem):

    table_name = 'car_com_detail'
    row_key_field = 'comment_id'
    required_fields = ['comment_id', 'product_id', 'url', 'content', 'author', 'publish_time']

    comment_id = Field()
    product_id = Field()
    url = Field()
    author = Field()
    content = Field()
    publish_time = Field()
    sentiment = Field()


class CarDanPinItem(HBaseItem):

    table_name = 'car_danpin'
    row_key_field = 'product_id'
    required_fields = ['product_id', 'brand', 'type']

    product_id = Field()
    brand = Field()
    type = Field()
