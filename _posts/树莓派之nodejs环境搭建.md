---
title: 树莓派之nodejs环境搭建
date: 2018-12-19 14:27:26
tags:
	- 树莓派

---



默认是没有安装的，apt-get安装的会是很老的版本。

我不想用编译的方式安装。太慢。

```
wget https://nodejs.org/dist/v10.0.0/node-v10.0.0-linux-armv7l.tar.xz
```

挪到/usr/local/node目录。

```
sudo mv node-v10.0.0-linux-armv7l /usr/local/node 
```

然后建立软连接。

```
sudo ln -s /usr/local/node/bin/node /usr/bin/node
sudo ln -s /usr/local/node/bin/npm /usr/bin/npm
```

