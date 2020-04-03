import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout, QPushButton, QTextBrowser)
import qdarkstyle
from PyQt5.QtGui import QIcon,QPixmap,QFont
from QUANTAXIS.QASU.main import (QA_SU_save_index_day, QA_SU_save_index_list,
                                 QA_SU_save_stock_block, QA_SU_save_stock_day,
                                 QA_SU_save_stock_info, QA_SU_save_stock_list,
                                 QA_SU_save_stock_xdxr)
import datetime


class UpdateDataDialog(QDialog):
    def __init__(self):
        super(UpdateDataDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(700,500)
        self.setWindowTitle("QUANT XH 金融终端——数据更新")
        self.setWindowIcon(QIcon("static/icon.png"))

        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('static/title.png')
        self.titlelabel.setPixmap(self.titleimage)

        self.updatebutton = QPushButton()
        self.updatebutton.setFont(QFont("仿宋", 12))
        self.updatebutton.setText("更新数据")
        self.updatebutton.clicked.connect(self.updateButtonClicked_before)
        self.updatebutton.clicked.connect(self.updateButtonClicked)
        self.updatebutton.clicked.connect(self.updateButtonClicked_after)
        self.timelabel = QLabel()
        f = open("./static/local.txt", "r+")
        self.timelabel.setText("上次更新时间："+f.readline())
        f.close()


        self.browser = QTextBrowser()
        self.browser.setFixedSize(500, 300)

        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.titlelabel)
        self.h1box.addStretch(1)

        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.updatebutton)
        self.h2box.addStretch(1)

        self.h3box = QHBoxLayout()
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.browser)
        self.h3box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h2box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h3box)
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.timelabel)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)

    def updateButtonClicked_before(self):

        self.updatebutton.setEnabled(False)

        self.browser.append("正在更新数据……")


    def updateButtonClicked(self):
        QA_SU_save_index_day('tdx')
        QA_SU_save_index_list('tdx')
        QA_SU_save_stock_block('tdx')
        QA_SU_save_stock_day('tdx')
        QA_SU_save_stock_info('tdx')
        QA_SU_save_stock_list('tdx')
        QA_SU_save_stock_xdxr('tdx')

    def updateButtonClicked_after(self):
        self.browser.append("更新结束！！")

        now = datetime.datetime.now()
        f = open("./static/local.txt", "r+")
        f.write(now.strftime("%Y-%m-%d %H:%M:%S"))
        f.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    updateWindow = UpdateDataDialog()
    updateWindow.show()
    sys.exit(app.exec_())