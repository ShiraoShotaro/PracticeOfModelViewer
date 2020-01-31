import dataclasses
import json
import os
from typing import Any

"""
ゆるーい感じのシングルトン（シングルトンとは呼べないが）
"""

class _RegisterBaseInstance:
    _instance = None


@dataclasses.dataclass
class RegisterBase:

    filename: dataclasses.InitVar[str] = "psbatcher.client.json"

    def __post_init__(self, filename):
        assert type(filename) is str
        self.__filepath = filename
        self.__validator = self.validator if hasattr(self, "validator") else None

    def save(self):
        fpath: str = self.getFilepath()
        if not os.path.exists(fpath):
            os.makedirs(os.path.dirname(fpath), exist_ok=True)

        with open(fpath, mode="w", encoding="utf-8") as f:
            json.dump(dataclasses.asdict(self), f)

    def getFilepath(self) -> str:
        app_root: str = os.getenv('APPDATA')
        if not app_root:
            raise RuntimeError("設定ファイルの保存先を取得できませんでした")
        return os.path.abspath(os.path.join(app_root, self.__filepath))

    def load(self):
        fpath: str = self.getFilepath()
        if os.path.exists(fpath):
            with open(fpath, mode="r", encoding="utf-8") as f:
                json_obj: dict = json.load(f)
                for k, v in json_obj.items():
                    if hasattr(self, k):
                        if self.validator is not None:
                            if not self.validator(k, v):
                                continue
                        setattr(self, k, v)

    @classmethod
    def getInstance(cls):
        if _RegisterBaseInstance._instance is None:
            _RegisterBaseInstance._instance = cls()
        return _RegisterBaseInstance._instance
