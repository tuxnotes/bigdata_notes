# 离线部署

这里的离线部署只不是用rpm的部署方式

## 部署概述

离线部署分为三个部分的部署：

1. MySQL离线部署：用于存储元数据
2. CM离线部署：
3. Parcel文件离线部署

## 部署所需的软件

1. CM：[cloudera-manager-centos7-cm5.16.1x8664.tar.gz][http://archive.cloudera.com/cm5/cm/5/cloudera-manager-centos7-cm5.16.1_x86_64.tar.gz]

2. Parcel:

   [CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel][http://archive.cloudera.com/cdh5/parcels/5.16.1/CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel]
   [CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1][http://archive.cloudera.com/cdh5/parcels/5.16.1/CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1]
   [manifest.json][http://archive.cloudera.com/cdh5/parcels/5.16.1/manifest.json]

3. JDK

4. MySQL

5. MySQL jdbc jar: [mysql-connector-java-5.1.47.jar][http://central.maven.org/maven2/mysql/mysql-connector-java/5.1.47/mysql-connector-java-5.1.47.jar] 

   **mv mysql-connector-java-5.1.47.jar mysql-connector-java.jar**

## 部署步骤

### 1 节点初始化

1. 所有节点，配置hosts

2. 所有节点关闭防火墙，清空iptables规则，确保默认规则是accept，关闭selinux

3. 设置时区和时间同步,如果时间服务器是CDH集群外的节点，则所有节点配置相同。如果是CDH中的某个节点，则CDH中的其他节点要与此timerserver同步

   ```bash
   # timedatectl set-timezone Asia/Shanghai
   # yum -y install ntp
   # crontab设置定时时间同步
   # /usr/sbin/ntpdate TIMESERVER
   ```

4. JDK安装：jdk的tar包**一定要解压到`/usr/java`下**,且要**执行`chown -R root:root /usr/java/jdk-1.8.0_45`**,最后修改/etc/profile配置环境变量

### 2 MySQL离线部署

1. 采用二进制包的方式安装，安装步骤可参考官网，重点是配置文件

2. 创建CDH的元数据库和用用户、amon服务的数据库及用用户

   ```mysql
   create database cmf DEFAULT CHARACTER SET utf8;
   create database amon DEFAULT CHARACTER SET utf8;
   grant all on cmf.* TO 'cmf'@'%' IDENTIFIED BY 'Ruozedata123456!';
   grant all on amon.* TO 'amon'@'%' IDENTIFIED BY 'Ruozedata123456!';
   flush privileges;
   ```

### 3 部署MySQL JDBC jar包

**cmf , amon这两个进程存在于哪些节点，哪些节点就需要部署JDBC jar包**

```bash
mkdir -p /usr/share/java/
cp mysql-connector-java.jar /usr/share/java/
```

### 4 CDH部署

### 4.1 离线部署cm server 及agent

1. 所有节点

```bash
# mkdir /opt/cloudera-manager(默认目录，不能更改)
#tar -zxvf cloudera-manager-centos7-cm5.16.1_x86_64.tar.gz -C /opt/cloudera-manager/
```

2. 配置agent

   所有节点修改agent的配置,指向server的节点hadoop001.生成中使用主机名，IP可能变化

```bash
# cd /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-agent
#sed -i "s/server_host=localhost/server_host=hadoop001/g" /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-agent/config.ini
```

3. 修改server配置

   这里选择hadoop001作为server节点，所以此操作在hadoop001上进行

   ```bash
   vi /opt/cloudera-manager/cm-5.16.1/etc/cloudera-scm-server/db.properties
   com.cloudera.cmf.db.type=mysql
   com.cloudera.cmf.db.host=hadoop001
   com.cloudera.cmf.db.name=cmf
   com.cloudera.cmf.db.user=cmf
   com.cloudera.cmf.db.password=Ruozedata123456!
   com.cloudera.cmf.db.setupType=EXTERNAL
   ```

4. 所有节点创建cloudera-scm用户

   ```bash
   # useradd --system --home=/opt/cloudera-manager/cm-5.16.1/run/cloudera-scm-server/ --no-create-home --shell=/bin/false --comment "Cloudera SCM User" cloudera-scm
   ```

5. 所有节点：修改/opt/cloudera-manager目录的用户及用户组

   ```bash
   # chown -R cloudera-scm:cloudera-scm /opt/cloudera-manager
   ```

### 5 部署离线parcel源

选取hadoop001部署parcel离线源

1. 拷贝parcel离线源相关文件,**切记cp时,重命名去掉1,不不然在部署过程CM认为如上文文件下载未完整,会持续下载**

   ```bash
   # mkdir -p /opt/cloudera/parcel-repo
   # ll
   total 3081664
   -rw-r--r-- 1 root root 2127506677 May 9 18:04 CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel
   -rw-r--r-- 1 root root
   41 May 9 18:03 CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1
   -rw-r--r-- 1 root root 841524318 May 9 18:03 cloudera-manager-centos7-cm5.16.1_x86_64.tar.gz
   -rw-r--r-- 1 root root 185515842 Aug 10 2017 jdk-8u144-linux-x64.tar.gz
   -rw-r--r-- 1 root root
   66538 May 9 18:03 manifest.json
   -rw-r--r-- 1 root root
   989495 May 25 2017 mysql-connector-java.jar
   # cp CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel /opt/cloudera/parcel-repo/
   #切记cp时,重命名去掉1,不不然在部署过程CM认为如上文文件下载未完整,会持续下载
   # cp CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1 /opt/cloudera/parcel-repo/CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha
   # cp manifest.json /opt/cloudera/parcel-repo/
   # 校验是否完整，与CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel.sha1的内容比较
   # /usr/bin/sha1sum CDH-5.16.1-1.cdh5.16.1.p0.3-el7.parcel
   ```

2. 修改/opt/cloudera的用户和用户组

   ```bash
   # chown -R cloudera-scm:cloudera-scm /opt/cloudera/
   ```

3. 所有节点创建目录，并修改用户即用户组，为解压准备

   这些目录是为安装Hadoop组件的目录，这些目录是默认，不能随意更改

   ```bash
   # mkdir -p /opt/cloudera/parcels 
   # chown -R cloudera-scm:cloudera-scm /opt/cloudera/
   ```

### 6 启动CM相关服务

#### 6.1 hadoop001节点启动server

```bash
# /opt/cloudera-manager/cm-5.16.1/etc/init.d/cloudera-scm-server start
```

阿里云web界面,设置该hadoop001节点防火墙放开7180端口.等待1min,打开 http://hadoop001:7180 账号密码:admin/admin。假如打不开,去看server的log,根据错误仔细排查错误

#### 6.2 所有节点启动Agent

```bash
# /opt/cloudera-manager/cm-5.16.1/etc/init.d/cloudera-scm-agent start
```

## 7 接下来，web UI操作

浏览器打开http://hadoop001:7180/ ， 账号密码:admin/admin













