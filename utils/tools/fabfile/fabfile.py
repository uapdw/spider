# -*- coding: UTF-8 -*-
import os, re
from datetime import datetime
from fabric.api import *
from fabric.contrib.console import confirm

__author__ = 'zhangxind'

_TAR_FILE = 'dist-spider.tar.gz'
_CODE_DIR = os.path.abspath('../../../')
_DIST_DIR = os.path.join(_CODE_DIR, 'utils/dist')
_DIST_FILE_PATH = os.path.join(_DIST_DIR, _TAR_FILE)
_TARGET_PATH = '/data0/sourcecode/spider'
_TARGET_TMP_FILE = '/tmp/%s' % _TAR_FILE
_SUPERVISOR_CONF_PATH = '/etc/supervisor'

env.user = 'root'
env.colorize_errors = True
env.roledefs = {
    'allWorker': [
        '172.20.14.80',
        '172.20.14.93',
        '172.20.14.94',
        '172.20.14.95',
    ],
    'workerPeriod': [
        '172.20.14.80',
        '172.20.14.93',
    ],
    'workerSpider': [
        '172.20.14.80',
        '172.20.14.93',
        '172.20.14.94',
        '172.20.14.95',
    ],
    'workerMail': [
        '172.20.14.94',
        '172.20.14.95',
    ],
    'beat': [
        '172.20.14.80',
    ],
    'flower': [
        '172.20.14.80',
    ]
}


def getNewCode():
    with lcd(_CODE_DIR):
        local('git pull origin develop')


def build():
  includes = ['hbase', '*.txt', '*.cfg', 'spider', 'utils']
  excludes = ['*.pyc','*.tar.gz']
  with settings(warn_only=True):
    if local('test -f %s' % _DIST_FILE_PATH).return_code == 0:
      print 'Remove dist file.'
      local('rm -f %s' % _DIST_FILE_PATH)

    with lcd(_CODE_DIR):
      cmd = ['tar', 'zcvf', _DIST_FILE_PATH]
      cmd.extend(['--exclude=\'%s\'' % i for i in excludes])
      cmd.extend(includes)
      local(' '.join(cmd))


def copyFile():
  newDir = 'spider-%s' % datetime.now().strftime('%Y%m%d_%H%M%S')

  with settings(warn_only=True):
    if run('test -d %s' % _TARGET_PATH).failed:
      run('mkdir -p %s' % _TARGET_PATH)

    run('rm -f %s' % _TARGET_TMP_FILE)
    put(_DIST_FILE_PATH, _TARGET_TMP_FILE)

    with cd(_TARGET_PATH):
      run('mkdir %s' % newDir)
      run('rm -f current')
      run('ln -s %s current' % newDir)

    with cd('%s/%s' % (_TARGET_PATH, newDir)):
      if not run('test -f %s' % _TARGET_TMP_FILE).failed:
        run('tar zxvf %s' % _TARGET_TMP_FILE)

    with cd(_TARGET_PATH):
      run('chown root:root current')
      run('chown -R root:root %s' % newDir)


def copyWorkerSpiderConf():
    run('cp {0}/current/utils/tools/conf/supervisor/worker_spider.conf {1}'.format(_TARGET_PATH, _SUPERVISOR_CONF_PATH))


def copyWorkerPeriodConf():
    run('cp {0}/current/utils/tools/conf/supervisor/worker_period.conf {1}'.format(_TARGET_PATH, _SUPERVISOR_CONF_PATH))


def copyWorkerMailConf():
    run('cp {0}/current/utils/tools/conf/supervisor/worker_mail.conf {1}'.format(_TARGET_PATH, _SUPERVISOR_CONF_PATH))


def copyBeatConf():
    run('cp {0}/current/utils/tools/conf/supervisor/beat.conf {1}'.format(_TARGET_PATH, _SUPERVISOR_CONF_PATH))


def copyFlowerConf():
    run('cp {0}/current/utils/tools/conf/supervisor/flower.conf {1}'.format(_TARGET_PATH, _SUPERVISOR_CONF_PATH))


@task
@parallel(pool_size=5)
@roles('allWorker')
def reloadSupervisor():
    '''重新加载所有节点的supervisor'''
    run('supervisorctl reload')


@task
@roles('allWorker')
def checkSupervisorStatus():
    '''检查所有节点的supervisor状态'''
    run('supervisorctl status')


@task
@roles('allWorker')
def deploySpiderCode():
    '''向所有节点部署爬虫相关代码'''
    getNewCode()
    build()
    copyFile()


@task
@roles('workerSpider')
def deployWorkerSpider():
    '''部署爬虫队列的配置文件'''
    copyWorkerSpiderConf()


@task
@roles('workerPeriod')
def deployWorkerPeriod():
    '''部署定时任务队列的配置文件'''
    copyWorkerPeriodConf()


@task
@roles('workerMail')
def deployWorkerMail():
    '''部署邮件队列的配置文件'''
    copyWorkerMailConf()


@task
@roles('beat')
def deployBeat():
    '''部署beat的配置文件'''
    copyBeatConf()


@task
@roles('flower')
def deployFlower():
    '''部署flower的配置文件'''
    copyFlowerConf()


def deployAllWorkers():
    deployWorkerPeriod()
    deployWorkerMail()
    deployWorkerSpider()
    deployBeat()
    deployFlower()
    reloadSupervisor()


def testEnv():
    print "Executing on %(host)s as %(user)s" % env
