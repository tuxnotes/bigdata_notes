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
将一句话通过空格提取单词，然后将一句话一行转变成每个单词一行
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
第一个from后面的括号表示将括号内的语句结果作为一张临时表，表别名为t，别名需要指定

`explode(split(sentence, ' '))`，行转列，接受数组
单独对hive函数测试：
```sql
select split('the heroic and that there', ' ');
```
output
```
["the", "heroic", "and", "that", there"]
```

```sql
select explode(split('the heroic and that there', ' '));
```

output
```
the
heroic
and
that
there
```

使用Hive中的正则进行过滤
select regexp_extract('(mentioned','[[\\w]]+',0);
执行的返回结果：mentioned

```sql
select
regexp_extract(word,'[[\\w]]+',0) as word,
count(1) as cnt
from
(
  select
  explode(split(sentence, ' ')) as word
  from article
) t
group by regexp_extract(word,'[[\\w]]+',0)
limit 100;
```
这里不仅仅是统计，业务上更多的是top，哪些是热销商品
所以这里还需要一个全局排序，order by,全局排序只有一个reduce
如果没有加order by:一个mapreduce
如果加了order by：两个mapreduce，也就是说order by语句也会产生mapreduce
```sql
select
regexp_extract(word,'[[\\w]]+',0) as word,
count(1) as cnt
from
(
  select
  explode(split(sentence, ' ')) as word
  from article
) t
group by regexp_extract(word,'[[\\w]]+',0)
order by cnt desc
limit 100;
```

如果文章是中文，则需要切词。首先进行jieba(很多公司在用)中文切词。ik是Elasticsearch中自带的切词工具。还有hanlp. pyspark scala spark udf 切词

Hive中的SQL与传统SQL的区别

| 比较项 | HQL | SQL |
| ---- | ---- | ---- |
| 数据存储 | HDFS,HBase | Local FS |
| 数据格式 | 用户自定义 | 系统决定 |
| 数据更新 | 不支持(把之前的数据覆盖) | 支持 |
| 索引 | 有(0.8版本之后增加) | 有 |
| 执行 | mapreduce(select * from table) | Executor |
| 执行延迟 | 高 | 低 |
| 可扩展性 | 高(UDF UDAF UDTF) | 低 |
| 数据规模 | 大(数据大于TB) | 小 |
| 数据检查 | 读时模式 | 写时模式 |


UDF： 用户定义的函数
UDAF：用户定义的聚合函数
UDTF：展开形式的一种函数
不需要定义第三方的时候，很多函数Hive就有

所以使用场景是不同的：Hive用于统计分析，而关系型数据库则是用于线上的增删改查

**与传统关系数据特点比较**

- Hive和关系数据库存储文件的系统不同，Hive使用的是Hadoop的HDFS，关系数据库则是服务器本地的文件系统
- Hive使用的计算模型是mapreduce，而关系数据库则是自己设计的计算模型
- 关系数据库都是为实时查询的业务进行设计的，而Hive则是为海量数据做数据挖掘设计的，实时性很差
- Hive很容易扩展自己的存储能力和计算能力，这是继承Hadoop的，而关系数据库在这个方面要比Hive差很多


## Hive体系架构

Cli工具：进行交互执行SQL，直接与driver进行交互
JDBC驱动：作为JAVA的API，JDBC是通过Thrift Server来接入，然后发送给Driver
Driver(驱动)模块：通过该模块对输入进行解析编译，对需求的计算进行优化，然后按照指定的步骤执行(通常启动多个MR任务来执行)
元数据：是一个独立的关系型数据库，通常是MySQL，Hive会在其中保存表模式和其他系统元数据
hive不是集群，它只是提交mapreduce任务，所以只要是一台机器能提交任务即可

### 用户接口

- CLI：启动时，会同时启动一个Hive副本
- JDBC：Hive客户端，用户用户连接至Hive server
- WebUI：通过浏览器访问hive

大公司有中台，很多工作由中台提供便利

### 语句转换

- 解析器：生成抽象语法树
- 语法分析器：验证查询语句
- 逻辑计划生成器(包括优化器)：生成操作符树
- 查询计划生成器：转换为mapreduce任务

### 数据存储

- Hive数据以文件形式存储在HDFS的指定目录下。每一张表都是一个目录
- Hive语句生成查询计划，有mapreduce调用执行。执行结果是不做存储的，如果要存储，则要将结果插入到已存在的表中

## Hive的数据管理

Hive的表，本质就是Hadoop的目录/文件。Hive默认表村存放路径一般都是在你工作目录(warehouse,hive-site.xml中可以配置)的Hive目录里面，按表名做文件夹分开，如果你有分区表的话，分区值是子文件夹，可以直接在其它的MR job里直接用于这部分数据

