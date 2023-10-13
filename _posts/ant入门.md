---
title: ant入门
date: 2019-03-30 13:58:32
tags:
	- 工具
typora-root-url: ../

---



先看看在Ubuntu下的安装。

从这里下载二进制包。有8M左右。



http://apache.cs.utah.edu//ant/binaries/apache-ant-1.10.5-bin.zip

解压放好。

在zshrc里添加这些内容：

```
export ANT_HOME=~/tools/apache-ant-1.10.5
export JAVA_HOME=/usr/lib/jvm/java-8-openjdk-amd64
export PATH=$PATH:$ANT_HOME/bin
export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar
```



ant是一个把软件编译、测试、部署等步骤联系在一起，加以自动化的工具。

ant的优点：

```
1、跨平台。
	使用java编写。
2、操作简单。
	有一个内置任务和可选任务组成。
	
```



HelloWorld

写一个build_test1.xml文件。内容如下：

```
<?xml version="1.0" ?>
<project name="helloworld">
	<target name="sayHello">
		<echo message="hello world"></echo>
	</target>
</project>
```

执行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/ant $ ant -buildfile build_test1.xml sayHello
Buildfile: /home/hlxiong/work/test/ant/build_test1.xml

sayHello:
     [echo] hello world

BUILD SUCCESSFUL
Total time: 0 seconds
```



# 常用标签

## project

是build文件的root标签。

常用属性有：

```
name
default
basedir
```

## target

表示一个个等待执行的任务。

一个project下面有多个target。

可以指定一个target依赖另外一个target。

常用属性：

```
name
depends
if
unless
```

举例：

```
<?xml version="1.0" ?>
<project name="targetStudy" default="targetB">
	<property name="xx" value="aa"></property>
	<target name="targetA" if="xx">
		<echo message="java version: ${ant.java.version}"></echo>
	</target>
	<target name="targetB" depends="targetA" unless="yy">
		<echo message="the base dir is: ${basedir}"></echo>
	</target>
</project>
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/ant $ ant -buildfile build_test1.xml         
Buildfile: /home/hlxiong/work/test/ant/build_test1.xml

targetA:
     [echo] java version: 1.8

targetB:
     [echo] the base dir is: /home/hlxiong/work/test/ant

BUILD SUCCESSFUL
Total time: 0 seconds
```

可以看到，2个target都执行了，默认是执行targetB。我们没有在命令行里明确指定target。

而targetB依赖了targetA。而这2个target需要的调节if和unless恰好都满足。

我们把targetB的unless改成xx。则target的条件不满足了。

运行情况如下：

```
hlxiong@hlxiong-VirtualBox ~/work/test/ant $ ant -buildfile build_test1.xml 
Buildfile: /home/hlxiong/work/test/ant/build_test1.xml

targetA:
     [echo] java version: 1.8

targetB:

BUILD SUCCESSFUL
Total time: 0 seconds
```

## mkdir

```
<mkdir dir="./xx"/>
```



## delete

删除。对象可以是文件、目录。

常用属性：

```
file
dir
includeEmptyDirs="true"
failonerror="true" 在出错时停止。
```


## copy

复制文件或者目录。

常用属性：

```
file
tofile
todir
overwrite="false" 是否覆盖。默认是不覆盖的。
```

复制单个文件：

```
<copy file="old.txt" tofile="new.txt" />
```

复制文件到另外一个目录：

```
<copy file="old.txt" todir="xx" overwrite="true" />
```

复制目录：

```
<copy todir="xx">
	<fileset dir="yy" />
</copy>
```

## move

移动文件或者目录。跟copy差不多。

## filelist

表示一个文件列表。

常用属性。

```
dir
files
refid
```

## fileset

## property



## path



## javac



## java



## jar





# 参考资料

1、ubuntu中ANT的安装和配置

https://www.cnblogs.com/shitouer/archive/2011/08/31/2160467.html

2、Apache Ant自动化脚本入门教程及常用命令介绍

https://www.jb51.net/article/87674.htm