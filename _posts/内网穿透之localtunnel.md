---
title: 内网穿透之localtunnel
date: 2019-05-09 11:56:11
tags:
	- 网络
---

1

localtunnel跟ngrok类似，ngrok是基于go的。

而localtunnel是基于nodejs的。

安装：

```
npm install -g localtunnel
```

当前我们的80端口打开的，有一个网站在这个端口上运行。

我们这样运行：

```
$ lt --port 80
your url is: https://green-otter-47.localtunnel.me
```

我们用输出的这个url就可以从外网访问到我们的网站了。

非常简单，比ngrok用起来还简单些。

我们再运行一次，看到url是这样：

```
your url is: https://tough-elephant-85.localtunnel.me
```

前面单词是随机生成的。

但是我停止当前的程序，再运行，会容易报这个错。

```
connection refused: localtunnel.me:46826 (check your firewall settings)
```

稍微等一下再试就好了。

如果希望固定域名，可以加-s参数。

```
lt -s xhl -p 80
```

这个会报错，因为xhl这个被占用了。

```
hlxiong@hlxiong-VirtualBox ~/work/test/wechat $ lt -s xhl -p 80
tunnel server offline: Request failed with status code 403, retry 1s
tunnel server offline: Request failed with status code 403, retry 1s
```

换成teddyxiong53，这个不会有人占用了。

得到：

```
your url is: https://teddyxiong53.localtunnel.me
```

跟ngrok一样，你也可以自己建立一个localtunnel服务器，来保证速度。





参考资料

1、Localtunnel 内网穿透工具的安装与使用

https://www.hi-linux.com/posts/24471.html