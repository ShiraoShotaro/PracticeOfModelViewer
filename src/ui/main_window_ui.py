import dataclasses

from PySide2.QtWidgets import (QMainWindow, QFileDialog, QMessageBox, QTabWidget, QLineEdit, QLabel,
                               QSpinBox, QCheckBox, QComboBox, QScrollArea, QPushButton, QSizePolicy,
                               QTextEdit, QLayoutItem, QWidgetItem, QTreeWidget, QToolButton, QFileDialog,
                               QTableWidgetItem, QAction, QWidget, QMenu, QPlainTextEdit, QTableWidget,
                               QGroupBox, QSlider, QHBoxLayout)

from PySide2.QtGui import QIcon, QFont
from PySide2 import QtCore
from util.ui_loader import UiContainerBase
from util.icon_store import IconStore


@dataclasses.dataclass
class MainWindowUi(UiContainerBase):

    viewer: QHBoxLayout

    def __post_init__(self):

        pass
