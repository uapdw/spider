# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import json
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm.exc import NoResultFound


SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:udh*123@172.20.8.115/uradar'
SQLALCHEMY_POOL_RECYCLE = 60 * 60 * 2  # 2 hours, same as uradar


some_engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    pool_recycle=SQLALCHEMY_POOL_RECYCLE
)
Session = sessionmaker(bind=some_engine)
Base = declarative_base()


class ReportSendLog(Base):
    __tablename__ = 'report_send_log'

    report_send_id = Column(String(36), primary_key=True)
    tenant_id = Column(String(36))
    user_id = Column(String(36))
    report_id = Column(String(36))
    report_name = Column(String(255))
    mailgroups = Column(Text)
    report_content = Column(LONGTEXT)
    create_time = Column(DateTime)
    modify_time = Column(DateTime)
    status = Column(String(30))
    mail_status = Column(Text)


def set_mail_status(report_send_id, mail, is_success):
    session = Session()

    try:
        report_send = session.query(ReportSendLog).filter(
            ReportSendLog.report_send_id == report_send_id
        ).with_for_update().one()

        mail_status = json.loads(report_send.mail_status)
        if mail in mail_status:
            if is_success:
                mail_status[mail] = 'success'
            else:
                mail_status[mail] = 'failed'
        report_send.mail_status = json.dumps(mail_status)
        report_send.modify_time = datetime.datetime.now()

        # 总体状态
        finished = True
        failed = False
        for mail, status in mail_status.iteritems():
            if status == 'sending':
                finished = False
            elif status == 'failed':
                failed = True

        if not finished:
            report_send.status = 'sending'
        elif failed:
            report_send.status = 'failed'
        else:
            report_send.status = 'success'

        session.commit()
    except NoResultFound:
        session.rollback()
    finally:
        session.close()
