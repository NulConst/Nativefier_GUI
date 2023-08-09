import json
import subprocess
import sys
import os
from PyQt5.QtCore import Qt, QLocale, QThread,pyqtSignal
from PyQt5.QtGui import QIcon,QDoubleValidator,QColor
from PyQt5.QtWidgets import QApplication , QFileDialog
from qframelesswindow import AcrylicWindow
from qfluentwidgets import setThemeColor, FluentTranslator, setTheme, Theme, SplitTitleBar,TeachingTipTailPosition,TeachingTipView,TeachingTip,FluentIcon,ColorPickerButton,MessageBox
from cm_core import CMCore
from Ui_Main import Ui_Form
icon_file = None
weblink = ""
electron_version = None
app_name = None
upgrade_version_files = None
loading_background = None
always_on_top = False
fullscreen = False
disable_dev_tools = False
disable_right_click = False
nativefier_command = ""
JSON_VERSION = 0
NPM_MIRROR = ""
ENV=dict(os.environ)
class CMThread(QThread):
    sig = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super(CMThread, self).__init__(parent)
    
    def run(self):
        self.sig.emit("Running")
        if(os.path.exists("nodejs")):
            if(sys.platform == "win32"):
                nativefier_command = "nodejs\\node nodejs\\node_modules\\nativefier\\lib\\cli.js"
            else:
                nativefier_command = "nodejs/node nodejs/node_modules/nativefier/lib/cli.js"
        else:
            nativefier_command = "cmd.exe /c npx nativefier"
        cm_1 = CMCore(url=weblink,icon=icon_file,electron_version=electron_version,
                      app_name=app_name,upgrade_version_dir=upgrade_version_files,loading_color=loading_background,
                      fullscreen=fullscreen,disable_devtools=disable_dev_tools,disable_right_click=disable_right_click,always_on_top=always_on_top,
                      nativefier_command=nativefier_command
        )
        fcm = cm_1.get_full_command()
        output=""
        #""
        p = subprocess.Popen(fcm, stdout=subprocess.PIPE,encoding="utf-8",stderr=subprocess.STDOUT,env=ENV)
        for line in iter(p.stdout.readline, ""):
            output += line
            self.sig.emit(output)
        self.sig.emit("out")
        
    
            
        
