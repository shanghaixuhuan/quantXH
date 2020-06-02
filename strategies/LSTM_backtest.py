import QUANTAXIS as QA
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import numpy as np
from QUANTAXIS.QAIndicator import base
from deeplearning.LSTM import LSTMpredict
import time


class LSTMtest:
    def __init__(self, cash):
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.cash = cash
        self.Broker = QA.QA_BacktestBroker()
        self.User = QA.QA_User(username='quantaxis', password='quantaxis')
        self.Portfolio = self.User.new_portfolio('p'+ time)
        self.ACstr = 'a'+ time
        self.AC = self.Portfolio.new_account(account_cookie=self.ACstr, init_cash=cash)

    def LSTM_backtest(self,tcode,codep,ckstart,ckend,ycstart,ycend,amount,model,buy,sell):
        self.tcode = tcode
        self.codep = codep
        self.ckstart = ckstart
        self.ckend = ckend
        self.ycstart = ycstart
        self.ycend = ycend
        self.amount = amount
        self.buy = buy
        self.sell = sell

        data = QA.QA_fetch_stock_day_adv(codep, ckstart, ckend).to_qfq()
        ind = {}
        for i in codep:
            ind[i] = QA.QA_fetch_stock_day_adv(i, ckstart, ckend).to_qfq().add_func(self.INDS)
            # ind[i] = QA.QA_indicator_CCI(QA.QA_fetch_stock_day_adv(i, ckstart, ckend).to_qfq(),14)
        data_forbacktest = data.select_time(ycstart, ycend)

        for items in data_forbacktest.panel_gen:
            for item in items.security_gen:
                _index = list(ind[item.code[0]].index.levels[0]).index(list(item.index[0])[0])
                close = ind[item.code[0]].iloc[_index,0]

                daily_ind = np.array(ind[item.code[0]].iloc[_index-5:_index,1:])
                close1 = model.predict(np.array([daily_ind]))[0][0]

                if close1 > close * (1+self.buy):
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
                elif close1 < close * (1-self.sell):
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
        init_coditions = {"cash":self.cash,"tcode":self.tcode,"codep":self.codep, "ckstarttime":self.ckstart,
                          "ckendtime":self.ckend, "ycstarttime":self.ycstart,"ycendtime":self.ycend,
                          "amount":self.amount,"up":str(self.buy),"down":str(self.sell)}
        self.db["init"].insert({"ac_id":self.ACstr, "type":"LSTM预测股价回测",
                                "profit":risk.profit , "init_conditions":init_coditions})

    def INDS(self,DataFrame):
        CLOSE = DataFrame['close']
        HIGH = DataFrame['high']
        LOW = DataFrame['low']

        # cci的天数取14
        typ = (HIGH + LOW + CLOSE) / 3
        CCI = ((typ - base.MA(typ, 14)) / (0.015 * base.AVEDEV(typ, 14) + 0.00000001))

        # rsi的天数取6
        LC = base.REF(CLOSE, 1)
        RSI = base.SMA(QA.MAX(CLOSE - LC, 0), 6) / base.SMA(base.ABS(CLOSE - LC), 6) * 100

        # macd long取26，short取12，mid取9
        DIF = base.EMA(CLOSE, 12) - base.EMA(CLOSE, 26)
        DEA = base.EMA(DIF, 9)
        MACD = (DIF - DEA) * 2

        # boll N取20
        boll = base.MA(CLOSE, 20)

        # kdj N取9，M1、M2取3
        RSV = (CLOSE - base.LLV(LOW, 9)) / (base.HHV(HIGH, 9) - base.LLV(LOW, 9)) * 100
        K = base.SMA(RSV, 3)
        D = base.SMA(K, 3)
        J = 3 * K - 2 * D

        DICT = {'CLOSE':CLOSE, 'CCI14': CCI, 'RSI6': RSI, 'MACD': MACD, 'BOLL': boll, 'KDJ_J': J}
        # DICT = {'CLOSE':CLOSE, 'CCI14':CCI, 'RSI6': RSI, 'MACD':MACD, 'BOLL':boll, 'KDJ_J': J, "CLOSE1": CLOSE1}
        return pd.DataFrame(DICT)


if __name__ == "__main__":
    code = ["000001","000004"]
    tcode = "000002"
    tstart = "2001-01-01"
    tend = "2020-04-30"

    lstm = LSTMpredict()
    lstm.get_data(tcode, tstart, tend)
    lstm.nomalize()
    lstm.cons_sets(cut=99)
    lstm.make_model()
    lstm.train_performance()
    lstm.test_performance()
    lstm.output_result()
    model = lstm.model

    r = LSTMtest(cash=1000000)
    print(code)
    r.LSTM_backtest(tcode=tcode, codep=code,ckstart="2018-07-01",ckend="2020-04-30",
                    ycstart="2019-04-30",ycend="2020-04-30",amount=10000,model=model,buy=0.02,sell=0.02)
    r.save_to_mongo()