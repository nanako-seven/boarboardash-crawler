from fastapi import FastAPI
from pydantic.main import BaseModel
import database_models as model

app = FastAPI()


@app.get('/page/{page_id}')
def get_page(page_id: int):
    p: model.Page = model.Page.select().where(model.Page.id == page_id).get()
    site: model.Site = p.site
    return {
        'url': p.url,
        'title': p.title,
        'content': p.content,
        'site_id': site.id,
    }


@app.get('/image/{image_id}')
def get_page(image_id: int):
    p: model.Image = model.Image.select().where(model.Image.id == image_id).get()
    site: model.Site = p.src_page
    return {
        'url': p.url,
        'src_page_id': site.id,
    }


class SubScribeParam(BaseModel):
    url: str


@app.post('/subscribe')
def subscribe(data: SubScribeParam):
    url = data.url
    m = model.Subscriber.create(url=url)
    return {
        'id': m.id
    }
