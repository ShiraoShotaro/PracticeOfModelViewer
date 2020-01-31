import dataclasses
import os
from PySide2 import QtWidgets
from util.ui_loader._CustomQUiLoader import CustomQUiLoader


@dataclasses.dataclass(frozen=False, eq=False)
class UiContainerBase:
    """ UIをdataclassに展開するための基底クラス

    必ずこのクラスを継承したdataclassを定義し、ウィジット名のメンバを用意すること

    Attributes:
        widgets (QtWidgets):
            すべてのuiが格納されているfield
    """

    widgets: QtWidgets

    @classmethod
    def loader(cls, filepath: str):
        """ UIファイルからUIを読み込みdataclassに展開する

        Parameter:
            filepath (str):
                ファイルパス

        Returns:
            UiContainerBase:
                UIファイルから構築されたUiContainerBaseの継承インスタンス.
        """
        assert os.path.exists(filepath), "Ui not found. {}".format(filepath)
        ui = CustomQUiLoader().load(filepath)
        kargs = {"widgets": ui}
        fields: dict = {f.name: f for f in dataclasses.fields(cls)}

        for k, v in ui.__dict__.items():
            if k in fields:
                if fields[k].type == type(v):
                    kargs[k] = v

        ret = cls(**kargs)
        return ret
