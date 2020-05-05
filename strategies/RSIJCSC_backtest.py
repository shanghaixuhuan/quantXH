import QUANTAXIS as QA
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
from QUANTAXIS.QAIndicator import base


class RSIJCSCtest:
    def __init__(self, cash):
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.cash = cash
        self.Broker = QA.QA_BacktestBroker()
        self.User = QA.QA_User(username='quantaxis', password='quantaxis')
        self.Portfolio = self.User.new_portfolio('p'+ time)
        self.ACstr = 'a'+ time
        self.AC = self.Portfolio.new_account(account_cookie=self.ACstr, init_cash=cash)

    def RSIJCSC_backtest(self,code,ckstart,ckend,ycstart,ycend,amount,Nshort,Nlong):
        self.code = code
        self.ckstart = ckstart
        self.ckend = ckend
        self.ycstart = ycstart
        self.ycend = ycend
        self.amount = amount
        self.Nshort = Nshort
        self.Nlong = Nlong
        data = QA.QA_fetch_stock_day_adv(code, ckstart, ckend).to_qfq()
        ind = {}
        for i in code:
            ind[i] = self.RSIJCSC(QA.QA_fetch_stock_day_adv(i, ckstart, ckend).to_qfq(), Nshort, Nlong)

        print(ind)
        data_forbacktest = data.select_time(ycstart, ycend)
        for items in data_forbacktest.panel_gen:
            for item in items.security_gen:
                daily_ind = ind[item.code[0]].loc[item.index]
                if daily_ind.JC.iloc[0] == 1:
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
                elif daily_ind.SC.iloc[0] == 1:
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
        init_coditions = {"cash":self.cash,"code":self.code,"ckstarttime":self.ckstart,"ckendtime":self.ckend,
                          "ycstarttime":self.ycstart,"ycendtime":self.ycend, "amount":self.amount, "Nshort":self.Nshort,
                          "Nlong": self.Nlong}
        self.db["init"].insert({"ac_id":self.ACstr, "type":"RSI 金叉死叉回测",
                                "profit":risk.profit , "init_conditions":init_coditions})

    def RSIJCSC(self, DataFrame, Nshort=6, Nlong=12):
        '相对强弱指标RSI1:SMA(MAX(CLOSE-LC,0),N1,1)/SMA(ABS(CLOSE-LC),N1,1)*100;'
        CLOSE = DataFrame['close']
        LC = base.REF(CLOSE, 1)
        RSIshort = base.SMA(base.MAX(CLOSE - LC, 0), Nshort) / base.SMA(base.ABS(CLOSE - LC), Nshort) * 100
        RSIlong = base.SMA(base.MAX(CLOSE - LC, 0), Nlong) / base.SMA(base.ABS(CLOSE - LC), Nlong) * 100
        JC = base.CROSS(RSIshort,RSIlong)
        SC = base.CROSS(RSIlong,RSIshort)
        DICT = {'RSIshort': RSIshort, "RSIlong":RSIlong, "JC": JC, "SC": SC}

        return pd.DataFrame(DICT)


if __name__ == "__main__":
    code = ["000001","000004"]
    r = RSIJCSCtest(cash=10000000)
    r.RSIJCSC_backtest(code=code,ckstart="2019-01-01",ckend="2019-12-31",ycstart="2019-07-01",ycend="2019-12-31",amount=10000,
                    Nshort=6, Nlong=12)
    r.save_to_mongo()


