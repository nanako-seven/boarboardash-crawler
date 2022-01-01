import peewee

db = peewee.SqliteDatabase('test.db')


class Category(peewee.Model):
    name = peewee.TextField()

    class Meta:
        database = db


class Site(peewee.Model):
    name = peewee.TextField()
    latest = peewee.DateTimeField()

    class Meta:
        database = db


class Page(peewee.Model):
    url = peewee.TextField()
    title = peewee.TextField()
    content = peewee.TextField()
    encoding = peewee.TextField()
    raw = peewee.BlobField()
    site = peewee.ForeignKeyField(Site, backref='pages')
    date = peewee.DateField()
    # category = peewee.ForeignKeyField(Category, backref='pages')  # 暂时不分类

    class Meta:
        database = db


class Image(peewee.Model):
    src_page = peewee.ForeignKeyField(Page, backref='images')
    url = peewee.TextField()

    class Meta:
        database = db



def init_database():
    db.create_tables([Category, Page, Image, Site])


db.connect()


if __name__ == '__main__':
    init_database()
