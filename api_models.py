from pydantic import BaseModel
import datetime
import hashlib
from config import signature_key


def sha3(s: str) -> str:
    b = s.encode()
    return hashlib.sha3_512(b).hexdigest()


class NewsHook(BaseModel):
    def __init__(self, *args, **kwargs):
        id = kwargs['id']
        url = kwargs['url']
        title = kwargs['title']
        content = kwargs['content']
        category = kwargs['category']
        date = kwargs['date']
        kwargs['signature'] = sha3(
            f'{id}{url}{title}{content}{category}{date}{signature_key}')
        super().__init__(*args, **kwargs)
    id: int
    url: str
    title: str
    content: str
    category: str
    date: str
    signature: str


class ImageHook(BaseModel):
    def __init__(self, *args, **kwargs):
        id = kwargs['id']
        url = kwargs['url']
        kwargs['signature'] = sha3(f'{id}{url}{signature_key}')
        super().__init__(*args, **kwargs)
    id: int
    url: str
    signature: str
