# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://uradar:uradar@172.20.19.132/greatwall?charset=utf8'
SQLALCHEMY_POOL_RECYCLE = 60 * 60 * 2  # 2 hours, same as uradar


engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_recycle=SQLALCHEMY_POOL_RECYCLE,
    encoding='utf-8'
)
Session = sessionmaker(bind=engine)
