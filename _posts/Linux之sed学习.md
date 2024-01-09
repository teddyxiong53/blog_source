---
title: Linux之sed学习
date: 2018-09-22 14:58:17
tags:
	- Linux

---

--

之前大略看过sed的语法。

现在要逐渐把工作中碰到的用法都总结下来。

```
sed -n 's@^//applet:@@p'
```

这个是在busybox的gen_build_files.sh里的。具体是什么效果呢？

这里的@是做分隔符用的。



sed 是一种在线编辑器，它一次处理一行内容。

处理时，把当前处理的行存储在临时缓冲区中，称为“模式空间”（pattern space），

接着用sed命令处理缓冲区中的内容，处理完成后，把缓冲区的内容送往屏幕。

接着处理下一行，这样不断重复，直到文件末尾。



文件内容并没有 改变，除非你使用重定向存储输出。



Sed主要用来自动编辑一个或多个文件；

简化对文件的反复操作；

编写转换程序等。



# 替换常用命令

基本的：

```
sed 's/old/new/'
```

构成分析：

1、s。表示替换。

2、/。有3根。也可以用?等其他的符号，都保持一样就好了。

3、单引号。可以换成双引号的。

把old替换为new。

全部替换：

```
sed 's/old/new/g'
```

在最后增加了一个g，如果没有，只替换匹配的第一个。

加上行数指定：

```
sed '2s/old/new/' 替换第二行的
sed '2,5s/old/new/'替换第2到第5行的。
```

执行多个规则：

```
sed 's/old/new/; s/old2/new2/'
```



# 常用选项

```
-n：
	安静模式，加上这个选项，则只有经过处理的行才显示出来。
-e：
	直接在命令列模式上进行sed动作编辑（？怎么理解？）
-f
	把所有的操作写在一个文件里，这个在规则比较复杂的时候用。
	
-i：
默认都是 直接输出到屏幕的，用i选项，就会直接插入到文件里去。
```

```
sed [opt] 'n1,n2function'  1.txt
```

function叫动作。

动作有：

```
a：增加
c：取代。
d：删除
i：插入
p：打印
s：取代
```



# 例子



# 思维导图

https://yemaosheng.com/wp-content/uploads/2009/05/sed.jpg



# 参考资料

1、sed命令

http://man.linuxde.net/sed

2、sed 字符串替换

https://www.cnblogs.com/linux-wangkun/p/5745584.html

3、

https://www.itdaan.com/blog/2017/09/08/1fbfa9a146319f526fc611999ada80b2.html