# -*- coding: utf-8 -*-

import datetime

from scrapy.item import Item, Field
from scrapy.exceptions import DropItem

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, String, DateTime, DECIMAL, Date, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError as SqlalchemyIntegrityError
from pymysql.err import IntegrityError as PymysqlIntegrityError


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://uradar:uradar@172.20.19.132/greatwall?charset=utf8'
SQLALCHEMY_POOL_RECYCLE = 60 * 60 * 2  # 2 hours, same as uradar


engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_recycle=SQLALCHEMY_POOL_RECYCLE,
    encoding='utf-8'
)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class RequiredFieldItem(Item):
    def validate(self):
        for required_field in self.required_fields:
            if required_field not in self or not self[required_field]:
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

    def add(self):
        self.validate()

        ModelClass = self.model
        session = Session()
        try:
            row = ModelClass()
            for key in self.fields.keys():
                setattr(row, key, self.get(key))
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


class CurrListedCorp(Base):
    __tablename__ = 'curr_listed_corp'

    stock_cd = Column(String(6), primary_key=True)
    corp_name = Column(String(500))
    indus = Column(String(100))

    stock_sname = Column(String(20))
    corp_sname = Column(String(100))


class CurrListedCorpItem(SqlalchemyItem):
    required_fields = ['stock_cd', 'corp_name', 'indus']
    model = CurrListedCorp

    stock_cd = Field()
    corp_name = Field()
    indus = Field()

    stock_sname = Field()
    corp_sname = Field()


class PeriodList(Base):
    __tablename__ = 'period_list'

    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)


class PeriodListItem(SqlalchemyItem):
    required_fields = ['year', 'period']
    model = PeriodList

    year = Field()
    period = Field()


class SpiderProcessInfo(Base):
    __tablename__ = 'spider_process_info'

    corp_stock_cd = Column(String(6), primary_key=True)
    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)
    data_sour = Column(String(1000))


class SpiderProcessInfoItem(SqlalchemyItem):
    required_fields = ['corp_stock_cd', 'year', 'period']
    model = SpiderProcessInfo

    corp_stock_cd = Field()
    year = Field()
    period = Field()
    data_sour = Field()


class ListedCorpInfo(Base):
    __tablename__ = 'listed_corp_info'

    data_sour = Column(String(1000), primary_key=True)
    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)
    stock_cd = Column(String(6), primary_key=True)
    stock_sname = Column(String(20))
    corp_sname = Column(String(50))
    corp_name = Column(String(500))
    eh_name = Column(String(100))
    indus = Column(String(50))
    reg_addr = Column(String(1000))
    corp_url = Column(String(200))
    legal_reps = Column(String(10))
    corp_sec = Column(String(10))
    reg_cap = Column(DECIMAL(24, 2))
    post_cd = Column(String(6))
    corp_tel = Column(String(15))
    corp_fax = Column(String(20))
    email = Column(String(50))
    listed_time = Column(Date)
    raise_cap = Column(Date)
    issue_qty = Column(Integer)
    issue_price = Column(DECIMAL(24, 2))
    issue_pe_ratio = Column(DECIMAL(12, 6))
    issue_way = Column(String(20))
    main_underw = Column(String(50))
    listed_referr = Column(String(50))
    recomm_org = Column(String(100))
    is_crawl = Column(String(2))
    modifytime = Column(String(19))


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


