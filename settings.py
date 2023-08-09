import os
import sys

from PyQt5.QtCore import Qt, QTranslator, QLocale
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QApplication
from qframelesswindow import FramelessWindow, StandardTitleBar, AcrylicWindow
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar
from Ui_settings import Ui_Form
import json
import threading
class SettingsWindow(AcrylicWindow, Ui_Form):
    def closeEvent(self, e):
        config_write = open("config.json","w")
        config_write.write(json.dumps(config))
        config_read.close()
        config_write.close()
        e.accept()
    def set_electron_mirror(self,a1):
        config["ELECTRON_MIRROR"] = a1
    def set_npm_mirror(self,a1):
        config["NPM_MIRROR"] = a1
    def run_change_npm_mirror(self):
        registry_url = self.LineEdit_2.text()
        s = os.popen(f"npm config set registry {registry_url}")
    def configure_npm_mirror(self):
        registry_url = self.LineEdit_2.text()
        t = threading.Thread(target=self.run_change_npm_mirror,args=())
        t.start()
        
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        global config_read,config_write,config
        config_read = open("config.json","r")
        config = json.loads(config_read.read())
        self.LineEdit.setText(config["ELECTRON_MIRROR"])
        self.LineEdit_2.setText(config["NPM_MIRROR"])
        # setTheme(Theme.DARK)
        setThemeColor('#28afe9')
        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()

        self.setWindowTitle('Setting')
        self.resize(450, 500)
        self.PrimaryPushButton_2.clicked.connect(self.configure_npm_mirror)
        self.setFixedSize(self.width(), self.height())
        self.setWindowIcon(QIcon(":/image/image/icon.png"))
        self.LineEdit.textChanged.connect(self.set_electron_mirror)
        self.LineEdit_2.textChanged.connect(self.set_npm_mirror)
        self.windowEffect.setMicaEffect(self.winId())
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)



if __name__ == '__main__':
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    app = QApplication(sys.argv)

    # Internationalization
    translator = FluentTranslator(QLocale())
    app.installTranslator(translator)

    w = SettingsWindow()
    w.show()
    app.exec_()
