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
