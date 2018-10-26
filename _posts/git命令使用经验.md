---
title: git命令使用经验
date: 2017-10-09 19:16:08
tags:
	- git

---



没有系统学习git的使用，有时候会跟github打交道。把碰到的问题及解决记录下来。

##取指定版本的代码

先把代码clone下来。

然后git log。找到对应版本的sha字符串。

然后git checkout sha字符串就好了。

但是这样就完全回退到指定版本了，怎么再继续到较新的版本呢？现在本地已经看不到更多的log信息了。

我觉得还是要下载多份，一份完全不动。只能用这种方式来做了。

##放弃本地修改，强制更新

```
git reset hard
```

## 查看某个文件的修改历史

```
git log -- xx.c
```

## git remote命令

1、查看远程的仓库情况。列出已经存在的远程分支。

```
git remote
```

后面加上-v，则得到更加详细的信息。



git远程建立仓库。



# 参考资料

1、git命令之git remote的用法

https://www.cnblogs.com/wuer888/p/7655856.html

2、菜鸟教程

http://www.runoob.com/git/git-branch.html