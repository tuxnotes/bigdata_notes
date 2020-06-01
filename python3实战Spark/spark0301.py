from pyspark import SparkConf,SparkContext

# 创建SparkConf: 设置的是Spark相关的参数信息
# 实际环境中master和appname配置不要hard code，应该在使用spark-submit
# 提交的时候指定
# conf = SparkConf().setMaster("local[2]").setAppName("spark0301")
conf = SparkConf()

# 穿件SparkContext
sc = SparkContext(conf=conf)


# 业务逻辑
data = [1,2,3,4,5]
distData = sc.parallelize(data)
print(distData.collect())

# 好的习惯,stop之后释放资源
sc.stop()
