import datetime
import logging
import os

# typing
from typing import Optional

# pyside2
from PySide2.QtWidgets import QMainWindow


# icon util
from util.icon_store import IconStore

# main window ui
from ui.main_window_ui import MainWindowUi

# SAMPLE: サンプル用
from PySide2.QtWidgets import QWidget
from PySide2 import QtCore

from PySide2.Qt3DExtras import Qt3DExtras
from PySide2.Qt3DInput import Qt3DInput
from PySide2.Qt3DCore import Qt3DCore
from PySide2.Qt3DRender import Qt3DRender
from PySide2 import QtGui


class MainWindow(QMainWindow):
    def __init__(self, args, parent=None):
        super().__init__(parent)
        ##############################################################################
        # UI初期化処理
        self.ui = MainWindowUi.loader(os.path.join(os.getcwd(), 'ui/main.ui'))
        self.setWindowTitle('self.viewer test')
        self.setCentralWidget(self.ui.widgets)

        self.view = Qt3DExtras.Qt3DWindow()
        self.view.defaultFrameGraph().setClearColor(QtGui.QColor(0, 0, 0))
        self.container = QWidget.createWindowContainer(self.view)

        screen_size = self.view.screen().size()
        self.ui.viewer.addWidget(self.container)
        self.container.setMinimumSize(QtCore.QSize(400, 600))
        self.container.setMaximumSize(screen_size)

        # QSize screenSize = self.view -> screen() -> size();
        # container -> setMinimumSize(QSize(200, 100));
        # container -> setMaximumSize(screenSize);

        # vLayout -> setAlignment(Qt: : AlignTop);
        # hLayout -> addWidget(container, 1);
        # hLayout -> addLayout(vLayout);

        # input_aspect = Qt3DInput.QInputAspect()
        # self.view.registerAspect(input_aspect)

        # root entity
        self.root_entity: Qt3DCore.QEntity = Qt3DCore.QEntity()

        # draw grid and axis
        """
        self.x_axis: Qt3DRender.QGeometry = Qt3DRender.QGeometry(self.root_entity)
        x_axis_pos: QtCore.QByteArray = QtCore.QByteArray()
        x_axis_pos.append(0)
        x_axis_pos.append(0)
        x_axis_pos.append(0)
        x_axis_pos.append(10)
        x_axis_pos.append(0)
        x_axis_pos.append(0)
        x_axis_buf: Qt3DRender.QBuffer = Qt3DRender.QBuffer(self.x_axis)
        x_axis_buf.setData(x_axis_pos)

        x_axis_attr: Qt3DRender.QAttribute = Qt3DRender.QAttribute(self.x_axis)
        x_axis_attr.setVertexBaseType(Qt3DRender.QAttribute.Float)
        x_axis_attr.setVertexSize(3)
        x_axis_attr.setAttributeType(Qt3DRender.QAttribute.VertexAttribute)
        x_axis_attr.setBuffer(x_axis_buf)
        x_axis_attr.setByteStride(3)
        x_axis_attr.setCount(2)
        self.x_axis.addAttribute(x_axis_attr)
        """

        test_mtl = Qt3DExtras.QTextureMaterial(self.root_entity)

        self.test = Qt3DCore.QEntity(self.root_entity)
        self.test_mesh: Qt3DExtras.QTorusMesh = Qt3DExtras.QTorusMesh()
        self.test_mesh.setRadius(5)
        self.test_mesh.setMinorRadius(1)
        self.test_mesh.setRings(100)
        self.test_mesh.setSlices(20)
        self.test_tr = Qt3DCore.QTransform()
        self.test_tr.setTranslation(QtGui.QVector3D(0, 0, 0))
        # test_tr.setScale3D()
        self.test.addComponent(self.test_mesh)
        self.test.addComponent(self.test_tr)
        self.test.addComponent(self.test_mtl)

        # camera entity
        camera_entity: Qt3DRender.QCamera = self.view.camera()

        camera_entity.lens().setPerspectiveProjection(45.0, 16.0 / 9.0, 0.1, 1000.0)
        camera_entity.setPosition(QtGui.QVector3D(0, 0, 20.0))
        camera_entity.setUpVector(QtGui.QVector3D(0, 1, 0))
        camera_entity.setViewCenter(QtGui.QVector3D(0, 0, 0))

        light_entity = Qt3DCore.QEntity(self.root_entity)
        light = Qt3DRender.QPointLight(light_entity)
        light.setColor("white")
        light.setIntensity(1)
        light_entity.addComponent(light)

        light_transform = Qt3DCore.QTransform(light_entity)
        light_transform.setTranslation(camera_entity.position())
        light_entity.addComponent(light_transform)

        # for camera controls
        cam_controller = Qt3DExtras.QFirstPersonCameraController(self.root_entity)
        cam_controller.setCamera(camera_entity)

        # set root object of the scene
        self.view.setRootEntity(self.root_entity)

    def printLog(self, message: str, **kwargs):
        """ ログを出力します

        ログは、ウィンドウ左下に出力
        加えて、「設定」->「ログ表示」にチェックを入れるとログ画面が出てくる

        Parameters:
            message(str):
                ログメッセージ
            kwargs:
                引数を全部ダンプするだけ
        """
        dtnow = datetime.datetime.now()
        message_log = "{0:%Y/%m/%d %H:%M:%S} {1}".format(dtnow, message)
        self.ui.pteLog.appendPlainText(message_log)
        self.ui.widgets.statusBar().showMessage(message)
        self.logger.debug(message)
        if kwargs:
            for k, v in kwargs.items():
                self.ui.pteLog.appendPlainText(" --- {0}={1}".format(k, v))
