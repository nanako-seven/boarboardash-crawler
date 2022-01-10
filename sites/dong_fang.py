from typing import Any, Dict, List
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date, datetime
from dataclasses import dataclass
from bs4 import BeautifulSoup
from .site_models import News
import requests


def get_html(driver: webdriver.Firefox, page: int) -> str:
    '''
    page一般取1-4就够了
    '''
    s = '' if page == 1 else str(page - 1)
    driver.get(f'http://news.eastday.com/gd2008/news/index{s}.html')
    el = WebDriverWait(driver, timeout=5).until(
        lambda d: d.find_element(By.CSS_SELECTOR, "#left"))
    return el.get_attribute('innerHTML')


def analyze_html(html: str) -> List[Any]:
    soup = BeautifulSoup(html, 'lxml')
    ans = []
    for li in soup.find_all('li'):
        li: Tag
        info = {}
        a = li.find('a')
        info['category'] = get_tag(a.string)
        if info['category'] == '图片':
            continue
        a: Tag = a.next_sibling
        # news.title = a.string
        info['url'] = a.get('href')
        span: Tag = a.next_sibling
        info['time'] = convert(span.string)
        ans.append(info)
    return ans


def convert(s: str) -> datetime:
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def get_tag(s: str) -> str:
    a = s.find('[')
    a += 1
    b = s.find(']', a)
    return s[a:b]


def get_news_since(driver: webdriver.Firefox, time: datetime) -> List[News]:
    html = get_html(driver, 1)
    news = analyze_html(html)
    i = 0
    while i < len(news):
        if news[i]['time'] <= time:
            break
        i += 1
    r = [analyze_page(x) for x in news[:i]]
    r = [x for x in r if x]
    return r


def analyze_page(news: Dict) -> News:
    '''
    分析一个具体的新闻网页
    '''
    try:
        req = requests.get(news['url'])
        news['raw'] = req.content
        news['encoding'] = req.encoding
        html = req.text
        soup = BeautifulSoup(html, 'lxml')
        article = soup.find(class_='article')
        news['title'] = article.find('h1').string
        detail = article.find(class_='detail')
        news['content'] = '\n'.join(
            [p.string for p in detail.find_all('p') if p.string])
        news['image_urls'] = [i.get('src') for i in detail.find_all('img')]
        return News(**news)
    except Exception as e:
        print(e)
        return None


if __name__ == '__main__':
    # with open('dong_fang.html', 'w', encoding='utf-8') as f:
    #     f.write(get_html(webdriver.Edge(), 1))
    # print(get_tag('  [国际]  '))
    with open('dong_fang.html', encoding='utf-8') as f:
        print(analyze_html(f.read())[-1])
    # print(get_news_since(webdriver.Edge(), datetime(2021, 12, 11, 10, 40)))
