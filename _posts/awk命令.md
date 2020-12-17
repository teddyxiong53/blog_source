---
title: awk命令
date: 2020-12-12 15:06:30
tags:
	- Linux
---

1

觉得有必要把awk这个命令仔细学习一下，因为经常有一些小的字符处理需求。

感觉用awk就足以解决了。不用去弄正则表达式。



AWK 是一种处理文本文件的语言，是一个强大的文本分析工具。

基本语法：

```
awk [选项] -f scriptfile -v var=value file
```

-f后面跟一个脚本文件。

var=value表示给变量幅值。

file表示要处理的目标文件。

常用选项：

```
-F 分隔符。默认是空格。例如可以改成-F:  -F, -F#

```

行匹配语句

```
awk '{[pattern] action}' {filenames}
```

行匹配语句，只能使用单引号。

后面可以跟多个文件。

action就是print这一类的操作。

pattern可以没有。

例如：

```
awk '{print $1}' 1.txt
```

1.txt里内容放这些，作为测试材料。

```
2 this is a test
3 Are you like awk
This's a test
10 There are orange,apple,mongo
```

# 多个分隔符

可以使用多个分隔符。

例如先用空格分割，在此基础上，再用都好分割。

```
awk -F '[ ,]' '{print $1, $2, $5}' 1.txt
```

# 变量

```
awk -v a=1 '{print $1,$1+a}' 1.txt
```

输出是这样：

```
2 3
3 4
This's 1
10 11
```

可以看到，字符串的加1，是在后面拼接字符1。

# 使用脚本

```
awk -f {script} {filename}
```

例如：

```
awk -f cal.awk 1.txt
```

# 运算符

过滤第一列大于2的行。

```
awk '$1 > 2' 1.txt
```

过滤第一列等于2，然后打印这样的行的第一个和第三个字符。

```
awk '$1==2 {print $1,$3}' 1.txt
```

多个条件与。

```
awk '$1>2 && $2=="Are" {print $1,$2,$3}' 1.txt
```

# 内建变量

```
$n 当前行的第几个字段。由FS分割。
$0 当前行的所有数据。

```

# 使用正则

```
awk '$2 ~ /th/ {print $2,$2}' 1.txt
```

~表示后面是正则表达式。

//  2个斜杠包裹的就是正则表达式。



# 忽略大小写

```
awk 'BEGIN{IGNORECASE=1} /this/' 1.txt
awk 'begin{ignorecase=1} /this/' 1.txt
```

这2个的输出为什么不同？

因为关键词大小写敏感？

```
teddy@VM-0-17-ubuntu:~/work$ awk 'BEGIN{IGNORECASE=1} /this/' 1.txt
2 this is a test
This's a test
```

```
teddy@VM-0-17-ubuntu:~/work$ awk 'begin{ignorecase=1} /this/' 1.txt
2 this is a test
```





参考资料

https://www.runoob.com/linux/linux-comm-awk.html

