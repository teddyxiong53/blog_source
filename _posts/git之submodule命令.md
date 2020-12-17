---
title: git之submodule命令
date: 2018-11-28 22:12:11
tags:
	- git

---



submodule的出现是为了应对这样的使用场景：

你的项目需要使用另外一个项目A，项目A是一个第三方的开源软件。

这样可以在后面单独拉下依赖的项目。

```
git submodule init
git submodule update
```



现在自己要做一个工具，需要依赖其他的github仓库。

看看怎么用submodule来做。

开发过程中，经常会有一些通用的部分希望抽取出来做成一个公共库来提供给别的工程来使用，

而公共代码库的版本管理是个麻烦的事情。

而且一旦更新了就要同步到多个引用的系统中，

这个时候使用git submodule，然后执行: git submodule update就全部搞定了。



我当前的项目，依赖了BiliExp这个项目。

添加

为当前工程添加submodule。

```
git submodule add https://github.com/happy888888/BiliExp BiliExp
```

这个会产生一次clone操作。

在当前目录下，会产生一个.gitmodule文件。内容如下：

```
[submodule "BiliExp"]
	path = BiliExp
	url = https://github.com/happy888888/BiliExp
```

我提交的时候，应该把BiliExp忽略。

如果后续BiliExp有更新。

这样进行更新。

```
git submodule update
```



我们在其他电脑上取代码的时候，应该这样来保证把所有代码都取下来。

```
git submodule update --init --recursive
```





# 参考资料

1、Git 工具 - 子模块

https://git-scm.com/book/zh/v1/Git-%E5%B7%A5%E5%85%B7-%E5%AD%90%E6%A8%A1%E5%9D%97

2、git submodule常用的几个命令

https://blog.csdn.net/luo451591667/article/details/50668226

3、详解git submodule使用以及注意事项

https://www.suibianlu.com/c/p/22754.html