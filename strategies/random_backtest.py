import QUANTAXIS as QA
import random
from datetime import datetime
from pymongo import MongoClient


class RBTest:
    def __init__(self, cash):
        time = datetime.now().strftime("%Y%m%d%H%M%S")
        self.cash = cash
        self.Broker = QA.QA_BacktestBroker()
        self.User = QA.QA_User(username='quantaxis', password='quantaxis')
        self.Portfolio = self.User.new_portfolio('p'+ time)
        self.ACstr = 'a'+ time
        self.AC = self.Portfolio.new_account(account_cookie=self.ACstr, init_cash=cash)

    def simple_backtest(self, code, start, end, amount):
        self.code = code
        self.start = start
        self.end = end
        self.amount = amount
        data = QA.QA_fetch_stock_day_adv(code, start, end).to_qfq()

        for items in data.panel_gen:
            for item in items.security_gen:
                if random.random() > 0.5:  # 加入一个随机 模拟买卖的
                    if self.AC.sell_available.get(item.code[0], 0) == 0:
                        order = self.AC.send_order(
                            code=item.code[0], time=item.date[0], amount=amount, towards=QA.ORDER_DIRECTION.BUY, price=0,
                            order_model=QA.ORDER_MODEL.MARKET, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                        )
                        if order:
                            self.Broker.receive_order(QA.QA_Event(
                                order=order, market_data=item))
                            trade_mes = self.Broker.query_orders(
                                self.AC.account_cookie, 'filled')
                            res = trade_mes.loc[order.account_cookie,
                                                order.realorder_id]
                            print('order {} {} {} {}'.format(
                                res.trade_id, res.trade_price, res.trade_amount, res.trade_time))
                            order.trade(res.trade_id, res.trade_price,
                                        res.trade_amount, res.trade_time)

                    else:
                        order = self.AC.send_order(
                            code=item.code[0], time=item.date[0], amount=amount, towards=QA.ORDER_DIRECTION.SELL, price=0,
                            order_model=QA.ORDER_MODEL.MARKET, amount_model=QA.AMOUNT_MODEL.BY_AMOUNT
                        )
                        if order:
                            self.Broker.receive_order(QA.QA_Event(
                                order=order, market_data=item))
                            trade_mes = self.Broker.query_orders(
                                self.AC.account_cookie, 'filled')
                            res = trade_mes.loc[order.account_cookie,
                                                order.realorder_id]
                            print('order {} {} {} {}'.format(
                                res.trade_id, res.trade_price, res.trade_amount, res.trade_time))
                            order.trade(res.trade_id, res.trade_price,
                                        res.trade_amount, res.trade_time)
            self.AC.settle()

    def save_to_mongo(self):
        self.client = MongoClient()
        self.db = self.client.quantaxis
        self.AC.save()
        risk = QA.QA_Risk(self.AC)
        risk.save()
        init_coditions = {"cash":self.cash,"code":self.code,"starttime":self.start,"endtime":self.end,
                          "amount":self.amount}
        self.db["init"].insert({"ac_id":self.ACstr, "type":"随机回测",
                                "profit":risk.profit , "init_conditions":init_coditions})


if __name__ == "__main__":
    code = ["000001","000002","000004"]
    r = RBTest(cash=1000000)
    r.simple_backtest(code, '2019-01-01', '2019-01-31', 1000)
    r.save_to_mongo()


