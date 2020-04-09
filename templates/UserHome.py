import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout)
import qdarkstyle
from PyQt5.QtGui import QIcon,QPixmap,QFont
from templates.StockViewer import StockViewer
from templates.Klines import KlinesDialog
from templates.KlineSelect import KlineSelect


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

        self.v1box = QVBoxLayout()
        self.v1box.addWidget(self.klines)
        self.v1box.addWidget(self.stockviewer)

        self.kswindow = KlineSelect()
        self.kswindow.setFixedWidth(1100)

        self.hbox = QHBoxLayout()
        self.hbox.addLayout(self.v1box)
        self.hbox.addWidget(self.kswindow)

        self.setLayout(self.hbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    userhome = UserHome("csxuhuan")
    userhome.show()
    sys.exit(app.exec_())