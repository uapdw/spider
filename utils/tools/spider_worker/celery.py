from __future__ import absolute_import
from celery import Celery
from celery.schedules import crontab
from celery.task import periodic_task
import subprocess
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Celery('spider_worker')

# import config
# app.config_from_object('config')

app.conf.update(
    BROKER_URL = 'redis://172.20.14.29:6379/0',
    CELERY_RESULT_BACKEND = 'redis://172.20.14.29:6379/0',
    CELERY_TASK_SERIALIZER = 'json',
    CELERY_ACCEPT_CONTENT = ['json'],
    CELERY_RESULT_SERIALIZER = 'json',
    CELERY_TIMEZONE = 'Asia/Shanghai',
    CELERY_ENABLE_UTC = False,
)

host = '172.20.8.115'
userName = 'root'
passWord = 'udh*123'
dataBase = 'uspider_manager'

DB_CONNECT_STRING = "mysql+mysqlconnector://%s:%s@%s:3306/%s?charset=utf8" % (userName, passWord, host, dataBase)
engine = create_engine(DB_CONNECT_STRING)
DBSession = sessionmaker(bind=engine)
session = DBSession()


def sendSpiderTask(funcName, spiderList):
    print '#'*50
    print "Enter %s ...." % funcName
    if len(spiderList) > 0:
        for spider in spiderList:
            spiderId = spider[0]
            spiderName = spider[1]
            print "set spider status to 'pending'...."
            session.execute("update spider_info set status = '%s' where spider_id = '%s'" % ('pending', spider[0]))

            try:
                print "send task: %s %s ...." % (spiderId, spiderName)
                app.send_task('spider_worker.celery.runSpider', args=[spiderId, spiderName])
            except Exception, e:
                print e
    else:
        print "no spiders need to run...."
    print '#'*50


# @periodic_task(run_every=crontab(minute='0', hour=0))
@periodic_task(run_every=crontab(minute='*/2'))
def runSpiderAtMidNight():
    spiderList = session.execute("SELECT spider_id, code_path, schedule_config FROM spider_info where enable=1 and schedule_config = 'once_a_day' and (status = 'init' or status = 'success' or status = 'failed')").fetchall()
    sendSpiderTask('runSpiderAtMidNight', spiderList)


@periodic_task(run_every=crontab(minute='*/1'))
def runLoopSpider():
    spiderList = session.execute("SELECT spider_id, code_path, schedule_config FROM spider_info where enable=1 and schedule_config = 'loop' and (status = 'init' or status = 'success' or status = 'failed')").fetchall()
    sendSpiderTask('runLoopSpider', spiderList)


@app.task(bind=True)
def runSpider(self, spiderId, spiderName):
    print '*'*50
    jobId = self.request.id
    hostName = self.request.hostname
    startTime = datetime.datetime.now()
    strStartTime = datetime.datetime.strftime(startTime, '%Y-%m-%d %H:%M:%S')

    print "set spider status to 'running'...."
    session.execute("update spider_info set status = '%s' where spider_id = '%s'" % ('running', spiderId))
    print "insert data into spider history...."
    session.execute("insert into spider_run_history (history_id, spider_id, start_time, run_host, run_status) values('%s', '%s', '%s', '%s', '%s')" % (jobId, spiderId, strStartTime, hostName, 'running'))

    print "run spider: %s ...." % spiderName
    # subprocess.call(['cd /data0/sourcecode/spider/current;/root/.virtualenvs/spider/bin/scrapy crawl %s' % spiderName], shell=True)
    time.sleep(70)

    endTime = datetime.datetime.now()
    strEndTime = datetime.datetime.strftime(endTime, '%Y-%m-%d %H:%M:%S')
    totalTime = (endTime - startTime).seconds

    print "set spider status to 'success'...."
    session.execute("update spider_info set status = '%s' where spider_id = '%s'" % ('success', spiderId))
    print "set spider history status to 'success'...."
    session.execute("update spider_run_history set end_time = '%s', total_time = '%s', run_status = '%s' where history_id = '%s'" % (strEndTime, totalTime, 'success', jobId))

    print spiderId, spiderName
    print 'job id: %s' % jobId
    print '%s is finished!' % spiderName
    print '*'*50
