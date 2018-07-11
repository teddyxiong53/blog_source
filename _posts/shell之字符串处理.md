---
title: shell之字符串处理
date: 2018-07-09 10:53:02
tags:
	- shell

---



之前处理字符串，我都是尽量用Python来做。

现在板子上没有Python。所以只能用shell里的那些工具来做。



awk

sed

expr

tr

cut





过滤出需要的行。

```
sed "/SW_VERSION/p" /etc/os-release -n
```

在用awk取得对应的位置。

```
sed "/SW_VERSION/p" /etc/os-release -n | awk -F "=" '{print $2}' 
```



```
function trim() 
{ 
	echo $1 |  awk 'gsub(/^ *| *$/,"")'
}
```

```
chip=`sed -n "/vendor_id/p" /proc/cpuinfo | awk -F ":" '{print $2}'`

chip=`trim $chip`
```



linux shell 字符串操作详解 （长度，读取，替换，截取，连接，对比，删除，位置 ）

https://www.cnblogs.com/gaochsh/p/6901809.html

linux学习：sed与awk与tr用法整理

http://www.cnblogs.com/LO-gin/p/6882490.html



强大的grep，sed和awk--用案例来讲解

https://www.cnblogs.com/ZGreMount/p/7655635.html