from pymongo import MongoClient
from pandas import DataFrame
from matplotlib import dates
import pandas as pd
import re
import time
from datetime import  datetime

province = ["黑龙江","新疆","吉林","甘肃","辽宁","青海","北京","陕西","天津","广西","河北","广东",
            "河南","宁夏","山东","上海","山西","深圳","湖北","福建","湖南","江西","四川","安徽",
            "重庆","江苏","云南","浙江","贵州","海南","西藏","内蒙"]

info_names = ["股票名称","市场", "股票代码", "流通股本", "省份", "更新日期", "上市日期", "总股本",
         "国家股", "发起人法人股", "法人股", "B股", "H股", "职工股", "总资产", "流动资产",
         "固定资产", "无形资产", "股东人数", "流动发债", "长期发债", "资本公积金", "净资产",
         "主营收入", "主营利润", "应收账款", "营业利润", "投资收益", "经营现金流", "总现金流",
         "存货", "利润总和", "税后利润", "净利润", "未分配利润", "每股净资产"]

info_isdigit = [False,False,False,True,False,False,False,True,
                True,True,True,True,True,True,True,True,
                True,True,True,True,True,True,True,
                True,True,True,True,True,True,True,
                True,True,True,True,True,True]


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

    def fetch_A_day(self, code="000001",start="2020-01-01",end="2020-03-01"):
        doc = list(self.db.stock_day.find({"code": code, "date": {"$lte": end, "$gte": start}},
                                          {"_id": 0, "date": 1,"open": 1, "close": 1,"high": 1, "low": 1,"vol": 1}))
        l = []
        for i in doc:
            li = list(i.values())
            li.insert(0, li[5])
            dt = datetime.strptime(li[0], "%Y-%m-%d")
            li[0] = dates.date2num(dt)
            li.pop()
            close = li.pop(2)
            li.insert(4, close)
            l.append(li)
        return l

    def fetch_stock_info(self, code="000001"):
        cursor = self.db.stock_info.find({"code":code})
        ob = list(list(cursor)[0].values())[1:-1]
        if ob[0] == 0:
            ob[0] = "深市"
        else:
            ob[0] = "沪市"
        del ob[4]
        ob[3] = province[ob[3]-1]
        ob.insert(0,"")
        for i in range(len(ob)):
            if info_isdigit[i]:
                ob[i] = round(ob[i],1)
                if abs(ob[i]) >= 100000000:
                    ob[i] = str(ob[i]//100000000) + "亿"
                elif abs(ob[i]) >= 10000:
                    ob[i] = str(ob[i]//10000) + "万"
        return dict(zip(info_names,ob))


if __name__ == "__main__":
    f = FETCH()
    l = list(f.fetch_stock_list()['code'])
    print(type(l))
    print(l)