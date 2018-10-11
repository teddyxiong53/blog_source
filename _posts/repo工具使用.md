---
title: repo工具使用
date: 2018-10-11 10:34:51
tags:
	- 工具

---



repo是谷歌开发的，用来管理Android代码的工具，是用Python对git进行了包装的工具。

简化了对多个git版本库的管理。

repo的使用流程是这样的：

1、初始化。基于xml文件。./repo/manifest.xml。

```
repo init
```

2、repo sync。

同步项目里的某一个部分，

repo sync xxx。



# 参考资料

1、Repo工具的使用

https://blog.csdn.net/davidsky11/article/details/23291483