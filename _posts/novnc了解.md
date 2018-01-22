---
title: novnc了解
date: 2018-01-20 12:29:18
tags:
	- novnc

---



novnc提供一种在网页上通过html5的Canvas，访问机器上的vncserver提供的vnc服务。需要做tcp到websocket的转换，才能在html5上显示出来。

网页就是一个客户端。类似于windows下面的vncviewer。



# 树莓派上安装novnc

1、下载novnc代码。

```
wget https://github.com/novnc/noVNC/zip/master
```

2、解压并执行。

```
unzip master

pi@raspberrypi:~/udisk/work/down/noVNC-master $ ./utils/launch.sh --vnc localhost:6080
Warning: could not find self.pem
Using local websockify at /home/pi/udisk/work/down/noVNC-master/utils/websockify/run
Starting webserver and WebSockets proxy on port 6080
WebSocket server settings:
  - Listen on :6080
  - Web server. Web root: /home/pi/udisk/work/down/noVNC-master
  - No SSL/TLS support (no cert file)
  - proxying from :6080 to localhost:6080


Navigate to this URL:

    http://raspberrypi:6080/vnc.html?host=raspberrypi&port=6080

Press Ctrl-C to exit


```

3、然后在windows上的浏览器里输入：

http://raspberrypi:6080/vnc.html?host=raspberrypi&port=6080

但是这样会报错，说连接被拒绝。因为需要另外启动vncserver。

另外开一个shell窗口。

```
vncserver
```

再连接，就可以了。默认用户就是pi，密码就是pi用户的密码。



