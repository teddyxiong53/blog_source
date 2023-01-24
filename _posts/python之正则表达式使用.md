---
title: python之正则表达式使用
date: 2023-01-16 22:33:31
tags:
	- Python

---



# match和search方法的区别

match要从字符串的开头开始匹配，如果开头不匹配，那就是不匹配。

举例：

```
aa 来match匹配 bbaacc 是不匹配的。因为bbaacc不是以aa开头的。
```

match方法，返回的是一个Match对象。

Match对象表示了什么呢？match和search方法返回的都是这个。

```
 |  The result of re.match() and re.search().
 |  Match objects always have a boolean value of True.
```

findall方法返回的是一个list。

# 查找

match
匹配string 开头，成功返回Match object, 失败返回None，只匹配一个。

search
在string中进行搜索，成功返回Match object, 失败返回None, 只匹配一个。

findall
在string中查找所有 匹配成功的组, 即用括号括起来的部分。返回list对象，每个list item是由每个匹配的所有组组成的list。

finditer
在string中查找所有 匹配成功的字符串, 返回iterator，每个item是一个Match object。

不多说概念，直接看栗子！



Match对象的group方法：

```
group(...)
    group([group1, ...]) -> str or tuple.
    Return subgroup(s) of the match by indices or names.
    For 0 returns the entire match.
```

参数为0，表示返回整个match。0可以不写，默认就是0

参数为1，表示第一个匹配的分组（指用小括号括起来的部分）

以此类推。



看一个例子。

```
import re

line = "Cats are smarter than dogs"

pattern = '(.*) are (.*?) .*'
matchObj = re.match(pattern, line, re.M|re.I)

if matchObj:
    print('group():', matchObj.group())
    print('group(1):', matchObj.group(1))
    print('group(2):', matchObj.group(2))
else:
    print('not match')
```

# 替换

用re.sub方法来进行替换。

```
re.sub(pattern, replacement, string, count=0, flag=0)
```

repacement是用来替换的字符串，也可以是一个函数。

count表示替换的次数。

例如，

```
import re
phone = '12-34 # 这个是假的号码'
num = re.sub('#.*$', '', phone)
print(num)
# 删除
num = re.sub('\D', "", phone)
print(num)
```

# compile函数

编译得到一个Pattern对象，给match和search使用。

主要提高运行效率。



# 参考资料

1、

https://cloud.tencent.com/developer/article/1335954

2、

https://blog.csdn.net/tp7309/article/details/72823258

3、

https://www.runoob.com/python/python-reg-expressions.html