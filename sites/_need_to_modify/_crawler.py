import logging
# from logger import get_logger
from _database import Database
import time
from selenium import  webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from bs4 import BeautifulSoup
# logger = get_logger(__name__, __file__, 'crawler.log')


class Crawler:
    def __init__(self, hook):
        # logger.info('init Crawler')
        self.hook = hook
        self._crawl('https://www.baidu.com')

    def _crawl(self, url):
        try:
            browser=webdriver.Chrome()
            browser.implicitly_wait(10)
            browser.get("https://search.sina.com.cn/img")
            submit=browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/input[2]")
            print(submit)
            input=browser.find_element_by_xpath("/html/body/div[1]/div[2]/div/form/input[1]")
            print(submit)
            input.send_keys('电影')
            submit.click()
            time.sleep(10)
            soup=BeautifulSoup(browser.page_source)
            imgs=soup.find_all("div",attrs={
                'class': 'cell'
            })
            print(len(imgs))
            for element in imgs:
                img_url=element.find('img').get('src')
                describe=element.find('p').text
                print(img_url)
                print(describe)

            

        except Exception as e:
            logging.error(e)
        self.hook({'url': url, 'data': 'blablabla'})

