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
        self.fig = Figure(facecolor="k", figsize=(width, height), dpi=dpi)
        super(MyFigure,self).__init__(self.fig)
        self.ax1 = self.fig.add_subplot(1,1,1)


class KlinesDialog(QDialog):
    def __init__(self, type="index", code="000001", fromtime="2020-01-01", totime="2020-03-01"):
        super(KlinesDialog,self).__init__()
        self.type = type
        self.code = code
        self.fromtime = fromtime
        self.totime = totime
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
        if self.type == "index":
            df = f.fetch_index_day(self.code,self.fromtime,self.totime)
        elif self.type == "A":
            df = f.fetch_A_day(self.code,self.fromtime,self.totime)

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
    klinesWindow = KlinesDialog(type="A", code="000001", fromtime="2020-01-01", totime="2020-03-01")
    klinesWindow.show()
    sys.exit(app.exec_())