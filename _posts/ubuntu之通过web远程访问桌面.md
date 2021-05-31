---
title: ubuntu之通过web远程访问桌面
date: 2021-05-27 19:38:25
tags:
	- ubuntu
---

--

这个借助的就是novnc这个东西。

先下载代码：

```
git clone git://github.com/kanaka/noVNC
```

安装一些软件：

```
sudo apt install websockify
sudo apt-get install tightvncserver
```

启动vncserver

```
vncserver :1
```

执行：

```
./utils/launch.sh --vnc 10.28.39.10:5901
```

可以启动

```
amlogic@amlogic-BAD-INDEX:~/tools/noVNC$ ./utils/launch.sh --vnc 10.28.39.10:5901
Warning: could not find self.pem
Using installed websockify at /usr/bin/websockify
Starting webserver and WebSockets proxy on port 6080
```

但是连接不成功

```
10.28.39.22 - - [27/May/2021 19:45:03] code 400, message Client must support 'binary' or 'base64' protocol
10.28.39.22 - - [27/May/2021 19:45:03] code 404, message File not found
```

可以解决。根据参考资料2

````
Solved editing file /novnc/core/websock.js
Locate line:
this._websocket = new WebSocket(uri, protocols);
replace with
this._websocket = new WebSocket(uri, ['binary', 'base64']); //protocols);
````

现在可以连上，但是显示桌面上空白。搜索“novnc gray screen x cursor”。





1、

https://blog.csdn.net/ypbsyy/article/details/80523596

2、

https://github.com/novnc/noVNC/issues/1276

3、

https://blog.csdn.net/weixin_30448685/article/details/95103282