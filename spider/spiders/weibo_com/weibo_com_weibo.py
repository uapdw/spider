# -*- coding: utf-8 -*-

import os
import re
import time
import json

from scrapy import Spider, Request
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from pyvirtualdisplay import Display

import spider
from spider.items import UradarWeiboItem


LOAD_MORE_TIMEOUT = 120
WEIBO_URL = 'http://weibo.com'
TARGET_URL = 'http://d.weibo.com/102803_ctg1_5188_-_ctg1_5188'
COOKIES_FILE_NAME = 'cookies.json'


class WeiboLoaded(object):

    def __init__(self, current_count):
        self.current_count = current_count

    def __call__(self, driver):
        return len(
            driver.find_elements_by_xpath('//*[@class="WB_feed"]/div')
        ) > self.current_count


class WeiboComWeiboSpider(Spider):

    name = 'weibo_com_weibo'
    allowed_domains = ['weibo.com']

    start_url = TARGET_URL

    repost_count_matcher = re.compile(u'\s*转发\s*(\d+)')
    comment_count_matcher = re.compile(u'\s*评论\s*(\d+)')

    def start_requests(self):

        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = self.get_driver()
        self.load_cookies(driver)

        cookies = []

        driver.get(WEIBO_URL)
        cookies.extend(driver.get_cookies())

        driver.get(self.start_url)
        item_list = []

        start_time = time.time()

        # 等待加载微博内容
        WebDriverWait(driver, 120).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'WB_feed'))
        )

        # 不是目标url返回
        if driver.current_url != TARGET_URL:
            cookies.extend(driver.get_cookies())
            self.save_cookies(driver, cookies)
            driver.close()
            display.stop()
            return []

        weibo_list = driver.find_elements_by_xpath(
            '//*[@class="WB_feed"]/div[@action-type="feed_list_item"]')

        while not driver.find_elements_by_class_name('W_pages'):

            # 超时时间，保证异常情况下，放弃加载更多内容，跳出循环
            if time.time() - start_time > LOAD_MORE_TIMEOUT:
                break

            try:
                time.sleep(1)
                driver.find_element_by_class_name('WB_empty').click()
                WebDriverWait(driver, 30).until(WeiboLoaded(len(weibo_list)))
                weibo_list = driver.find_elements_by_xpath(
                    '//*[@class="WB_feed"]/div[@action-type="feed_list_item"]')
            except:
                continue

        weibo_list = driver.find_elements_by_xpath(
            '//*[@class="WB_feed"]/div[@action-type="feed_list_item"]')

        for weibo in weibo_list:
            try:
                i = UradarWeiboItem()

                i['weibo_id'] = weibo.get_attribute('mid')
                i['weibo_url'] = weibo.find_element_by_xpath(
                    './/*[contains(@class, "WB_from")]/a'
                ).get_attribute('href')
                i['content'] = weibo.find_element_by_xpath(
                    './/*[contains(@class, "WB_text")]').text
                i['created_at'] = weibo.find_element_by_xpath(
                    './/*[contains(@class, "WB_from")]/a'
                ).get_attribute('title')
                i['user_url'] = weibo.find_element_by_xpath(
                    './/*[@class="WB_info"]/a[1]').get_attribute('href')
                i['screen_name'] = weibo.find_element_by_xpath(
                    './/*[@class="WB_info"]/a[1]').get_attribute('nick-name')
                i['user_pic'] = weibo.find_element_by_xpath(
                    './/*[contains(@class, "WB_face")][1]/div[1]/a/img'
                ).get_attribute('src')

                comments_count = weibo.find_element_by_xpath(
                    '//*[contains(@class, "WB_handle")]/ul/li[3]').text
                match = self.comment_count_matcher.match(comments_count)
                if match:
                    i['comment_count'] = match.group(1)
                else:
                    i['comment_count'] = 0

                reposts_count = weibo.find_element_by_xpath(
                    '//*[contains(@class, "WB_handle")]/ul/li[2]').text
                match = self.repost_count_matcher.match(reposts_count)
                if match:
                    i['repost_count'] = match.group(1)
                else:
                    i['repost_count'] = 0

                item_list.append(i)
            except:
                continue

        cookies.extend(driver.get_cookies())
        self.save_cookies(driver, cookies)
        driver.close()
        display.stop()

        return [Request('http://weibo.com', meta={'item_list': item_list})]

    def parse(self, response):
        return response.meta['item_list']

    def load_cookies(self, driver):
        f = open(self.cookies_file_path(), 'r')
        cookies = json.loads(f.read())
        f.close()

        for cookie in cookies:
            try:
                driver.add_cookie(cookie)
            except:
                continue

    def save_cookies(self, driver, cookies):
        f = open(self.cookies_file_path(), 'w')
        f.write(json.dumps(cookies))
        f.flush()
        f.close()

    def get_driver(self):
        driver = webdriver.Firefox()
        return driver

    def cookies_file_path(self):
        return os.path.join(self.root_path(), COOKIES_FILE_NAME)

    def root_path(self):
        return os.path.abspath(os.path.dirname(spider.__file__))
