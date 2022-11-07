from random import randint
from itertools import permutations
from typing import List
from math import sqrt
import time

operand = ['+', '-', '*', '/']
startTime = time.time()


def get_all_possible_val(p_numlist: List) -> List:
    all_possiblepos_val = set()
    for nums in p_numlist:
        a, b, c, d = nums
        L1 = pos_val((a, str(a)), (b, str(b)))
        L2 = pos_val((c, str(c)), (d, str(d)))
        for x1, str_x1 in L1:
            for x2, str_x2 in L2:
                all_possiblepos_val.update(pos_val((x1, str_x1), (x2, str_x2)))

    print("all possible way: " + str(len(all_possiblepos_val)) + " ways")
    return list(all_possiblepos_val)


def pos_val(num1: tuple(), num2: tuple()) -> tuple():
    pos_value = []

    num1, str1 = num1
    num2, str2 = num2
    pos_value += pos_val_basic((num1, str1), (num2, str2))
    pos_value += pos_val_basic((-num1, f'-{str1}'), (num2, str2))

    temp1 = sqrt(abs(num1))
    temp2 = sqrt(abs(num2))

    pos_value += pos_val_basic((temp1,
                                f'root|{str1}|'), ((temp2, f'root|{str2}|')))
    pos_value += pos_val_basic((-temp1,
                                f'-root|{str1}|'), ((temp2, f'root|{str2}|')))

    pos_value += pos_val_basic((temp1,
                                f'root|{str1}|'), ((num2, str2)))
    pos_value += pos_val_basic((-temp1,
                                f'-root|{str1}|'), ((num2, str2)))

    pos_value += pos_val_basic((num1, str1),
                               ((temp2, f'root|{str2}|')))
    pos_value += pos_val_basic((-num1,
                                f'-{str1}'), (temp2, f'root|{str2}|'))

    dic = dict()
    for val, string in pos_value:
        if val not in dic:
            dic[val] = string
        elif len(string) < len(dic[val]):
            dic[val] = string

    pos_value = list(dic.items())
    return pos_value


def pos_val_basic(num1: tuple(), num2: tuple()) -> tuple():
    pos_value = []
    num1, str1 = num1
    num2, str2 = num2
    for oper in operand:
        if oper == '/' and num2 == 0:
            continue
        # value = eval(f'{num1}{oper}{num2}')
        if oper == '+':
            value = num1 + num2
        if oper == '-':
            value = num1 - num2
        if oper == '*':
            value = num1 * num2
        if oper == '/':
            value = num1 / num2

        pos_value.append((value, f'({str1}{oper}{str2})'))
    return pos_value


def main():
    numlist = [randint(0, 9) for _ in range(4)]
    while(numlist.count(0) >= 2):
        numlist = [randint(0, 9) for _ in range(4)]
    result = randint(0, 2400)//100

    p_numlist = list(permutations(numlist))

    prototype = f'{numlist[0]} {numlist[1]} {numlist[2]} {numlist[3]} = {result}'
    print(prototype)

    all_possible = get_all_possible_val(p_numlist)
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
        best_way[i][1] = best_way[i][1].replace('root', '√')
        val, equ = best_way[i]
        parenthesis = []
        remove = True
        for j in range(len(equ)):
            if len(parenthesis) != 0:
                if parenthesis[0] != 0:
                    remove = False
                    break
            if equ[j] == '(':
                parenthesis.append(j)
            elif equ[j] == ')':
                parenthesis.pop(-1)
        if remove:
            best_way[i][1] = equ[1:-1]

    for way in best_way[:5]:
        print(way)
    print(f'cost time: {time.time()-startTime}')


if __name__ == "__main__":
    main()
