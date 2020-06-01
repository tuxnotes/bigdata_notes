import re

p = re.compile(r'\w+')  # 去掉紧挨着单词的如“(双引号)等其他特殊字符
data_path = './data/test.txt'
with open(data_path, 'r', encoding='utf-8') as f:  # Hadoop上要使用Hadoop streaming的方式，而不是open本地文件
    for line in f.readlines():
        word_list = line.strip().split(' ')
        for word in word_list:
            re_word = p.findall(word)
            if len(re_word) < 1:
                continue
            word = p.findall(word)[0].lower()  # 统一成小写，统计更加准确
            print("%s,%s"%(word, '1'))
