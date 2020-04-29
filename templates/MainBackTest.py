import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout,QGridLayout,QPushButton)
import qdarkstyle
from PyQt5.QtGui import QIcon,QPixmap,QFont
from templates.RandomBackTest import RandomBackTest
from templates.MACDBackTest import MACDBackTest


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
        self.randombtn.setFixedSize(150,50)
        self.randombtn.setFont(QFont("仿宋", 13))
        self.randombtn.clicked.connect(self.RandomBackTestDialog)

        self.MACDbtn = QPushButton()
        self.MACDbtn.setText("随机买卖回测")
        self.MACDbtn.setFixedSize(150, 50)
        self.MACDbtn.setFont(QFont("仿宋", 13))
        self.MACDbtn.clicked.connect(self.MACDBackTestDialog)

        self.comingbtn = QPushButton()
        self.comingbtn.setText("敬请期待")
        self.comingbtn.setFixedSize(150, 50)
        self.comingbtn.setFont(QFont("仿宋", 13))
        self.comingbtn.setEnabled(False)

        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.titlelabel)
        self.h1box.addStretch(1)

        self.gridbox = QGridLayout()
        self.gridbox.addWidget(self.randombtn,0,0)
        self.gridbox.addWidget(self.MACDbtn,0,1)
        self.gridbox.addWidget(self.comingbtn,0,2)

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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mbtWindow = MainBackTest()
    mbtWindow.show()
    sys.exit(app.exec_())