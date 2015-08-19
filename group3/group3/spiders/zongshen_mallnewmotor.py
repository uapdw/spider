# -*- coding: utf-8 -*-

__author__ = 'liufeng'

import re
import json
import datetime

from scrapy import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from group3.items import NewMotorProductItem, NewMotorRateStastisticItem, NewMotorRateDetailItem, NewMotorProductDynamicItem
from thrift.transport.TSocket import TSocket
from thrift.transport.TTransport import TBufferedTransport
from thrift.protocol import TBinaryProtocol
from group3.hbase import Hbase
from group3.hbase.ttypes import *

class ZongShenMallNewMotorSpider(Spider):
  name = "zongshen_mallnewmotor"
  allowed_domains = ["mall.newmotor.com.cn", "www.newmotor.com.cn"]

  start_urls = [
    'http://mall.newmotor.com.cn/motor/'
  ]
    
  custom_settings = {
    'DOWNLOAD_DELAY': 0,
  }
    
  spec_dict = {
    u'发表上市时间：':'release_time',
    u'排量（cc）：':'engine_displacement',
    u'在产/停产：':'production_status',
    u'缸数：':'cylinders_count',
    u'长×宽×高（mm）：':'size',
    u'冲程：':'stroke',
    u'轴距（mm）：':'wheelbase',
    u'冷却方式：':'cooling',
    u'座垫高（mm）：':'seat_height',
    u'压缩比：':'compression_ratio',
    u'制动方式：':'brake',
    u'最大功率（kw/rp/m）：':'maximum_power',
    u'离地间隙（mm）：':'clearance',
    u'最大扭矩（N·m/rp/m）：':'maximum_torque',
    u'空车质量（kg）：':'empty_weight',
    u'供油方式：':'oil_supply',
    u'整备质量（kg）：':'full_weight',
    u'经济油耗（L/100km）：':'fuel_economy',
    u'最高车速（km/h）：':'top_speed',
    u'环保标准：':'environmental_standards',
    u'轮数：':'wheel_count',
    u'启动方式：':'starting_method',
    u'轮辋：':'rim',
    u'离合器形式：':'clutch',
    u'前轮规格：':'front_wheel_size',
    u'变速器型式：':'transmission_type',
    u'后轮规格：':'rear_wheel_size',
    u'可选颜色：':'available_colors',
    u'油箱容量(L)：':'fuel_capacity',
  }
    
  def __init__(self):
    self.host = "172.20.6.61"
    self.port = 9090
    self.transport = TBufferedTransport(TSocket(self.host, self.port))
    self.transport.open()
    self.protocol = TBinaryProtocol.TBinaryProtocol(self.transport)
    self.client = Hbase.Client(self.protocol)

  def __del__(self):
    self.transport.close()

  def parse(self, response):
    return self.parse_brand(response)

  def parse_brand(self, response):
    xpath = XPath(Selector(response))
    brand_link_selector_list = xpath.selector('//*[@class="a-key" and text()="' + u'品牌：' + '"]/../*[@class="a-values"]/*[@class="v-fold"]/ul/li/a')
    for brand_link_selector in brand_link_selector_list:
      brand_link_xpath = XPath(brand_link_selector)
      brand_link = 'http://mall.newmotor.com.cn/motor/' + brand_link_xpath.first('@href')
      brand = brand_link_xpath.first('text()')
      yield Request(brand_link, callback=self.parse_list, meta={'brand': brand})

  def parse_list(self, response):
    xpath = XPath(Selector(response))

    product_link_list = xpath.list('//*[@id="plist"]/ul/li/.//*[@class="p-name"]/a/@href')
    for product_link in product_link_list:
      yield Request(product_link, callback=self.parse_product, meta={'brand': response.meta['brand']})

    next_link = xpath.first('//*[@class="next"]/@href')
    if next_link:
      yield Request('http://mall.newmotor.com.cn/motor/' + next_link, callback=self.parse_list, meta={'brand': response.meta['brand']})

  def parse_product(self, response):

    xpath = XPath(Selector(response))
    i = NewMotorProductItem()

    i['pinlei'] = u'摩托'
    i['dalei'] = u'摩托'
    i['xiaolei'] = u'摩托'

    i['danpin_code'] = re.match('.*/(\d+)\.html', response.url).group(1)
    i['pt_name'] = 'newmotor'
    i['pt_sp_address'] = response.url
    i['name'] = xpath.first('//*[@id="seller"]/dd/a/text()')
    i['brand'] = response.meta['brand']
    i['danpin_name'] = xpath.first('//*[@class="cspz_title"]/h3/text()')
    match = re.match(u'(.+?)\s*参数', i['danpin_name'])
    if match:
      i['danpin_name'] = match.group(1)
    i['danpin_longname'] = xpath.first('//*[@id="name"]/h1/text()')
    i['danpin_photo'] = xpath.first('//*[@id="preview"]/.//img/@src')
    i['danpin_intro'] = xpath.first('//*[@class="detail-content"]')

    spec_list = []
    spec_selector_list = xpath.selector('//*[@class="canshu_Table"]/.//td')
    key = None
    value = None
    for index, spec_selector in enumerate(spec_selector_list):
      spec_xpath = XPath(spec_selector)
      if index % 2 == 0:
        key = spec_xpath.first('text()')
      else:
        value = ''
        try:
          value = spec_xpath.first('text()')
        except:
          pass
        if key:
          self.set_spect(i, key, value)
          spec_list.append((key, value))
    i['danpin_spec'] = ', '.join(key + ': ' + value for (key, value) in spec_list)

    i['danpin_package'] = xpath.first('//*[@class="item-detail"]')
    i['danpin_slogan'] = xpath.first('//*[@id="name"]/strong/text()')

    price_str = xpath.first('//*[@id="vipprice"]/text()')
    if not price_str:
      price_str = xpath.first('//*[@id="new-price"]/text()')

    if u'￥' in price_str:
      price_str = re.sub(u'￥', '', xpath.first('//*[@id="vipprice"]/text()'))
    price_str = price_str.replace(',', '')
    i['danpin_price'] = price_str

    i['danpin_service_tips'] = xpath.first('//*[@class="promise"]')

    yield Request('http://www.newmotor.com.cn/shop/getstock.shtml?action=HasSold&id=' + i['danpin_code'], callback=self.parse_sale, meta={'item': i})

    rsi = NewMotorRateStastisticItem()
    rsi['pt_name'] = i['pt_name']
    rsi['danpin_name'] = i['danpin_name']
    rsi['pt_sp_address'] = i['pt_sp_address']

    yield Request('http://www.newmotor.com.cn/plus/Ajaxs.shtml?action=getproductpingjia&proid=' + i['danpin_code'], callback=self.parse_rate_stastistic, meta={'item': rsi})

    rate_selector_list = xpath.selector('//*[@id="comments-list"]/ul/li[1]/.//*[@class="item"]')

    for rate_selector in rate_selector_list:
      rate_xpath = XPath(rate_selector)
      rdi = NewMotorRateDetailItem()

      rdi['pt_name'] = i['pt_name']
      rdi['danpin_name'] = i['danpin_name']
      rdi['pt_sp_address'] = i['pt_sp_address']
      rdi['com_feel'] = rate_xpath.first('*[@class="i-item"]/*[@class="comment-content"]/*[@class="dl-extra"]/text()')
      rdi['com_id'] = rate_xpath.first('*[@class="user"]/*[@class="u-name"]/text()')
      publis_time_str = rate_xpath.first('.//*[@class="date-comment"]/text()')

      try:
        rdi['com_establish_time'] = datetime.datetime.strptime(publis_time_str, '%Y-%m-%d %H:%M:%S')
      except:
        rdi['com_establish_time'] = datetime.datetime(1970,1,1)

      yield rdi

  def parse_sale(self, response):
    i = response.meta['item']
    i['danpin_sale'] = re.match('document\.write\(\'(\d+)\'\);', response.body).group(1)
    return Request('http://www.newmotor.com.cn/shop/getstock.shtml?id=' + i['danpin_code'], callback=self.parse_stock, meta={'item': i})

  def parse_stock(self, response):
    i = response.meta['item']
    i['danpin_stock'] = re.match('document\.write\(\'(\d+)\'\);', response.body).group(1)
    yield i

    dyni = NewMotorProductDynamicItem()
    dyni['pt_sp_address'] = i['pt_sp_address']
    dyni['pt_name'] = i['pt_name']
    dyni['danpin_name'] = i['danpin_name']
    dyni['crawl_time'] = datetime.date.today()
    dyni['danpin_sale'] = i['danpin_sale']
    dyni['danpin_price'] = i['danpin_price']
    yield dyni

  def parse_rate_stastistic(self, response):
    i = response.meta['item']

    json_str = re.match('var pingjia=(.*)', response.body).group(1)
    json_str = re.sub('\'', '"', json_str)
    rate_dict = json.loads(json_str)

    i['com_count'] = rate_dict['totalpingjia']
    i['positive_com_count'] = rate_dict['haoping']
    i['moderate_com_count'] = rate_dict['zhongping']
    i['negative_com_count'] = rate_dict['chaping']
    yield i
    
  def set_spect(self, item, spec_text, value):
    key = self.spec_dict[spec_text]
    if key == 'release_time':
      try:
        item[key] = datetime.datetime.strptime(value, '%Y-%m-%d')
      except:
        item[key] = datetime.datetime(1970,1,1)
    else:
      item[key] = value

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
    l = self.list(path)
    if l:
      return l[0].strip()
    else:
      return ''
