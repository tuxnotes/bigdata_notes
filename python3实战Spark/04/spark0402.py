import sys
from pyspark import SparkConf, SparkContext

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: wordcount <input> <output>", file=sys.stderr)
        sys.exit(-1)

    conf = SparkConf()
    sc = SparkContext(conf=conf)

    def printResult():
        counts = sc.textFile(sys.argv[1]) \
            .flatMap(lambda line: line.split("\t")) \
            .map(lambda x: (x, 1)).reduceByKey(lambda a, b: a + b)
        output = counts.collect()

        for (word, count) in output:
            print("%s: %i" % (word, count))

    def saveFile():
        sc.textFile(sys.argv[1]).flatMap(lambda line: line.split("\t")).map(
            lambda x: (x, 1)).reduceByKey(lambda a, b: a + b).saveAsTextFile(
                sys.argv[2])

    saveFile()
    sc.stop()

# 脚本使用方法
# cd $SPARK_HOME/bin
# ./spark-submit --master local[2] \
# --name spark0402 /home/hadoop/script/spark0402.py \
# file:///home/hadoop/data/hello.txt file:///home/hadoop/tmp/wc


# file:///home/hadoop/data/hello.txt读取的可以是单个文件，也可以是
# 一个目录，如file:///home/hadoop/data/wc/
# 还支持通配符格式如：file:///home/hadoop/data/wc/*.txt,这样就
# 只读取目录下以.txt结尾的文件，注意脚本运行后输出的日志，其中
# InputFileFormat会提示处理的文件个数
