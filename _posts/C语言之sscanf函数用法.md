---
title: C语言之sscanf函数用法
date: 2018-05-28 23:06:14
tags:
	- C语言

---



sscanf跟scanf的关系。就跟sprintf和printf的关系一样。

sscanf的从一个字符串里提取出想要的内容。



#最简单的用法

```
char buf[512];
sscanf("123456", "%s", buf);
printf("%s\n", buf)
```

这个没有什么实际用途。只是演示最最简单情况。

#取指定长度的字符串

例如，下面就是取4个字符。

```
sscanf("123456", "%4s", buf);
```

# 直到取到指定字符为止

下面这个表示取到空格为止。

```
sscanf("1234 abcd", "%[^ ]", buf);
```

得到的结果是1234 。

# 只取指定的字符集的字符串

```
sscanf("1234abcdABCD", "%[1-9a-z]", buf);
```

结果：1234abcd。

# 取到直到指定字符集为止

```
sscanf("1234abcdABCD, "[^A-Z]", buf);
```

结果：1234abcd。

# 取二者之间部分

```
sscanf("abc/123@edf", "%*[^/]/%[^@]", buf)
```

结果：123 。

取得/到@之间的部分。

# 过滤一部分

```
sscanf("hello, world", "%*s%s", buf);
```

结果：world。

`%*s`表示hello被过滤掉了。



# 参考资料

1、百度百科

https://baike.baidu.com/item/sscanf/10551550?fr=aladdin