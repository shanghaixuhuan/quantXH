import QUANTAXIS as QA
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
from QUANTAXIS.QAIndicator import base
import time


class KDJtest:
    def __init__(self, cash):
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.cash = cash
        self.Broker = QA.QA_BacktestBroker()
        self.User = QA.QA_User(username='quantaxis', password='quantaxis')
        self.Portfolio = self.User.new_portfolio('p'+ time)
        self.ACstr = 'a'+ time
        self.AC = self.Portfolio.new_account(account_cookie=self.ACstr, init_cash=cash)

    def KDJ_backtest(self,code,ckstart,ckend,ycstart,ycend,amount,N,M1,M2):
        self.code = code
        self.ckstart = ckstart
        self.ckend = ckend
        self.ycstart = ycstart
        self.ycend = ycend
        self.amount = amount
        self.N = N
        self.M1 = M1
        self.M2 = M2
        data = QA.QA_fetch_stock_day_adv(code, ckstart, ckend).to_qfq()
        ind = {}
        for i in code:
            ind[i] = self.KDJ(QA.QA_fetch_stock_day_adv(i, ckstart, ckend).to_qfq(),N,M1,M2)
            # ind[i] = QA.QA_indicator_KDJ(QA.QA_fetch_stock_day_adv(i, ckstart, ckend).to_qfq(),N,M1,M2)
        data_forbacktest = data.select_time(ycstart,ycend)
        for items in data_forbacktest.panel_gen:
            for item in items.security_gen:
                daily_ind = ind[item.code[0]].loc[item.index]
                if daily_ind.KDJ_K.iloc[0] < 20 and daily_ind.KDJ_D.iloc[0] < 20 and daily_ind.KDJ_J.iloc[0] < 20:
                    order = self.AC.send_order(
                        code=item.code[0],
                        time=item.date[0],
                        amount=amount,
                        towards=QA.ORDER_DIRECTION.BUY,
                        price=0,
                        order_model=QA.ORDER_MODEL.CLOSE,
                        amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                    )
                    self.Broker.receive_order(QA.QA_Event(order=order, market_data=item))
                    trade_mes = self.Broker.query_orders(self.AC.account_cookie, 'filled')
                    res = trade_mes.loc[order.account_cookie, order.realorder_id]
                    order.trade(res.trade_id, res.trade_price,
                                res.trade_amount, res.trade_time)
                elif daily_ind.KDJ_K.iloc[0] > 80 and daily_ind.KDJ_D.iloc[0] > 80 and daily_ind.KDJ_J.iloc[0] > 80:
                    if self.AC.sell_available.get(item.code[0], 0) > 0:
                        order = self.AC.send_order(
                            code=item.code[0],
                            time=item.date[0],
                            amount=self.AC.sell_available.get(item.code[0], 0),
                            towards=QA.ORDER_DIRECTION.SELL,
                            price=0,
                            order_model=QA.ORDER_MODEL.MARKET,
                            amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                        )
                        self.Broker.receive_order(QA.QA_Event(
                            order=order, market_data=item))
                        trade_mes = self.Broker.query_orders(
                            self.AC.account_cookie, 'filled')
                        res = trade_mes.loc[order.account_cookie, order.realorder_id]
                        order.trade(res.trade_id, res.trade_price, res.trade_amount, res.trade_time)
            self.AC.settle()

    def save_to_mongo(self):
        self.client = MongoClient()
        self.db = self.client.quantaxis
        self.AC.save()
        risk = QA.QA_Risk(self.AC)
        risk.save()
        init_coditions = {"cash":self.cash,"code":self.code,"ycstarttime":self.ycstart,"ycendtime":self.ycend, "amount":self.amount, "N":self.N,
                          "M1":self.M1, "M2":self.M2}
        self.db["init"].insert({"ac_id":self.ACstr, "type":"KDJ指标回测",
                                "profit":risk.profit , "init_conditions":init_coditions})

    def KDJ(self, DataFrame, N=9, M1=3, M2=3):
        C = DataFrame['close']
        H = DataFrame['high']
        L = DataFrame['low']

        RSV = (C - base.LLV(L, N)) / (base.HHV(H, N) - base.LLV(L, N)) * 100
        K = base.SMA(RSV, M1)
        D = base.SMA(K, M2)
        J = 3 * K - 2 * D
        DICT = {'KDJ_K': K, 'KDJ_D': D, 'KDJ_J': J}
        return pd.DataFrame(DICT)


if __name__ == "__main__":
    code = ["000001","000004"]
    r = KDJtest(cash=10000000)
    r.KDJ_backtest(code=code,ckstart="2019-01-01",ckend="2019-12-31",ycstart="2019-07-01",ycend="2019-12-31",amount=10000,
                    N=9,M1=3,M2=3)
    r.save_to_mongo()


