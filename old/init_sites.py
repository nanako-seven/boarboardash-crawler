import database_models as model
from enum import Enum
from datetime import datetime

sites = ['eastday']

for i in sites:
    model.Site.create(name=i, latest=datetime(1970, 1, 1))
