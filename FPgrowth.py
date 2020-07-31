import time
from collections import Counter


def frequenitem(file, min_sopport):
    headertable=dict()
    c = Counter()
    with open(file, 'r') as f:
        for data in f.readlines():
            row = data.replace('\n', '').split(', ')
            itemsets = []
            for item in row:
                itemsets.append((item))
            c.update(itemsets)
    L1 = []
    i=0
    for item in dict(c.most_common(len(c))):
        if (c[item] >= min_sopport):
            L1.append(item)
            headertable[item]=[]
            i+=1
    return L1,headertable

class treeNode:
    def __init__(self, key, count, parentNode):
        self.key = key
        self.count = count
        self.linknode=id(self)
        self.parent = parentNode
        self.children = {}

    def inc(self, count):
        self.count += count

    def search_parent(self,carch,count):
        carch[self.key]=count
        if id(self.parent)!=id(tree):
            self.parent.search_parent(carch,count)

    def search(self,carch,link):
        if(self.linknode == link):
            self.search_parent(carch,self.count)
        for child in self.children.values():
            child.search(carch,link)

    def printf(self, space=1):
        if(self.key=='{}'):
            print('  ' * space, self.key)
        else:
            print('  ' * space,'{}[{}]'.format(self.key, self.count))
        for child in self.children.values():
            child.printf(space + 1)

def updateTree(tree, X,headertable):
    if X[0] in tree.children:
        tree.children[X[0]].inc(1)
    else:
        tree.children[X[0]] = treeNode(X[0], 1, tree)
        headertable[X[0]].append(id(tree.children[X[0]]))
    if(len(X)>1):
        updateTree(tree.children[X[0]],X[1::],headertable)

def frequent_patterns_2(ck,output,X,result,search_node):
    global sum_count
    comb=X+','+result[len(result)-1]
    comb=sorted(map(int,str(comb).split(',')))
    A = []
    A.append(str(comb).replace('[', '(').replace(']', ')'))
    sum_count.update(A)
    # output[search_node][comb]=ck[result[len(result)-1]]
    if (len(result) > 1):
        frequent_patterns_2(ck,output,X, result[0:len(result) - 1],search_node)

def frequent_patterns_1(ck,output,X,result,search_node):
    frequent_patterns_2(ck,output,X,result,search_node)
    if(len(result)>1):
        X+=','+result[len(result)-1]
        frequent_patterns_1(ck,output,X,result[0:len(result)-1],search_node)

def freq_itemsets(output,search_node,headertable):
    ck = Counter()
    for i in range(0, len(headertable[search_node])):
        carch = dict()
        tree.search(carch,headertable[search_node][i])
        ck.update(carch)
    result = []
    for item in dict(ck.most_common(len(ck))):
        if (ck[item] >= min_sopport):
            result.append(item)
        else:
            del ck[item]
    output[search_node] = {}
    output[search_node][search_node] = ck[search_node]
    del result[result.index(search_node)]
    for i in range(0, len(result) - 1):
        frequent_patterns_1(ck,output, search_node, result[0:len(result) - i],search_node)

def fp_growth(tree,file,headertable):
    with open(file, 'r') as f:
        for data in f.readlines():
            row = data.replace('\n', '').split(', ')
            itemsets=[]
            for i in freq_item:
                if i in row:
                    itemsets.append(i)
            updateTree(tree,itemsets,headertable)
# def testt2(output,X,result):
#     comb=X+','+result[len(result)-1]
#     output['m'][comb]=ck_test[result[len(result)-1]]
#     if (len(result) > 1):
#         testt2(output,X, result[0:len(result) - 1])
# def testt(output,X,result):
#     print(X)
#     testt2(output,X,result)
#     if(len(result)>1):
#         X+=','+result[len(result)-1]
#         testt(output,X,result[0:len(result)-1])


file = "T15I7N0.5KD1K.txt"
min_sopport = 5
sum_count=Counter()
result_output=[]
# search_node='221'   #132,221,238
output=dict()
start = time.time()
#
tree = treeNode('{}', 0, None)
freq_item,headertable = frequenitem(file, min_sopport)
fp_growth(tree,file,headertable)
for i in freq_item:
    freq_itemsets(output,i,headertable)

for item in dict(sum_count):
    if (sum_count[item] >= min_sopport):
        result_output.append(item)
print(len(result_output))
# print(result_output)
# print(output)
## test
# ck_test=Counter('mmmfffcccaaa')
# result_test=['m','f','c','a']
# output_test=dict()
# output_test['m']={}
# output_test['m']['m']=ck_test['m']
# del result_test[result_test.index('m')]
# for i in range(0,len(result_test)-1):
#     testt(output_test,'m',result_test[0:len(result_test)-i])
# print(output_test)
#
end = time.time()
print('{} s'.format(end - start))