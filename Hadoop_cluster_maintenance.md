# Hadoop Cluster Maintenance

https://community.cloudera.com/t5/Community-Articles/Hadoop-Cluster-Maintenance/ta-p/245858

As a hadoop Admin it's our responsibility to perform Hadoop Cluster Maintenance frequently.

## 1 Filesystem Checks

check the health of HDFS periodically by running fsck command
```
# sudo -u hdfs hadoop fcks /
```

This command contacts the Namenode and checks each file recursively which comes under the provided path.

We can schedule a weekly cron job on edge node which will run the fsck and send the output via email to Hadoop Admin.

## 2 HDFS Balancer utility

Over the period of time data becomes un-balanced across all the Datanodes in the cluster, this could be because of maintenance activity on specific Datanode, power failure, kenerl panic, unexpected reboots etc. In this case because of data locality, Datanodes which are having more data will get churned and ultimately un-balanced cluster can deirectly affect your MapReduce job performance.You can use below command to run hdfs balancer
sudo -u hdfs hdfs balancer -threshold <threshold-value>
By default threshold value is 10, we can reduce it upto 1 ( It’s better to run balancer with lowest threshold )

```bash
[root@sandbox ~]# sudo -u hdfs hdfs balancer -threshold 1
```

We can schedule a weekly cron job on edge node which will run balancer and send the results via email to Hadoop Admin.

## 3 Adding new nodes to the cluster

We should always maintain the list of Datanodes which are authorized to communicate with Namenode, it can be achieved by setting `dfs.hosts` property in `hdfs-site.xml`:
```xml
<property>
  <name>dfs.hosts</name>
  <value>/etc/hadoop/conf/allowed-datanodes.txt</value>
</property>
```
If we don’t set this property then any machine which has Datanode installed and hdfs-site.xml property file can easily contact Namenode and become part of Hadoop cluster.

### 3.1 For Nodemanagers

We can add below property in yarn-site.xml

```xml
<property>
  <name>yarn.resourcemanager.nodes.include-path</name>
  <value>/etc/hadoop/conf/allowed-nodemanagers.txt</value>
</property>
```

## 4 Decommissioning a node from the cluster

**It’s a bad idea to stop single or multiple Datanode daemons or shutdown them gracefully though HDFS is fault tolerant. Better solution is to add ip address of Datanode machine that we need to remove from cluster to exclude file which is maintained by dfs.hosts.exclude property and run below command**
```bash
# sudo -u hdfs hdfs dfsadmin -refreshNodes
```
After this, Namenode will start replicating all the blocks to other existing Datanodes in the cluster, once decommission process is complete then it’s safe to shutdown Datanode daemon. You can track progress of decommission process on NN Web UI.

### 4.1 For YARN

Add ip address of node manager machine to the file maintained by yarn.resourcemanager.nodes.exclude-path property and run below command.
```bash
sudo -u yarn yarn rmadmin -refreshNodes
```
## 5 Datanode Vlume Failures
Namenode WebUI shows information about Datanode volume failures, we should check this information periodically or set some kind of automated monitoring system using **Nagios or Ambari Metrics** if you are using Hortonworks Hadoop Distribution or JMX monitoring (http://<namenode-host>:50070/jmx) etc. Multiple disk failures on single Datanode could cause shutdown of Datanode daemon. ( Please check dfs.datanode.failed.volumes.tolerated property and set it accordingly in hdfs-site.xml )

# 6 Database Backup

If we you have multiple Hadoop ecosystem components installed then you should schedule a backup script to take database dumps.

for e.g.

1. Hive metastore database

2. Oozie-DB

3. Ambari DB

4. Ranger DB

Create a simple shell script to have backup commands and schedule it on a weekend, add a logic to send an email once backups are done.
```
# 7 HDFS Metadata backup

fsimage has metadata about your Hadoop file system and if for some reason it gets corrupted then your cluster is un-usable, it’s very important to keep periodic backups of filesystem fsimage.

You can schedule a shell script which will have below command to take backup of fsimage

```bash
hdfs dfsadmin -fetchImage fsimage.backup.ddmmyyyy
```

# 8 Purging older log files

In production clusters, if we don’t clean older Hadoop log files then it can eat your entire disk and daemons could crash because of “no space left on device” error. Always get older log files cleaned via cleanup script!

