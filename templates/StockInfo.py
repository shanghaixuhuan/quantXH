import sys
from PyQt5.QtWidgets import (QDialog,QApplication,QGridLayout,QLabel,QHBoxLayout,
                             QVBoxLayout)
import qdarkstyle
from PyQt5.QtGui import QIcon, QFont,QPixmap
from fetch_data import FETCH


class StockInfo(QDialog):
    def __init__(self, code, name):
        super(StockInfo,self).__init__()
        self.code = code
        self.name = name
        self.resize(700, 500)
        self.setWindowTitle("QUANT XH 金融终端")
        self.setWindowIcon(QIcon("static/icon.png"))
        self.initUI()

    def initUI(self):
        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('static/title.png')
        self.titlelabel.setPixmap(self.titleimage)
        self.hbox = QHBoxLayout()
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.titlelabel)
        self.hbox.addStretch(1)

        f = FETCH()
        data = f.fetch_stock_info(self.code)
        data['股票名称'] = self.name
        self.grid = QGridLayout()
        keys = list(data.keys())
        values = list(data.values())
        for i in range(len(data)):
            row = i // 4
            col = i % 4
            label = QLabel()
            label.setText(keys[i]+":"+str(values[i]))
            label.setFont(QFont("仿宋", 15))
            self.grid.addWidget(label, row, col)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.grid)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    stockinfoWindow = StockInfo("000001","平安银行")
    stockinfoWindow.show()
    sys.exit(app.exec_())