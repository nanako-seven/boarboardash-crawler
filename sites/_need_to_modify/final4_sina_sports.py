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
browser.get("https://sports.sina.com.cn/")
localpath = "E:\\电工作业\\final\\Exercise\\sina_sports.txt"
count = 0
target_num=1000
f = open(localpath, "a+")
count = 0



while count < target_num:
    try:
        rolldown(50)
        soup=BeautifulSoup(browser.page_source,"lxml")
        next_page = browser.find_element_by_xpath("/html/body/div[6]/div/div[2]/div[1]/div/div/div[1]/div[6]/div[3]/span[7]/a")
        informations = soup.find_all("div", attrs={
            'class': 'feed-card-item'
        })
        for element in informations:
                    title = element.find("h2").find("a").text
                    img_urls =element.find_all('img')
                    imgs=[]
                    for img_url in img_urls:
                        img="https:"+img_url.get('src')
                        imgs.append(img)
                    describe_bunk = element.find('div', attrs={
                        "class": "feed-card-txt"
                    })
                    if describe_bunk:
                        describe = describe_bunk.text
                    else:
                        describe = "没有描述信息"
                    tags=element.find("div",attrs={
                        "class":"feed-card-tags"
                    }).find_all('a')
                    keywords=[tag.text for tag in tags]
                    date=element.find("div",attrs={
                        "class":"feed-card-time"
                    }).text
                    f.write("标题："+title+"\n")
                    # f.write('关键词：')
                    for img in imgs:
                        f.write(img+"\n")
                    f.write("详细:"+describe+'\n')
                    f.write("日期："+date+'\n')
                    print(count)
                    count += 1
        if(count>=target_num):
            break
        else:
            next_page.click()
    except Exception as e:
        print(e)

browser.close()