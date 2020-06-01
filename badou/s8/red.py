import sys

data_path = '../data/test_reduce.txt'
cur_word = None
sum = 0

for line in sys.stdin:
# with open(data_path, 'r', encoding='utf-8') as f:
    for line in f.readlines():
        word, value = line.strip().split(',')
        if cur_word == None:
            cur_word = word
        if cur_word != word:
            print("%s,%s" % (cur_word, sum))
            cur_word = word
            sum = 0
        sum += 1
    print("%s,%s" % (cur_word, sum))
