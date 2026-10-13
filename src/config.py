from typing import Self


class Config:
    def __init__(
        self,
        token: str,
        dispatch_template_path: str,
        telegram_template_path: str,
        roles_path: str,
    ):
        self._token = token
        self._dispatch_template_path = dispatch_template_path
        self._telegram_template_path = telegram_template_path
        self._roles_path = roles_path

    @property
    def token(self) -> str:
        return self._token

    @property
    def dispatch_template_path(self) -> str:
        return self._dispatch_template_path

    @property
    def telegram_template_path(self) -> str:
        return self._telegram_template_path

    @property
    def roles_path(self) -> str:
        return self._roles_path

    @classmethod
    def from_yaml(cls, path: str | None = None) -> Self:
        import yaml

        if not path:
            path = "./config.yml"

        with open(path, "r") as f:
            data = yaml.safe_load(f)

        config = cls(
            token=data["token"],
            dispatch_template_path=data["dispatch_template_path"],
            telegram_template_path=data["telegram_template_path"],
            roles_path=data["roles_path"],
        )

        return config
