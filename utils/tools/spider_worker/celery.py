# -*- coding: utf-8 -*-

from __future__ import absolute_import

from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
from celery.utils.log import get_task_logger

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from kombu import Exchange, Queue
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .uradar import set_mail_status

import subprocess
import datetime
import time
import smtplib

app = Celery('spider_worker')

# import config
# app.config_from_object('config')

app.conf.update(
    BROKER_URL='redis://172.20.14.29:6379/0',
    CELERY_RESULT_BACKEND='redis://172.20.14.29:6379/1',
    #BROKER_URL='redis://127.0.0.1:6379/0',
    #CELERY_RESULT_BACKEND='redis://127.0.0.1:6379/1',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    CELERY_TIMEZONE='Asia/Shanghai',
    CELERY_ENABLE_UTC=False,
    CELERY_DISABLE_RATE_LIMITS=True,
    BROKER_TRANSPORT_OPTIONS={
        'fanout_prefix': True,
        'fanout_patterns': True,
    },
    CELERY_DEFAULT_QUEUE='default',
    CELERY_QUEUES=(
        Queue('default', Exchange('default'), routing_key='default'),
        Queue('mail', Exchange('mail'), routing_key='mail'),
        Queue('spider', Exchange('spider'), routing_key='spider'),
        Queue('period', Exchange('period'), routing_key='period'),
    ),
    CELERY_ROUTES={
        'spider_worker.celery.sendMail': {'queue': 'mail', 'routing_key': 'mail'},
        'spider_worker.celery.runSpiderAtMidNight': {'queue': 'period', 'routing_key': 'period'},
        'spider_worker.celery.runLoopSpider': {'queue': 'period', 'routing_key': 'period'},
        'spider_worker.celery.runSpider': {'queue': 'spider', 'routing_key': 'spider'},
    },

    # 邮件
    EMAIL_USER = 'info@uradar.com.cn',
    EMAIL_PASSWORD = 'yonyou@123',
    EMAIL_HOST = 'smtp.exmail.qq.com',
    EMAIL_PORT = 465,

    MYSQL_HOST = '127.0.0.1',
    MYSQL_USER = 'root',
    MYSQL_PASSWORD = 'kevenking',
    #MYSQL_HOST = '172.20.8.115',
    #MYSQL_USER = 'root',
    #MYSQL_PASSWORD = 'udh*123',
    MYSQL_DATABASE = 'uspider_manager'
)
app.config = app.conf

logger = get_task_logger(__name__)

def getDBSession():
    '''创建数据库连接'''
    logger.info('connecting to mysql server: {0}'.format(app.config['MYSQL_HOST']))
    dbConnectString = "mysql+mysqlconnector://%s:%s@%s:3306/%s?charset=utf8" % (app.config['MYSQL_USER'], app.config['MYSQL_PASSWORD'], app.config['MYSQL_HOST'], app.config['MYSQL_DATABASE'])
    engine = create_engine(dbConnectString)
    dbSession = sessionmaker(bind=engine)
    return dbSession()


def sendSpiderTask(funcName, spiderList):
    logger.info('#'*50)
    logger.info('Enter {0} ....'.format(funcName))
    if len(spiderList) > 0:
        session = getDBSession()
        for spider in spiderList:
            spiderId = spider[0]
            spiderName = spider[1]
            logger.info("set spider status to 'pending'....")
            session.execute("update spider_info set status = '%s' where spider_id = '%s'" % ('pending', spider[0]))

            try:
                logger.info("send task: {0} {1} ....".format(spiderId, spiderName))
                app.send_task('spider_worker.celery.runSpider', args=[spiderId, spiderName])
            except Exception, e:
                logger.warning("Something's wrong! {0}".format(e))
        session.close()
    else:
        logger.info("no spiders need to run....")
    logger.info('#'*50)


@periodic_task(run_every=crontab(minute=0, hour=0))
def runSpiderAtMidNight():
    session = getDBSession()
    spiderList = session.execute("SELECT spider_id, code_path, schedule_config FROM spider_info where enable=1 and schedule_config = 'once_a_day' and (status = 'init' or status = 'success' or status = 'failed')").fetchall()
    session.close()
    logger.info('send spider to task queue....')
    sendSpiderTask('runSpiderAtMidNight', spiderList)


@periodic_task(run_every=crontab(minute='*/1'))
def runLoopSpider():
    session = getDBSession()
    spiderList = session.execute("SELECT spider_id, code_path, schedule_config FROM spider_info where enable=1 and schedule_config = 'loop' and (status = 'init' or status = 'success' or status = 'failed')").fetchall()
    session.close()
    logger.info('send spider to task queue....')
    sendSpiderTask('runLoopSpider', spiderList)


@app.task(bind=True)
def runSpider(self, spiderId, spiderName):
    logger.info('*'*50)
    jobId = self.request.id
    hostName = self.request.hostname
    startTime = datetime.datetime.now()
    strStartTime = datetime.datetime.strftime(startTime, '%Y-%m-%d %H:%M:%S')

    session = getDBSession()
    logger.info("set spider status to 'running'....")
    session.execute("update spider_info set status = '%s' where spider_id = '%s'" % ('running', spiderId))

    logger.info("insert data into spider history....")
    session.execute("insert into spider_run_history (history_id, spider_id, start_time, run_host, run_status) values('%s', '%s', '%s', '%s', '%s')" % (jobId, spiderId, strStartTime, hostName, 'running'))
    session.close()

    logger.info("run spider: {0} ....".format(spiderName))
    #subprocess.call(['cd /data0/sourcecode/spider/current;/root/.virtualenvs/spider/bin/scrapy crawl {0}'.format(spiderName)], shell=True)
    time.sleep(150)

    endTime = datetime.datetime.now()
    strEndTime = datetime.datetime.strftime(endTime, '%Y-%m-%d %H:%M:%S')
    totalTime = (endTime - startTime).seconds

    session = getDBSession()
    logger.info("set spider status to 'success'....")
    session.execute("update spider_info set status = '%s' where spider_id = '%s'" % ('success', spiderId))
    logger.info("set spider history status to 'success'....")
    session.execute("update spider_run_history set end_time = '%s', total_time = '%s', run_status = '%s' where history_id = '%s'" % (strEndTime, totalTime, 'success', jobId))
    session.close()

    logger.info("Finished! spiderId: {0}, spiderName: {1}, job id: {2}".format(spiderId, spiderName, jobId))
    logger.info('*'*50)


@app.task(bind=True, default_retry_delay=3*60, name='spider_worker.celery.sendMail')
def sendMail(self, subject, mail_to, content, report_send_id=None):
    msgRoot = MIMEMultipart('related')

    # 创建一个实例，这里设置为html格式邮件
    msgText = MIMEText(content, _subtype='html', _charset='utf-8')
    msgRoot.attach(msgText)

    msgRoot['Subject'] = subject
    msgRoot['From'] = app.config['EMAIL_USER']
    msgRoot['To'] = mail_to

    is_success = True
    try:
        s = smtplib.SMTP_SSL(
            app.config['EMAIL_HOST'],
            port=app.config['EMAIL_PORT']
        )

        # 登陆服务器
        s.login(app.config['EMAIL_USER'], app.config['EMAIL_PASSWORD'])

        # 发送邮件
        s.sendmail(app.config['EMAIL_USER'], [mail_to], msgRoot.as_string())
        logger.info('send mail to {}'.format(mail_to))
    except Exception as exc:
        is_success = False
        raise self.retry(exc=exc)
    finally:
        s.close()

    if report_send_id is not None:
        set_mail_status(report_send_id, mail_to, is_success)
