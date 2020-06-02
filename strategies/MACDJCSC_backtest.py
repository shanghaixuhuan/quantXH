import QUANTAXIS as QA
from datetime import datetime
from pymongo import MongoClient
import pandas as pd
import time


class MACDTest:
    def __init__(self, cash):
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.cash = cash
        self.Broker = QA.QA_BacktestBroker()
        self.User = QA.QA_User(username='quantaxis', password='quantaxis')
        self.Portfolio = self.User.new_portfolio('p'+ time)
        self.ACstr = 'a'+ time
        self.AC = self.Portfolio.new_account(account_cookie=self.ACstr, init_cash=cash)

    def MACD_backtest(self, code, ckstart, ckend, ycstart, ycend, amount,
                      SHORT, LONG, M):
        self.code = code
        self.ckstart = ckstart
        self.ckend = ckend
        self.ycstart = ycstart
        self.ycend = ycend
        self.amount = amount
        self.SHORT = SHORT
        self.LONG = LONG
        self.M = M
        data = QA.QA_fetch_stock_day_adv(code, ckstart, ckend).to_qfq()

        ind = data.add_func(self.MACD_JCSC)
        data_forbacktest = data.select_time(ycstart, ycend)
        for items in data_forbacktest.panel_gen:
            for item in items.security_gen:
                daily_ind = ind.loc[item.index]

                if daily_ind.CROSS_JC.iloc[0] > 0:
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
                elif daily_ind.CROSS_SC.iloc[0] > 0:
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
                        # print
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
                          "ycstarttime":self.ycstart,"ycendtime":self.ycend, "amount":self.amount, "SHORT":self.SHORT,
                          "LONG":self.LONG, "M":self.M}
        self.db["init"].insert({"ac_id":self.ACstr, "type":"MACD金叉死叉回测",
                                "profit":risk.profit , "init_conditions":init_coditions})

    def MACD_JCSC(self, dataframe):
        """
        1.DIF向上突破DEA，买入信号参考。
        2.DIF向下跌破DEA，卖出信号参考。
        """
        CLOSE = dataframe.close
        DIFF = QA.EMA(CLOSE, self.SHORT) - QA.EMA(CLOSE, self.LONG)
        DEA = QA.EMA(DIFF, self.M)
        MACD = 2 * (DIFF - DEA)

        CROSS_JC = QA.CROSS(DIFF, DEA)
        CROSS_SC = QA.CROSS(DEA, DIFF)
        ZERO = 0
        return pd.DataFrame(
            {'DIFF': DIFF, 'DEA': DEA, 'MACD': MACD, 'CROSS_JC': CROSS_JC, 'CROSS_SC': CROSS_SC, 'ZERO': ZERO})


if __name__ == "__main__":
    code = ["000001","000002","000004"]
    r = MACDTest(cash=1000000)
    r.MACD_backtest(code=code,ckstart='2017-09-01',ckend='2018-05-20',ycstart='2018-01-01',ycend='2018-05-01',amount=5000,
                    SHORT=12, LONG=26, M=9)
    r.save_to_mongo()