分区表：首先表名对应的是一个目录，如果有分区的话，目录下会有对应的目录，如`action=insight`,action对应的字段，insight对应的值。如dt=20131020，则是日期对应某一天的数据作为一个分区。按日期分到子文件夹中

分区表： partition. hive表名/子文件夹。工作中一般根据日期做partition，每天一个partition，这一天所有的数据都放到对应日期的文件夹中。这样有什么好处呢。正常情况下，我们设置一个字段dt(date) ,子文件夹名字：dt=20190421。
分区的好处：
1. 对于查询效率上分区表更快。如果所有数据都放到一个表的文件夹中查询数据需要遍历(扫一遍所有数据)，如果这个文件夹中的数据包含了一年的用户行为数据，这样扫一边数据就是扫一年所有数据.
2. 如果做了分区，想要获取分析昨天的数据，只需要取对应昨天日志的文件夹中的数据即可，只需用找到对应日期的文件夹就行，具体限定约束条件在where后面： select userid from table where dt='20190421'. dt是其中表中的一个日期的字段名(列名)。用作分区的字段一般为：日期，客户端：pc，mobile， app。还有业务，部门，其他的就不是很常见了。

| item | Name | HDFS Directory |
| ---- | ---- | ---- |
| Table | mobile_user | /lbs/mobile_user |
| Partition | action=insight, dt=20131020 pc m app | /lbs/mobile_user/action=insight/dt=20131020 |
| Bucket | clusted by user into 32 buckets | /lbs/mobile_user/action=insight/dt=20131020/part-00031 |


内容查看

```bash
# hadoop fs -cat /usr/local/src/apache-hive-1.2.2-bin/warehouse/badou.db/news_jieba/* | head -2
```

Hive的方式查看

```sql
select * from news_jieba limit 2;
```

## Hive内部表和外部表

Hive的warehouse中的所有数据都是内部表。
Hive的create创建表的时候，选择的创建方式：

- create table 内部表
- create external table location 'hdfs_path' 外部表(必须是文件)

为什么需要外部表：文件已经存在HDFS上，在不移动数据到hive内部表的前提下，使用SQL的方式访问数据

建立外部表：

假设HDFS上有数据，路径为/data/The_man_of_property.txt

创建外部表不需要导入数据，但是需要指定数据位置。内部表需要导入数据

```sql
create external table art_ext(sentence string) row format delimited fields terminated by '\n'
[sprted as textfile中括号的可不加] location '/data/The_man_of_property.txt'
```

drop table 内部表后；文件夹和数据都会被删除。drop table 外部表后，表名没有了，但数据还在，只是删除了元数据信息。


特点：

- 导入数据到外部表，数据并没有一定到自己的数据仓库目录下，也就是说外部表中的数据并不是由它自己来管理的，而内部表则不一样；
- 在删除表的时候，Hive将会把属于表的元数据和数据全部删掉；而删除外部表的时候，Hive仅仅删除外部表的元数据，数据是不会删除的

当公司中使用sqoop或flame将数据拉倒HDFS上时，使用Hive创建外部表，创建数据仓库，然后使用SQL去处理。使用mr处理成本高，使用spark相对好点。但SQL最简单。

## hive中的partition

```
hive>set hive.cli.print.header=true;
```
上面的语句作用是执行select的时候，会打印表头

分区表partition
1. 创建分区表：create table art_dt(sentence string) partitioned by (dt string) row format delimited fields terminated by '\n';

2. 插入数据

```sql
insert overwrite table art_dt partition(dt='20190420') 
select * from art_ext limit 100;
insert overwrite table art_dt partition(dt='20190421') 
select * from art_ext limit 100; --sql做数据的ETL，或统计分析等的处理逻辑。这里的SQL可以变的很复杂。处理逻辑不需要上面一行的partition
```
如查询昨天的数据，关联用户属性表，用户属性表一般是在关系型数据库中。
查看分区数：
```
show partitions art_dt;
```
为什么采用上面的方式建立，因为在工作中hive任务一般都是在凌晨定时任务，比如凌晨1点执行这个SQL(逻辑：统计分析，ETL的数据清洗转换)，跑昨天一天的数据，(昨天以及昨天之前的数据)写入对应昨天日期的文件夹中。这主要是对行为数据。离线表T+1.


在Hive中，表中的一个partition对应于表下的一个目录，所有的partition的数据都存储在对应的目录中。例如，pvs表中包含ds和city两个partition，则：

- 对应于ds=20180801, city=US的HDFS子目录为：/warehouse/pvs/ds=20180801/city=US;
- 对应于ds=20180801, city=CA的HDFS子目录为：/warehouse/pvs/ds=20180801/city=CA;

partition是辅助查询，缩小查询范围，加快数据的检索速度和丢数据按一定的规格和条件进行管理。

