from pyspark.sql import SparkSession, Row
from pyspark import SparkConf,SparkContext

def bsic(spark):
    df = spark.read.json("file:///path/to/spark_home/examples/src/main/resources/people.json")
    df.show()
    df.printSchema()
    df.select("name").show()
    df.select(df['name'],df['age'] + 1).show()
    df.filter(df['age'] > 21).show()
    df.createOrReplaceTempView("people") # 注册临时视图people，全局视图工作中用的少
    sqlDF = spark.sql("select * FROM people")
    sqlDF.show()
    df.filter(df.age > 3).show() # 不同写法

def schema_inference_example(spark):
    sc = spark.sparkContext
    

if __name__ == "__main__":
    spark = SparkSession.builder.appName("spark0801").getOrCreate()


    spark.stop()