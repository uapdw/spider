# -*- coding: utf-8 -*-

#
# 首页 http://www.51job.com/default.php -> 高级搜索 //div[@class="spsearch"]/a[1]/@href
# 高级搜索 -> 按地区搜索 //table[@id="typeSearchTbl2"]/a/@href
# 按地区搜索 -> 按地区搜索(发布日期所有) //div[@class="search_left"]/div[2]/div[12]/.//a[text()="所有"]/@href
# 按地区搜索(发布日期所有) -> Job //a[@class="jobname"] , 下一页 //table[@class="navBold"]/.//td[3]/a/@href
#


import re
import datetime
from scrapy.spider import Spider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http import Request
import scrapy
from infomation_crawler.items import HRDataItem
# from thrift.transport.TSocket import TSocket
# from thrift.transport.TTransport import TBufferedTransport
# from thrift.protocol import TBinaryProtocol
# from hbase import Hbase
# from hbase.ttypes import Mutation
# import hashlib

class Job51JobSpider(Spider):
  name = "Job51JobSpider"
  allowed_domains = ["51job.com"]
  start_urls = [
    'http://www.51job.com/'
    # 'http://search.51job.com/job/58704488,c.html'
  ]

  # host = "172.20.8.84"
  # port = 9090
  # transport = TBufferedTransport(TSocket(host, port))
  # transport.open()
  # protocol = TBinaryProtocol.TBinaryProtocol(transport)
  # client = Hbase.Client(protocol)

  def parse(self, response):
    return self.parse_front(response)

  def parse_front(self, response):
    xpath = XPath(Selector(response=response))
    sp_url = xpath.first('//div[@class="spsearch"]/a[1]/@href')
    return Request(sp_url, callback=self.parse_spsearch)

  def parse_spsearch(self, response):
    xpath = XPath(Selector(response=response))
    for area_url in xpath.list('//table[@id="typeSearchTbl2"]/.//a/@href'):
      yield Request(area_url, callback=self.parse_area)

  def parse_area(self, response):
    xpath = XPath(Selector(response=response))
    area_url_alltime = xpath.first('//div[@class="search_left"]/div[2]/div[12]/.//a[text()="' + u'所有' + '"]/@href')
    return Request(area_url_alltime, callback=self.parse_area_alltime)

  def parse_area_alltime(self, response):
    xpath = XPath(Selector(response=response))

    for job_url in xpath.list('//a[@class="jobname"]/@href'):
      meta = {
       'splash': {
            'endpoint': 'render.html',
            'args': {
              'wait': 0.5,
              'images': 0,
              'render_all': 1
            }
        },
        'url': job_url
      }
      yield Request(job_url, callback=self.parse_job, meta=meta)

    next_url = xpath.first('//table[@class="navBold"]/.//td[3]/a/@href')
    if next_url:
      yield Request(next_url, callback=self.parse_area_alltime)

  def parse_job(self, response):
    xpath = XPath(Selector(response=response))

    i = self._init_item()
    i['url'] = response.meta['url']

    i['websource'] = 'www.51job.com'
    i['name_company'] = xpath.first('//*[starts-with(text(), "' + u'查看公司简介' + '")]/../../a/text()')

    klist = xpath.list('//div[@class="s_txt_jobs"]/table[1]/tbody/tr[3]/td[1]/strong/text()')
    vlist = xpath.list('//div[@class="s_txt_jobs"]/table[1]/tbody/tr[3]/td[1]/text()')
    for k, v in zip(klist, vlist):
      if re.match(u'.*公司行业',k):
        i['industry_company'] = v
      elif re.match(u'.*公司性质',k):
        i['type_company'] = v
      elif re.match(u'.*公司规模',k):
        i['scale_company'] = v

    i['website_company'] = xpath.first('//*[starts-with(text(),"' + u'公司网站' + '")]/a/@href')

    text_list = xpath.list('//div[@class="s_txt_jobs"]/div[@class="jobs_com"][2]/div[@class="grayline"]/.//*/text()')
    for text in text_list:
      if re.match(u'.*地.*址.*：', text):
        index = text.index(u'：')
        if index:
          i['address_company'] = text[index + 1:].strip()

    info_list = xpath.list('//div[@class="s_txt_jobs"]/div[@class="jobs_com"][2]/div[@class="grayline"]/div[@class="jobs_txt"]/*[@class="txt_font"]/text()')

    i['info_company'] = '\r\n'.join(info_list)

    # if not i['website_company']:
    #   for info in info_list:
    #     if re.match('.*http://', info):
    #       i['website_company'] = info
    #       break
    #     elif re.match('.*https://', info):
    #       i['website_company'] = info
    #       break

    i['name_position'] = xpath.first('//div[@class="s_txt_jobs"]/table[1]/tbody/tr[1]/td[1]/text()')
    i['keywords_position'] = ' '.join(xpath.list('//*[@class="jobdetail_divRight_span"]/*[@class="position_label"]/text()'))

    klist = xpath.list('//td[@class="txt_1"]/text()')
    vlist = xpath.list('//td[@class="txt_2 "]/text()')
    otherdict = {}
    for k, v in zip(klist, vlist):
      if re.match(u'薪水范围',k):
        i['pay_position'] = v
      elif re.match(u'工作地点',k):
        i['location_position'] = v
      elif re.match(u'发布日期',k):
        try:
          i['release_time'] = datetime.datetime.strptime(v, '%Y-%m-%d')
        except:
          i['release_time'] = datetime.datetime(1970,1,1)
      elif re.match(u'工作年限',k):
        i['experience_position'] = v
      elif re.match(u'学.*历',k):
        i['education_demand'] = v
      elif re.match(u'招聘人数',k):
        i['number_demand'] = v
      else:
        if k not in otherdict:
          otherdict[k] = v
        elif v.strip():
          otherdict[k] = otherdict[k] + ' ' + v.strip()

    # if otherdict:
    #   i['info_position'] = str(otherdict)

    sellist = xpath.selector('//td[contains(@class, "job_detail")]/strong')
    for sel in sellist:
      k = XPath(sel).first('text()')
      if re.match(u'职位职能[：:]', k):
        v = '\r\n'.join(XPath(sel).list('../text()'))
        # v = v[v.index(u'职位职能：') + 6:].strip()
        i['type_position'] = v
      elif re.match(u'职位描述', k):
        info_list = XPath(sel).list('.././/*/text()')
        if len(info_list) <= 1:
          v = ''
        else:
          v = '\r\n'.join(info_list[1:])
        i['jd_position'] = v

    i['welfare_position'] = ' '.join(xpath.list('//*[@class="jobdetail_divRight_span"]/*[@class="Welfare_label"]/text()'))

    i['salary_position'] = '' #pay_position
    i['dutypos'] = '' #jd_position
    i['requiremen_position'] = '' #jd_position
    i['name_contact'] = '' #nil
    i['tele_contact'] = '' #nil
    i['email_contact'] = '' #nil
    i['sex_requrment'] = '' #nil
    i['nature_position'] = '' #nil

    return i

  def _init_item(self):
    i = HRDataItem()
    i['websource'] = ''
    i['name_company'] = ''
    i['scale_company'] = ''
    i['type_company'] = ''
    i['industry_company'] = ''
    i['website_company'] = ''
    i['address_company'] = ''
    i['info_company'] = ''
    i['name_position'] = ''
    i['keywords_position'] = ''
    i['salary_position'] = ''
    i['location_position'] = ''
    i['release_time'] = ''
    i['nature_position'] = ''
    i['experience_position'] = ''
    i['education_demand'] = ''
    i['sex_requrment'] = ''
    i['number_demand'] = ''
    i['type_position'] = ''
    i['jd_position'] = ''
    i['dutypos'] = ''
    i['requiremen_position'] = ''
    i['pay_position'] = ''
    i['welfare_position'] = ''
    i['name_contact'] = ''
    i['tele_contact'] = ''
    i['email_contact'] = ''

    # i['info_position'] = '' #其他职位信息
    return i

class XPath():

  _selecter = None

  def __init__(self, selector):
    self._selecter = selector

  def selector(self, xpath = None):
    if xpath:
      return self._selecter.xpath(xpath)
    else:
      return self._selecter

  def list(self, path):
    return [s.strip() for s in self._selecter.xpath(path).extract() if s.strip()]

  def first(self, path):
    list = self.list(path)
    if list:
      return list[0].strip()
    else:
      return ''