class AsstLiabTable(Base):
    __tablename__ = 'asset_liab_table'

    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)
    stock_cd = Column(String(6), primary_key=True)
    data_sour = Column(String(1000), primary_key=True)
    curr_fund = Column(DECIMAL(24, 2))
    notes_recev = Column(DECIMAL(24, 2))
    txn_fin_ast = Column(DECIMAL(24, 2))
    reces = Column(DECIMAL(24, 2))
    prepay = Column(DECIMAL(24, 2))
    oth_recev = Column(DECIMAL(24, 2))
    recev_afflt_account = Column(DECIMAL(24, 2))
    recev_intr = Column(DECIMAL(24, 2))
    recev_dividn = Column(DECIMAL(24, 2))
    inventy = Column(DECIMAL(24, 2))
    consum_bio_ast = Column(DECIMAL(24, 2))
    oyear_not_current_ast = Column(DECIMAL(24, 2))
    other_current_ast = Column(DECIMAL(24, 2))
    current_ast_sum = Column(DECIMAL(24, 2))
    saleable_fin_ast = Column(DECIMAL(24, 2))
    hold_investm_due = Column(DECIMAL(24, 2))
    lterm_reces = Column(DECIMAL(24, 2))
    lterm_equity_investm = Column(DECIMAL(24, 2))
    real_estate_investm = Column(DECIMAL(24, 2))
    fixed_ast = Column(DECIMAL(24, 2))
    under_constr_proj = Column(DECIMAL(24, 2))
    proj_goods = Column(DECIMAL(24, 2))
    fixed_ast_clean = Column(DECIMAL(24, 2))
    prod_bio_ast = Column(DECIMAL(24, 2))
    oil_ast = Column(DECIMAL(24, 2))
    intang_ast = Column(DECIMAL(24, 2))
    develop_costs = Column(DECIMAL(24, 2))
    goodwill = Column(DECIMAL(24, 2))
    deferred_ast = Column(DECIMAL(24, 2))
    deferred_tax_ast = Column(DECIMAL(24, 2))
    oth_non_current_ast = Column(DECIMAL(24, 2))
    non_current_ast_sum = Column(DECIMAL(24, 2))
    ast_sum = Column(DECIMAL(24, 2))
    sterm_liab = Column(DECIMAL(24, 2))
    txn_fin_liab = Column(DECIMAL(24, 2))
    notes_payable = Column(DECIMAL(24, 2))
    accounts_payable = Column(DECIMAL(24, 2))
    adv_account = Column(DECIMAL(24, 2))
    payroll_payable = Column(DECIMAL(24, 2))
    tax_payable = Column(DECIMAL(24, 2))
    intr_payable = Column(DECIMAL(24, 2))
    dividn_payable = Column(DECIMAL(24, 2))
    oth_payable = Column(DECIMAL(24, 2))
    due_related_corp = Column(DECIMAL(24, 2))
    oyear_not_current_liab = Column(DECIMAL(24, 2))
    oth_current_liab = Column(DECIMAL(24, 2))
    current_liab_sum = Column(DECIMAL(24, 2))
    lterm_loan = Column(DECIMAL(24, 2))
    bonds_payable = Column(DECIMAL(24, 2))
    term_payable = Column(DECIMAL(24, 2))
    spec_payable = Column(DECIMAL(24, 2))
    estim_liab = Column(DECIMAL(24, 2))
    deferr_inc_tax_liab = Column(DECIMAL(24, 2))
    oth_not_current_liab = Column(DECIMAL(24, 2))
    not_current_liab_sum = Column(DECIMAL(24, 2))
    liab_sum = Column(DECIMAL(24, 2))
    real_reces_cap = Column(DECIMAL(24, 2))
    cap_reserve = Column(DECIMAL(24, 2))
    earned_surplus = Column(DECIMAL(24, 2))
    treas_stock = Column(DECIMAL(24, 2))
    undistr_profit = Column(DECIMAL(24, 2))
    minority_equity = Column(DECIMAL(24, 2))
    fcurr_trans_spreads = Column(DECIMAL(24, 2))
    abnorm_run_proj_inc_adjust = Column(DECIMAL(24, 2))
    owner_intr_sum = Column(DECIMAL(24, 2))
    liab_owner_sum = Column(DECIMAL(24, 2))
    modifytime = Column(String(19))


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
    lterm_loan = Field()
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


class ProfitTable(Base):
    __tablename__ = 'profit_table'

    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)
    stock_cd = Column(String(6), primary_key=True)
    data_sour = Column(String(1000), primary_key=True)
    biz_income = Column(DECIMAL(24, 2))
    biz_cost = Column(DECIMAL(24, 2))
    sell_cost = Column(DECIMAL(24, 2))
    manage_cost = Column(DECIMAL(24, 2))
    explor_cost = Column(DECIMAL(24, 2))
    fin_cost = Column(DECIMAL(24, 2))
    ast_devalu_loss = Column(DECIMAL(24, 2))
    fair_value_chng_net_inc = Column(DECIMAL(24, 2))
    inv_prft = Column(DECIMAL(24, 2))
    invest_assoc_joint_comp = Column(DECIMAL(24, 2))
    operat_prft_oth_subj = Column(DECIMAL(24, 2))
    run_prft = Column(DECIMAL(24, 2))
    subs_reven = Column(DECIMAL(24, 2))
    nonbiz_incom = Column(DECIMAL(24, 2))
    nonbiz_cost = Column(DECIMAL(24, 2))
    ncurrt_ast_dispos_nloss = Column(DECIMAL(24, 2))
    oth_subj_affect_total_prft = Column(DECIMAL(24, 2))
    profit_tamt = Column(DECIMAL(24, 2))
    income_tax = Column(DECIMAL(24, 2))
    oth_subj_affect_net_prft = Column(DECIMAL(24, 2))
    net_profit = Column(DECIMAL(24, 2))
    nprf_attrib_parent_corp = Column(DECIMAL(24, 2))
    less_intr_income = Column(DECIMAL(24, 2))
    modifytime = Column(DECIMAL(24, 2))


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


