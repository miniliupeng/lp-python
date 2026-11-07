"""数据描述符、__init_subclass__ 与最小元类。"""

from __future__ import annotations


class Field:
    def __set_name__(self, owner: type, name: str) -> None:
        self.private = "_" + name

    def __get__(self, obj: object, objtype: type | None = None):
        if obj is None:
            return self
        return obj.__dict__[self.private]

    def __set__(self, obj: object, value: object) -> None:
        obj.__dict__[self.private] = value


class User:
    name = Field()

    def __init__(self, name: str) -> None:
        self.name = name


class Plugin:
    registry: list[type] = []

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        Plugin.registry.append(cls)


class JsonPlugin(Plugin):
    pass


class RequireLabel(type):
    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict):
        if bases and "label" not in namespace:
            raise TypeError("子类必须定义 label")
        return super().__new__(mcs, name, bases, namespace)


class Labeled(metaclass=RequireLabel):
    pass


class OkLabeled(Labeled):
    label = "ok"


def main() -> None:
    user = User("Ada")
    assert user.name == "Ada"
    assert user.__dict__["_name"] == "Ada"
    assert JsonPlugin in Plugin.registry
    assert Plugin not in Plugin.registry
    assert OkLabeled.label == "ok"
    try:

        class Missing(Labeled):
            pass

    except TypeError:
        pass
    else:
        raise AssertionError("缺少 label 的子类应被元类拒绝")
    print("ok c08")


if __name__ == "__main__":
    main()
