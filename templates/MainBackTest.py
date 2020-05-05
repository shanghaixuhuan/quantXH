import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout,QGridLayout,QPushButton)
import qdarkstyle
from PyQt5.QtGui import QIcon,QPixmap,QFont
from templates.RandomBackTest import RandomBackTest
from templates.MACDBackTest import MACDBackTest
from templates.RSINBackTest import RSINBackTest
from templates.CCINBackTest import CCINBackTest
from templates.RSIJCSCBackTest import RSIJCSCBackTest
from templates.KDJBackTest import KDJBackTest


class MainBackTest(QDialog):
    def __init__(self):
        super(MainBackTest,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(700,500)
        self.setWindowTitle("QUANT XH 金融终端")
        self.setWindowIcon(QIcon("static/icon.png"))

        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('static/title.png')
        self.titlelabel.setPixmap(self.titleimage)

        self.randombtn = QPushButton()
        self.randombtn.setText("随机买卖回测")
        self.randombtn.setFixedSize(180,50)
        self.randombtn.setFont(QFont("仿宋", 12))
        self.randombtn.clicked.connect(self.RandomBackTestDialog)

        self.MACDbtn = QPushButton()
        self.MACDbtn.setText("MACD金叉死叉回测")
        self.MACDbtn.setFixedSize(180, 50)
        self.MACDbtn.setFont(QFont("仿宋", 12))
        self.MACDbtn.clicked.connect(self.MACDBackTestDialog)

        self.RSINbtn = QPushButton()
        self.RSINbtn.setText("RSI N日回测")
        self.RSINbtn.setFixedSize(180, 50)
        self.RSINbtn.setFont(QFont("仿宋", 12))
        self.RSINbtn.clicked.connect(self.RSINBackTestDialog)

        self.CCINbtn = QPushButton()
        self.CCINbtn.setText("CCI N日回测")
        self.CCINbtn.setFixedSize(180, 50)
        self.CCINbtn.setFont(QFont("仿宋", 12))
        self.CCINbtn.clicked.connect(self.CCINBackTestDialog)

        self.RSIJCSCbtn = QPushButton()
        self.RSIJCSCbtn.setText("RSI金叉死叉回测")
        self.RSIJCSCbtn.setFixedSize(180, 50)
        self.RSIJCSCbtn.setFont(QFont("仿宋", 12))
        self.RSIJCSCbtn.clicked.connect(self.RSIJCSCBackTestDialog)

        self.KDJbtn = QPushButton()
        self.KDJbtn.setText("KDJ指标回测")
        self.KDJbtn.setFixedSize(180, 50)
        self.KDJbtn.setFont(QFont("仿宋", 12))
        self.KDJbtn.clicked.connect(self.KDJBackTestDialog)

        self.comingbtn = QPushButton()
        self.comingbtn.setText("敬请期待")
        self.comingbtn.setFixedSize(180, 50)
        self.comingbtn.setFont(QFont("仿宋", 12))
        self.comingbtn.setEnabled(False)

        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.titlelabel)
        self.h1box.addStretch(1)

        self.gridbox = QGridLayout()
        self.gridbox.addWidget(self.randombtn,0,0)
        self.gridbox.addWidget(self.MACDbtn,0,1)
        self.gridbox.addWidget(self.RSINbtn,0,2)
        self.gridbox.addWidget(self.CCINbtn,1,0)
        self.gridbox.addWidget(self.RSIJCSCbtn,1,1)
        self.gridbox.addWidget(self.KDJbtn, 1, 2)
        self.gridbox.addWidget(self.comingbtn,2,0)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.gridbox)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)

    def RandomBackTestDialog(self):
        dialog = RandomBackTest()
        dialog.show()
        dialog.exec_()

    def MACDBackTestDialog(self):
        dialog = MACDBackTest()
        dialog.show()
        dialog.exec_()

    def RSINBackTestDialog(self):
        dialog = RSINBackTest()
        dialog.show()
        dialog.exec_()

    def CCINBackTestDialog(self):
        dialog = CCINBackTest()
        dialog.show()
        dialog.exec_()

    def RSIJCSCBackTestDialog(self):
        dialog = RSIJCSCBackTest()
        dialog.show()
        dialog.exec_()

    def KDJBackTestDialog(self):
        dialog = KDJBackTest()
        dialog.show()
        dialog.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mbtWindow = MainBackTest()
    mbtWindow.show()
    sys.exit(app.exec_())