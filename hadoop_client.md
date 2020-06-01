# hadoop中一些节点的意义

hadoop client , hadoop edge node, hadoop gateway

## hadoop client

hadoop client作为集群的堡垒机使用，是的集群环境和开发环境分离开来

选择集群外的一台机器，搭建client，流程如下：

（1）配置单向(master可以ssh到client，但client不可以ssh到master）ssh免密登陆。把master的id_pub.rsa内容添加到client的authorized__keys中

（2）修改client的/etc/hosts文件，添加master节点的ip和hostname
（3）把master节点的Hadoop包scp到client上
（4）修改client的/etc/profile文件，添加HADOOP_HOME环境变量，并把$HADOOP_HOME/bin添加到PATH
（5）修改core-site.xml文件，其中master_host:port是NN的地址

```xml
<property>
<name>fs.defaultFS</name>
<value>hdfs://master_host:port</value>
</property>
```

(6) 测试是否成功

```bash
# hadoop dfs -ls /
```

https://stackoverflow.com/questions/38533394/hadoop-client-node-installation

Client should have same copy of Hadoop Distribution and configuration which is present at Namenode then Only Client will come to know on which node Job tracker/Resourcemanager is running, and IP of Namenode to access HDFS data.

Also you need to update /etc/hosts of client machine with IP addresses and hostnames of namenode and datanode. Note that, you shouldn’t start any hadoop service on client machine.

Steps to follow on client machine:

create an user account on the cluster, say user1
create an account on client machine with the same name: user1
configure client machine to access the cluster machines (ssh w\out passphrase i.e, password less login)
copy/get a hadoop distribution same as cluster to client machine and extract it to /home/user1/hadoop-2.x.x
copy(or Edit) the hadoop configuration files (*-site.xml) from Namenode of the cluster - from this client will know where the Namenode/resourcemanager is running.
Set environment variables: JAVA_HOME, HADOOP_HOME (/home/user1/hadoop-2.x.x)
Set hadoop bin to your path: export PATH=$HADOOP_HOME/bin:$PATH
test it out: hadoop fs -ls / which should list the root directory of the cluster hdfs.

you may face some issues like privileges, may need to set JAVA_HOME places like conf/hadoop-env.sh on client machine. update/comment any error you get.


**Answers to more questions from comments:**

1. How to load data from client node to hdfs ? - Just run hadoop fs commands from client machine: hadoop fs -put /home/user1/data/* /user/user1/data - you can also write shell-scripts that would run these command(s) if you need to run them many times.

2. Why I am installing hadoop on the client if we only use ssh to connect remotely to the master node ?

 - because client need to communicate with cluster, and need to know where cluster nodes are.
 - client will be running hadoop jobs like hadoop fs commands, hive queries, hadoop jar commnads, spark jobs, developing mapreduce jobs etc for which client will need hadoop binaries on client node.
 - Basically you are not only using the ssh to connect, but you are performing some operations on hadoop cluster from client node so you would need hadoop binaries.
 - ssh is used by hadoop binaries on client node, when you run such operations like hadoop fs
-ls/ from client node to cluster. (remember adding $HADOOP_HOME/bin to PATH as part of installation process above)

- when you are saying "we only use ssh" - that sounds to me like when you want to make changes/access hadoop configuration files from cluster you are connecting using ssh to cluster nodes - you do this as part of administrative work but when you need to run hadoop commands/jobs against cluster from client node you dont need to ssh manually - hadoop installation on client node will take care of it.

- with out hadoop instalations how can you run hadoop commands/jobs/queries from client node to cluster?

3. should user name 'user1' must be same ? what if it is different ? - it will work. you can install hadoop on client node under group user say: qa or dev, and all users on client node as sudo under that group. than when user1 on client node need to run any hadoop job on cluster: user1 should be able to sudo -i -u qa and then run hadoop command from it.


https://stackoverflow.com/questions/43221993/what-does-client-exactly-mean-for-hadoop-hdfs

**Client** in Hadoop refers to the Interface used to communicate with the Hadoop Filesystem. There are different type of Clients available with Hadoop to perform different tasks.

The basic filesystem client hdfs dfs is used to connect to a Hadoop Filesystem and perform basic file related tasks. **It uses the ClientProtocol to communicate with a NameNode daemon, and connects directly to DataNodes to read/write block data**. To perform administrative tasks on HDFS, there is hdfs dfsadmin. For HA related tasks, hdfs haadmin. There are similar clients available for performing YARN related tasks.


These Clients can be invoked using their respective CLI commands from a node where Hadoop is installed and has the necessary configurations and libraries required to connect to a Hadoop Filesystem. Such nodes are often referred as Hadoop Clients.


>For example, if I just write an hdfs command on the Terminal, is it still a "client"?

Technicall, **Yes**. if you are able to access the FS using the `hdfs` command , then the node has the configurations and libraries required to be a hadoop Client.

**PS**:APIs are  also available to create these Clients programmatically.

## hadoop edge node

detailed information refers to book "hadoop for dummies" on page 326

Edge nodes (aka gateway nodes), contents about how to configure hadoop gateway node , refers to book "Hadoop 2.x Administration"


https://www.quora.com/What-is-a-simple-explanation-of-edge-nodes-Hadoop

**What is a simple explanation of edge nodes? (Hadoop)**

A Hadoop cluster ideally has 3 different kind of nodes: the masters, the edge nodes and the worker nodes.

The masters are the nodes that host the core more-unique Hadoop roles that usually orchestrate/coordinate/oversee processes and roles on the other nodes — think HDFS NameNodes (of which max there can only be 2), Hive Metastore Server (only one at the time of writing this answer), YARN ResourceManager (just the one), HBase Masters, Impala StateStore and Catalog Server (one of each). All master roles need not necessarily have a fixed number of instances (you can have many Zookeeper Servers) but they all have associated roles within the same service that rely on them to function. A typical enterprise production cluster has 2–3 master nodes, scaling up as per size and services installed on the cluster.

Contrary to this, the workers are the actual nodes doing the real work of storing data or performing compute or other operations. Roles like HDFS DataNode, YARN NodeManager, HBase RegionServer, Impala Daemons etc — they need the master roles to coordinate the work and total instances of each of these roles usually scale more linearly with the size of the cluster. A typical cluster has about 80-90% nodes dedicated to hosting worker roles.

Put simply, edge nodes are the nodes that are neither masters, nor workers. They usually act as gateways/connection-portals for end-users to reach the worker nodes better. Roles like HiveServer2 servers, Impala LoadBalancer (Proxy server for Impala Daemons), Flume agents, config files and web interfaces like HttpFS, Oozie servers, Hue servers etc — they all fall under this category. Most of each of these roles can be installed on multiple nodes (assigning more nodes for each role helps prevent everybody from connecting to one instance and overwhelming that node).

The purpose of introducing edge nodes as against direct worker node access is: one — they act as network interface for the cluster and outside world (you don’t want to leave the entire cluster open to the outside world when you can make do with a few nodes instead. This also helps keep the network architecture costs low); two — uniform data/work distribution (users directly connecting to the same set of few worker nodes won’t harness the entire cluster’s resources resulting in data skew/performance issues); and three — edge nodes serve as staging space for final data (stuff like data ingest using Sqoop, Oozie workflow setup etc).

That said, there is no formal rule that forces cluster admins to adhere to strict distinction between node types, and most Hadoop service roles can be assigned to any node which further blurs these boundaries. But following certain role-co-location guidelines can significantly boost cluster performance and availability, and some might be vendor-mandated.


