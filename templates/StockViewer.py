import sys
from PyQt5.QtWidgets import (QWidget,QApplication,QVBoxLayout,QHBoxLayout,
                             QLineEdit,QPushButton,QComboBox,QLabel,QMessageBox,
                             QTableView,QHeaderView,QAbstractItemView,QDialog)
from PyQt5.QtGui import QIcon, QFont, QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
import qdarkstyle
from fetch_data import FETCH


class StockViewer(QDialog):
    def __init__(self):
        super(StockViewer,self).__init__()
        self.resize(800,500)
        self.setWindowTitle('QUANT XH 金融终端')
        self.setWindowIcon(QIcon('static/icon.png'))
        self.queryModel = None
        self.tableView = None
        self.currentPage = 1
        self.totalPage = 0
        self.displayRecord = 0
        self.totalRecord = 0
        self.pageRecord = 10
        self.initUI()

    def initUI(self):
        f = FETCH()
        self.stock_data = f.fetch_stock_list()
        self.totalRecord = len(self.stock_data)
        self.totalPage = self.totalRecord // 10 + 1
        self.vbox = QVBoxLayout()
        self.h1box = QHBoxLayout()
        self.h2box = QHBoxLayout()

        self.searchEdit = QLineEdit()
        self.searchEdit.setFixedHeight(32)
        self.searchEdit.setFont(QFont("仿宋", 15))

        self.searchButton = QPushButton("查询")
        self.searchButton.setFixedHeight(32)
        self.searchButton.setFont(QFont("仿宋", 15))

        self.condisionComboBox = QComboBox()
        searchCondision = ["按股票编号查找","按股票名称查找"]
        self.condisionComboBox.setFixedHeight(32)
        self.condisionComboBox.setFont(QFont("仿宋", 15))
        self.condisionComboBox.addItems(searchCondision)

        self.h1box.addWidget(self.searchEdit)
        self.h1box.addWidget(self.condisionComboBox)
        self.h1box.addWidget(self.searchButton)

        self.currentPageLabel = QLabel(self)
        self.currentPageLabel.setFixedWidth(140)
        self.currentPageLabel.setFont(QFont("仿宋", 12))

        self.jumpToLabel = QLabel(self)
        self.jumpToLabel.setText("跳转到第")
        self.jumpToLabel.setFont(QFont("仿宋", 12))
        self.jumpToLabel.setFixedWidth(90)
        self.pageEdit = QLineEdit()
        self.pageEdit.setFixedWidth(30)
        self.pageEdit.setFont(QFont("仿宋", 12))
        self.pageLabel = QLabel(self)
        self.pageLabel.setText("/" + str(self.totalPage) + "页")
        self.pageLabel.setFont(QFont("仿宋", 12))
        self.pageLabel.setFixedWidth(60)
        self.jumpToButton = QPushButton(self)
        self.jumpToButton.setText("跳转")
        self.jumpToButton.setFont(QFont("仿宋", 12))
        self.jumpToButton.setFixedHeight(30)
        self.jumpToButton.setFixedWidth(60)
        self.prevButton = QPushButton("前一页")
        self.prevButton.setFont(QFont("仿宋", 12))
        self.prevButton.setFixedHeight(30)
        self.prevButton.setFixedWidth(80)
        self.backButton = QPushButton("后一页")
        self.backButton.setFont(QFont("仿宋", 12))
        self.backButton.setFixedHeight(30)
        self.backButton.setFixedWidth(80)
        self.prevButton.clicked.connect(self.prevButtonClicked)
        self.backButton.clicked.connect(self.backButtonClicked)
        self.jumpToButton.clicked.connect(self.jumpToButtonClicked)
        self.searchButton.clicked.connect(self.searchButtonClicked)

        self.detailbutton = QPushButton(self)
        self.detailbutton.setText("详细信息")
        self.detailbutton.setFixedWidth(90)
        self.detailbutton.setFont(QFont("仿宋", 12))

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.currentPageLabel)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.jumpToLabel)
        self.hbox.addWidget(self.pageEdit)
        self.hbox.addWidget(self.pageLabel)
        self.hbox.addWidget(self.jumpToButton)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.detailbutton)
        self.hbox.addStretch(1)
        self.hbox.addWidget(self.prevButton)
        self.hbox.addWidget(self.backButton)
        widget = QWidget()
        widget.setLayout(self.hbox)
        self.h2box.addWidget(widget)

        self.tableView = QTableView()
        self.tableView.horizontalHeader().setStretchLastSection(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableView.setFont(QFont("仿宋", 12))
        self.tableView.horizontalHeader().setFont(QFont("仿宋", 12))

        self.queryModel = QStandardItemModel(self.pageRecord, 2)
        self.updateQueryModel()

        self.vbox.addLayout(self.h1box)
        self.vbox.addWidget(self.tableView)
        self.vbox.addLayout(self.h2box)
        self.setLayout(self.vbox)

    def setButtonStatus(self):
        if(self.currentPage==self.totalPage and self.currentPage == 1):
            self.prevButton.setEnabled(False)
            self.backButton.setEnabled(False)
        elif(self.currentPage==self.totalPage):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(False)
        elif(self.currentPage==1):
            self.backButton.setEnabled(True)
            self.prevButton.setEnabled(False)
        elif(self.currentPage<self.totalPage and self.currentPage>1):
            self.prevButton.setEnabled(True)
            self.backButton.setEnabled(True)

    def searchButtonClicked(self):
        f = FETCH()
        try:
            if self.searchEdit.text() == "":
                self.stock_data = f.fetch_stock_list()
                self.totalRecord = len(self.stock_data)
                self.totalPage = self.totalRecord // 10 + 1
                self.currentPage = 1
                self.pageLabel.setText("/" + str(self.totalPage) + "页")
                self.updateQueryModel()
            elif self.condisionComboBox.currentText() == "按股票编号查找":
                self.stock_data = f.fuzzy_fetch_stock_list(self.searchEdit.text(),"code")
                self.totalRecord = len(self.stock_data)
                self.totalPage = self.totalRecord // 10 + 1
                self.currentPage = 1
                self.pageLabel.setText("/" + str(self.totalPage) + "页")
                self.updateQueryModel()
            elif self.condisionComboBox.currentText() == "按股票名称查找":
                self.stock_data = f.fuzzy_fetch_stock_list(self.searchEdit.text(), "name")
                self.totalRecord = len(self.stock_data)
                self.totalPage = self.totalRecord // 10 + 1
                self.currentPage = 1
                self.pageLabel.setText("/" + str(self.totalPage) + "页")
                self.updateQueryModel()
        except KeyError:
            print(QMessageBox.warning(self, "警告", "没有记录与之匹配", QMessageBox.Yes, QMessageBox.Yes))


    def prevButtonClicked(self):
        self.currentPage -= 1
        self.updateQueryModel()

    def backButtonClicked(self):
        self.currentPage += 1
        self.updateQueryModel()

    def jumpToButtonClicked(self):
        if (self.pageEdit.text().isdigit()):
            self.currentPage = int(self.pageEdit.text())
            if (self.currentPage > self.totalPage):
                self.currentPage = self.totalPage
            if (self.currentPage <= 1):
                self.currentPage = 1
        else:
            self.currentPage = 1
        self.updateQueryModel()

    def updateQueryModel(self):
        self.queryModel.clear()
        self.displayRecord = self.pageRecord if self.currentPage < self.totalPage else self.totalRecord % self.pageRecord
        for row in range(0, self.displayRecord):
            for column in range(2):
                item = QStandardItem(self.stock_data.iloc[(self.currentPage - 1) * self.pageRecord + row, column])
                self.queryModel.setItem(row, column, item)
        self.currentPageLabel.setText("当前页数：" + str(self.currentPage))
        self.tableView.setModel(self.queryModel)
        self.setButtonStatus()
        self.queryModel.setHeaderData(0, Qt.Horizontal, "股票编号")
        self.queryModel.setHeaderData(1, Qt.Horizontal, "股票名称")
        self.pageEdit.setText("")
        return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    stockviewerWindow = StockViewer()
    stockviewerWindow.show()
    sys.exit(app.exec_())