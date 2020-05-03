import QUANTAXIS as QA
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import time


class RSINtest:
    def __init__(self, cash):
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.cash = cash
        self.Broker = QA.QA_BacktestBroker()
        self.User = QA.QA_User(username='quantaxis', password='quantaxis')
        self.Portfolio = self.User.new_portfolio('p'+ time)
        self.ACstr = 'a'+ time
        self.AC = self.Portfolio.new_account(account_cookie=self.ACstr, init_cash=cash)

    def RSIN_backtest(self,code,ckstart,ckend,ycstart,ycend,amount,N):
        self.code = code
        self.ckstart = ckstart
        self.ckend = ckend
        self.ycstart = ycstart
        self.ycend = ycend
        self.amount = amount
        self.N = N
        data = QA.QA_fetch_stock_day_adv(code, ckstart, ckend).to_qfq()
        ind = {}
        for i in code:
            ind[i] = QA.QA_fetch_stock_day_adv(i, ckstart, ckend).to_qfq().add_func(self.RSIN)
            # ind[i] = QA.QA_indicator_RSI(QA.QA_fetch_stock_day_adv(i, ckstart, ckend).to_qfq(),6,12,24)
        data_forbacktest = data.select_time(ycstart, ycend)
        rsi = dict(zip(code,[None for _ in range(len(code))]))
        for items in data_forbacktest.panel_gen:
            for item in items.security_gen:
                daily_ind = ind[item.code[0]].loc[item.index]
                if rsi[item.code[0]] is None:
                    pass
                elif daily_ind.RSI.iloc[0] >= 20 and rsi[item.code[0]] < 20:
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
                elif daily_ind.RSI.iloc[0] <= 80 and rsi[item.code[0]] > 80:
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
                rsi[item.code[0]] = daily_ind.RSI.iloc[0]
            self.AC.settle()

    def save_to_mongo(self):
        self.client = MongoClient()
        self.db = self.client.quantaxis
        self.AC.save()
        risk = QA.QA_Risk(self.AC)
        risk.save()
        init_coditions = {"cash":self.cash,"code":self.code,"ckstarttime":self.ckstart,"ckendtime":self.ckend,
                          "ycstarttime":self.ycstart,"ycendtime":self.ycend, "amount":self.amount, "N":self.N,}
        self.db["init"].insert({"ac_id":self.ACstr, "type":"RSI N日回测",
                                "profit":risk.profit , "init_conditions":init_coditions})

    def RSIN(self,dataframe):
        CLOSE = dataframe['close']
        LC = QA.REF(CLOSE, 1)
        RSI = QA.SMA(QA.MAX(CLOSE - LC, 0), self.N) / QA.SMA(QA.ABS(CLOSE - LC), self.N) * 100
        return pd.DataFrame({"RSI":RSI})


if __name__ == "__main__":
    code = ["000001","000004"]
    r = RSINtest(cash=10000000)
    r.RSIN_backtest(code=code,ckstart="2019-01-01",ckend="2019-12-31",ycstart="2019-07-01",ycend="2019-12-31",amount=10000,
                    N=6)
    r.save_to_mongo()


