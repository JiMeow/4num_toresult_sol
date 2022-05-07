from random import randint
from pprint import pp
from itertools import permutations
from typing import List
from math import sqrt


def get_all_possiblepos_val(p_numlist: List) -> List:
    all_possiblepos_val = set()
    for nums in p_numlist:
        a, b, c, d = nums

        L1 = pos_val((a, str(a)), (b, str(b)))
        for x1, str_x1 in L1:
            L2 = pos_val((x1, str_x1), (c, str(c)))
            for x2, str_x2 in L2:
                all_possiblepos_val.update(pos_val((x2, str_x2), (d, str(d))))

        L3 = pos_val((a, str(a)), (b, str(b)))
        L4 = pos_val((c, str(c)), (d, str(d)))
        for x3, str_x3 in L3:
            for x4, str_x4 in L4:
                all_possiblepos_val.update(pos_val((x3, str_x3), (x4, str_x4)))
    # print(len(all_possiblepos_val))
    return list(all_possiblepos_val)


def pos_val(num1: tuple(), num2: tuple()) -> tuple():

    pos_value = []

    num1, str1 = num1
    num2, str2 = num2
    pos_value += pos_val_notpermu((num1, str1), (num2, str2))
    pos_value += pos_val_notpermu((-num1, f'-{str1}'), (num2, str2))
    pos_value += pos_val_notpermu((num1, str1), (-num2, f'-{str2}'))
    pos_value += pos_val_notpermu((-num1, f'-{str1}'), (-num2, f'-{str2}'))

    pos_value += pos_val_notpermu((sqrt(abs(num1)),
                                  f'root|{str1}|'), ((sqrt(abs(num2)), f'root|{str2}|')))

    pos_value += pos_val_notpermu((sqrt(abs(num1)),
                                  f'root|{str1}|'), ((num2, str2)))
    pos_value += pos_val_notpermu((sqrt(abs(num1)),
                                  f'root|{str1}|'), ((-num2, f'-{str2}')))
    pos_value += pos_val_notpermu((num1, str1),
                                  ((sqrt(abs(num2)), f'root|{str2}|')))
    pos_value += pos_val_notpermu((-num1,
                                  f'-{str1}'), (sqrt(abs(num2)), f'root|{str2}|'))

    dic = dict()
    for val, string in pos_value:
        dic[val] = string
    for val, string in dic.items():
        pos_value.append((val, string))

    return pos_value


def pos_val_notpermu(num1: tuple(), num2: tuple()) -> tuple():
    pos_value = []
    num1, str1 = num1
    num2, str2 = num2
    for oper in range(len(operand)):
        try:
            value = eval(f'{num1}{operand[oper]}{num2}')
            pos_value.append((value, f'({str1}{operand[oper]}{str2})'))
        except:
            pass
    return pos_value


numlist = [randint(0, 9) for _ in range(4)]
while(numlist.count(0) >= 2):
    numlist = [randint(0, 9) for _ in range(4)]

p_numlist = list(permutations(numlist))

result = randint(0, 2400)/100

operand = ['+', '-', '*', '/']
prototype = f'{numlist[0]} {numlist[1]} {numlist[2]} {numlist[3]} = {result}'
print(prototype)

all_possible = get_all_possiblepos_val(p_numlist)
best_way = [list(x) for x in sorted(
    all_possible, key=lambda x: abs(x[0]-result))[0:100]]

for i in range(len(best_way)):
    best_way[i][1] = best_way[i][1].replace('-+', '-')
    best_way[i][1] = best_way[i][1].replace('--', '+')
    best_way[i][1] = best_way[i][1].replace('+-', '-')
    best_way[i][1] = best_way[i][1].replace('|(', '|')
    best_way[i][1] = best_way[i][1].replace(')|', '|')

best_way.sort(key=lambda x: (abs(
    x[0]-result),  len(x[1]), x[1].count('('), x[1].count('root'), x[1].count('-')))

for i in range(len(best_way[:10])):
    val, equ = best_way[i]
    z = []
    p = 0
    for j in range(len(equ)):
        if len(z) != 0:
            if z[0] != 0:
                p = 1
                break
        if equ[j] == '(':
            z.append(j)
        elif equ[j] == ')':
            z.pop(-1)

    if p == 0:
        best_way[i][1] = equ[1:-1]

print(best_way[0])