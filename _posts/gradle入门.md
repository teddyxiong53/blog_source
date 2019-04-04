---
title: gradle入门
date: 2019-03-30 14:33:32
tags:
	- 工具
typora-root-url: ../

---





gradle是一个基于jvm的具有突破性的构建工具。

特点：

```
1、像ant一样，是通用灵活的构建工具。
2、可切换的，像maven一样。
3、多工程构建支持。
4、强大的依赖管理。
5、对已有的maven和ivy仓库的支持。
6、支持传递性的依赖管理。
7、ant一样的任务和构建是第一等公民。
8、具有广泛的领域模型来支持你的构建。

```

从这里下载二进制包。

https://gradle.org/install/

这个包的大小就更加夸张了，有80M之多。

在zshrc里加入：

```
export GRADLE_HOME=~/tools/gradle-5.3.1 
export PATH=$GRADLE_HOME/bin:$PATH
```



查看版本信息。

```
hlxiong@hlxiong-VirtualBox ~/work/test/gradle $ gradle -v

Welcome to Gradle 5.3.1!

Here are the highlights of this release:
 - Feature variants AKA "optional dependencies"
 - Type-safe accessors in Kotlin precompiled script plugins
 - Gradle Module Metadata 1.0

For more details see https://docs.gradle.org/5.3.1/release-notes.html


------------------------------------------------------------
Gradle 5.3.1
------------------------------------------------------------

Build time:   2019-03-28 09:09:23 UTC
Revision:     f2fae6ba563cfb772c8bc35d31e43c59a5b620c3

Kotlin:       1.3.21
Groovy:       2.5.4
Ant:          Apache Ant(TM) version 1.9.13 compiled on July 10 2018
JVM:          1.8.0_191 (Oracle Corporation 25.191-b12)
OS:           Linux 4.13.0-45-generic amd64
```



projects和tasks是gradle里最重要的2个概念。

这个跟ant是一样的。



在Android Studio出来之前，大家都是用eclipse进行Android开发。

eclipse里的构建项目的工具是ant。

而在j2ee开发里，大家都是用maven来做构建。maven可以从网上的仓库给你拉取jar包。



gradle就是融合了ant和maven的功能。



在一个Android工程里，一般有3个.gradle文件。

一个build.gradle在顶层目录，是负责整个工程的构建的。

还有一个在

```
./app/build.gradle
./settings.gradle
./build.gradle
```

settings.gradle，里面一般就是一句话：

```
include ':app'
```

如果你的工程还包括库文件。那么可能是这样：

```
include ':app',':library'
```



#HelloWorld

新建一个build.gradle文件。

```
task hello {
	doLast {
		println "hello world"
	}
}
```

执行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/gradle $ gradle -q hello
hello world
```

-q参数是因为执行过程中有一大堆的打印，看起来不爽。

上面的代码可以简化为这样。

```
task hello << {
    println 'Hello world!'
}
```

但是这个写法在我的当前版本上执行不通过。



在gradle里使用groovy脚本

```
task upper {
	doLast {
		String str = "aaBB"
		println "original: " + str
		println "upper case: " + str.toUpperCase()
	}
}
```

# 任务依赖

```
task hello {
	doLast {
		println("hello world")
	}
}

task intro(dependsOn: hello) {
	doLast {
		println("I am gradle")
	}
}
```

执行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/gradle $ gradle -q intro
hello world
I am gradle
```



# 动态任务

```
4.times {
	counter ->
	task "task$counter"  {
		doLast {
			println("I ams task number $counter")
		}
	}
}
```

运行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/gradle $ gradle -q task1
I ams task number 1
```



# java构建

大部分java项目基本流程都是一样的。

```
1、编译源文件。
2、进行单元测试。
3、创建jar包。
```

正因为如此，gradle默认提供了插件，可以帮我们完成这个任务。

写build.gradle如下：

````
apply plugin: 'java'
````

是的，只需要写这一行。

然后在目录下执行：

```
hlxiong@hlxiong-VirtualBox ~/work/test/gradle $ gradle build   

BUILD SUCCESSFUL in 1s
1 actionable task: 1 executed
```

查看目录：

```
hlxiong@hlxiong-VirtualBox ~/work/test/gradle $ tree              
.
├── build
│   ├── libs
│   │   └── gradle.jar
│   └── tmp
│       └── jar
│           └── MANIFEST.MF
└── build.gradle

4 directories, 3 files
```

## 一个完整的java构建脚本





参考资料

1、Gradle 使用指南

http://wiki.jikexueyuan.com/project/gradle/

2、Ubuntu环境安装Gradle

https://blog.csdn.net/tanlon_0308/article/details/40423707

3、Ant,Maven与Gradle的概念的理解

https://blog.csdn.net/wwlwwy89/article/details/71641378