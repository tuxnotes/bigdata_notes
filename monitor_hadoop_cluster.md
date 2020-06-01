
https://www.quora.com/What-tools-are-best-practice-for-configuring-and-monitoring-Hadoop-clusters

## 1 Cloudera

Cloudera produces an exceptional tool for precisely this purpose called Cloudera Manager [1]. For clusters of less than 50 nodes, it's free to use, and can be downloaded at [4].

## 2 Nagios and Ganglia

- Use a Configuration Management system.  It doesn't matter what you pick, just pick something.  Be prepared that you will likely want different sets of config files per node-type (NN, JT, compute node, client, ...).

- Monitor the service, not the nodes, with a package that allows you to build custom checks.  Tools that have an "all or nothing" approach won't work for distributed systems. In our case, we configure a Nagios check that connects to the NN and JT to see what percentage of nodes are down.  This accomplishes two things:  if the NN/JT is down the check fails.  If the % is below a certain threshold, we know we better get some hardware back up soon.

- Check the output of fsck for warnings and errors every day.

- Run a small job (1 map, 1 reduce) every so often to make sure things are working as expected.  Some failure scenarios can't be picked up just by port checks.

I have no real suggestion for Metrics .  A lot of folks use Ganglia (monitoring) , but I'll be honest that it isn't my favorite.

## 3 Apache Ambari Project

There are many tools one can use to analyze and optimize performance of a Hadoop cluster, both open source, free (but closed source) and commercial.

Open Source tools

Starting with open source, each component of Hadoop comes packaged with its own administrative interface which can be used to collect cluster-wide performance metrics. Unfortunately, aggregating these metrics for correlation from multiple, disparate sources can be a challenge in and of itself. That being said, you can do it. Here’s a guide I wroteon collecting performance metrics from YARN, HDFS, and MapReduce, using the HTTP APIs exposed by each technology.

A great open source offering for Hadoop management and performance analysis is the Apache Ambari project, which provides users with a well-designed graphical interface for cluster management. In a single interface, you can provision, manage, and monitor clusters of thousands of machines. I can say from personal experience that it really is a great tool for working with Hadoop.

Free, closed source tools

Cloudera Manager is a free, but closed source tool out of Cloudera. There are both paid and free versions of this tool available, and for experimentation I have found the free version to be adequate. Unfortunately I do not have a comparison of the difference in features offered by version. I will say that Cloudera Manager provides a good graphical interface to Hadoop management, but in my personal experience I found Ambari easier to configure and deploy (your experience may vary).

Commerical tools

Shameless plug, but the company I work for (Datadog) also does Hadoop monitoring. Though Datadog does not provide a management interface like the other tools listed above, it monitors more than the Hadoop ecosystem. With Datadog, you can aggregate metrics from every application in your environment

Choosing the appropriate solution depends on many factors, including your collective team's experience, personal preference, and, let's face it, budget. But all of the above solutions do a great job of keeping an eye on your cluster when you're not looking.

-> Nagios
-> Ganglia
-> Brightcomputing
-> If you use Cloudera, You might want to check Hue. It is an excellent GUI to monitor hadoop jobs. Perhaps better than what your browser provides at 50070 and 50030 ports..

Apache Ambari: http://incubator.apache.org/ambari/

Ambari relies on open technologies (Ganglia, Nagios, Puppet) and, equally importantly, has features specific to monitoring/debugging to MapReduce, Pig, Hive applications etc. which you won't find in any other option - commercial or not. For e.g. it has built-in support for understanding/debugging Pig/Hive similar to Twitter Ambrose (https://github.com/twitter/ambrose). It then goes further to allow for performance analytics for individual MapReduce jobs too.

Finally, it's free, open-source and community driven and has none of the vendor lock-in issues one would face with a proprietary solution.

Given it's open nature, Ambari has also been integrated into other solutions like Teradata ViewPoint and similar other products.

## datadog

https://www.datadoghq.com/blog/collecting-hadoop-metrics/


