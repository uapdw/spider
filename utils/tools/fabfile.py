import os, re
from datetime import datetime
from fabric.api import *
from fabric.contrib.console import confirm

__author__ = 'zhangxind'

env.user = 'root'
env.colorize_errors = True
env.roledefs = {
  'spider-test': ['172.20.8.162'],
  'spider-worker': [
    '172.20.14.80',
    '172.20.14.93',
    '172.20.14.94',
    '172.20.14.95',
  ],
  'spider-beat': [
    '172.20.14.80',
  ],
  'flower': [
    '172.20.14.80',
  ]
}

_TAR_FILE = 'dist-spider.tar.gz'
_CODE_DIR = os.path.abspath('../../')
_DIST_DIR = os.path.join(_CODE_DIR, 'utils/dist')
_DIST_FILE_PATH = os.path.join(_DIST_DIR, _TAR_FILE)
_TARGET_PATH = '/data0/sourcecode/spider'
_TARGET_TMP_FILE = '/tmp/%s' % _TAR_FILE


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


def copySupervisorWorkerConf():
    run('cp /data0/sourcecode/spider/current/utils/tools/conf/supervisor_spider_worker.conf /etc/supervisor')


def copySupervisorBeatConf():
    run('cp /data0/sourcecode/spider/current/utils/tools/conf/supervisor_spider_beat.conf /etc/supervisor')


def copySupervisorFlowerConf():
    run('cp /data0/sourcecode/spider/current/utils/tools/conf/supervisor_flower.conf /etc/supervisor')


def reloadSupervisor():
    run('supervisorctl reload')


def deploySpider():
    getNewCode()
    build()
    copyFile()


def deploySpiderWorker():
    getNewCode()
    build()
    copyFile()
    copySupervisorWorkerConf()
    reloadSupervisor()


def deploySpiderBeat():
    copySupervisorBeatConf()
    reloadSupervisor()


def deployFlower():
    copySupervisorFlowerConf()
    reloadSupervisor()


def testEnv():
    print "Executing on %(host)s as %(user)s" % env



