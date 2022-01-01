import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait


def sina_shouye_starter(browser, max_pages):
    browser.get("https://ent.sina.com.cn/")
    max_pages = 100
    # scrollTop = 1000
    # js_model = 'var q=document.documentElement.scrollTop='  # 向下滑动页面
    count = 0
    title_record = set()
    for i in range(100):
        ActionChains(browser).key_down(
            Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        time.sleep(0.2)
    # f = open(localpath, "a+")
    soup = BeautifulSoup(browser.page_source, "lxml")
    informations = soup.find_all("div", attrs={
        'class': 'ty-card ty-card-type1 clearfix'
    })
    print(len(informations))
    while count < max_pages:
        try:
            for element in informations:
                # print(element)
                title = element.find("h3").find("a").text
                if(title in title_record):
                    continue
                else:
                    title_record.add(title)
                    img_urls = "https"+element.find('img').get('src')
                    tags = date = element.find_all("span", attrs={
                        "class": "ty-card-tag"
                    })
                    keywords = [tag.find('a').text for tag in tags]
                    date = element.find("span", attrs={
                        "class": "ty-card-tip2-i ty-card-time"
                    }).text
                    f.write("标题：" + title + "\n")
                    # f.write("关键词："+keywords+'\n')
                    f.write("图片地址"+img_urls+'\n')
                    f.write(date+'\n')
                    print(count)
                    count += 1
            if(count >= max_pages):
                break
        except Exception as e:
            print(e)
    # browser.close()
