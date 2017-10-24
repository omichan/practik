'''
Created on 19 окт. 2017 г.

@author: local
Данный модуль позволяет конвертировать ui файл QT creator в файл *.py
'''

import os
import tkinter as tk
from tkinter import filedialog
from PyQt5 import uic

# диалоговое окно выбора файла *.ui
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=(("QT Creator files", "*.ui"), ("all files", "*.*")))  # Путь к файлу .ui
newfile_path = file_path.replace(".ui", ".py")                                                          # создаем файл *.py в той же дирректории

# Процесс компиляции
try:  # пробуем скомпилировать наш открытый файл из .ui в .py
    #file_name = str(os.path.split(file_path)[1]).replace(".ui", "")    # используем имя исходного файла
    newFile = open(newfile_path, "w")
    uic.compileUi(file_path, newFile)
except:  # если возникла ошибка
    print("Что-то пошло не так")






