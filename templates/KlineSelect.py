import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,QMessageBox,
                             QVBoxLayout,QTextEdit,QDateEdit,QPushButton)
import qdarkstyle
from PyQt5.QtGui import QIcon, QFont
from Klines import KlinesDialog
from datetime import datetime
from fetch_data import FETCH


class KlineSelect(QDialog):
    def __init__(self, code="000001", fromtime="2020-01-01", totime="2020-03-01"):
        super(KlineSelect,self).__init__()
        self.code = code
        self.fromtime = fromtime
        self.totime = totime
        self.initUI()

    def initUI(self):
        self.resize(800,600)
        self.setWindowTitle("QUANT XH 金融终端")
        self.setWindowIcon(QIcon("static/icon.png"))

        self.h1box = QHBoxLayout()
        self.codelabel = QLabel()
        self.codelabel.setText("股票代码")
        self.codelabel.setFont(QFont("仿宋", 12))
        self.codeedit = QTextEdit()
        self.codeedit.setFont(QFont("仿宋", 12))
        self.codeedit.setFixedSize(120,25)
        self.codeedit.setText(self.code)

        self.fromtimelabel = QLabel()
        self.fromtimelabel.setText("起始时间")
        self.fromtimelabel.setFont(QFont("仿宋", 12))
        self.fromtimeedit = QDateEdit()
        self.fromtimeedit.setFixedSize(150, 25)
        self.fromtimeedit.setFont(QFont("仿宋", 12))
        datefrom = datetime.strptime(self.fromtime,"%Y-%m-%d").date()
        self.fromtimeedit.setDate(datefrom)

        self.totimelabel = QLabel()
        self.totimelabel.setText("起始时间")
        self.totimelabel.setFont(QFont("仿宋", 12))
        self.totimeedit = QDateEdit()
        self.totimeedit.setFixedSize(150, 25)
        self.totimeedit.setFont(QFont("仿宋", 12))
        dateto = datetime.strptime(self.totime, "%Y-%m-%d").date()
        self.totimeedit.setDate(dateto)

        self.selectbutton = QPushButton()
        self.selectbutton.setText("选择")
        self.selectbutton.setFont(QFont("仿宋", 12))
        self.selectbutton.clicked.connect(self.updateKlines)

        self.h1box.addStretch(1)
        self.h1box.addWidget(self.codelabel)
        self.h1box.addWidget(self.codeedit)
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.fromtimelabel)
        self.h1box.addWidget(self.fromtimeedit)
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.totimelabel)
        self.h1box.addWidget(self.totimeedit)
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.selectbutton)
        self.h1box.addStretch(1)

        self.klineswindow = KlinesDialog(type="A",code=self.code,fromtime=self.fromtime,totime=self.totime)

        self.v1box = QVBoxLayout()
        self.v1box.addWidget(self.klineswindow)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.v1box)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)

    def updateKlines(self):
        self.code = self.codeedit.toPlainText()

        def change_name(s):
            l = s.split('/')
            if len(l[1]) == 1:
                l[1] = "0" + l[1]
            if len(l[2]) == 1:
                l[2] = "0" + l[2]
            return ("-".join(l))

        self.fromtime = change_name(self.fromtimeedit.text())
        self.totime = change_name(self.totimeedit.text())

        f = FETCH()
        stock_list = list(f.fetch_stock_list()['code'])
        if self.code not in stock_list:
            print(QMessageBox.information(self, "提示", "您输入了不正确的或是已下架的代码!", QMessageBox.Yes, QMessageBox.Yes))
        else:
            self.klineswindow.close()
            self.klineswindow = KlinesDialog(type="A",code=self.code,fromtime=self.fromtime,totime=self.totime)
            self.v1box.addWidget(self.klineswindow)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    klineselect = KlineSelect(code="000001", fromtime="2020-01-01", totime="2020-03-01")
    klineselect.show()
    sys.exit(app.exec_())