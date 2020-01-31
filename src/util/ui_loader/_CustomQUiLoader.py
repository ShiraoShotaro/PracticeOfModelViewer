from PySide2.QtUiTools import QUiLoader
import ui.custom


class CustomQUiLoader(QUiLoader):
    """ カスタムUIのローダー """

    def createWidget(self, className, parent=None, name=''):
        if className in ui.custom.__all__:
            ret = getattr(ui.custom, className)(parent)
            ret.setObjectName(name)
            return ret
        return super().createWidget(className, parent, name)
