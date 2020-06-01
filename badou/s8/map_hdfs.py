import re
import sys

p = re.compile(r'\w+')

for line in sys.stdin:
    word_list = line.strip().split(' ')
    for word in word_list:
        if len(p.findall(word)) < 1:
            continue
        word = p.findall(word)[0].lower()
        print("%s,%s" % (word, '1'))
