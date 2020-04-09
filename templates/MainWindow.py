import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction
from PyQt5.QtGui import QIcon, QFont
from templates.SignIn import SignInWidget
from templates.SignUp import SignUpWidget
from templates.About import AboutDialog
from templates.ChangePsw import ChangePswDialog
from templates.UserHome import UserHome
from templates.UpdateData import UpdateDataDialog
import qdarkstyle


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.initUI()

    def initUI(self):
        self.resize(800, 600)
        self.setWindowTitle('QUANT XH 金融终端')
        self.setWindowIcon(QIcon('static/icon.png'))

        self.widget = SignInWidget()
        self.setCentralWidget(self.widget)

        menubar = self.menuBar()
        menubar.setFont(QFont("仿宋", 15))
        self.menu = menubar.addMenu('菜单栏')
        self.menu.setFont(QFont("仿宋", 15))
        self.signupaction = QAction("注    册",self)
        self.signinaction = QAction('登    录',self)
        self.changepswaction = QAction("修改密码", self)
        self.aboutaction = QAction("关    于",self)
        self.quitsigninaction = QAction("退出登录",self)
        self.quitaction = QAction("退    出", self)
        self.updateaction = QAction("数据更新", self)
        self.menu.addAction(self.signupaction)
        self.menu.addAction(self.signinaction)
        self.menu.addAction(self.changepswaction)
        self.menu.addAction(self.aboutaction)
        self.menu.addAction(self.quitsigninaction)
        self.menu.addAction(self.quitaction)
        self.menu.addAction(self.updateaction)
        self.signupaction.setEnabled(True)
        self.changepswaction.setEnabled(True)
        self.signinaction.setEnabled(False)
        self.quitsigninaction.setEnabled(False)

        self.widget.is_user_signal[str].connect(self.userSignIn)
        self.menu.triggered[QAction].connect(self.menuTriggered)

    def menuTriggered(self,q):
        if(q.text() == "注    册"):
            self.widget = SignUpWidget()
            self.setCentralWidget(self.widget)
            self.signupaction.setEnabled(False)
            self.changepswaction.setEnabled(True)
            self.signinaction.setEnabled(True)
            self.quitsigninaction.setEnabled(False)
        if(q.text() == "登    录"):
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_user_signal[str].connect(self.userSignIn)
            self.signupaction.setEnabled(True)
            self.changepswaction.setEnabled(True)
            self.signinaction.setEnabled(False)
            self.quitsigninaction.setEnabled(False)
        if(q.text() == "退出登录"):
            self.widget = SignInWidget()
            self.setCentralWidget(self.widget)
            self.widget.is_user_signal[str].connect(self.userSignIn)
            self.resize(800, 600)
            self.signupaction.setEnabled(True)
            self.changepswaction.setEnabled(True)
            self.signinaction.setEnabled(False)
            self.quitsigninaction.setEnabled(False)
        if (q.text() == "修改密码"):
            changepswDialog = ChangePswDialog()
            changepswDialog.show()
            changepswDialog.exec_()
        if(q.text() == "关    于"):
            aboutDialog = AboutDialog()
            aboutDialog.show()
            aboutDialog.exec_()
        if (q.text() == "数据更新"):
            updateDialog = UpdateDataDialog()
            updateDialog.show()
            updateDialog.exec_()
        if(q.text() == "退    出"):
            qApp = QApplication.instance()
            qApp.quit()
        return

    def userSignIn(self,userId):
        self.widget = UserHome(userId)
        self.setCentralWidget(self.widget)
        self.signupaction.setEnabled(False)
        self.changepswaction.setEnabled(False)
        self.signinaction.setEnabled(False)
        self.quitsigninaction.setEnabled(True)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())