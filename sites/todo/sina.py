from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep


class Category:
    QUAN_BU = 0
    GUO_NEI = 1
    GUO_JI = 2
    SHE_HUI = 3
    TI_YU = 4
    YU_LE = 5
    JUN_SHI = 6
    KE_JI = 7
    CAI_JING = 8
    GU_SHI = 9
    MEI_GU = 10


category_id = {
    Category.QUAN_BU: 2509,
    Category.GUO_NEI: 2510,
    Category.GUO_JI: 2511,
    Category.SHE_HUI: 2669,
    Category.TI_YU: 2512,
    Category.YU_LE: 2513,
    Category.JUN_SHI: 2514,
    Category.KE_JI: 2515,
    Category.CAI_JING: 2516,
    Category.GU_SHI: 2517,
    Category.MEI_GU: 2518,
}


def get_page_source(driver: webdriver.Firefox, category, page):
    driver.get(
        f'https://news.sina.com.cn/roll/#pageid=153&lid={category_id[category]}&k=&num=50&page={page}')
    el = WebDriverWait(driver, timeout=5).until(
        lambda d: d.find_element(By.CSS_SELECTOR, '#d_list'))
    return el.get_attribute('innerHTML')

    # element = WebDriverWait(driver, timeout=5).until(
    #     lambda d: d.find_element(By.CSS_SELECTOR, f"[s_id='{category_id[category]}']"))
    # element.click()

    # element = WebDriverWait(driver, timeout=5).until(
    #     lambda d: d.find_element(By.CLASS_NAME, "pagebox"))
    # button = element.find_element(
    #     By.CSS_SELECTOR, f"[onClick='newsList.page.goTo(2);return false;'")
    # button.click()

    # with open('sina.html', 'w', encoding='utf-8') as f:
    #     js = "return document.documentElement.outerHTML"
    #     html = driver.page_source
    #     f.write(html)


if __name__ == '__main__':
    with open('sina.html', 'w', encoding='utf-8') as f:
        f.write(get_page_source(webdriver.Edge(), Category.QUAN_BU, 2))
