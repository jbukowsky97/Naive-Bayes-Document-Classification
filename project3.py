from os import listdir
from decimal import *
import re

getcontext().prec = 100

words_neg = {}
words_pos = {}
neg_files = listdir("./aclImdb/train/neg")
pos_files = listdir("./aclImdb/train/pos")
vocabulary = {}

pp_neg = Decimal(str(len(neg_files) / (len(neg_files) + len(pos_files))))
pp_pos = Decimal(str(len(pos_files) / (len(neg_files) + len(pos_files))))

print(pp_neg)
print(pp_pos)

for filename in neg_files:
    contents = None
    with open("./aclImdb/train/neg/%s" % filename) as f:
        contents = f.read()
    w_list = re.findall(r"\w+", contents)
    for word in w_list:
        if word.lower() not in words_neg:
            words_neg[word.lower()] = 1
        else:
            words_neg[word.lower()] += 1
        if word.lower() not in vocabulary:
            vocabulary[word.lower()] = 1
        else:
            vocabulary[word.lower()] += 1

for filename in pos_files:
    contents = None
    with open("./aclImdb/train/pos/%s" % filename) as f:
        contents = f.read()
    w_list = re.findall(r"\w+", contents)
    for word in w_list:
        if word.lower() not in words_pos:
            words_pos[word.lower()] = 1
        else:
            words_pos[word.lower()] += 1
        if word.lower() not in vocabulary:
            vocabulary[word.lower()] = 1
        else:
            vocabulary[word.lower()] += 1

cp_neg = {}
cp_pos = {}

for word, count in words_neg.items():
    cp_neg[word] = Decimal(str(count + 1)) / Decimal(str(vocabulary[word] + len(vocabulary)))

for word, count in words_pos.items():
    cp_pos[word] = Decimal(str(count + 1)) / Decimal(str(vocabulary[word] + len(vocabulary)))

neg_files = listdir("./aclImdb/test/neg")
pos_files = listdir("./aclImdb/test/pos")

num_correct = 0
num_total = len(neg_files) + len(pos_files)

for filename in neg_files:
    product_features_neg = Decimal("1")
    product_features_pos = Decimal("1")

    contents = None
    with open("./aclImdb/test/neg/%s" % filename) as f:
        contents = f.read()
    w_list = re.findall(r"\w+", contents)

    for word in w_list:
        if word.lower() in cp_neg:
            product_features_neg *= cp_neg[word.lower()]
        if word.lower() in cp_pos:
            product_features_pos *= cp_pos[word.lower()]
    
    product_features_neg *= pp_neg
    product_features_pos *= pp_pos

    if product_features_neg > product_features_pos:
        num_correct += 1

for filename in pos_files:
    product_features_neg = Decimal("1")
    product_features_pos = Decimal("1")

    contents = None
    with open("./aclImdb/test/pos/%s" % filename) as f:
        contents = f.read()
    w_list = re.findall(r"\w+", contents)

    for word in w_list:
        if word.lower() in cp_neg:
            product_features_neg *= cp_neg[word.lower()]
        if word.lower() in cp_pos:
            product_features_pos *= cp_pos[word.lower()]
    
    product_features_neg *= pp_neg
    product_features_pos *= pp_pos
    

    if product_features_pos > product_features_neg:
        num_correct += 1

print(num_correct)
print("%d%%" % (num_correct / num_total * 100))