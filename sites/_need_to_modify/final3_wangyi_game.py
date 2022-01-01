import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
def rolldown(num:int):
    for i in range(num):
        ActionChains(browser).key_down(Keys.PAGE_DOWN).key_up(Keys.PAGE_DOWN).perform()
        time.sleep(0.1)
browser = webdriver.Chrome()
browser.get("https://tech.163.com/game/")
localpath = "E:\\电工作业\\final\\Exercise\\wangyi_game.txt"
count = 0
target_num=1000
f = open(localpath, "a+")
count = 0
record=set()
while count < target_num:
    try:
        rolldown(5)
        soup=BeautifulSoup(browser.page_source,"lxml")
        load_more= browser.find_element_by_class_name("load_more_btn")
        informations = soup.find_all("div", attrs={
            'class': 'data_row news_article clearfix'
        })
        for element in informations:
                    title = element.find("h3").find("a").text
                    if(title in record):
                        continue
                    else:
                        record.add(title)
                        url=element.find('h3').find('a').get("href")
                        img_url=element.find('img').get('src')
                        # describe_bunk = element.find('div', attrs={
                        #     "class": "feed-card-txt"
                        # })
                        # if describe_bunk:
                        #     describe = describe_bunk.text
                        # else:
                        #     describe = "没有描述信息"
                        # tags=element.find("div",attrs={
                        #     "class":"feed-card-tags"
                        # }).find_all('a')
                        # keywords=[tag.text for tag in tags]
                        date=element.find("span",attrs={
                            "class":"time"
                        }).text
                        f.write("标题："+title+"\n")
                        f.write('url:'+url+'\n')
                        f.write("img_url:"+img_url+'\n')
                        # f.write('关键词：')
                        # for img in imgs:
                        #     f.write(img+"\n")
                        # f.write("详细:"+describe+'\n')
                        f.write("日期："+date+'\n')
                        print(count)
                        count += 1
        if(count>=target_num):
            break
        else:
            load_more.click()
    except Exception as e:
        print(e)

browser.close()