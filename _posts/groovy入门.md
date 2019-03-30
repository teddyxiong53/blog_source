---
title: groovy入门
date: 2019-03-30 14:54:32
tags:
	- groovy
typora-root-url: ../

---





看gradle的教程，说是用groovy来写的。那就看看groovy的基本语法。

上面是groovy？

```
1、一种基于java的面向对象的语言。
2、2007年1月发布的第一个版本。
3、主要是作为java平台的脚本语言来使用。
4、是一种动态语言。
```

在这里下载。

http://www.groovy-lang.org/download.html#distro

我就下载2.4版本的。

在zshrc里加入：

```
export GROOVY_HOME=~/tools/groovy-2.4.16
export PATH=$GROOVY_HOME/bin:$PATH
```

验证，查看版本。

```
hlxiong@hlxiong-VirtualBox ~/tools/groovy-2.4.16 $ groovy -v
Groovy Version: 2.4.16 JVM: 1.8.0_191 Vendor: Oracle Corporation OS: Linux
```

进入repl工具命令行。

```
hlxiong@hlxiong-VirtualBox ~/work/test/groovy $ groovysh             
三月 30, 2019 3:28:37 下午 java.util.prefs.FileSystemPreferences$1 run
信息: Created user preferences directory.
Groovy Shell (2.4.16, JVM: 1.8.0_191)
Type ':help' or ':h' for help.
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
groovy:000> 
```



# HelloWorld

新建一个hello.groovy文件。

里面内容如下：

```
println("hello groovy")
```

执行：

```
groovy ./hello.groovy
```

可以没有分号，函数可以没有括号。



# 关键字

```
as
assert
def
instanceof
```

多了def这个东西。

定义动态类型变量。

# 字符串

有两种：

1、java.lang.String。

2、groovy.lang.GString。

这里有些坑。

单引号的字符串，是java类型的。

双引号的字符串。会处理里面的$展开。

三引号的字符串。可以随意多行。





参考资料

1、groovy教程

https://www.w3cschool.cn/groovy/groovy_overview.html

2、groovy

https://zh.wikipedia.org/wiki/Groovy

3、Ubuntu上搭建groovy 环境

https://blog.csdn.net/gxgxyjy062/article/details/77891981

4、Groovy脚本基础全攻略

https://blog.csdn.net/yanbober/article/details/49047515

5、Groovy语法介绍

http://blog.javachen.com/2014/09/05/about-groovy.html