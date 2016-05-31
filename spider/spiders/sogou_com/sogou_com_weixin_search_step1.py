# -*- coding: utf-8 -*-

from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class SogouWeixinSearchStep1Spider(CrawlSpider):

    u"""搜狗微信搜索第一步爬虫

    需要配置：
    DOWNLOAD_DELAY = 3
    CONCURRENT_REQUESTS_PER_DOMAIN = 1
    CONCURRENT_REQUESTS = 1

    写入文件（追加）：
    article_links
    profile_links
    """

    name = 'sogou_com_weixin_search_step1'

    allowed_domains = [
        'weixin.sogou.com',
        'mp.weixin.qq.com'
    ]

    rules = (
        Rule(
            LinkExtractor(
                allow=('weixin\.sogou\.com/weixin\?query=\S+&type=2.*'),
                allow_domains=allowed_domains,
                restrict_xpaths=('//*[@id="sogou_next"]')
            ),
            callback='parse_page',
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=('weixin\.sogou\.com/weixin\?query=\S+&type=1.*'),
                allow_domains=allowed_domains,
                restrict_xpaths=('//*[@id="sogou_next"]')
            ),
            callback='parse_page',
            follow=True
        )
    )

    def start_requests(self):
        keywords = [
            u'章源钨业',
            u'有色金属'
        ]

        search_article_pattern = u'http://weixin.sogou.com/weixin?query={}&type=2'
        search_profile_pattern = u'http://weixin.sogou.com/weixin?query={}&type=1'

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Host': 'weixin.sogou.com',
            'Pragma': 'no-cache',
            'Referer': 'http://weixin.sogou.com/antispider/?from=%2fweixin%3Fquery%3d%E6%9C%89%E8%89%B2%E9%87%91%E5%B1%9E%26type%3d2',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
        }

        cookies = {
            'ABTEST': '0|1464681399|v1',
            'IPLOC': 'CN1100',
            'JSESSIONID': 'aaacYPGYSSown_zmo1euv',
            # 'LCLKINT': '3268310',
            # 'LSTMV': '325%2C162',
            'PHPSESSID': 'i4n5g4qiker4raenugd55r82i2',
            'SNUID': '8A5DF4F88E88B99298900CDC8EB7A86B',
            'SUID': '04D07A7560C80D0A00000000574D49BC',
            'SUID': '04D07A752708930A00000000574D49BB',
            'SUIR': '1464682939',
            'SUV': '00677B1B757AD004574D49BC312F5146',
            # 'refresh': '1',
            'seccodeRight': 'success',
            'successCount': '2|Tue, 31 May 2016 12:12:02 GMT',
            # 'seccodeErrorCount': '1|Tue, 31 May 2016 11:01:24 GMT'
        }

        for keyword in keywords:
            yield Request(search_article_pattern.format(keyword), headers=headers, cookies=cookies)
            yield Request(search_profile_pattern.format(keyword), headers=headers, cookies=cookies)

    def parse_page(self, response):
        profile_extractor = LinkExtractor(
            allow=('mp\.weixin\.qq\.com/profile.*'),
            allow_domains=self.allowed_domains
        )

        article_extractor = LinkExtractor(
            allow=('mp\.weixin\.qq\.com/s.*'),
            allow_domains=self.allowed_domains
        )

        profile_links = profile_extractor.extract_links(response)
        article_links = article_extractor.extract_links(response)

        if profile_links:
            with open('profile_links', 'a') as f:
                f.write('\n'.join(
                    [profile_link.url for profile_link in profile_links]
                ))
        if article_links:
            with open('article_links', 'a') as f:
                f.write('\n'.join(
                    [article_link.url for article_link in article_links]
                ))
