---
title: Ubuntu之升级Python3的版本
date: 2018-06-10 23:12:51
tags:
	- Ubuntu

---



手动安装HomeAssistant，提示我的Python3的版本太低。要升级。



操作方法如下：

```
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
sudo rm /usr/bin/python3
sudo ln -s /usr/bin/python3.6 /usr/bin/python3
```



提示了错误。gpg:找不到可写的公钥钥匙环：eof

因为root用户没有key。所以按下面的步骤生成。

```
cd /root

mkdir .gunpg

chmod 555 .gnupg/

gpg --gen-key
```

其实不是这个原因，根本原因是我之前在/etc/apt目录下删掉了一些东西。包括/etc/apt/trusted.gpg.d。

把/etc/apt/trusted.gpg.d目录创建一下就好了。



现在又是不信任这个源的东西。

我还是编译安装吧。下载还非常快。

```
wget https://www.python.org/ftp/python/3.6.3/Python-3.6.3.tgz
```

直接三步走就行了。没有什么特别的配置。



切换默认的python为python3.6 。

模仿这个，在python的条目下新增一条。

```
sudo update-alternatives --install /usr/bin/java java /usr/lib/jvm/jdk1.8.0.05/bin/java 1
```

语法是：

```
sudo update-alternatives --install <link> <name> <path> <priority>
```

那么

```
sudo update-alternatives --install /usr/bin/python python /usr/local/bin/python3.6 3 
```

现在查询一下：

```
 sudo update-alternatives --list python
/usr/bin/python2.7
/usr/bin/python3.5
/usr/local/bin/python3.6
```

设置默认为python3.6 。

```
sudo update-alternatives --config python
```



# 参考资料

1、ubuntu14.04 升级python3.4到3.6

https://blog.csdn.net/u012551524/article/details/80419441

2、gpg:找不到可写的公钥钥匙环：eof gpg: no writable public keyring found: eof

https://blog.csdn.net/mlzhu007/article/details/3933977

