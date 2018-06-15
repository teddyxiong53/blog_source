---
title: Python之monkey patch
date: 2018-06-15 22:54:46
tags:
	- Python

---



看HomeAssistant代码。里面看到monkey patch这个概念，搜索相关资料如下。

# 概念

这个概念起源于Zope框架。

大家在修正Zope的bug的时候，经常在程序后面追加更新部分。这些被叫做“guerilla patch”。

后面guerilla渐渐被写成了gorllia（猩猩）。再后来就干脆写成了monkey了。

所以就有了猴子补丁这么个说法。



猴子补丁的主要作用有：

1、在运行时替换方法，属性。

2、在不修改第三方代码的情况下，给它增加功能。

3、在运行时为内存里的对象增加patch。（这个用法听起来很高端啊，就像飞机的空中加油一样）。



# 参考资料

1、猴子补丁(monkey patch)

https://www.jianshu.com/p/f1060b22aab8