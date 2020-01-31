
import argparse
import logging
import sys
import os

# PySide2
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QIcon


# custom style
from pdi.widgets.qstyle import darkstyle

# main window
from ui.main_window import MainWindow

# logger utility
from util.setup_log import setupLogger

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(os.path.join(__file__, "../"))))
    print(os.getcwd())
    print("AAA")

    # アプリケーション作成
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon("icon.png"))

    # オブジェクト作成
    window = MainWindow(sys.argv)

    # MainWindowの表示
    window.show()
    window.resize(1200, 800)

    ret = app.exec_()
    print(ret)
    sys.exit(ret)