class GM_Window(AcrylicWindow, Ui_Form):
    def closeEvent(self, event):
        title = "请问是否关闭此窗口？"
        content = "关闭后会无法使用此程序"
        w = MessageBox(title, content, self)
        if w.exec():
            event.accept()
            self.t.quit()
            ws.close()
        else:
            event.ignore()
    def switchmode(self,a0:bool):
        if(a0):
            setTheme(Theme.DARK)
            self.windowEffect.setMicaEffect(self.winId(), isDarkMode=True)
            ws.windowEffect.setMicaEffect(ws.winId(),isDarkMode=True)
            self.PlainTextEdit.setStyleSheet("PlainTextEdit {\n"
            "    color: green;\n"
            "    background-color: black;\n"
            "    border: 1px solid rgba(0, 0, 0, 13);\n"
            "    border-bottom: 1px solid rgba(0, 0, 0, 100);\n"
            "    border-radius: 5px;\n"
            "    /* font: 14px \"Segoe UI\", \"Microsoft YaHei\"; */\n"
            "    padding: 0px 10px;\n"
            "}\n"
            "")
        else:
            setTheme(Theme.LIGHT)
            self.windowEffect.setMicaEffect(self.winId(),isDarkMode=False)
            ws.windowEffect.setMicaEffect(ws.winId(),isDarkMode=False)
            self.PlainTextEdit.setStyleSheet("PlainTextEdit {\n"
            "    color: green;\n"
            "    background-color: black;\n"
            "    border: 1px solid rgba(0, 0, 0, 13);\n"
            "    border-bottom: 1px solid rgba(0, 0, 0, 100);\n"
            "    border-radius: 5px;\n"
            "    /* font: 14px \"Segoe UI\", \"Microsoft YaHei\"; */\n"
            "    padding: 0px 10px;\n"
            "}\n"
            "")
    def showtips(self):
        pos = TeachingTipTailPosition.BOTTOM_RIGHT
        view = TeachingTipView(
            icon=None,
            title='Tips',
            content="如果您需要制作一个网页应用的更新版本，请填入旧版应用的完整路径。",
            isClosable=True,
            tailPosition=pos,
        )
        w = TeachingTip.make(
            target=self.PushButton_3,
            view=view,
            duration=-1,
            tailPosition=pos,
            parent=self
        )
        view.closed.connect(w.close)
    def get_icon_files(self):
        fileInfo = QFileDialog.getOpenFileName(self, "选择文件", "C:/Users/Administrator/Desktop/test", "图标(*.ico)")
        self.BodyLabel.setText(fileInfo[0])
        global icon_file
        icon_file = fileInfo[0]
    def save_color(self,a1):
        global loading_background
        loading_background = a1.name()
        self.LineEdit_5.setText(a1.name())
    
    def set_always_on_top(self,a1):
        global always_on_top
        always_on_top = a1
    def set_fullscreen(self,a1):
        global fullscreen
        fullscreen = a1
    def set_disable_devtools(self,a1):
        global disable_dev_tools
        disable_dev_tools = a1
    def set_disable_right_click(self,a1):
        global disable_right_click
        disable_right_click = a1
    def update_command_view(self,text):
        if(text == "out"):
            self.PrimaryPushButton.setDisabled(False)
            self.IndeterminateProgressBar.setHidden(True)
            global weblink,icon_file,electron_version,app_name,upgrade_version_files,loading_background,fullscreen,disable_dev_tools,disable_right_click,always_on_top,nativefier_command
            if("https" in weblink or "http" in weblink):
                    cml = CMCore(url=weblink,icon=icon_file,electron_version=electron_version,
                      app_name=app_name,upgrade_version_dir=upgrade_version_files,loading_color=loading_background,
                      fullscreen=fullscreen,disable_devtools=disable_dev_tools,disable_right_click=disable_right_click,always_on_top=always_on_top,
                      nativefier_command=nativefier_command
                    )

                    os.startfile(cml.get_full_dir())
            else:
                w = MessageBox("提醒","您未输入前缀，请自行到此程序文件夹下查看",self)
                w.exec()
        else:
            self.PlainTextEdit.setPlainText(text)
    def start(self):
        global weblink
        if(weblink == ""):
            title = "Warning"
            content = "请填写链接后再运行"
            w = MessageBox(title,content,self)
            if(w.exec()):
                return
        elif("https" not in weblink or "http" not in weblink):
            title = "Warning"
            content = "链接未填写完整"
            w = MessageBox(title,content,self)
            if(w.exec()):
                return
        else:
            self.t.start()
            self.PrimaryPushButton.setDisabled(True)
            self.IndeterminateProgressBar.setHidden(False)
    def start_settings(self):
        if(self.settings_on == False):
            ws.show()
            self.PlainTextEdit.setStyleSheet("PlainTextEdit {\n"
            "    color: green;\n"
            "    background-color: black;\n"
            "    border: 1px solid rgba(0, 0, 0, 13);\n"
            "    border-bottom: 1px solid rgba(0, 0, 0, 100);\n"
            "    border-radius: 5px;\n"
            "    /* font: 14px \"Segoe UI\", \"Microsoft YaHei\"; */\n"
            "    padding: 0px 10px;\n"
            "}\n"
            "")
            self.settings_on = True
        else:
            ws.close()
            ws.show()
            self.PlainTextEdit.setStyleSheet("PlainTextEdit {\n"
            "    color: green;\n"
            "    background-color: black;\n"
            "    border: 1px solid rgba(0, 0, 0, 13);\n"
            "    border-bottom: 1px solid rgba(0, 0, 0, 100);\n"
            "    border-radius: 5px;\n"
            "    /* font: 14px \"Segoe UI\", \"Microsoft YaHei\"; */\n"
            "    padding: 0px 10px;\n"
            "}\n"
            "")
            
            
    def LineEdit_6_changed(self):
        global weblink
        weblink = self.LineEdit_6.text()
    def LineEdit_changed(self):
        global electron_version
        electron_version = self.LineEdit.text()
    def LineEdit_3_changed(self):
        global app_name
        app_name = self.LineEdit_3.text()
    def LineEdit_4_changed(self):
        global upgrade_version_files
        upgrade_version_files = self.LineEdit_4.text()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #setTheme(Theme.DARK)
        setThemeColor('#28afe9')
        self.settings_on = False
        doubleValidator = QDoubleValidator(self)
        doubleValidator.setRange(-360,360)
        doubleValidator.setNotation(QDoubleValidator.StandardNotation)
        # 设置精度，小数点2位
        doubleValidator.setDecimals(2)
        self.setTitleBar(SplitTitleBar(self))
        self.titleBar.raise_()
        self.ToolButton.setIcon(FluentIcon.SETTING)
        self.LineEdit.setValidator(doubleValidator)
        self.color_picker_button = ColorPickerButton(QColor("#ffffff"),"加载时背景颜色",self)
        self.horizontalLayout_4.addWidget(self.color_picker_button)
        self.setWindowTitle('Nativefier GUI')
        self.setWindowIcon(QIcon(":/image/image/icon.png"))
        self.resize(1000, 550)
        self.CheckBox.clicked.connect(self.set_always_on_top)
        self.CheckBox_2.clicked.connect(self.set_fullscreen)
        self.CheckBox_3.clicked.connect(self.set_disable_devtools)
        self.CheckBox_4.clicked.connect(self.set_disable_right_click)
        self.color_picker_button.colorChanged.connect(self.save_color)
        self.PushButton_3.clicked.connect(self.showtips)
        self.PushButton.clicked.connect(self.get_icon_files)
        self.LineEdit.textChanged.connect(self.LineEdit_changed)
        self.LineEdit_3.textChanged.connect(self.LineEdit_3_changed)
        self.LineEdit_4.textChanged.connect(self.LineEdit_4_changed)
        self.LineEdit_6.textChanged.connect(self.LineEdit_6_changed)
        self.ToolButton.clicked.connect(self.start_settings)
        self.t = CMThread()
        self.t.sig.connect(self.update_command_view)
        self.PrimaryPushButton.clicked.connect(self.start)
        self.SwitchButton.checkedChanged['bool'].connect(self.switchmode)
        self.windowEffect.setMicaEffect(self.winId())
        self.IndeterminateProgressBar.setHidden(True)
        self.titleBar.titleLabel.setStyleSheet("""
            QLabel{
                background: transparent;
                font: 13px 'Segoe UI';
                padding: 0 4px;
            }
        """)
        self.PlainTextEdit.setStyleSheet("PlainTextEdit {\n"
"    color: green;\n"
"    background-color: black;\n"
"    border: 1px solid rgba(0, 0, 0, 13);\n"
"    border-bottom: 1px solid rgba(0, 0, 0, 100);\n"
"    border-radius: 5px;\n"
"    /* font: 14px \"Segoe UI\", \"Microsoft YaHei\"; */\n"
"    padding: 0px 10px;\n"
"}\n"
"")
        desktop = QApplication.desktop().availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w//2 - self.width()//2, h//2 - self.height()//2)

    def resizeEvent(self, e):
        super().resizeEvent(e)

            


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

    if not(os.path.exists("config.json")):
        with open('config.json', 'w') as f:
            data = {"ELECTRON_MIRROR":"https://npmmirror.com/mirrors/electron/","NPM_MIRROR":"https://registry.npmmirror.com","version":1.0}
            f.write(json.dumps(data))
        from settings import SettingsWindow
    else:
        with open("config.json") as f:
            config_dict = json.loads(f.read())
            ENV["ELECTRON_MIRROR"] = config_dict["ELECTRON_MIRROR"]
            JSON_VERSION = config_dict["version"]
            NPM_MIRROR = config_dict["NPM_MIRROR"]
        from settings import SettingsWindow
    ws = SettingsWindow()
    try:
        w = GM_Window()
        w.show()
    except Exception as err:
        print(f"Error {err}")
    app.exec_()