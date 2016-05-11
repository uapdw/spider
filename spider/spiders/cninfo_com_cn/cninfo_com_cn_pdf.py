# -*- coding: utf-8 -*-

from scrapy.http import FormRequest
from scrapy.spider import Spider

from spider.items import PdfItem
from spider.db import Session
from spider.models import CurrListedCorp, PeriodList


class CninfoComCnPdfSpider(Spider):
    """巨潮网pdf"""

    name = "cninfo_com_cn_pdf"
    allowed_domains = ['cninfo.com.cn']

    pdf_search_url = 'http://www.cninfo.com.cn/search/search.jsp'

    market_part_market_type_dict = {
        'szmb': '012002',
        'shmb': '012001',
        'szsme': '012003',
        'szcn': '012015'
    }

    period_notice_type_dict = {
        '3': '010301',
        '0': '010305',
        '1': '010303',
        '2': '010307'
    }

    def start_requests(self):
        session = Session()
        try:
            year_period_list = session.query(
                PeriodList.year, PeriodList.period
            ).all()

            stock_cd_market_part_list = session.query(
                CurrListedCorp.stock_cd, CurrListedCorp.market_part
            ).all()
            for stock_cd_market_part in stock_cd_market_part_list:
                stock_cd = stock_cd_market_part[0]
                market_part = stock_cd_market_part[1]
                for year_period in year_period_list:
                    year = int(year_period[0])
                    period = year_period[1]

                    if period == '4':
                        year += 1
                    start_time = '{}-01-01'.format(year)
                    end_time = '{}-01-01'.format(year+1)

                    formdata = {
                        'orderby': 'date11',
                        'marketType': self.market_part_market_type_dict.get(market_part),
                        'noticeType': self.period_notice_type_dict.get(period),
                        'stockCode': stock_cd,
                        'keyword': '',
                        'startTime': start_time,
                        'endTime': end_time,
                        'pageNo': '1'
                    }
                    print formdata

                    yield FormRequest(
                        url=self.pdf_search_url,
                        formdata=formdata,
                        headers={
                            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                            'Accept-Encoding': 'gzip, deflate',
                            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
                            'Content-Type': 'application/x-www-form-urlencoded',
                            'Host': 'www.cninfo.com.cn',
                            'Origin': 'http://www.cninfo.com.cn',
                            'Referer': 'http://www.cninfo.com.cn/search/search.jsp'
                        },
                        meta={
                            'stock_cd': stock_cd,
                            'year': year,
                            'period': period,
                        },
                        callback=self.parse_search
                    )
        finally:
            session.close()

    def parse_search(self, response):
        pdf_link_list = response.selector.xpath(
            '//*[@class="da_tbl"]//a[contains(@href,  "PDF")]'
        )

        for pdf_link in pdf_link_list:
            url = pdf_link.xpath('@href').extract()[0]
            url = 'http://www.cninfo.com.cn' + url
            title = pdf_link.xpath('text()').extract()[0]

            i = PdfItem()
            i['stock_cd'] = response.meta['stock_cd']
            i['year'] = response.meta['year']
            i['period'] = response.meta['period']
            i['title'] = title
            i['file_urls'] = [{
                'file_url': url,
                'file_name': u'{}_{}_{}_{}.pdf'.format(
                    i['stock_cd'],
                    i['year'],
                    i['period'],
                    i['title']
                )
            }]
            yield i
