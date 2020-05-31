import pandas as pd
from QUANTAXIS.QAIndicator import base
import QUANTAXIS as QA
import matplotlib.pyplot as plt
import numpy as np


class BPpredict:
    def get_data(self):
        data = QA.QA_fetch_stock_day_adv("000001", "2010-01-01", "2020-04-30").to_qfq()
        data_indicators = self.get_indicators(data)
        self.df = data_indicators.iloc[50:-1,]

    def nomalize(self):
        from sklearn import preprocessing
        min_max_scaler = preprocessing.MinMaxScaler()
        df0 = min_max_scaler.fit_transform(self.df)
        df = pd.DataFrame(df0, columns=self.df.columns)
        self.X = df.iloc[:, :-1]
        self.y = df['CLOSE1']

    def cons_sets(self):
        y = pd.DataFrame(self.y.values, columns=['goal'])
        x = self.X
        cut = 50
        self.X_train, self.X_test = x.iloc[:-cut], x.iloc[-cut:]
        self.y_train, self.y_test = y.iloc[:-cut], y.iloc[-cut:]
        self.X_train, self.X_test, self.y_train, self.y_test = self.X_train.values, self.X_test.values, \
                                                               self.y_train.values, self.y_test.values

    def make_model(self):
        from keras.models import Sequential
        from keras.layers.core import Dense, Activation
        from keras.optimizers import Adam
        self.model = Sequential()  # 层次模型
        self.model.add(Dense(64, input_dim=6, init='uniform'))  # 输入层，Dense表示BP层
        self.model.add(Activation('relu'))  # 添加激活函数
        self.model.add(Dense(4, init='uniform'))  # 中间层
        self.model.add(Activation('sigmoid'))  # 添加激活函数
        self.model.add(Dense(1))  # 输出层
        self.model.compile(loss='mean_squared_error', optimizer='Adam')  # 编译模型
        self.model.fit(self.X_train, self.y_train, nb_epoch=50, batch_size=256)  # 训练模型nb_epoch=50次
        print(self.model.summary())

    def train_performance(self):
        self.y_train_predict = self.model.predict(self.X_train)
        self.y_train_predict = pd.DataFrame(self.y_train_predict[:, 0])
        self.y_train = pd.DataFrame(self.y_train)
        # sum = 0
        # for i in range(len(self.y_train)):
        #     if self.y_train.iloc[i,0] * self.y_train_predict.iloc[i,0] > 0:
        #         sum += 1
        # print(sum/len(self.y_train))
        draw = pd.concat([self.y_train, self.y_train_predict], axis=1)
        draw.iloc[:, 0].plot(figsize=(12, 6))
        draw.iloc[:, 1].plot(figsize=(12, 6))
        plt.legend(('real', 'predict'), fontsize='15')
        plt.title("Train Data", fontsize='30')  # 添加标题
        plt.show()

    def test_performance(self):
        self.y_test_predict = self.model.predict(self.X_test)
        self.y_test_predict = pd.DataFrame(self.y_test_predict[:, 0])
        self.y_test = pd.DataFrame(self.y_test)
        # sum = 0
        # for i in range(len(self.y_test)):
        #     if self.y_test.iloc[i, 0] * self.y_test_predict.iloc[i, 0] > 0:
        #         sum += 1
        # print(sum / len(self.y_test))
        draw = pd.concat([self.y_test, self.y_test_predict], axis=1);
        draw.iloc[:, 0].plot(figsize=(12, 6))
        draw.iloc[:, 1].plot(figsize=(12, 6))
        plt.legend(('real', 'predict'), loc='upper right', fontsize='15')
        plt.title("Test Data", fontsize='30')  # 添加标题
        plt.show()
        # 展示在测试集上的表现

    def output_result(self):
        from sklearn.metrics import mean_absolute_error
        from sklearn.metrics import mean_squared_error
        def mape(y_true, y_pred):
            return np.mean(np.abs((y_pred - y_true) / y_true)) * 100
        # 输出结果
        self.y_test = self.y_test.values
        y_var_test = self.y_test[1:] - self.y_test[:len(self.y_test) - 1]
        self.y_test_predict = self.y_test_predict.values
        y_var_predict = self.y_test_predict[1:] - self.y_test[:len(self.y_test) - 1]

        print('训练集上的MAE/MSE/MAPE：')
        print(mean_absolute_error(self.y_train_predict, self.y_train),end="  ")
        print(mean_squared_error(self.y_train_predict, self.y_train),end="  ")
        print(mape(self.y_train_predict, self.y_train))
        print('测试集上的MAE/MSE/MAPE：')
        print(mean_absolute_error(self.y_test_predict, self.y_test),end="  ")
        print(mean_squared_error(self.y_test_predict, self.y_test),end="  ")
        print(mape(self.y_test_predict, self.y_test))

        txt = np.zeros(len(y_var_test))
        for i in range(len(y_var_test - 1)):
            txt[i] = np.sign(y_var_test[i]) == np.sign(y_var_predict[i])
        result = sum(txt) / len(txt)
        print('预测涨跌正确:', result)

    def get_indicators(self,DataFrame):
        CLOSE = DataFrame['close']
        CLOSE1 = CLOSE.copy()
        for i in range(len(CLOSE)-1):
            CLOSE1[i] = CLOSE1[i+1]
        HIGH = DataFrame['high']
        LOW = DataFrame['low']
        CHANGE = (CLOSE1-CLOSE) / CLOSE
        # for i in range(len(CHANGE)):
        #     if CHANGE[i] > 0:
        #         CHANGE[i] = True
        #     else:
        #         CHANGE[i] = False
        # CHANGE =

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

        # DICT = {'CCI14': CCI, 'RSI6': RSI, 'MACD': MACD, 'BOLL': boll, 'KDJ_J': J, "CLOSE1": CLOSE1}
        DICT = {'CLOSE':CLOSE, 'CCI14':CCI, 'RSI6': RSI, 'MACD':MACD, 'BOLL':boll, 'KDJ_J': J, "CLOSE1": CLOSE1}
        return pd.DataFrame(DICT)


if __name__ == "__main__":
    bpp = BPpredict()
    bpp.get_data()
    bpp.nomalize()
    bpp.cons_sets()
    bpp.make_model()
    bpp.train_performance()
    bpp.test_performance()
    bpp.output_result()
