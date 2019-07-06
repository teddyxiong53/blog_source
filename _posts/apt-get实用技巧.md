---
title: apt-get实用技巧
date: 2017-04-22 22:07:40
tags:
	- Linux

---



重新安装

```
sudo apt-get --reinstall install XXX
```

```
sudo apt-get remove xx 卸载，但是会保留配置文件。
sudo apt-get --purge remove xx 卸载，而且会把配置文件也删除。
sudo dpkg --force-all --purge xx 强力卸载。有点风险。
sudo dpkg -l

```

apt-cache用法

```
sudo apt-cache search xx 查找软件。
sudo apt-cache showpkg xx 查看包的情况。
```



典型场景应用

你想要在Linux上玩赛车游戏。

于是，你进行搜索：

```
sudo apt-cache search racing game
```

你想看看有没有torcs这款游戏。

```
sudo apt-cache show torcs
```

仓库上是有的。你想确认一下自己的电脑上是否已经安装了。

```
apt-cache policy torcs
```

````
teddy@teddy-ThinkPad-SL410:/usr/lib$ apt-cache policy torcs
torcs:
  已安装：(无)
  候选： 1.3.3+dfsg-0.2
  版本列表：
     1.3.3+dfsg-0.2 500
        500 http://mirrors.aliyun.com/ubuntu xenial/universe i386 Packages
````

并没有安装。

好的，我们来安装。

````
sudo apt-get install torcs
````

现在我的磁盘空间有点不够了，清理一下。

```
sudo apt-get clean
```

完了一会儿，不想玩了。

卸载。但是配置暂时不删除。

```
sudo apt-get remove torcs
```

