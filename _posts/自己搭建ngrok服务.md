---
title: 自己搭建ngrok服务
date: 2018-11-29 21:41:16
tags:
	- 网络

---



我终于还是决定在我的vps上搭建ngrok服务，来让我的局域网的树莓派可以从外网进行访问。

花生壳的那个6元的服务，其实也就是在国内搭建的ngrok服务。

花生壳的还有流量限制。

但是我没有域名，这是个问题，我得先找一个免费的二级域名。

我在freenom上申请了一个免费域名，teddyxiong53.ml。

需要在这个上面建立2个A记录。

ngrok.teddyxiong53.ml和*.ngrok.teddyxiong53.ml。

用来关联ngrok服务。

ngrok是基于go语言的。所以需要先安装golang。

```
apt-get install golang
```

在vps上，是以root身份登陆的。

在~/.bashrc最后加上这个。

```
export GOPATH=$HOME/go
PATH=$PATH:$HOME/.local/bin:$HOME/bin:$GOPATH/bin
```

然后

```
source ~/.bashrc
```

然后下载ngrok的源代码。

```
 mkdir -p ~/go/src/github.com/inconshreveable
 cd  ~/go/src/github.com/inconshreveable
 git clone https://github.com/inconshreveable/ngrok.git
 export GOPATH=~/go/src/github.com/inconshreveable/ngrok
```



# 参考资料

1、从零教你搭建ngrok服务，解决外网调试本地站点

https://morongs.github.io/2016/12/28/dajian-ngrok/