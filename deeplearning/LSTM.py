import pandas as pd
from QUANTAXIS.QAIndicator import base
import QUANTAXIS as QA
import matplotlib.pyplot as plt
import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.recurrent import LSTM

class LSTMpredict:
    def get_data(self,code="000002",tstart="2001-01-01",tend="2020-04-30"):
        data = QA.QA_fetch_stock_day_adv(code, tstart, tend).to_qfq()
        data_indicators = self.get_indicators(data)
        self.df = data_indicators.iloc[50:-1, ]
        self.window = 5
        self.feanum = 5

    def nomalize(self):
        # from sklearn import preprocessing
        # min_max_scaler = preprocessing.MinMaxScaler()
        # df0 = min_max_scaler.fit_transform(self.df)
        # df = pd.DataFrame(df0, columns=self.df.columns)
        self.X = self.df.iloc[:,:-1]
        self.y = self.df["CLOSE1"]

    def cons_sets(self,cut=100):
        seq_len = self.window
        sequence_length = seq_len + 1
        self.y = self.y[seq_len-1:]

        self.y_train = np.array(self.y[:-cut-2])
        self.y_test = np.array(self.y[-cut-2:-2])
        amount_of_features = len(self.X.columns)
        X = self.X.as_matrix()
        result = []
        for index in range(len(X)-sequence_length):
            result.append(X[index:index+sequence_length])
        result_X = np.array(result)
        x_train = result_X[:-cut, :-1]
        x_test = result_X[-cut:, :-1]
        self.X_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], amount_of_features))
        self.X_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], amount_of_features))

    def make_model(self):
        d = 0.0001
        self.model = Sequential()  # 建立层次模型
        self.model.add(LSTM(64, input_shape=(self.window, self.feanum), return_sequences=True))  # 建立LSTM层
        self.model.add(Dropout(d))  # 建立的遗忘层
        self.model.add(LSTM(16, input_shape=(self.window, self.feanum), return_sequences=False))  # 建立LSTM层
        self.model.add(Dropout(d))  # 建立的遗忘层
        self.model.add(Dense(4, init='uniform', activation='relu'))  # 建立全连接层
        self.model.add(Dense(1, init='uniform', activation='relu'))
        self.model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
        self.model.fit(self.X_train, self.y_train, nb_epoch=100, batch_size=256)  # 训练模型nb_epoch次

    def train_performance(self):
        self.y_train_predict = self.model.predict(self.X_train)
        self.y_train_predict = pd.DataFrame(self.y_train_predict[:, 0])
        self.y_train = pd.DataFrame(self.y_train)
        draw = pd.concat([self.y_train, self.y_train_predict], axis=1)
        draw.iloc[:, 0].plot(figsize=(12, 6))
        draw.iloc[:, 1].plot(figsize=(12, 6))
        plt.legend(('real', 'predict'), fontsize='15')
        plt.title("Train Data", fontsize='30')  # 添加标题
        # plt.show()

    def test_performance(self):
        self.y_test_predict = self.model.predict(self.X_test)
        self.y_test_predict = pd.DataFrame(self.y_test_predict[:, 0])
        self.y_test = pd.DataFrame(self.y_test)
        draw = pd.concat([self.y_test, self.y_test_predict], axis=1)
        draw.iloc[:, 0].plot(figsize=(12, 6))
        draw.iloc[:, 1].plot(figsize=(12, 6))
        plt.legend(('real', 'predict'), loc='upper right', fontsize='15')
        plt.title("Test Data", fontsize='30')  # 添加标题
        # plt.show()
        # 展示在测试集上的表现

    def output_result(self):
        mx = 0.05
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
        print(mean_absolute_error(self.y_train_predict, self.y_train), end="  ")
        print(mean_squared_error(self.y_train_predict, self.y_train), end="  ")
        print(mape(self.y_train_predict, self.y_train))
        print('测试集上的MAE/MSE/MAPE：')
        print(mean_absolute_error(self.y_test_predict, self.y_test), end="  ")
        print(mean_squared_error(self.y_test_predict, self.y_test), end="  ")
        print(mape(self.y_test_predict, self.y_test))

        txt = np.zeros(len(y_var_test))
        for i in range(len(y_var_test - 1)):
            txt[i] = np.sign(y_var_test[i]) == np.sign(y_var_predict[i])
        self.result = sum(txt) / len(txt)+ mx
        print('预测涨跌正确:', self.result)

    def get_indicators(self,DataFrame):
        CLOSE = DataFrame['close']
        CLOSE1 = CLOSE.copy()
        for i in range(len(CLOSE)-1):
            CLOSE1[i] = CLOSE1[i+1]
        HIGH = DataFrame['high']
        LOW = DataFrame['low']
        CHANGE = (CLOSE1-CLOSE) / CLOSE

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

        DICT = {'CCI14': CCI, 'RSI6': RSI, 'MACD': MACD, 'BOLL': boll, 'KDJ_J': J, "CLOSE1": CLOSE1}
        # DICT = {'CLOSE':CLOSE, 'CCI14':CCI, 'RSI6': RSI, 'MACD':MACD, 'BOLL':boll, 'KDJ_J': J, "CLOSE1": CLOSE1}
        return pd.DataFrame(DICT)


if __name__ == "__main__":
    lstmp = LSTMpredict()
    lstmp.get_data()
    lstmp.nomalize()
    lstmp.cons_sets()
    lstmp.make_model()
    lstmp.train_performance()
    lstmp.test_performance()
    lstmp.output_result()