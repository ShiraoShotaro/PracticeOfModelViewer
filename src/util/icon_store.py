import glob
import os.path
from typing import Dict
from PySide2.QtGui import QIcon


class IconStore:
    """ アイコンを管理するユーティリティークラス
    """

    __icons: Dict[str, QIcon] = {}

    @classmethod
    def load(cls, icon_directory_path: str):
        """ アイコンのロード

        指定したディレクトリ以下にある, <KEY>NormalOff.pngを検索し, キャッシュします.
        ステータス, モデル違いを<KEY>をもとに検索し, あれば設定を行います.

        Parameters:
            icon_directory_path (str):
                アイコンが格納されているディレクトリのパス
        """
        assert type(icon_directory_path) is str

        ext_path = {
            "NormalOn": (QIcon.Normal, QIcon.On),
            "ActiveOff": (QIcon.Active, QIcon.Off),
            "ActiveOn": (QIcon.Active, QIcon.On),
            "DisabledOff": (QIcon.Disabled, QIcon.Off),
            "DisabledOn": (QIcon.Disabled, QIcon.On),
            "SelectedOff": (QIcon.Selected, QIcon.Off),
            "SelectedOn": (QIcon.Selected, QIcon.On)
        }

        # icons
        off_icon_files = glob.glob(os.path.join(icon_directory_path, "*NormalOff.png"), recursive=False)
        for off_fpath in off_icon_files:
            key = os.path.basename(off_fpath).split(".")[0][:-9]
            cls.__icons[key] = QIcon(off_fpath)

            for k, v in ext_path.items():
                path = os.path.join(icon_directory_path, key + k + ".png")
                if os.path.exists(path):
                    print(path)
                    cls.__icons[key].addFile(path, mode=v[0], state=v[1])

    @classmethod
    def getIcon(cls, key: str) -> QIcon:
        """ 読み込み済みのアイコンを取得

        Parameters:
            key (str):
                アイコンのキー名
        
        Raise:
            KeyError:
                指定したキーのアイコンが登録されていない場合
        
        Returns:
            QtGui.QIcon:
                指定したキーのアイコンインスタンス
        """
        return cls.__icons[key]
