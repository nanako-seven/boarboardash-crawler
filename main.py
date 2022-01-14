import aiohttp
import sites
from selenium import webdriver
from models import Website, News, Image
import asyncio
from api_models import NewsHook, ImageHook
import time
from config import news_hook_url, image_hook_url
import traceback
import sys


driver = webdriver.Edge()


async def crawl():
    '''
    爬取一波网页，并更新数据库中的信息
    '''
    news_hooks = []
    image_hooks = []
    for w in sites.SupportedSites:
        website = await Website.objects.get(Website.name == sites.website_names[w])
        news = sites.get_news_since(w, driver, website.last_crawl_time)

        if news:
            website.last_crawl_time = news[0].time
            await website.update()
        for i in news:
            page = await News.objects.create(
                url=i.url, title=i.title, content=i.content, encoding=i.encoding, raw=i.raw, time=i.time, website=website, category=i.category)
            news_hooks.append(NewsHook(id=page.id, url=page.url, title=page.title,
                              content=page.content, category=page.category, date=str(page.time.date())))

            for j in i.image_urls:
                img = await Image.objects.create(news=page, url=j)
                image_hooks.append(ImageHook(id=img.id, url=img.url))
    async with aiohttp.ClientSession() as session:
        for i in news_hooks:
            await session.post(news_hook_url, json=dict(i))

        for i in image_hooks:
            await session.post(image_hook_url, json=dict(i))


def main():
    # asyncio.run(crawl())
    while True:
        try:
            asyncio.run(crawl())
        except Exception as e:
            traceback.print_exc(file=sys.stderr)
        # 每隔一小时爬取一次
        time.sleep(3600)


if __name__ == '__main__':
    main()
