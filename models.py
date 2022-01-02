import databases
import sqlalchemy
import ormar
import datetime
from typing import Optional
import config

database = databases.Database(config.database_url)
metadata = sqlalchemy.MetaData()


# note that this step is optional -> all ormar cares is a internal
# class with name Meta and proper parameters, but this way you do not
# have to repeat the same parameters if you use only one database
class BaseMeta(ormar.ModelMeta):
    metadata = metadata
    database = database


class Website(ormar.Model):
    class Meta(BaseMeta):
        tablename = "websites"

    id: int = ormar.Integer(primary_key=True)
    name: str = ormar.Text()
    last_crawl_time: datetime.datetime = ormar.DateTime()


class News(ormar.Model):
    class Meta(BaseMeta):
        tablename = "news"

    id: int = ormar.Integer(primary_key=True)
    url: str = ormar.Text()
    title: str = ormar.Text()
    content: str = ormar.Text()
    encoding: str = ormar.Text()
    category: str = ormar.Text()
    raw: bytes = ormar.LargeBinary(max_length=1000000000)
    time: datetime.datetime = ormar.DateTime()
    website: Optional[Website] = ormar.ForeignKey(Website)


class Image(ormar.Model):
    class Meta(BaseMeta):
        tablename = "images"

    id: int = ormar.Integer(primary_key=True)
    news: Optional[News] = ormar.ForeignKey(News)
    url: str = ormar.Text()


async def init_database():
    # create the database
    # note that in production you should use migrations
    # note that this is not required if you connect to existing database
    engine = sqlalchemy.create_engine(config.database_url)
    # just to be sure we clear the db before
    metadata.drop_all(engine)
    metadata.create_all(engine)
    time = datetime.datetime.now() - datetime.timedelta(hours=3)
    await Website.objects.create(name='东方网', last_crawl_time=time)
    await Website.objects.create(name='人民网', last_crawl_time=time)
    await Website.objects.create(name='参考消息网', last_crawl_time=time)
    await Website.objects.create(name='新浪网', last_crawl_time=time)
    await Website.objects.create(name='中国新闻网', last_crawl_time=time)