from sqlalchemy import Column, String, DateTime, DECIMAL, Date, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class CurrListedCorp(Base):
    __tablename__ = 'curr_listed_corp'

    stock_cd = Column(String(6), primary_key=True)
    corp_name = Column(String(500))
    indus = Column(String(100))
    data_sour = Column(String(20))

    stock_sname = Column(String(20))
    corp_sname = Column(String(100))
    market_part = Column(String(10))


class PeriodList(Base):
    __tablename__ = 'period_list'

    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)


class SpiderProcessInfo(Base):
    __tablename__ = 'spider_process_info'

    corp_stock_cd = Column(String(6), primary_key=True)
    year = Column(String(4), primary_key=True)
    period = Column(String(8), primary_key=True)
    data_sour = Column(String(1000))


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
    issue_way = Column(String(200))
    main_underw = Column(String(200))
    listed_referr = Column(String(50))
    recomm_org = Column(String(100))
    modifytime = Column(String(19))


class AsstLiabTable(Base):
    __tablename__ = 'asst_liab_table'

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
    ltrem_loan = Column(DECIMAL(24, 2))
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
    modifytime = Column(String(19))


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
    modifytime = Column(String(19))


class StockReport(Base):
    __tablename__ = 'stock_report'

    report_id = Column(String(36), primary_key=True)
    stock_code = Column(String(45))
    publish_time = Column(DateTime)
    report_name = Column(String(255))
    pdf_url = Column(String(255))
    pdf_path = Column(String(255))
