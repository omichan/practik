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


# recursive function for deep search depedencies
def cross_dep(libs: List[Library], index: int, deped_stack: []):
    # input: List of libraries, curent library index, list for all depedencies

    # go by all depedencies
    for item in libs[index].dependencies:
        # check if depedency already added to list
        if item in deped_stack:
            break

        # add current depedency to depedancy stack
        deped_stack.append(item)

        # rearch index of depedency in all libraries list
        deped_index = [d for d in libs if d.name == item][0]

        # add new depedencies to depedancies stack
        deped_stack += cross_dep(libs, libs.index(deped_index), deped_stack)
    # return all depedencies to load function
    return deped_stack


def load(libs: List[Library]):
    """
    Функция, которая выводит в консоль имена библиотек в порядке их загрузки.

    РЕАЛИЗУЙ ЭТУ ФУНКЦИЮ
    """
    # Lenght of libraries list
    libs_count = len(libs)

    # list of loaded libs by func
    libs_loaded = []

    # Test for cross depedencies any libraries 
    for i in range(libs_count):
        
        # List of all chain items
        all_depedences_stack = []

        # recursive func for fulling al
        cross_dep(libs, i, all_depedences_stack)

        #check all libraries chain for cross depedencies
        if libs[i].name in all_depedences_stack:
            print("Обнаружены перекрестные ссылки с библиотекой ", libs[i].name)
            raise NotImplementedError

    # get list of all libs
    libs_stack = [item.name for item in libs]

    # loading process flag
    all_libs_loaded = False

    # for loading control
    last_loaded_count =0

    # libs loading process 
    while(not all_libs_loaded):
        # go by lib index
        for i in range(libs_count):
            # skip loop if current lib loaded already
            if libs[i].name in libs_loaded:
                break

            # check if can load library
            if set(libs[i].dependencies).issubset(libs_loaded) or len(libs[i].dependencies)==0:
                print("Загружена библиотека:", libs[i].name)
                libs_loaded.append(libs[i].name)

            # check if no independed library
            if i >= libs_count-1 and len(libs_loaded)<=0:
                print("В списке нет независимых пакетов")
                raise NotImplementedError
            
            # if all libs are loaded  can end loop   
            if set(libs_stack).issubset(libs_loaded):
                all_libs_loaded = True

        # check if depedencies from unexisting libraries    
        if (len(libs_loaded) <= last_loaded_count):
            print("Нет библиотек для загрузки")        
            raise NotImplementedError
        last_loaded_count = len(libs_loaded)



if __name__ == "__main__":
    # должно пройти успешно ("D" -> "C" -> "B" -> "A")
    load(LIBS_WITHOUT_CYCLES)
    # должно выбросить иссключение о найденых циклических зависимостях
    load(LIBS_WITH_CYCLES)
