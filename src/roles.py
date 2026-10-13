import json


class Roles:
    def __init__(
        self,
        path: str,
        mowaa_nation: str,
        mowaa_forum: str,
        europeia_del: str,
        estalcia_del: str,
    ):
        self._path = path
        self._mowaa_nation = mowaa_nation.lower().replace(" ", "_")
        self._mowaa_forum = mowaa_forum
        self._europeia_del = europeia_del.lower().replace(" ", "_")
        self._estalcia_del = estalcia_del.lower().replace(" ", "_")

    @classmethod
    def from_json(cls, path: str):
        with open(path, "r") as f:
            data = json.loads(f.read())

        roles = cls(
            path,
            data.get("mowaa_nation"),
            data.get("mowaa_forum"),
            data.get("europeia_del"),
            data.get("estalcia_del"),
        )

        return roles

    def _to_dict(self) -> dict[str, str]:
        return {
            "mowaa_nation": self._mowaa_nation,
            "mowaa_forum": self._mowaa_forum,
            "europeia_del": self._europeia_del,
            "estalcia_del": self._estalcia_del,
        }

    def save(self):
        with open(self._path, "w") as f:
            f.write(json.dumps(self._to_dict()))

    @property
    def mowaa_nation(self) -> str:
        return self._mowaa_nation

    @mowaa_nation.setter
    def mowaa_nation(self, nation: str):
        self._mowaa_nation = nation.lower().replace(" ", "_")

        self.save()

    @property
    def mowaa_forum(self) -> str:
        return self._mowaa_forum

    @mowaa_forum.setter
    def mowaa_forum(self, username: str):
        self._mowaa_forum = username

        self.save()

    @property
    def europeia_del(self) -> str:
        return self._europeia_del

    @europeia_del.setter
    def europeia_del(self, nation: str):
        self._europeia_del = nation.lower().replace(" ", "_")

        self.save()

    @property
    def estalcia_del(self) -> str:
        return self._estalcia_del

    @estalcia_del.setter
    def estalcia_del(self, nation: str):
        self._estalcia_del = nation.lower().replace(" ", "_")

        self.save()
