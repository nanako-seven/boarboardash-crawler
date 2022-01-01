from enum import Enum
from .site_models import News
from selenium import webdriver
from datetime import datetime
from . import dong_fang
from . import can_kao_xiao_xi
# from . import renmin
# from . import sina
# from . import zhong_guo_xin_wen


class SupportedSites(Enum):
    DONG_FANG = 0
    CAN_KAO_XIAO_XI = 1


table = {
    SupportedSites.DONG_FANG: dong_fang.get_news_since,
    SupportedSites.CAN_KAO_XIAO_XI: can_kao_xiao_xi.get_news_since,
}


def get_news_since(site: SupportedSites, driver: webdriver.Firefox, time: datetime) -> list[News]:
    return table[site](driver, time)
