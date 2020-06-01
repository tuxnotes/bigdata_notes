import sys
from pyspark import SparkConf, SparkContext

"""平均数
数据样本如下：
1   13
2   16
3   96
4   44
5   67
6   4
7   98
8   1
9   28
10  56
11  87
.   .
.   .
第一列是id，第二列是年龄。要求统计平均年龄
开发步骤分析：
1) 取出年龄 map
2) 计算年龄总和 reduce
3) 计算记录总数 count
4) 求平均数
"""

if __name__ == "__main__":
    if len(sys.argv != 2):
        print("Usage: avg <input>", file=sys.stderr)
        sys.exit(-1)

    conf = SparkConf()
    sc = SparkContext(conf=conf)

    ageData = sc.textFile(sys.argv[1]).map(lambda x: x.split(" ")[1])
    totalAge = ageData.map(lambda age: int(age)).reduce(lambda a, b: a + b)
    counts = ageData.count()
    avgAge = totalAge / counts

    print(counts)
    print(totalAge)
    sc.stop()
