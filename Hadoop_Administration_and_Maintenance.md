# Hadoop Administratioin and Maintenance

http://www.hadoopadmin.co.in/hadoop-administration-and-maintenance/

In the Hadoop world, a Systems Administrator is called a Hadoop Administrator. Hadoop Admin Roles and Responsibilities include setting up Hadoop clusters. Other duties involve backup, recovery and maintenance. Hadoop administration requires good knowledge of hardware systems and excellent understanding of Hadoop architecture.

It’s easy to get started with Hadoop administration because Linux system administration is a pretty well-known beast, and because systems administrators are used to administering all kinds of existing complex applications. However, there are many common missteps we’re seeing that make us believe there’s a need for some guidance in Hadoop administration. Most of these mistakes come from a lack of understanding about how Hadoop works. Here are just a few of the common issues we find.

With increased adoption of Hadoop in traditional enterprise IT solutions and increased number of Hadoop implementations in production environment, the need for Hadoop Operations and Administration experts to take care of the large Hadoop Clusters is becoming vital.

What does a Hadoop Admin do on day to day ?

Installation and Configuration
Cluster Maintenance
Resource Management
Security Management
Troubleshooting
Cluster Monitoring
Backup And Recovery Task
Aligning with the systems engineering team to propose and deploy new hardware and software environments required for Hadoop and to expand existing environments.
Diligently teaming with the infrastructure, network, database, application and business intelligence teams to guarantee high data quality and availability.
Some of the potential problems, which Hadoop administrators face in day to day operations are caused due to:
Human: Humans cause most common errors in health of systems or machines. Even a simple mistake can create a disaster and lead to down time. To avoid these errors it is important to have proper and proactive diagnostic process in place.
Miss-configuration is another problem that Hadoop administrators come across. Even now, after so much of development in Hadoop, it is considered a young technology. Let us look at the solution to this problem. You need to perform the following steps to get rid of mis-configuration.
• Start with basic parameters related with storage and operation.
• Gain thorough understanding of what needs to be achieved and where we are?
• Do lot of trail runs before moving on with changes in production environment.
Next problem is Hardware. One would rarely hear about a problem related to memory, mother boards and disk controllers but hard drive is mostly the cause of most of the problems. Almost every manufacturer do specify different measures of drive such as: Mean time to failure, Mean time between failures. Hardware does not fail straight away, but they degrade over time and lead to different failures. HDFS is best in detecting corrupt data blocks and automatically replicate to new copies without human intervention.

Remaining factors causing problems for hadoop administrators are:
Resource exhaustion: It is also a major factor that causes problem. As an administrator, one should measure and track task failures so as to help the user identify and correct the processes. Repetitive task failures can occupy task slots and can also take away resources from other jobs. Therefore, it should be seen as a drain on overall capacity.Next is the Host identification and Naming. Incorrectly configured host configuration file, will lead to a situation where client will never be able to communicate with data nodes.
The other problem is network partition: it is a situation where network is unable to communicate with other hosts on segment of network. This means that host X on switch 1 cannot send messages to host Y present on switch 2.



If you are working on Hadoop, you’ll realize there are several shell commands available to manage your hadoop cluster.

1. Hadoop Namenode Commands
Command	Description
hadoop namenode -format	Format HDFS filesystem from Namenode
hadoop namenode -upgrade	Upgrade the NameNode
start-dfs.sh	Start HDFS Daemons
stop-dfs.sh	Stop HDFS Daemons
start-mapred.sh	Start MapReduce Daemons
stop-mapred.sh	Stop MapReduce Daemons
hadoop namenode -recover -force	Recover namenode metadata after a cluster failure (may lose data)
2. Hadoop fsck Commands
Command	Description
hadoop fsck /	Filesystem check on HDFS
hadoop fsck / -files	Display files during check
hadoop fsck / -files -blocks	Display files and blocks during check
hadoop fsck / -files -blocks -locations	Display files, blocks and its location during check
hadoop fsck / -files -blocks -locations -racks	Display network topology for data-node locations
hadoop fsck -delete	Delete corrupted files
hadoop fsck -move	Move corrupted files to /lost+found directory
3. Hadoop Job Commands
Command	Description
hadoop job -submit <job-file>	Submit the job
hadoop job -status <job-id>	Print job status completion percentage
hadoop job -list all	List all jobs
hadoop job -list-active-trackers	List all available TaskTrackers
hadoop job -set-priority <job-id> <priority>	Set priority for a job. Valid priorities: VERY_HIGH, HIGH, NORMAL, LOW, VERY_LOW
hadoop job -kill-task <task-id>	Kill a task
hadoop job -history	Display job history including job details, failed and killed jobs
4. Hadoop dfsadmin Commands
Command	Description
hadoop dfsadmin -report	Report filesystem info and statistics
hadoop dfsadmin -metasave file.txt	Save namenode’s primary data structures to file.txt
hadoop dfsadmin -setQuota 10 /quotatest	Set Hadoop directory quota to only 10 files
hadoop dfsadmin -clrQuota /quotatest	Clear Hadoop directory quota
hadoop dfsadmin -refreshNodes	Read hosts and exclude files to update datanodes that are allowed to connect to namenode. Mostly used to commission or decommsion nodes
hadoop fs -count -q /mydir	Check quota space on directory /mydir
hadoop dfsadmin -setSpaceQuota /mydir 100M	Set quota to 100M on hdfs directory named /mydir
hadoop dfsadmin -clrSpaceQuota /mydir	Clear quota on a HDFS directory
hadooop dfsadmin -saveNameSpace	Backup Metadata (fsimage & edits). Put cluster in safe mode before this command.
5. Hadoop Safe Mode (Maintenance Mode) Commands
The following dfsadmin commands helps the cluster to enter or leave safe mode, which is also called as maintenance mode. In this mode, Namenode does not accept any changes to the name space, it does not replicate or delete blocks.

