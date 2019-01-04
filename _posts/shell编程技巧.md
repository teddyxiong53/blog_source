---
title: shell编程技巧
date: 2019-01-04 15:37:37
tags:
	- shell
---





检查返回值：

最简单常见的方式。

```
echo abcdef | grep abcd
if [ $? -ne 0 ]; then
	echo "not found"
else
	echo "found"
fi
```

再简洁一点的。我觉得这个不好，不直观，只是一个冷门的技巧而已。

```
if echo abcdef | grep -q abcd; then
	echo "found"
else
	echo "not found"
fi
```

再简洁点的。

```
echo abcdef |grep -q abcd && echo "found" || echo "not found"
```



把stdout和stderr重定向到/dev/null。

```
./test.sh 1>/dev/null 2>&1
```

简洁的：

```
./test.sh &> /dev/null
```





参考资料

1、

http://kodango.com/simple-bash-programming-skills