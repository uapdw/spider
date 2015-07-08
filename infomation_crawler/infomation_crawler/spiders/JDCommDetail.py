# -*- coding: utf-8 -*-
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider,Rule
from infomation_crawler.items import JDCommDetailItem,JDCommDetailReplyItem
from scrapy.http import Request
import datetime
import pymongo
import re
class JDCommDetailSpider(CrawlSpider):
	name = 'JDCommDetail'
	allowed_domain = ['jd.com']
	conn = pymongo.Connection('172.20.8.3',27017)
	infoDB = conn.info
	tJDBaseInfo = infoDB.tJDBaseInfo
	tJdCommDetail = infoDB.tJdCommDetail
	listshop = tJDBaseInfo.find()

	urls = []
	for item in listshop:
		shopid = item['shopid']
		url = 'http://club.jd.com/review/'+ shopid + '-3-1-0.html'
		urls.append(url)

	start_urls = urls

	rules = [
			Rule(SgmlLinkExtractor(allow=(r'http://club.jd.com/review/\d+-3-\d+-0.html'),restrict_xpaths=('//a[@class="next"]')),callback='parse_item',follow=True)
			]

	def parse_item(self, response):
		items = []
		sel = Selector(response)
		commtmpurl = sel.xpath('//div[@class="item"]')[0:]
		for comm in commtmpurl:
			i = JDCommDetailItem()
			satisfaction = comm.xpath('div[@class="i-item"]/div[@class="o-topic"]/span[1]/@class').extract()
			i['satisfaction'] = str(len(satisfaction)>0 and re.findall(r'\d',satisfaction[0])[0] or '')
			if comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/dl/dd/span[@class="comm-tags"]'):
				com_keywords = comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/dl/dd/span[@class="comm-tags"]/span/text()').extract()
				keyWords = len(com_keywords)>0 and com_keywords[0].strip() or ''
				for key in range(len(com_keywords)-1):
					keyWords = keyWords + ',' + com_keywords[key+1].strip()
				i['comkeywords'] = keyWords
				com_feel = comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/dl[2]/dd/text()').extract()
				i['comfeel'] = len(com_feel)>0 and com_feel[0] or ''
				if comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/dl[3]'):
					com_order_show = comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/dl[3]/dd//a[@class="comment-show-pic-wrap"]/@href').extract()
					i['comordershow'] = len(com_order_show)>0 and com_order_show[0] or ''
				else:
					i['comordershow'] = ''
			else:
				com_feel = comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/dl[1]/dd/text()').extract()
				i['comfeel'] = len(com_feel)>0 and com_feel[0] or ''
				if comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/dl[3]'):
					com_order_show = comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/dl[2]/dd//a[@class="comment-show-pic-wrap"]/@href').extract()
					i['comordershow'] = len(com_order_show)>0 and com_order_show[0] or ''
				else:
					i['comordershow'] = ''
				i['comkeywords'] = ''
			com_feel_reply = comm.xpath('div[@class="i-item"]/div[@class="btns"]/a[@class="btn-reply"]/@title').extract()
			i['comfeelreply'] = len(com_feel_reply)>0 and com_feel_reply[0] or ''
			i['com_reply_name'] = []
			i['com_reply_addtime'] = []
			i['com_reply_content'] = []
			com_establish_time = comm.xpath('div[@class="i-item"]//span[@class="date-comment"]/a/text()').extract()
			i['comestablishtime'] = len(com_establish_time)>0 and com_establish_time[0].replace('\r','').replace('\n','') or ''
			if len(comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/div[@class="dl-extra"]/dl').extract()) > 1:
				order_buy_info = comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/div[@class="dl-extra"]/dl[1]/dd/text()').extract()
				i['orderbuyinfo'] = len(order_buy_info)>0 and order_buy_info[0].replace('\r','').replace('\n','') or ''
				order_buy_time = comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/div[@class="dl-extra"]/dl[2]/dd/text()').extract()
				i['orderbuytime'] = len(order_buy_time)>0 and order_buy_time[0].replace('\r','').replace('\n','') or ''
			else:
				i['orderbuyinfo'] = ""
				order_buy_time = comm.xpath('div[@class="i-item"]/div[@class="comment-content"]/div[@class="dl-extra"]/dl/dd/text()').extract()
				i['orderbuytime'] = len(order_buy_time)>0 and order_buy_time[0].replace('\r','').replace('\n','') or ''
			if comm.xpath('div[@class="user"]/div[@class="u-name"]/a'):
				com_id = comm.xpath('div[@class="user"]/div[@class="u-name"]/a/text()').extract()
				i['comid'] = len(com_id)>0 and com_id[0].replace('\r','').replace('\n','') or ''
			else:
				com_id = comm.xpath('div[@class="user"]/div[@class="u-name"]/text()').extract()
				i['comid'] = len(com_id)>0 and com_id[0].replace('\r','').replace('\n','') or ''
			if comm.xpath('div[@class="user"]/span[@class="u-level"]/span'):
				com_id_level = comm.xpath('div[@class="user"]/span[@class="u-level"]/span[1]/text()').extract()
				i['comidlevel'] = len(com_id_level)>0 and com_id_level[0].replace('\r','').replace('\n','') or ''
				com_id_address = comm.xpath('div[@class="user"]/span[@class="u-level"]/span[2]/text()').extract()
				i['comidaddress'] = len(com_id_address)>0 and com_id_address[0].replace('\r','').replace('\n','') or ''
			else:
				i['comidlevel'] = ''
				i['comidaddress'] = ''
			pt_name = 'jd'
			i['ptname'] = pt_name
			danpin_name = sel.xpath('//li[@class="p-name"]/a/text()').extract()
			com_feel_up = comm.xpath('div[@class="i-item"]/div[@class="btns"]//a[@id="agree"]/@title').extract()
			i['com_feel_up'] = len(com_feel_up) and com_feel_up[0] or ''
			i['danpinname'] = len(danpin_name)>0 and danpin_name[0].strip() or ''
			pt_sp_address = 'http://item.jd.com/' + response.url.decode('utf8').split('/')[-1].split('-')[0] + '.html'
			i['ptspaddress'] = pt_sp_address
			#items.append(roy[0])
			#print i
			#print '#'*40

			#items.append(i)
			#items.append(rose)

			if int(com_feel_reply[0])>0:

				if comm.xpath('div[@class="i-item"]/div[@class="ac"]/a').extract():
					flag = 0
					reurl = comm.xpath('div[@class="i-item"]/div[@class="ac"]/a/@href').extract()[0]
					r = Request(reurl,callback=self.parse_reply)
					r.meta['item'] = i
					yield r
				else:
					reply_url = comm.xpath('div[@class="i-item"]/div[@class="item-reply none"]')[0:]
					for reply in reply_url:
						j = {}
						k = {}
						h = {}
						com_reply_name = reply.xpath('div[@class="reply-list"]/div[@class="reply-con"]/span[@class="u-name"]/a/text()').extract()
						com_reply_addtime = reply.xpath('div[@class="reply-list"]/div[@class="reply-meta"]/span[@class="reply-left fl"]/text()').extract()
						com_reply_content = reply.xpath('div[@class="reply-list"]/div[@class="reply-con"]/span[@class="u-con"]/text()').extract()
						j['com_reply_name'] = len(com_reply_name)>0 and com_reply_name[0].replace('\n','').replace('\r','') or ''
						k['com_reply_addtime'] = len(com_reply_addtime)>0 and com_reply_addtime[0].replace('\n','').replace('\r','') or ''
						h['com_reply_content'] = len(com_reply_content)>0 and com_reply_content[0].replace('\n','').replace('\r','') or ''
						i['com_reply_name'].append(j['com_reply_name'])
						#print i['com_reply_name']
						#print '#' * 40
						i['com_reply_addtime'].append(k['com_reply_addtime'])
						i['com_reply_addtime'].append(h['com_reply_content'])
			items.append(i)
			#print '*' * 40


		for item in items:
			yield item

	def parse_reply(self, response):
		sel = Selector(response)
		item = response.meta['item']
		reply_url = sel.xpath('//div[@class="item-reply none"]')[0:]
		for reply in reply_url:
			j = {}
			k = {}
			h = {}
			com_reply_name = reply.xpath('div[@class="reply-list"]/div[@class="reply-con"]/span[@class="u-name"]/a/text()').extract()
			com_reply_addtime = reply.xpath('div[@class="reply-list"]/div[@class="reply-meta"]/span[@class="reply-left fl"]/text()').extract()
			com_reply_content = reply.xpath('div[@class="reply-list"]/div[@class="reply-con"]/span[@class="u-con"]/text()').extract()
			j['com_reply_name'] = len(com_reply_name)>0 and com_reply_name[0].replace('\n','').replace('\r','').strip() or ''
			k['com_reply_addtime'] = len(com_reply_addtime)>0 and com_reply_addtime[0].replace('\n','').replace('\r','').strip() or ''
			h['com_reply_content'] = len(com_reply_content)>0 and com_reply_content[0].replace('\n','').replace('\r','').strip() or ''
			item['com_reply_name'].append(j['com_reply_name'])
			item['com_reply_addtime'].append(k['com_reply_addtime'])
			item['com_reply_content'].append(h['com_reply_content'])

		return item
