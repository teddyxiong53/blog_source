---
title: nodejs之多个环境共存
date: 2018-12-28 11:04:17
tags:
	- nodejs
---

--

nodejs的版本环境问题，比起python来说，更加严重，因为nodejs的版本更多。

版本高了低了都是问题。

怎么让多个版本的nodejs共存在一台电脑呢？

nvm就是这样一个工具。

node version manager。

安装：

```
git clone https://github.com/creationix/nvm.git ~/.nvm && cd ~/.nvm && git checkout `git describe --abbrev=0 --tags`
```

在.bashrc里加上这一行。要配置淘宝的源。不然慢到怀疑人生。

```
export NVM_NODEJS_ORG_MIRROR=http://npmmirror.com/mirrors/node
source ~/.nvm/nvm.sh
```

```
hlxiong@hlxiong-VirtualBox:~$ nvm --version
0.33.11
```



nvm常用命令：

```
nvm ls //列出当前安装的node
nvm ls-remote //列出服务器上可用的node

```

```
hlxiong@hlxiong-VirtualBox:~$ nvm ls
               
->       system *
node -> stable (-> N/A) (default)
iojs -> N/A (default)
lts/* -> lts/dubnium (-> N/A)
lts/argon -> v4.9.1 (-> N/A)
lts/boron -> v6.16.0 (-> N/A)
lts/carbon -> v8.15.0 (-> N/A)
lts/dubnium -> v10.15.0 (-> N/A)
```

我选择安装nvm install v8.15.0

```
hlxiong@hlxiong-VirtualBox:~$ nvm install v8.15.0
Downloading and installing node v8.15.0...
Downloading http://npm.taobao.org/mirrors/node/v8.15.0/node-v8.15.0-linux-x64.tar.xz...
######################################################################## 100.0%
Computing checksum with sha256sum
Checksums matched!
Now using node v8.15.0 (npm v6.4.1)
Creating default alias: default -> v8.15.0 *
```



使用这个版本。

```
nvm use v8.15.0
```



```
hlxiong@hlxiong-VirtualBox:~$ node -v
v8.15.0
```

```
hlxiong@hlxiong-VirtualBox:~$ which node
/home/hlxiong/.nvm/versions/node/v8.15.0/bin/node
hlxiong@hlxiong-VirtualBox:~$ which npm
/home/hlxiong/.nvm/versions/node/v8.15.0/bin/npm
```



安装的环境在这里。

```
hlxiong@hlxiong-VirtualBox:~/.nvm/versions/node$ ls
v8.15.0
```

怎样在项目里指定使用哪个版本的nvm呢？

需要写一个.nvmrc文件。我暂时先手动管理吧。





nvm也同时解决了全局安装的问题。这样只在个人目录下操作。



设置默认的nvm的node版本。

```
nvm alias default v10.14.0
```

# node版本问题

## ubuntu18.04上无法运行node v18以上版本

有C库问题。

```
node: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.28' not found (required by node)
```

https://github.com/nodesource/distributions/issues/1392

看起来这个问题不好解决。



# 参考资料

1、使用 nvm 管理不同版本的 node 与 npm

http://bubkoo.com/2017/01/08/quick-tip-multiple-versions-node-nvm/

2、nvm 使用淘宝镜像

https://www.chenky.com/archives/746