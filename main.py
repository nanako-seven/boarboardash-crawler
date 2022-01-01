import requests
import sites
from selenium import webdriver
from models import Website, News, Image
import asyncio


# site_models: dict[sites.SupportedSites, model.Site] = {
#     sites.SupportedSites.DONG_FANG: model.Site.select().where(model.Site.id == 1).get()
# }


# class Crawler:
#     def __init__(self):
#         self.driver = webdriver.Edge()

#     def start(self, site: sites.SupportedSites):
#         s = site_models[site]
#         news = sites.get_news_since(site, self.driver, s.latest)
#         if news:
#             s.latest = news[0].time
#             s.save()
#         pages = []
#         images = []
#         for i in news:
#             page = model.Page.create(
#                 url=i.url, title=i.title, content=i.content, encoding=i.encoding, raw=i.raw, date=i.time, site=s)
#             pages.append(page.id)
#             for j in i.images:
#                 img = model.Image.create(src_page=page, url=j)
#                 images.append(img.id)
#         for i in model.Subscriber.select():
#             i: model.Subscriber
#             requests.post(i.url, json={'page_ids': pages, 'image_ids': images})


# if __name__ == '__main__':
#     c = Crawler()
#     c.start(sites.SupportedSites.DONGFANG)

async def test():
    driver = webdriver.Edge()
    website = await Website.objects.get(Website.name == '参考消息网')
    news = sites.get_news_since(
        sites.SupportedSites.CAN_KAO_XIAO_XI, driver, website.last_crawl_time)

    if news:
        website.last_crawl_time = news[0].time
        await website.update()
    pages = []
    images = []
    for i in news:
        page = await News.objects.create(
            url=i.url, title=i.title, content=i.content, encoding=i.encoding, raw=i.raw, time=i.time, website=website, category=i.category)
        pages.append(page.id)
        for j in i.image_urls:
            img = await Image.objects.create(news=page, url=j)
            images.append(img.id)

loop = asyncio.get_event_loop()
loop.run_until_complete(test())
loop.close()