class CashFlowTable(Base):
    __tablename__ = 'cash_flow_table'

    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)
    stock_cd = Column(String(6), primary_key=True)
    data_sour = Column(String(1000), primary_key=True)
    cash_recev_sell_goods = Column(DECIMAL(24, 2))
    refund_taxes = Column(DECIMAL(24, 2))
    cash_recev_oth_run_biz = Column(DECIMAL(24, 2))
    operat_activ_cash_inflows = Column(DECIMAL(24, 2))
    cash_paid_buy_goods = Column(DECIMAL(24, 2))
    tax_paym = Column(DECIMAL(24, 2))
    cash_paid_staff = Column(DECIMAL(24, 2))
    cash_paid_oth_run_biz = Column(DECIMAL(24, 2))
    operat_activ_cash_outflow = Column(DECIMAL(24, 2))
    operat_activ_cash_flow_net = Column(DECIMAL(24, 2))
    cash_recev_invests = Column(DECIMAL(24, 2))
    cash_recev_invest_intr = Column(DECIMAL(24, 2))
    net_cash_recev_disp_fix_ast = Column(DECIMAL(24, 2))
    net_cash_recev_oth_biz = Column(DECIMAL(24, 2))
    recev_oth_invest_activ_cash = Column(DECIMAL(24, 2))
    cash_inflow_invest_activ = Column(DECIMAL(24, 2))
    cash_paid_constr_fixed_ast = Column(DECIMAL(24, 2))
    inv_payment = Column(DECIMAL(24, 2))
    net_cash_acqu_oth_biz_units = Column(DECIMAL(24, 2))
    pay_oth_invest_activ_cash = Column(DECIMAL(24, 2))
    cash_outflow_invest_activ = Column(DECIMAL(24, 2))
    net_cashflow_make_invest_activ = Column(DECIMAL(24, 2))
    cash_recev_invest = Column(DECIMAL(24, 2))
    cash_recev_debts = Column(DECIMAL(24, 2))
    oth_fin_activ_recv_cash = Column(DECIMAL(24, 2))
    fina_activ_cash_inflow = Column(DECIMAL(24, 2))
    debt_payment = Column(DECIMAL(24, 2))
    pay_intr_cash = Column(DECIMAL(24, 2))
    cash_payment_rela_fina_activ = Column(DECIMAL(24, 2))
    cash_outflow_fina_activ = Column(DECIMAL(24, 2))
    ncash_flow_make_fina_activ = Column(DECIMAL(24, 2))
    modifytime = Column(DECIMAL(24, 2))


class CashFlowTableItem(SqlalchemyItem, HBaseItem):
    required_fields = ['stock_cd', 'year', 'period', 'data_sour']
    model = ProfitTable

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


class StockReport(Base):
    __tablename__ = 'stock_report'

    report_id = Column(String(36), primary_key=True)
    stock_code = Column(String(45))
    publish_time = Column(DateTime)
    report_name = Column(String(255))
    pdf_url = Column(String(255))
    pdf_path = Column(String(255))


class StockReportItem(Item):
    stock_code = Field()
    publish_time = Field()
    report_name = Field()

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


class UradarNewsItem(PublishItem):

    def __init__(self):
        super(UradarNewsItem, self).__init__(article_type='1')


class UradarBlogItem(PublishItem):

    def __init__(self):
        super(UradarBlogItem, self).__init__(article_type='3')


class UradarWeixinItem(PublishItem):

    def __init__(self):
        super(UradarWeixinItem, self).__init__(article_type='2')


class UradarReportItem(PublishItem):

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
