# coding:utf-8
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import (QDialog, QPushButton, QVBoxLayout, QApplication, QGridLayout,
                             QLabel,QHBoxLayout,QTextBrowser)
import qdarkstyle
from fetch_data import FETCH
from PyQt5.QtGui import QIcon, QFont
import matplotlib.pyplot as plt
from datetime import datetime
import sys
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()


class BackTestResult(QDialog):
    def __init__(self, ACid):
        super().__init__()
        f = FETCH()
        self.risk = f.fetch_risk(AC_id=ACid)
        self.account = f.fetch_account(AC_id=ACid)
        self.initUI()

    def initUI(self):
        self.resize(1000, 700)
        self.setWindowTitle("QUANT XH 金融终端")
        self.setWindowIcon(QIcon("static/icon.png"))
        self.figure = plt.figure(facecolor='#FFFFFF')
        self.canvas = FigureCanvas(self.figure)
        self.Draw()

        self.tb = QTextBrowser()
        self.tb.setFixedSize(300,500)
        self.tb.setFont(QFont("仿宋", 10))
        for line in self.account["history"]:
            s = str(line[0])
            if line[3] >= 0:
                s += " 买入"
            else:
                s += " 卖出"
            s += line[1] + "共" + str(abs(line[3])) + "股，单股价格是" + str(line[2]) + "\n"
            self.tb.append(s)

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.canvas)
        self.hbox.addWidget(self.tb)

        self.grid = QGridLayout()

        label = QLabel()
        label.setText("回测收益："+str(self.risk["profit"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label,0,0)
        label = QLabel()
        label.setText("年化回测收益：" + str(self.risk["annualize_return"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 0, 1)
        label = QLabel()
        label.setText("基准收益：" + str(self.risk["bm_profit"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 0, 2)
        label = QLabel()
        label.setText("年化基准收益：" + str(self.risk["bm_annualizereturn"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 0, 3)

        label = QLabel()
        label.setText("Alpha：" + str(self.risk["alpha"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 1, 0)
        label = QLabel()
        label.setText("Beta：" + str(self.risk["beta"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 1, 1)
        label = QLabel()
        label.setText("夏普率：" + str(self.risk["sharpe"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 1, 2)
        label = QLabel()
        label.setText("信息比率：" + str(self.risk["ir"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 1, 3)

        label = QLabel()
        label.setText("波动性：" + str(self.risk["volatility"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 2, 0)
        label = QLabel()
        label.setText("最大回撤：" + str(self.risk["max_dropback"]))
        label.setFont(QFont("仿宋", 12))
        self.grid.addWidget(label, 2, 1)

        self.layout = QVBoxLayout()
        self.layout.addLayout(self.hbox)
        self.layout.addLayout(self.grid)
        self.setLayout(self.layout)

    def Draw(self):

        xs = [datetime.strptime(d, '%Y-%m-%d').date() for d in self.risk["totaltimeindex"]]
        plt.plot(xs,self.risk["assets"], color = 'red', linewidth = 2)
        plt.plot(xs,self.risk["benchmark_assets"], color="blue",linewidth=2)

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    btrdialog = BackTestResult(ACid="a20200420213401")
    btrdialog.show()
    app.exec()