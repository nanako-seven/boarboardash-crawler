from pydantic import BaseModel
from datetime import datetime


class News(BaseModel):
    url: str  # 新闻页面的URL
    category: str  # 新闻网站上的分类，例如：财经、军事
    title: str  # 新闻标题
    time: datetime  # 新闻发布时间
    raw: bytes  # 原始HTML数据
    encoding: str  # HTML编码
    content: str  # 新闻正文内容
    image_urls: list[str]  # 新闻正文中所有图片的URL
