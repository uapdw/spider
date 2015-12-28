import datetime
import time
import os
from spider_worker import celery
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector
import uuid
import logging


class SpiderScheduler(object):
  def __init__(self):
    self.host = '172.20.8.115'
    self.userName = 'root'
    self.passWord = 'udh*123'
    self.dataBase = 'uspider_manager'
    
    self.conn = mysql.connector.connect(host=self.host, user=self.userName, password=self.passWord, database=self.dataBase, use_unicode=True)
    self.cursor = self.conn.cursor()


  def __del__(self):
    self.cursor.close()
    self.conn.close()


  def runSpider(self):
    self.cursor.execute("SELECT spider_id, code_path, schedule_config FROM spider_info where enable=1 and schedule_config != 'manual'")
    spiderList = self.cursor.fetchall()
    for spider in spiderList:
      historyId = str(uuid.uuid1())
      spiderId = spider[0]
      spiderName = spider[1]
      scheduleConfig = spider[2]
      startTime = datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d %H:%M:%S')
      runStatus = 'running'



      print "insert into spider_run_history (history_id, spider_id, start_time, run_status) values('%s', '%s', '%s', '%s')" % (historyId, spiderId, startTime, runStatus)
      self.cursor.execute("insert into spider_run_history (history_id, spider_id, start_time, run_status) values('%s', '%s', '%s', '%s')" % (historyId, spiderId, startTime, runStatus))
      
      print spiderId, spiderName, scheduleConfig

      # add spider into the queue
      try:
        # res = celery.runSpider.apply_async(args=[historyId, spiderName, startTime])
        res = celery.add.apply_async(args=[3, 5])
      except Exception, e:
        print e
      

      print res
      # print res.ready()
      print res.id
      # print 'Is task failed? %s' % res.failed()
      # print 'Is task suceed? %s' % res.successful()
      # print 'task state: %s' % res.state

    print('The time is: %s' % datetime.datetime.now())
    print '#'*50


  def checkSpiderStatus(self):

    pass


class SchedulerErrListener(object):
  def errListener(ev):
    errLogger = logging.getLogger('schedErrJob')
    if ev.exception:
      errLogger.exception('%s error.', str(ev.job))
    else:
      errLogger.info('%s miss', str(ev.job))
    
    

if __name__ == '__main__':
    try:
        spiderScheduler = SpiderScheduler()
        schedulerErrListener = SchedulerErrListener()

        scheduler = BackgroundScheduler()
        scheduler.add_job(spiderScheduler.runSpider, 'interval', seconds=30)
        scheduler.add_listener(schedulerErrListener.errListener, apscheduler.events.EVENT_JOB_ERROR | apscheduler.events.EVENT_JOB_MISSED)
        scheduler.start()

        print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    
        # This is here to simulate application activity (which keeps the main thread alive).
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        # Not strictly necessary if daemonic mode is enabled but should be done if possible
        scheduler.shutdown()
    except Exception,e:
      print e