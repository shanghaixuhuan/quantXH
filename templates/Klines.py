import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout,QGridLayout)
import qdarkstyle
from PyQt5.QtGui import QIcon
from matplotlib.finance import candlestick_ohlc
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib import dates as mdates
from fetch_data import FETCH


class MyFigure(FigureCanvas):
    def __init__(self,width=5, height=4, dpi=100):
        # 创建一个创建Figure
        self.fig = Figure(facecolor="k", figsize=(width, height), dpi=dpi)
        print(type(self.fig))
        # 在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig) # 此句必不可少，否则不能显示图形
        # 创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.ax1 = self.fig.add_subplot(1,1,1)


class KlinesDialog(QDialog):
    def __init__(self):
        super(KlinesDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(900,600)
        self.setWindowTitle("QUANT XH 金融终端")
        self.setWindowIcon(QIcon("static/icon.png"))

        self.F = MyFigure(width=6, height=5, dpi=100)
        self.plotKlines()

        self.gbox = QGridLayout()
        self.gbox.addWidget(self.F,0,1)

        self.setLayout(self.gbox)

    def plotKlines(self):
        f = FETCH()
        df = f.fetch_index_day("000001","2019-01-01","2019-12-31")
        candlestick_ohlc(self.F.ax1, df, width=.6, colorup='r', colordown='g')
        self.F.ax1.plot()
        self.F.ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.F.ax1.grid(True, color='w')
        self.F.ax1.set_facecolor("k")
        self.F.ax1.tick_params(axis='y', colors='w')
        self.F.ax1.tick_params(axis='x', colors='w')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    klinesWindow = KlinesDialog()
    klinesWindow.show()
    sys.exit(app.exec_())