使用city作为分区可能会有一个问题，比如北上广的数据特别多，但其他三线城市数据特别少，这样的问题就是有些文件夹下就几条数据，而有些文件夹下可能有上亿数据。如果where条件经常需要city，则可使用city分区。

## Hive中的Bucket分桶

Hive中的table可以拆分成partition， table和partition可以通过'CLUSTERED BY'进一步分bucket，bucket中的数据可以通过'SORT BY'排序或'ORDER BY'操作。通过下面的语句创建

```sql
create table bucket_user(id int,name string) clustered by (id) into 4 buckets;
```

使用`set hive.enforce.bucketing = true`可以自动控制上一轮reduce的数量从而适配bucket的个数，当然用户也可以自主设置mapred.reduce.task去适配bucket个数。一个bucket就是一个文件，一个文件就需要一个reduce

**Bucket主要作用**

- 数据sampling,数据采样
- 提升某些查询操作效率，例如mapside join ， left out

建分桶表：需要查询当前已经在Hive中的表的数据进行分桶的
1. 生成辅助表：create table bucket_num(num int);load data local inpath '/home/badou/Documents/data/hive/bucket_test.txt' into table bucket_num;
2. 每个数字进入一个bucket
2.1 建表(表的元数据信息建立)
set hive.enforce.bucketing = true;
create table bucket_test(num int) clustered by (num) into 32 buckets; 
2.2 查询数据并导入
insert overwrite table bucket_test select cast(num as int) as num from bucket_num limit 100;

3. sample采样

select * from bucket_test tablesample(bucket 1 out of 32 on num);-- 1 表示在第一个桶里，返回第一个桶中的数据
select * from bucket_test tablesample(bucket 1 out of 16 on num);-- 返回第一个桶和第17个桶内的数据，相当于将32个桶从中间截断为2个部分

tablesample是抽样语句，语法： TABLESAMPLE(BUCKET x OUT OF y). y必须是table总bucket的倍数或因子。hive根据y的大小，决定抽样的比例。例如，table总共分了64份，当y=32时，抽取(64/32=2)2个bucket的数据。当y=128时，抽取(64*1/128)1/2个bucket的数据。x表示从哪个bucket开始抽取。例如table总bucket数为32，tablesample(bucket 1 out of 16),表示总共抽取(32/16)2个bucket的数据，分别为第3个bucket和第(3+16)19个bucket的数据。
3 % 16 = 3  1
19 % 16 = 3 17
5 % 16 = 5
21 % 16 = 5

测试1/2个bucket

set hive.enforce.bucketing = true;
create table bucket_test4(num int)
clustered by(num)
into 4 bucket;
insert overwrite table bucket_test select num from bucket_num;

 结论：以hash的形式去取

 如果没有分桶，想采样90%的数据，如何实现：

select * from bucket_test4 where num % 10 > 0;

## Hive数据类型

### 原生类型

- TYNIINT
- SMALLINT
- INT    cast(userid as int)
- BIGINT userid 2389589540
- BOOLEAN
- FLOAT
- DOUBLE  spark用的较多
- STRING
- BINARY (Hive0.8.0以上才可用)
- TIMESTAMP (Hive0.8.0以上才可用)

### 复合类型

- Arrays：ARRAY <data_type>
- Maps: MAP <orimitive_type, data_type>
- Structs: STRUCT <col_name:data_type[COMMET col_comment], ...>
- Union: UNIONTYPE <data_type, data_type, ...>

## Hive SQL --- Join in MR

group by 可以用两个字段


### 订单数据表
先查看一下数据
```bash
head orders.csv

2539329.1.prior,1,2,08,
...
```

order_id, user_id, evel_set(有三种，先前数据，训练数据，测试数据),order_num(订单编号)，order_dow(dow,day of wait),order_hour_of_day, days_since_prior_order
工作中可能涉及到40-50个字段
order_id,订单编号
user_id, 用户id
eval_set,标识订单数据是否为历史数据,推荐会用到这部分数据
order_number,用户购买订单的编号，按用户购买的先后顺序编写
order_dow, dow : day of week星期几，0-6
order_hour_of_day,一天中哪一个小时产生的订单
days_since_prior_order,此订单距离上一个订单的天数

order_products_prior.csv这个数据比较大，3000多万条

drop table orders;

1. 创建表：create table orders(
  order_id string,
  user_id string,
  eval_set string,
  order_number string,
  order_dow string,
  order_hour_of_day string,
  days_since_prior_order string,
) row format delimited fields terminated by ',';
用的时候在转换为其他类型数据，开始建表的时候全部定义为string类型
2. 导入数据

load data local inpath '/home/badou/Documents/data/order_data' into table orders;

select count(1) from orders;
也可传到HDFS上，创建外部表

查看星期几字段是否为0-6
select order_dow,count(1) as cnt from orders group by order_dow;
select distinct(order_dow) from orders;


## hive的优化