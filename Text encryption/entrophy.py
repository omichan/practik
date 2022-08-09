from math import log
import collections
import re

# Открытие файла с текстом
file1_source = open("1normal_text.txt", mode="r", encoding='utf-8')
s=file1_source.read()

# Фильтрация лишних символов в тексте
s_flt = re.sub(r'[?|$|.|!|\"|\-|\:|\n|\,]',r'',s)

# Подсчет вероятности, энтропии
c = collections.Counter(s_flt.lower())
D = collections.Counter(dict(c))  
P = {}  # Словарь символ : вероятность
H = {}  # Словарь символ : энтропия

total = sum(c.values())
for item in D:
    pi = D.get(item)/total
    P[item] = round(pi,5)
    Hentr = round(-pi*log(pi,2),3)
    H[item] = Hentr
    #print()
total_H = sum(H.values())   # Полная энтропия
P_list = list(P.values())   # Список вероятностей
Dp = 1 - (total_H/log(32,2))    # Избыточность
print("Количество символов: ",D)
print("Распределение: ",P)
print("Энтропия: ",H)
print(P_list)

# Кодирование по методу Хаффмана
def haf_code(d1,d2):
    if len(d1) > 1:
        dict_items = sorted(d1, key=d1.get,reverse=True)
        new_symbol = {f'{dict_items[-2]}{dict_items[-1]}':d1[dict_items[-2]]+d1[dict_items[-1]]}
        for letter in list(dict_items[-2]):
            d2[letter] = '1' + (d2[letter] if (d2[letter]) else '')
        for letter in list(dict_items[-1]):
            d2[letter] = '0' + (d2[letter] if (d2[letter]) else '')
        del d1[dict_items[-2]]
        del d1[dict_items[-1]]
        d1.update(new_symbol)
        if len(d1) > 1:
            haf_code(d1,d2)
    return d2

# Кодирование по методу Шеннона-Фано
def Shen_code(d3,d4):
    if len(d3)>2:
        p_sum = sum(d3.values())
        dict_items = sorted(d3, key=d3.get,reverse=True)
        d3_1_p_sum = 0
        for count, item in enumerate(dict_items):
            d3_1_p_sum += d3[item]
            if (d3_1_p_sum >= p_sum/2):
                for sub_item in dict_items[:count+1]:
                    d4[sub_item] = (d4[sub_item] if (d4[sub_item]) else '') + '1'
                for sub_item in dict_items[count+1:]:
                    d4[sub_item] = (d4[sub_item] if (d4[sub_item]) else '') + '0'     
                if (len(dict_items[:count+1]) > 1):
                    sub_dict1 = {key:d3[key] for key in dict_items[:count+1]}
                    Shen_code(sub_dict1,d4) 
                else:
                    pass
                if (len(dict_items[count+1:]) > 1):
                    sub_dict2 = {key:d3[key] for key in dict_items[count+1:]}
                    Shen_code(sub_dict2,d4)                      
                else:
                    pass
                break
    if len(d3)==2:
        dict_items = sorted(d3, key=d3.get,reverse=True)
        d4[dict_items[0]] = (d4[dict_items[0]] if (d4[dict_items[0]]) else '') + '1'
        d4[dict_items[1]] = (d4[dict_items[1]] if (d4[dict_items[1]]) else '') + '0' 
    if len(d3)==1:
        dict_items = sorted(d3, key=d3.get,reverse=True)
        d4[dict_items[0]] = (d4[dict_items[0]] if (d4[dict_items[0]]) else '') + '1'
    return d4

print("Кодировка по метоу Хаффмана")
P_half = P.copy()
P_source = dict.fromkeys(P.keys())
half_dict = haf_code(P_half, P_source)
for item in half_dict.items():
    print(item)

print("Кодировка по метоу Шеннона-Фано")
P_shen = dict.fromkeys(P.keys())
P_shen_tmp = P.copy()
Shenon_dict = Shen_code(P_shen_tmp, P_shen)
for item in Shenon_dict.items():
    print(item)


print('\n',"Для метода Хаффмана:")
# Средняя длина кода
lsr = 0
for symbol in P.keys():
    lsr += P[symbol]*len(half_dict[symbol])
print("Средняя длина= ",round(lsr,3))

# Коэффициент сжатия
Kss = round(log(32,2)/lsr,3)
print("Коэффициент статистического сжатия= ",Kss)

# Коэффициент относительной эффективности
H = 4.374
Koe = round(H/lsr,3)
print("Коэффициент относительной эффективности= ",Koe,"\n")

print("Для метода Шеннона-Фано")
# Средняя длина кода
lsr = 0
for symbol in P.keys():
    lsr += P[symbol]*len(Shenon_dict[symbol])
print("Средняя длина= ",round(lsr,3))

# Коэффициент сжатия
Kss = round(log(32,2)/lsr,3)
print("Коэффициент статистического сжатия= ",Kss)

# Коэффициент относительной эффективности
H = 4.374
Koe = round(H/lsr,3)
print("Коэффициент относительной эффективности= ",Koe)

# Кодирование текста
file_text = open("1text_for_cod.txt", mode="r", encoding='utf-8')






text_str = file_text.read()

text_flt = re.sub(r'[?|$|.|!|\"|\-|\:|\n|\,]',r'',text_str.lower())
# кодирование методом Хаффмана
bin_haf = []
for symbol in text_flt:
    bin_haf.append(half_dict[symbol])
    bin_haf.append('\n')

file2_bin_haf = open("2file2_bin_haf.txt", mode="w", encoding='utf-8')
file2_bin_haf.writelines(bin_haf)
file2_bin_haf.close()

#декодирование методом Хаффмана
text_haf = []
for line in bin_haf:
    for k, v in half_dict.items():
        if v == line:
            text_haf.append(k)
            break
file2_txt_haf = open("2file2_txt_haf.txt", mode="w", encoding='utf-8')
file2_txt_haf.writelines(text_haf)
file2_txt_haf.close()

# кодирование методом Шеннона-Фано
bin_shen = []
for symbol in text_flt:
    bin_shen.append(Shenon_dict[symbol])
    bin_shen.append('\n')

file3_bin_shen = open("3file3_bin_shen.txt", mode="w", encoding='utf-8')
file3_bin_shen.writelines(bin_shen)
file3_bin_shen.close()

#декодирование методом Шеннона-Фано
text_shen = []
for line in bin_shen:
    for k, v in Shenon_dict.items():
        if v == line:
            text_shen.append(k)
            break
file3_txt_shen = open("3file3_txt_shen.txt", mode="w", encoding='utf-8')
file3_txt_shen.writelines(text_shen)
file3_txt_shen.close()


