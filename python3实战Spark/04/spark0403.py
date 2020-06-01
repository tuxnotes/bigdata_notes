import sys
from pyspark import SparkConf, SparkContext

"""TopN的问题
1) input : 1/n文件  文件夹  后缀名
2) 求某个维度的topn, 假设一行记录里有10个字段，统计其中某个字段的TopN
3）开发步骤分析
    文本内容的每一行根据需求提取出你所需要的字段： map 提取字段
    单词 ==> (单词, 1):  map
    把所有相同单词的计数相加得到最终的结果: reduceByKey
    取最多出现次数的降序： sortByKey

示例文件类似访问日志，其中第六个字段是用户ID，求访问最多的用户，也就是第六个字段的TopN的问题
"""

if __name__ == "__main__":
    if len(sys.argv != 2):
        print("Usage: topn <input>", file=sys.stderr)
        sys.exit(-1)

    conf = SparkConf()
    sc = SparkContext(conf=conf)

    counts = sc.textFile(sys.argv[1]) \
        .map(lambda x: x.split("\t")) \
        .map(lambda x: (x[5], 1)) \
        .reduceByKey(lambda a, b: a + b) \
        .map(lambda x: (x[1], x[0])) \
        .sortByKey(False) \
        .map(lambda x: (x[1], x[0])).take(5)

    for (word, count) in counts:
        print("%s: %i" % (word, count))

    sc.stop()

