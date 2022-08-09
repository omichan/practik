"""
Необходимо реализовать функцию load - условный аналог пакетного менеджера, который "загружает" библиотеки класса Library в порядке их зависимостей.
(Для простоты пусть просто выводит их названия в консоль)

Основное ограничение: Библиотека не может быть загружена, пока не загружены все ее зависимости.

Допустим нужно загрузить следующий набор библиотек:

[
    Library(name="A", dependencies=["B"]),
    Library(name="B", dependencies=["C"]),
    Library(name="C", dependencies=[])
]

Мы не можем загрузить библиотеку A пока не загрузим библиотеку B, а B пока не загрузим  С. поэтому порядок загрузки следующий:

С -> B -> A


Также необходимо учитывать случаи, в которых во входных библиотеках присутствуют циклические зависимости:

[
    Library(name="A", dependencies=["B"]),
    Library(name="B", dependencies=["A"])
]

При таких входных данных библиотека B зависит от А, а А от В, т е загрузка невозможна. Необходимо учесть эти случаи в своей реализации
"""
from typing import List


class Library:

    def __init__(self, name: str, dependencies: List[str]):
        self.name = name
        self.dependencies = dependencies


LIBS_WITHOUT_CYCLES = [
    Library(name="B", dependencies=["C", "D"]),
    Library(name="A", dependencies=["B"]),
    Library(name="C", dependencies=["D"]),
    Library(name="D", dependencies=[])
]


LIBS_WITH_CYCLES = [
    Library(name="A", dependencies=["B"]),
    Library(name="B", dependencies=["C"]),
    Library(name="C", dependencies=["A"])
]


def load(libs: List[Library]):
    """
    Функция, которая выводит в консоль имена библиотек в порядке их загрузки.

    РЕАЛИЗУЙ ЭТУ ФУНКЦИЮ
    """
    raise NotImplementedError



if __name__ == "__main__":
    # должно пройти успешно ("D" -> "C" -> "B" -> "A")
    load(LIBS_WITHOUT_CYCLES)
    # должно выбросить иссключение о найденых циклических зависимостях
    load(LIBS_WITH_CYCLES)
