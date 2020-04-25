import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout,QTextBrowser,QTextEdit,QPushButton,
                             QDateEdit,QMessageBox)
import qdarkstyle
from PyQt5.QtGui import QIcon,QPixmap,QFont
from datetime import datetime
from fetch_data import FETCH
from random_backtest import RBTest
from templates.BackTestResult import BackTestResult
from PyQt5.QtCore import Qt


class RandomBackTest(QDialog):
    def __init__(self):
        super(RandomBackTest,self).__init__()
        self.codepool = ["000001","000002","000004",]
        self.initUI()

    def initUI(self):
        self.resize(900,600)
        self.setWindowTitle("QUANT XH 金融终端——随机买卖回测")
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

        self.fromtimelabel = QLabel()
        self.fromtimelabel.setText("开始时间")
        self.fromtimelabel.setFont(QFont("仿宋", 15))
        self.fromtimeedit = QDateEdit()
        datefrom = datetime.strptime("2019-01-01", "%Y-%m-%d").date()
        self.fromtimeedit.setDate(datefrom)
        self.fromtimeedit.setFont(QFont("仿宋", 12))
        self.fromtimeedit.setFixedSize(200,30)

        self.totimelabel = QLabel()
        self.totimelabel.setText("结束时间")
        self.totimelabel.setFont(QFont("仿宋", 15))
        self.totimeedit = QDateEdit()
        dateto = datetime.strptime("2019-12-31", "%Y-%m-%d").date()
        self.totimeedit.setDate(dateto)
        self.totimeedit.setFont(QFont("仿宋", 12))
        self.totimeedit.setFixedSize(200,30)

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

        self.v1box = QVBoxLayout()
        self.v1box.addStretch(1)
        self.v1box.addWidget(self.poollabel)
        self.v1box.addLayout(self.h11box)
        self.v1box.addLayout(self.h12box)
        self.v1box.addStretch(1)

        self.h21box = QHBoxLayout()
        self.h21box.addWidget(self.selectbtn)
        # self.h21box.addWidget(self.resultbtn)

        self.v2box = QVBoxLayout()
        self.v2box.addStretch(1)
        self.v2box.addWidget(self.fromtimelabel)
        self.v2box.addWidget(self.fromtimeedit)
        self.v2box.addStretch(1)
        self.v2box.addWidget(self.totimelabel)
        self.v2box.addWidget(self.totimeedit)
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
        self.hbox.addLayout(self.v1box)
        self.hbox.addLayout(self.v2box)

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

        r = RBTest(cash=int(self.cashedit.toPlainText()))
        r.simple_backtest(self.codepool,change_name(self.fromtimeedit.text()),
                          change_name(self.totimeedit.text()),int(self.amountedit.toPlainText()))
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
    rbtwindow = RandomBackTest()
    rbtwindow.show()
    sys.exit(app.exec_())
