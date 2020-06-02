import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout,QTextBrowser,QTextEdit,QPushButton,
                             QDateEdit,QMessageBox)
import qdarkstyle
from PyQt5.QtGui import QIcon, QFont
from datetime import datetime
from fetch_data import FETCH
from strategies.LSTM_backtest import LSTMtest
from deeplearning.LSTM import LSTMpredict
from templates.BackTestResult import BackTestResult
from PyQt5.QtCore import Qt


class LSTMBacktest(QDialog):
    def __init__(self):
        super(LSTMBacktest,self).__init__()
        self.codepool = ["000001","000004",]
        self.initUI()

    def initUI(self):
        self.resize(900,600)
        self.setWindowTitle("QUANT XH 金融终端——LSTM预测股价回测")
        self.setWindowIcon(QIcon("static/icon.png"))

        self.tcodelabel = QLabel()
        self.tcodelabel.setText("训练股票")
        self.tcodelabel.setFont(QFont("仿宋", 15))
        self.tcodeedit = QTextEdit()
        self.tcodeedit.setFont(QFont("仿宋", 12))
        self.tcodeedit.setFixedSize(150, 30)
        self.tcodeedit.setText("000002")

        self.tfromtimelabel = QLabel()
        self.tfromtimelabel.setText("开始时间")
        self.tfromtimelabel.setFont(QFont("仿宋", 15))
        self.tfromtimeedit = QDateEdit()
        datefrom = datetime.strptime("2001-01-01", "%Y-%m-%d").date()
        self.tfromtimeedit.setDate(datefrom)
        self.tfromtimeedit.setFont(QFont("仿宋", 12))
        self.tfromtimeedit.setFixedSize(200, 30)
        self.ttotimelabel = QLabel()
        self.ttotimelabel.setText("结束时间")
        self.ttotimelabel.setFont(QFont("仿宋", 15))
        self.ttotimeedit = QDateEdit()
        dateto = datetime.strptime("2020-04-30", "%Y-%m-%d").date()
        self.ttotimeedit.setDate(dateto)
        self.ttotimeedit.setFont(QFont("仿宋", 12))
        self.ttotimeedit.setFixedSize(200, 30)

        self.trainbtn = QPushButton()
        self.trainbtn.setText("开始训练")
        self.trainbtn.setFixedSize(120, 40)
        self.trainbtn.setFont(QFont("仿宋", 12))
        self.trainbtn.clicked.connect(self.con_model)

        self.acclabel = QLabel()
        self.acclabel.setFont(QFont("仿宋", 12))
        self.acclabel.setText("准确率：")
        self.accnlabel = QLabel()
        self.accnlabel.setFont(QFont("仿宋", 12))
        self.accnlabel.setText("")
        self.accnlabel.setFixedWidth(100)

        self.poollabel = QLabel()
        self.poollabel.setText("股票池")
        self.poollabel.setFont(QFont("仿宋", 15))
        self.pooledit = QTextEdit()
        self.pooledit.setFont(QFont("仿宋", 12))
        self.pooledit.setFixedSize(120, 30)
        self.pooladdbtn = QPushButton()
        self.pooladdbtn.setText("添加股票")
        self.pooladdbtn.setFont(QFont("仿宋", 12))
        self.pooladdbtn.setFixedSize(100, 30)
        self.pooladdbtn.clicked.connect(self.addCode)
        self.poolclbtn = QPushButton()
        self.poolclbtn.setText("清空")
        self.poolclbtn.setFont(QFont("仿宋", 12))
        self.poolclbtn.setFixedSize(80, 30)
        self.poolclbtn.clicked.connect(self.clearPool)
        self.pooltb = QTextBrowser()
        self.pooltb.setFixedSize(300, 200)
        self.pooltb.setFont(QFont("仿宋", 12))

        self.buylabel = QLabel()
        self.buylabel.setText("买入涨幅")
        self.buylabel.setFont(QFont("仿宋", 15))
        self.buyedit = QTextEdit()
        self.buyedit.setFont(QFont("仿宋", 12))
        self.buyedit.setFixedSize(120, 30)
        self.buyedit.setText("0.02")

        self.selllabel = QLabel()
        self.selllabel.setText("卖出跌幅")
        self.selllabel.setFont(QFont("仿宋", 15))
        self.selledit = QTextEdit()
        self.selledit.setFont(QFont("仿宋", 12))
        self.selledit.setFixedSize(120, 30)
        self.selledit.setText("0.02")

        self.ckfromtimelabel = QLabel()
        self.ckfromtimelabel.setText("窗口开始时间")
        self.ckfromtimelabel.setFont(QFont("仿宋", 15))
        self.ckfromtimeedit = QDateEdit()
        datefrom = datetime.strptime("2018-07-01", "%Y-%m-%d").date()
        self.ckfromtimeedit.setDate(datefrom)
        self.ckfromtimeedit.setFont(QFont("仿宋", 12))
        self.ckfromtimeedit.setFixedSize(200, 30)
        self.cktotimelabel = QLabel()
        self.cktotimelabel.setText("窗口结束时间")
        self.cktotimelabel.setFont(QFont("仿宋", 15))
        self.cktotimeedit = QDateEdit()
        dateto = datetime.strptime("2019-12-31", "%Y-%m-%d").date()
        self.cktotimeedit.setDate(dateto)
        self.cktotimeedit.setFont(QFont("仿宋", 12))
        self.cktotimeedit.setFixedSize(200, 30)

        self.ycfromtimelabel = QLabel()
        self.ycfromtimelabel.setText("预测开始时间")
        self.ycfromtimelabel.setFont(QFont("仿宋", 15))
        self.ycfromtimeedit = QDateEdit()
        datefrom = datetime.strptime("2019-01-01", "%Y-%m-%d").date()
        self.ycfromtimeedit.setDate(datefrom)
        self.ycfromtimeedit.setFont(QFont("仿宋", 12))
        self.ycfromtimeedit.setFixedSize(200,30)
        self.yctotimelabel = QLabel()
        self.yctotimelabel.setText("预测结束时间")
        self.yctotimelabel.setFont(QFont("仿宋", 15))
        self.yctotimeedit = QDateEdit()
        dateto = datetime.strptime("2019-12-31", "%Y-%m-%d").date()
        self.yctotimeedit.setDate(dateto)
        self.yctotimeedit.setFont(QFont("仿宋", 12))
        self.yctotimeedit.setFixedSize(200,30)

        self.cashlabel = QLabel()
        self.cashlabel.setText("初始资金")
        self.cashlabel.setFont(QFont("仿宋", 15))
        self.cashedit = QTextEdit()
        self.cashedit.setText("1000000")
        self.cashedit.setFont(QFont("仿宋", 12))
        self.cashedit.setFixedSize(200,30)

        self.amountlabel = QLabel()
        self.amountlabel.setText("单笔交易股数")
        self.amountlabel.setFont(QFont("仿宋", 15))
        self.amountedit = QTextEdit()
        self.amountedit.setText("1000")
        self.amountedit.setFont(QFont("仿宋", 12))
        self.amountedit.setFixedSize(200,30)

        self.selectbtn = QPushButton()
        self.selectbtn.setText("开始回测")
        self.selectbtn.setFixedSize(120,40)
        self.selectbtn.setFont(QFont("仿宋", 12))
        self.selectbtn.clicked.connect(self.backTest)
        self.selectbtn.setEnabled(False)

        self.h10box = QHBoxLayout()
        self.h10box.addWidget(self.tcodelabel)
        self.h10box.addWidget(self.tcodeedit)
        self.h105box = QHBoxLayout()
        self.h105box.addWidget(self.tfromtimelabel)
        self.h105box.addWidget(self.tfromtimeedit)
        self.h106box = QHBoxLayout()
        self.h106box.addWidget(self.ttotimelabel)
        self.h106box.addWidget(self.ttotimeedit)
        self.h107box = QHBoxLayout()
        self.h107box.addWidget(self.trainbtn)
        self.h107box.addWidget(self.acclabel)
        self.h107box.addWidget(self.accnlabel)
        self.h11box = QHBoxLayout()
        self.h11box.addWidget(self.pooledit)
        self.h11box.addWidget(self.pooladdbtn)
        self.h11box.addWidget(self.poolclbtn)
        self.h12box = QHBoxLayout()
        self.h12box.addWidget(self.pooltb)
        self.h13box = QHBoxLayout()
        self.h13box.addWidget(self.buylabel)
        self.h13box.addWidget(self.buyedit)
        self.h14box = QHBoxLayout()
        self.h14box.addWidget(self.selllabel)
        self.h14box.addWidget(self.selledit)


        self.v1box = QVBoxLayout()
        self.v1box.addStretch(1)
        self.v1box.addLayout(self.h10box)
        self.v1box.addLayout(self.h105box)
        self.v1box.addLayout(self.h106box)
        self.v1box.addLayout(self.h107box)
        self.v1box.addStretch(1)
        self.v1box.addWidget(self.poollabel)
        self.v1box.addLayout(self.h11box)
        self.v1box.addLayout(self.h12box)
        self.v1box.addStretch(1)
        self.v1box.addLayout(self.h13box)
        self.v1box.addLayout(self.h14box)
        self.v1box.addStretch(1)

        self.h21box = QHBoxLayout()
        self.h21box.addWidget(self.selectbtn)
        # self.h21box.addWidget(self.resultbtn)

        self.v2box = QVBoxLayout()
        self.v2box.addStretch(1)
        self.v2box.addWidget(self.ckfromtimelabel)
        self.v2box.addWidget(self.ckfromtimeedit)
        self.v2box.addStretch(1)
        self.v2box.addWidget(self.cktotimelabel)
        self.v2box.addWidget(self.cktotimeedit)
        self.v2box.addStretch(1)
        self.v2box.addWidget(self.ycfromtimelabel)
        self.v2box.addWidget(self.ycfromtimeedit)
        self.v2box.addStretch(1)
        self.v2box.addWidget(self.yctotimelabel)
        self.v2box.addWidget(self.yctotimeedit)
        self.v2box.addStretch(1)
        self.v2box.addWidget(self.cashlabel)
        self.v2box.addWidget(self.cashedit)
        self.v2box.addStretch(1)
        self.v2box.addWidget(self.amountlabel)
        self.v2box.addWidget(self.amountedit)
        self.v2box.addStretch(1)
        self.v2box.addLayout(self.h21box)
        self.v2box.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.v1box)
        self.hbox.addStretch(1)
        self.hbox.addLayout(self.v2box)
        self.hbox.addStretch(1)

        self.setLayout(self.hbox)
        self.pooltb.setPlainText(' '.join(self.codepool))

    def addCode(self):
        f = FETCH()
        code = self.pooledit.toPlainText()
        if code in self.codepool:
            print(QMessageBox.information(self, "提示", "该股票已经存在于股票池中！", QMessageBox.Yes, QMessageBox.Yes))
        elif code not in list(f.fetch_stock_list()['code']):
            print(QMessageBox.information(self, "提示", "该股票代码不存在！", QMessageBox.Yes, QMessageBox.Yes))
        else:
            self.codepool.append(code)
            self.pooledit.clear()
        self.pooltb.setPlainText(' '.join(self.codepool))

    def clearPool(self):
        self.codepool = []
        self.pooltb.setPlainText(' '.join(self.codepool))

    def con_model(self):
        self.tcode = self.tcodeedit.toPlainText()
        lstm = LSTMpredict()
        lstm.get_data(self.tcodeedit.toPlainText(), self.change_name(self.tfromtimeedit.text()),
                      self.change_name(self.ttotimeedit.text()))
        lstm.nomalize()
        lstm.cons_sets(cut=99)
        lstm.make_model()
        lstm.train_performance()
        lstm.test_performance()
        lstm.output_result()
        self.model = lstm.model
        self.accnlabel.setText(str(lstm.result * 100)[:4] + "%")
        self.selectbtn.setEnabled(True)

    def backTest(self):
        r = LSTMtest(cash=int(self.cashedit.toPlainText()))
        print(self.codepool)

        r.LSTM_backtest(tcode=self.tcode,codep=self.codepool,ckstart=self.change_name(self.ckfromtimeedit.text()),
                          ckend=self.change_name(self.cktotimeedit.text()),ycstart=self.change_name(self.ycfromtimeedit.text()),
                          ycend=self.change_name(self.yctotimeedit.text()),amount=int(self.amountedit.toPlainText()),
                        model=self.model,buy=float(self.buyedit.toPlainText()),sell=float(self.selledit.toPlainText()))
        r.save_to_mongo()
        self.btResult(r.ACstr)

    def change_name(self,s):
        l = s.split('/')
        if len(l[1]) == 1:
            l[1] = "0" + l[1]
        if len(l[2]) == 1:
            l[2] = "0" + l[2]
        return ("-".join(l))

    def btResult(self,AC_id):
        dialog = BackTestResult(ACid=AC_id)
        dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        dialog.show()
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    lstmbwindow = LSTMBacktest()
    lstmbwindow.show()
    sys.exit(app.exec_())
