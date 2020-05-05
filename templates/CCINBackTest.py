import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout,QTextBrowser,QTextEdit,QPushButton,
                             QDateEdit,QMessageBox)
import qdarkstyle
from PyQt5.QtGui import QIcon, QFont
from datetime import datetime
from fetch_data import FETCH
from strategies.CCIN_backtest import CCINtest
from templates.BackTestResult import BackTestResult
from PyQt5.QtCore import Qt


class CCINBackTest(QDialog):
    def __init__(self):
        super(CCINBackTest,self).__init__()
        self.codepool = ["000001","000002","000004",]
        self.initUI()

    def initUI(self):
        self.resize(900,600)
        self.setWindowTitle("QUANT XH 金融终端——CCI N日回测")
        self.setWindowIcon(QIcon("static/icon.png"))

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
        self.pooltb.setFixedSize(300, 300)
        self.pooltb.setFont(QFont("仿宋", 12))

        self.nlabel = QLabel()
        self.nlabel.setText("N:")
        self.nlabel.setFont(QFont("仿宋", 15))
        self.nedit = QTextEdit()
        self.nedit.setText("14")
        self.nedit.setFont(QFont("仿宋", 12))
        self.nedit.setFixedSize(50, 30)

        self.texttb = QTextBrowser()
        self.texttb.setFont(QFont("仿宋", 10))
        self.texttb.setFixedSize(300, 150)
        self.texttb.setText("1.当CCI指标曲线从上向下突破+100线而重新进入常态区间时，表明市场价格的上涨阶段可能结束，将进入一个比较长时间的震荡整理阶段，应及时平多做空。\n\n"
                            "2.当CCI指标曲线从上向下突破-100线而进入另一个非常态区间（超卖区）时，表明市场价格的弱势状态已经形成，将进入一个比较长的寻底过程，可以持有空单等待更高利润。")

        self.ckfromtimelabel = QLabel()
        self.ckfromtimelabel.setText("窗口开始时间")
        self.ckfromtimelabel.setFont(QFont("仿宋", 15))
        self.ckfromtimeedit = QDateEdit()
        datefrom = datetime.strptime("2018-09-01", "%Y-%m-%d").date()
        self.ckfromtimeedit.setDate(datefrom)
        self.ckfromtimeedit.setFont(QFont("仿宋", 12))
        self.ckfromtimeedit.setFixedSize(200,30)

        self.cktotimelabel = QLabel()
        self.cktotimelabel.setText("窗口结束时间")
        self.cktotimelabel.setFont(QFont("仿宋", 15))
        self.cktotimeedit = QDateEdit()
        dateto = datetime.strptime("2019-05-20", "%Y-%m-%d").date()
        self.cktotimeedit.setDate(dateto)
        self.cktotimeedit.setFont(QFont("仿宋", 12))
        self.cktotimeedit.setFixedSize(200,30)

        self.ycfromtimelabel = QLabel()
        self.ycfromtimelabel.setText("预测开始时间")
        self.ycfromtimelabel.setFont(QFont("仿宋", 15))
        self.ycfromtimeedit = QDateEdit()
        datefrom = datetime.strptime("2019-01-01", "%Y-%m-%d").date()
        self.ycfromtimeedit.setDate(datefrom)
        self.ycfromtimeedit.setFont(QFont("仿宋", 12))
        self.ycfromtimeedit.setFixedSize(200, 30)

        self.yctotimelabel = QLabel()
        self.yctotimelabel.setText("预测结束时间")
        self.yctotimelabel.setFont(QFont("仿宋", 15))
        self.yctotimeedit = QDateEdit()
        dateto = datetime.strptime("2019-05-01", "%Y-%m-%d").date()
        self.yctotimeedit.setDate(dateto)
        self.yctotimeedit.setFont(QFont("仿宋", 12))
        self.yctotimeedit.setFixedSize(200, 30)

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
        self.amountedit.setText("3000")
        self.amountedit.setFont(QFont("仿宋", 12))
        self.amountedit.setFixedSize(200,30)

        self.selectbtn = QPushButton()
        self.selectbtn.setText("开始回测")
        self.selectbtn.setFixedSize(120,40)
        self.selectbtn.setFont(QFont("仿宋", 12))
        self.selectbtn.clicked.connect(self.backTest)

        # self.resultbtn = QPushButton()
        # self.resultbtn.setText("回测结果")
        # self.resultbtn.setFixedSize(120,40)
        # self.resultbtn.setFont(QFont("仿宋", 12))
        # self.resultbtn.setEnabled(False)

        self.h11box = QHBoxLayout()
        self.h11box.addWidget(self.pooledit)
        self.h11box.addWidget(self.pooladdbtn)
        self.h11box.addWidget(self.poolclbtn)
        self.h12box = QHBoxLayout()
        self.h12box.addWidget(self.pooltb)
        self.h14box = QHBoxLayout()
        self.h14box.addStretch(1)
        self.h14box.addWidget(self.texttb)
        self.h14box.addStretch(1)

        self.v1box = QVBoxLayout()
        self.v1box.addStretch(1)
        self.v1box.addWidget(self.poollabel)
        self.v1box.addLayout(self.h11box)
        self.v1box.addLayout(self.h12box)
        self.v1box.addStretch(1)
        self.v1box.addLayout(self.h14box)
        self.v1box.addStretch(1)

        self.h21box = QHBoxLayout()
        self.h21box.addWidget(self.selectbtn)
        # self.h21box.addWidget(self.resultbtn)
        self.h22box = QHBoxLayout()
        self.h22box.addStretch(1)
        self.h22box.addWidget(self.nlabel)
        self.h22box.addWidget(self.nedit)
        self.h22box.addStretch(1)

        self.v2box = QVBoxLayout()
        self.v2box.addStretch(1)
        self.v2box.addLayout(self.h22box)
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

    def backTest(self):

        def change_name(s):
            l = s.split('/')
            if len(l[1]) == 1:
                l[1] = "0" + l[1]
            if len(l[2]) == 1:
                l[2] = "0" + l[2]
            return ("-".join(l))

        r = CCINtest(cash=int(self.cashedit.toPlainText()))
        r.CCIN_backtest(code=self.codepool,ckstart=change_name(self.ckfromtimeedit.text()),
                          ckend=change_name(self.cktotimeedit.text()),ycstart=change_name(self.ycfromtimeedit.text()),
                        ycend=change_name(self.yctotimeedit.text()), amount=int(self.amountedit.toPlainText()),
                        N=int(self.nedit.toPlainText()))
        r.save_to_mongo()
        # self.resultbtn.clicked.connect(self.btResult(r.ACstr))
        # self.resultbtn.setEnabled(True)
        self.btResult(r.ACstr)

    def btResult(self,AC_id):
        dialog = BackTestResult(ACid=AC_id)
        dialog.setWindowFlags(Qt.WindowStaysOnTopHint)
        dialog.show()
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    ccinbtwindow = CCINBackTest()
    ccinbtwindow.show()
    sys.exit(app.exec_())
