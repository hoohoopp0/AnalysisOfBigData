import time
from collections import Counter
import math
import csv


def entropy(p, n):
    if (p == 0 and n == 0):
        return 0
    elif (p == 0):
        # print(((-n) / (p + n)) * math.log2(n / (p + n)))
        return (((-n) / (p + n)) * math.log2(n / (p + n)))
    elif (n == 0):
        # print(((-p) / (p + n)) * math.log2(p / (p + n)))
        return (((-p) / (p + n)) * math.log2(p / (p + n)))
    else:
        # print((((-p) / (p + n)) * math.log2(p / (p + n))) + (((-n) / (p + n)) * math.log2(n / (p + n))))
        return ((((-p) / (p + n)) * math.log2(p / (p + n))) + (((-n) / (p + n)) * math.log2(n / (p + n))))


def gain(D, attr, space=0):
    # if result != 0:
    count_p = Counter()
    count_n = Counter()
    attribute = []
    count = []
    for size in range(len(attr)):
        count.append([])
        count[size].append(Counter())
        count[size].append(Counter())
        attribute.append(Counter())
    for i in D:
        if (i[attr[len(attr) - 1]] == 'Yes'):
            count_p.update(['root'])
        else:
            count_n.update(['root'])
        for size in range(len(attr)):
            attribute[size].update([i[attr[size]]])
    # print((attribute[len(attribute)-1]).get(list(attribute[len(attribute)-1])[0],0))
    for i in D:
        for size in range(len(attr)):
            for j in attribute[size]:
                if (i[attr[len(attr) - 1]] == 'Yes'):
                    if (i[attr[size]] == j):
                        count[size][0].update([j])
                else:
                    if (i[attr[size]] == j):
                        count[size][1].update([j])
    Max = 0
    next_attr = 0
    for size in range(len(attr) - 1):
        X = entropy((attribute[len(attribute)-1]).get(list(attribute[len(attribute)-1])[0],0), (attribute[len(attribute)-1]).get(list(attribute[len(attribute)-1])[1],0))  # root
        for i in attribute[size]:
            X -= ((count[size][0].get(i, 0) + count[size][1].get(i, 0)) / len(D)) * entropy(
                count[size][0].get(i, 0), count[size][1].get(i, 0))
            # print(i, count[size][0].get(i, 0), count[size][1].get(i, 0), entropy(count[size][0].get(i, 0),count[size][1].get(i, 0)))
        if (Max < X):
            Max = X
            next_attr = size
    # for C in range(len(list(attribute[next_attr]))):

    for C in list(attribute[next_attr]):
        next_D = []
        count_next = Counter()
        # print('**'+str(attr))
        print('  ' * space, '{}({})'.format(attr[next_attr], C))
        for i in D:
            if (i[attr[next_attr]] == C):
                X = i.copy()
                X.pop(attr[next_attr])
                # i.pop(attr[next_attr])
                count_next.update([i.get(attr[len(attr) - 1])])
                next_D.append(i)
        attr_next = []
        attr_next += attr
        attr_next.remove(attr_next[next_attr])
        # print(next_D)
        if (len(count_next) == 1):
            print('  ' * (space + 1) +'├─('+str(C)+')──', '{}'.format(next_D[0].get(attr[len(attr) - 1])))
        # elif (len(attr_next) > 3):
        elif (abs(Max) != 0):
            gain(next_D, attr_next, space + 1)
        else:
            print('  ' * (space + 1) + '├─('+str(C)+')──', '{}'.format(next_D[0].get(attr[len(attr) - 1])))


def loaddata(file, data):
    with open(file, newline='') as csvFile:
        rows = csv.DictReader(csvFile)
        for row in rows:
            data.append(dict(row))


start = time.time()
#
file = 'test3.csv'
data = []
loaddata(file, data)
print('root')
gain(data, list(data[0].keys()), 1)
#
end = time.time()
print('{} s'.format(end - start))
