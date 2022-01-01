

import requests


def get_page_source(page):
    r = requests.get(
        f'https://www.chinanews.com.cn/scroll-news/news{page}.html')
    r.encoding = 'utf-8'
    print(r.text)


if __name__ == '__main__':
    get_page_source(2)
