import sys
from PyQt5.QtWidgets import (QDialog, QHBoxLayout, QApplication,
                             QVBoxLayout, QPushButton)
import qdarkstyle
from PyQt5.QtGui import QIcon, QFont
from templates.StockViewer import StockViewer
from Klines import KlinesDialog
from templates.KlineSelect import KlineSelect
from templates.MainBackTest import MainBackTest
from templates.BackTestViewer import BackTestViewer


class UserHome(QDialog):
    def __init__(self, UserId):
        self.userid = UserId
        super(UserHome,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(700,1000)
        self.setWindowTitle("quant XH 金融终端")
        self.setWindowIcon(QIcon("static/icon.png"))

        self.stockviewer = StockViewer()
        self.stockviewer.setFixedSize(700,500)
        self.klines = KlinesDialog()
        self.klines.setFixedHeight(400)
        self.backtestbtn = QPushButton()
        self.backtestbtn.setFont(QFont("仿宋", 12))
        self.backtestbtn.setText("量化回测")
        self.backtestbtn.setFixedSize(120,50)
        self.backtestbtn.clicked.connect(self.mbtDialog)
        self.historybtn = QPushButton()
        self.historybtn.setFont(QFont("仿宋", 12))
        self.historybtn.setText("回测历史")
        self.historybtn.setFixedSize(120, 50)
        self.historybtn.clicked.connect(self.btvDialog)
        self.kswindow = KlineSelect()
        self.kswindow.setFixedWidth(1000)

        self.v1box = QVBoxLayout()
        self.v1box.addWidget(self.klines)
        self.v1box.addWidget(self.stockviewer)

        self.h21box = QHBoxLayout()
        self.h21box.addStretch(5)
        self.h21box.addWidget(self.backtestbtn)
        self.h21box.addStretch(1)
        self.h21box.addWidget(self.historybtn)
        self.h21box.addStretch(1)

        self.v2box = QVBoxLayout()
        self.v2box.addStretch(3)
        self.v2box.addWidget(self.kswindow)
        self.v2box.addStretch(2)
        self.v2box.addLayout(self.h21box)
        self.v2box.addStretch(1)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.v1box)
        self.hbox.addLayout(self.v2box)

        self.setLayout(self.hbox)

    def mbtDialog(self):
        dialog = MainBackTest()
        dialog.show()
        dialog.exec_()

    def btvDialog(self):
        dialog = BackTestViewer()
        dialog.show()
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    userhome = UserHome("csxuhuan")
    userhome.show()
    sys.exit(app.exec_())