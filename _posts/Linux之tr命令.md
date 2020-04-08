---
title: Linux之tr命令
date: 2020-04-07 13:15:51
tags:
	- Linux

---

1

tr工具是用来转换、挤压以及删除字符的工具。输入是stdin，输出到stdout。

tr可以很容易实现sed的许多基本功能，可以看成一个简化版本的sed。



最简单的用法：

```
echo "123" | tr -d '\n'
```

这一行命令的效果是去掉123后面的换行符。

命令格式是：

```
tr [options] SET1 [SET2]
```

一般我们不带SET2这部分的。

一般是用来从字符串里删掉一部分，得到我们需要的东西。

# 一些示例

## 替换

```
cat 1.txt | tr "abc" "xyz" > 2.txt
```

这个是把1.txt里的所有a替换为x，b替换为y，c替换为z。而不是abc替换为xyz。

## 大小写转化

```
cat 1.txt | tr [a-z] [A-Z] > 2.txt
```

## 删除连续的相同字符

```
cat 1.txt | tr -s [a-zA-Z] > 2.txt
```

## 删除空行

```
cat 1.txt | tr -s "\n" > 2.txt
```

## 删除windows导致的`^M`字符

```
cat 1.txt | tr -d "\r" > 2.txt
```

## 用空格替换制表符

```
cat 1.txt | tr -s "\011" "\040" > 2.txt
```





参考资料

1、

https://blog.csdn.net/jeffreyst_zb/article/details/8047065