import sys
from PyQt5.QtWidgets import (QDialog,QHBoxLayout,QLabel,QApplication,
                             QVBoxLayout)
import qdarkstyle
from PyQt5.QtGui import QIcon,QPixmap,QFont


class AboutDialog(QDialog):
    def __init__(self):
        super(AboutDialog,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(700,500)
        self.setWindowTitle("QUANT XH 金融终端——关于")
        self.setWindowIcon(QIcon("static/icon.png"))

        # 标题标签组件
        self.titlelabel = QLabel(self)
        self.titleimage = QPixmap('static/title.png')
        self.titlelabel.setPixmap(self.titleimage)

        self.textlabel = QLabel(self)
        self.textlabel.setText("    QuantXH是证券投资分析系统，实现从MongoDB\n"
                               "数据库调取历史股票数据、使用基于PyQt5的前端界\n"
                               "面实现股票数据可视化、输入多因子选股策略实现回\n"
                               "测、策略回测结果的展示及分析等多种功能。")
        self.textlabel.setFont(QFont("仿宋",15))

        self.toolslabel = QLabel(self)
        self.toolslabel.setText("数据库：MongoDB  数据源:tushare\n"
                                "图形界面：PyQt5  回测框架：zipline\n"
                                "市场分析：TA-Lib")
        self.toolslabel.setFont(QFont("仿宋", 15))

        self.memberslabel = QLabel(self)
        self.memberslabel.setText("华东理工大学 徐涣 ( 个人主页：xhhh.fun )")
        self.memberslabel.setFont(QFont("仿宋", 15))

        self.h1box = QHBoxLayout()
        self.h1box.addStretch(1)
        self.h1box.addWidget(self.titlelabel)
        self.h1box.addStretch(1)

        self.h2box = QHBoxLayout()
        self.h2box.addStretch(1)
        self.h2box.addWidget(self.textlabel)
        self.h2box.addStretch(1)

        self.h3box = QHBoxLayout()
        self.h3box.addStretch(1)
        self.h3box.addWidget(self.toolslabel)
        self.h3box.addStretch(1)

        self.h4box = QHBoxLayout()
        self.h4box.addStretch(1)
        self.h4box.addWidget(self.memberslabel)
        self.h4box.addStretch(1)

        self.vbox = QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h1box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h2box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h3box)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.h4box)
        self.vbox.addStretch(1)

        self.setLayout(self.vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    aboutWindow = AboutDialog()
    aboutWindow.show()
    sys.exit(app.exec_())