Command	Description
hadoop dfsadmin -safemode enter	Enter safe mode
hadoop dfsadmin -safemode leave	Leave safe mode
hadoop dfsadmin -safemode get	Get the status of mode
hadoop dfsadmin -safemode wait	Wait until HDFS finishes data block replication
6. Hadoop Configuration Files
File	Description
hadoop-env.sh	Sets ENV variables for Hadoop
core-site.xml	Parameters for entire Hadoop cluster
hdfs-site.xml	Parameters for HDFS and its clients
mapred-site.xml	Parameters for MapReduce and its clients
masters	Host machines for secondary Namenode
slaves	List of slave hosts
7. Hadoop mradmin Commands
Command	Description
hadoop mradmin -safemode get	Check Job tracker status
hadoop mradmin -refreshQueues	Reload mapreduce configuration
hadoop mradmin -refreshNodes	Reload active TaskTrackers
hadoop mradmin -refreshServiceAcl	Force Jobtracker to reload service ACL
hadoop mradmin -refreshUserToGroupsMappings	Force jobtracker to reload user group mappings
8. Hadoop Balancer Commands
Command	Description
start-balancer.sh	Balance the cluster
hadoop dfsadmin -setBalancerBandwidth <bandwidthinbytes>	Adjust bandwidth used by the balancer
hadoop balancer -threshold 20	Limit balancing to only 20% resources in the cluster
9. Hadoop Filesystem Commands
Command	Description
hadoop fs -mkdir mydir	Create a directory (mydir) in HDFS
hadoop fs -ls	List files and directories in HDFS
hadoop fs -cat myfile	View a file content
hadoop fs -du	Check disk space usage in HDFS
hadoop fs -expunge	Empty trash on HDFS
hadoop fs -chgrp hadoop file1	Change group membership of a file
hadoop fs -chown huser file1	Change file ownership
hadoop fs -rm file1	Delete a file in HDFS
hadoop fs -touchz file2	Create an empty file
hadoop fs -stat file1	Check the status of a file
hadoop fs -test -e file1	Check if file exists on HDFS
hadoop fs -test -z file1	Check if file is empty on HDFS
hadoop fs -test -d file1	Check if file1 is a directory on HDFS
10. Additional Hadoop Filesystem Commands
Command	Description
hadoop fs -copyFromLocal <source> <destination>	Copy from local fileystem to HDFS
hadoop fs -copyFromLocal file1 data	e.g: Copies file1 from local FS to data dir in HDFS
hadoop fs -copyToLocal <source> <destination>	copy from hdfs to local filesystem
hadoop fs -copyToLocal data/file1 /var/tmp	e.g: Copies file1 from HDFS data directory to /var/tmp on local FS
hadoop fs -put <source> <destination>	Copy from remote location to HDFS
hadoop fs -get <source> <destination>	Copy from HDFS to remote directory
hadoop distcp hdfs://192.168.0.8:8020/input hdfs://192.168.0.8:8020/output	Copy data from one cluster to another using the cluster URL
hadoop fs -mv file:///data/datafile /user/hduser/data	Move data file from the local directory to HDFS
hadoop fs -setrep -w 3 file1	Set the replication factor for file1 to 3
hadoop fs -getmerge mydir bigfile	Merge files in mydir directory and download it as one big file
