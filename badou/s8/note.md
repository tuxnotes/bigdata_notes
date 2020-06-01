# MapReduce

重点是mapreduce计算框架的执行流程
partition的个数由reduce的个数决定，一般与reduce个数相同，也可是reduce的整数倍。但不能是其他，目的是为了保证落入每个reduce的key是全局的，不会在其他的reduce中出现。

Hadoop中的map，reduce都是进程
spark中的map，reduce都是线程【可以把数据放到共同进程的内存中】

HDFS的副本优势：
吞吐量很大：很多用户请求同一份数据：网络，i/o.如果有三分，三台机器同时可以对外提供服务
如果一个文件的大小超过128M了怎么划分？
这里的mapreduce开始使用Python，借助Hadoop streaming，目的是为了演示mapreduce原理。目前工作了都不再使用Java编写mapreduce任务了。都是使用Hive或spark。工作中用到了storm的，一定会有spark。

map阶段：
**map不仅仅是生成我们期望的(word, 1)这中格式，map更多的是进行数据的清洗，对key做处理**.比如统计单词，更多的是对单词的清洗，正则用的比较多。

shuffle阶段：
map阶段完成后，进行shuffle。
```
cat test.txt | python map.py | sort -k1
```
sort -k1将相同的单词排在一起，Shuffle阶段就是要做这个类似sort的工作

reduce阶段：统计

对于Python环境，可直接使用anaconda，如果是Windows，需要使用GPU的情况下，则要安装anaconda3
测试小说上传到HDFS上

```bash
# hadoop fs -put The_Man_of_Property.txt /data
```
`run.sh`脚本解释
```bash
# cat run.sh

HADOOP_CMD="/usr/local/src/hadoop-2.6.5/bin/hadoop"
STREAM_JAR_PATH="/usr/local/src/hadoop-2.6.5/share/hadoop/tools/lib/hadoop-streaming-2.6.5.jar"

INPUT_FILE_PATH_1="/data/The_Man_of_Property.txt"
#INPUT_FILE_PATH_1="/1.data"
OUTPUT_PATH="/output/wc"

$HADOOP_CMD fs -rmr -skipTrash $OUTPUT_PATH

# Step 1.
$HADOOP_CMD jar $STREAM_JAR_PATH \
    -input $INPUT_FILE_PATH_1 \
    -output $OUTPUT_PATH \
    -mapper "python map_new.py" \
    -reducer "python red_new.py" \
    -file ./map_new.py \
    -file ./red_new.py
```

- HADOOP_CMD hadoop命令的路径
- STREAM_JAR_PATH Hadoop streaming jar包的位置
- INPUT_FILE_PATH_1 要统计单词的文件
- OUTPUT_PATH 统计结果的输出目录 
- skipTrash 跳过回收站
- rmr 如果输出结果已经存在会报错，所以要删除，第一次执行不需要删除，因为还没有结果文件。如果没有，还要删的话，也会报错
- file 由于map和reduce两个Python脚本在HDFS上是不存在的，需要上传。需要分发到对应执行的每个节点上。我们有对应的master和slave，也就是执行的从节点上都需要有这两个脚本。

map结束之后是shuffle的过程
shuffle过程：性能优化大有可为的地方。
包括：partition ， sort， spill， merge， Combiner， copy，MEMORY， disk...
整个map和reduce中间的过程属于shuffle过程。shuffle过程是比较耗性能的，涉及到io，内存，网络传输。调优也是在shuffle过程。

- Partitioner:决定数据有哪个Reduce处理，从而分区。比如采用hash算法，有n个Reducer，那么数据{"are": 1}的key "are"对n进行取模。返回m，而生成{partition, key, value}
- Combiner:数据合并的时候，相同的key的数据，value值合并，减少输出传输量。**Combiner函数事实上是reducer函数，满足Combiner处理不影响{sum, max等}最终的reduce的结果时，可极大提升性能**。Combiner出现在spill和merge过程。需要手动指定。
- Spill：内存缓冲区达到阈值时，溢写spill线程锁住这80M的缓冲区，开始将数据写出到本地磁盘中，然后释放内存。每次溢写都生成一个数据文件。溢出的数据到磁盘前会**对数据进行key排序sort**以及合并Combiner。泛型相同Reduce的key数量，会拼接到一起，减少partition的索引数量。
- sort：缓冲区数据按照key进行排序，实际是对partition和key两部分排序。排序结果如下：
  ![sort](./sort.png)




reduce个数设置：
mapred.reduce.tasks,默认为1
reduce个数太少：单词执行慢，出错再试成本高
reduce个数太多：shuffle开销大，输出大量小文件。NameNode会有影响

scala用起来很爽
Split对应一个map
下周：Hive
Hive在Master上搭建一下就性
主要是练习，工作中常用的，不离手，数据开发和数据仓库。

# Hive

### 引入原因

- 对存在HDFS上的文件或HBase中的表进行查询时，是要手工写一堆MapReduce代码
- 对于统计任务，只能由懂MapReduce的程序员才能搞定
- 耗时耗力，更多奖励没有有效的释放出来

**Hive基于一个统一的查询分析层，通过SQL语句的方式对HDFS上的数据进行查询，统计和分析**

大部分公司都将sql做成了页面的形式，直接在页面上写sql，并且会有关键词的提示。这些写起来更加方便。
Hive是一个SQL解析引擎，将SQL语句转义成MR Job，然后在Hadoop平台上运行，达到快速开发的目的。
Hive中的表是纯逻辑表，只有表结构，不存储数据。最终的数据在HDFS上。元数据的本质就是HDFS的目录和文件。就只是表的定义等，即表的元数据。本质就是Hadoop的目录文件，达到了元数据与数据存储分离的目的。比如数据已经通过Flume拉取到了HDFS上，这样就只需通过Hive对拉过来的数据进行建表，就可以通过SQL对拉过来的数据进行查询了。
Hive本身不存储数据，它完全依赖HDFS和MapReduce
Hive的内容是读多写少，不支持对数据的改写和删除。数据写回HDFS
Hive中没有定义专门的数据格式，由用户指定，需要指定三个属性：
- 列分隔符： 空格， ','  '\t'
- 行分隔符：'\n'
- 读取文件数据的方法

建表article
```
create table article(sentence string)
row format delimited fields terminated by '\n';
```
查看元数据信息
```
desc article;
```
导入数据
```
load data local inpath '/home/badou/Documents/code/mr/The_man_of_property.txt into table article;
```

```sql
select word, count(*)
from (
select
explode(split(sentence, ' '))
as word
from article
) t
group by word
```




