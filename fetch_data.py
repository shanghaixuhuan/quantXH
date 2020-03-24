from pymongo import MongoClient
from pandas import DataFrame
from matplotlib import dates
import pandas as pd
import re
import time
from datetime import  datetime


class FETCH:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.quantaxis

    def str_now(self):
        return time.strftime("%Y-%m-%d",time.localtime())

    def fetch_stock_list(self):
        cursor = self.db.stock_list.find()
        df = DataFrame(list(cursor))[["code", "name"]]
        return df

    def fuzzy_fetch_stock_list(self, s = "00000", item = "code"):
        cursor = self.db.stock_list.find({item:re.compile(s)})
        df = DataFrame(list(cursor))[["code", "name"]]
        return df


    def fetch_index_day(self, code="000001",start="2020-01-01",end="2020-03-01"):
        doc = list(self.db.index_day.find({"code":code, "date":{"$lte":end, "$gte":start}},{"_id": 0,"date":1,
                                                                    "open":1, "close":1,"high":1,"low":1,"vol":1}))
        l = []
        for i in doc:
            li = list(i.values())
            li.insert(0, li[5])
            dt = datetime.strptime(li[0], "%Y-%m-%d")
            li[0] = dates.date2num(dt)
            li.pop()
            close = li.pop(2)
            li.insert(4,close)
            l.append(li)
        return l


if __name__ == "__main__":
    f = FETCH()
    l = f.fuzzy_fetch_stock_list()
    print(l)