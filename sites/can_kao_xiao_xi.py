from typing import Any, Dict
from bs4.element import Tag
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import date, datetime
from dataclasses import dataclass
from bs4 import BeautifulSoup
from .site_models import News
import requests


def get_page_source(page) -> str:
    r = requests.get(f'http://www.cankaoxiaoxi.com/roll/{page}.shtml')
    return r.text


def analyze_html(html: str) -> list[Any]:
    soup = BeautifulSoup(html, 'lxml')
    ans = []
    categories = ['全部', '中国', '国际', '台海', '军事', '财经', '科技健康', '观点·专栏']
    for i, tag in enumerate(soup.find_all('ul', class_='txt-list-a fz-14 clear')):
        if i == 0:
            continue
        for li in tag.find_all('li'):
            info = {}
            a: Tag = li.find('a')
            if not a:
                continue
            info['category'] = categories[i]
            info['url'] = a.get('href')
            info['title'] = a.string
            span: Tag = a.previous_sibling
            info['time'] = convert(span.string + ':00')
            ans.append(info)
    ans.sort(key=lambda x: x['time'], reverse=True)
    return ans


def convert(s: str) -> datetime:
    return datetime.strptime(s, '%Y-%m-%d %H:%M:%S')


def get_news_since(driver: webdriver.Firefox, time: datetime) -> list[News]:
    html = get_page_source(1)
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
        url = news['url']
        req = requests.get(url)
        news['raw'] = req.content
        news['encoding'] = req.encoding

        news['image_urls'] = []
        html = req.text
        soup = BeautifulSoup(html, 'lxml')

        abstract = soup.find(class_='articleAbs').span.string
        news['content'] = [abstract]
        n_pages = 1
        page = soup.find(class_='page')
        if page:
            n_pages = len(page.find_all('li')) - 2
        analyze_page_2(soup, news)
        for i in range(1, n_pages):
            url2 = url[:-6] + f'_{i+1}.shtml'
            req = requests.get(url2)
            html = req.text
            soup = BeautifulSoup(html, 'lxml')
            analyze_page_2(soup, news)
        news['content'] = '\n'.join(news['content'])

        return News(**news)
    except:
        return None


def analyze_page_2(soup: BeautifulSoup, news: Dict):
    article = soup.find(class_='articleText')
    for tag in article.find_all('p'):
        img = tag.find('img')
        if img:
            news['image_urls'].append(img.get('src'))
        else:
            news['content'].append(tag.get_text())


if __name__ == '__main__':
    # with open('can_kao_xiao_xi.html', 'w', encoding='utf-8') as f:
    #     f.write(get_page_source(1))

    # with open('can_kao_xiao_xi.html', encoding='utf-8') as f:
    #     print(analyze_html(f.read())[-1])
    # print(get_news_since(webdriver.Edge(), datetime(2021, 12, 11, 10, 40)))
    print(233)
