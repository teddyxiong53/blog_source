---
title: Linux之sed学习
date: 2018-09-22 14:58:17
tags:
	- Linux

---



之前大略看过sed的语法。

现在要逐渐把工作中碰到的用法都总结下来。

```
sed -n 's@^//applet:@@p'
```

这个是在busybox的gen_build_files.sh里的。具体是什么效果呢？

这里的@是做分隔符用的。



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

-i：

默认都是 直接输出到屏幕的，用i选项，就会直接插入到文件里去。





# 参考资料

1、sed命令

http://man.linuxde.net/sed

2、sed 字符串替换

https://www.cnblogs.com/linux-wangkun/p/5745584.html