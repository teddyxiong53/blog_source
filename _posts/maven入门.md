---
title: maven入门
date: 2019-03-30 13:34:32
tags:
	- 工具
typora-root-url: ../
---





什么是maven？

这个单词来自于意地绪语。意思是知识的积累。

是一个项目管理工具。负责管理项目开发过程中的所有东西。

从这里下载二进制包进行安装。

http://maven.apache.org/download.cgi

在~/.zshrc里加上下面这些。

```
export M2_HOME=~/tools/apache-maven-3.6.0
export M2=$M2_HOME/bin
export PATH=$M2:$PATH
```

不建议用apt-get的方式进行安装。

查看版本信息。

```
hlxiong@hlxiong-VirtualBox ~/work/tmp/0330 $ mvn --version    
Apache Maven 3.6.0 (97c98ec64a1fdfee7767ce5ffb20918da4f719f3; 2018-10-25T02:41:47+08:00)
Maven home: /home/hlxiong/tools/apache-maven-3.6.0
Java version: 1.8.0_191, vendor: Oracle Corporation, runtime: /usr/lib/jvm/java-8-openjdk-amd64/jre
Default locale: zh_CN, platform encoding: UTF-8
OS name: "linux", version: "4.13.0-45-generic", arch: "amd64", family: "unix"
```



HelloWorld

```
mvn archetype:generate -DgroupId=com.xhl.helloworld -DartifactId=helloworld -Dpackage=com.xhl.helloworld -Dversion=1.0-SNAPSHOT
```

这个命令会执行几分钟，看到下载了很多的东西。

最后的打印是这样：

```
[INFO] Using property: groupId = com.xhl.helloworld
[INFO] Using property: artifactId = helloworld
[INFO] Using property: version = 1.0-SNAPSHOT
[INFO] Using property: package = com.xhl.helloworld
Confirm properties configuration:
groupId: com.xhl.helloworld
artifactId: helloworld
version: 1.0-SNAPSHOT
package: com.xhl.helloworld
 Y: : 
[INFO] ----------------------------------------------------------------------------
[INFO] Using following parameters for creating project from Archetype: maven-archetype-quickstart:1.4
[INFO] ----------------------------------------------------------------------------
[INFO] Parameter: groupId, Value: com.xhl.helloworld
[INFO] Parameter: artifactId, Value: helloworld
[INFO] Parameter: version, Value: 1.0-SNAPSHOT
[INFO] Parameter: package, Value: com.xhl.helloworld
[INFO] Parameter: packageInPathFormat, Value: com/xhl/helloworld
[INFO] Parameter: package, Value: com.xhl.helloworld
[INFO] Parameter: version, Value: 1.0-SNAPSHOT
[INFO] Parameter: groupId, Value: com.xhl.helloworld
[INFO] Parameter: artifactId, Value: helloworld
[INFO] Project created from Archetype in dir: /home/hlxiong/work/test/maven/helloworld
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time:  01:44 min
[INFO] Finished at: 2019-03-30T13:49:18+08:00
[INFO] ------------------------------------------------------------------------
```

得到的目录如下：

```
hlxiong@hlxiong-VirtualBox ~/work/test/maven $ tree                                 
.
└── helloworld
    ├── pom.xml
    └── src
        ├── main
        │   └── java
        │       └── com
        │           └── xhl
        │               └── helloworld
        │                   └── App.java
        └── test
            └── java
                └── com
                    └── xhl
                        └── helloworld
                            └── AppTest.java

12 directories, 3 files
```

然后进入到helloworld目录。

执行：

```
mvn package
```

又是要几分钟，不知道是因为我第一次执行这些命令呢，还是每次都要这么就。

执行一下测试程序。

```
hlxiong@hlxiong-VirtualBox ~/work/test/maven/helloworld/target $ java -cp ./helloworld-1.0-SNAPSHOT.jar com.xhl.helloworld.App
Hello World!
```



我们看看maven的几个核心概念。

pom

```
工程对象模型。

```



参考资料

1、Apache Maven 入门篇 ( 上 )

https://www.oracle.com/technetwork/cn/community/java/apache-maven-getting-started-1-406235-zhs.html

2、Ubuntu 16.04安装Maven

https://www.cnblogs.com/EasonJim/p/7203635.html