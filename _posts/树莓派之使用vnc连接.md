---
title: 树莓派之使用vnc连接
date: 2017-07-28 21:54:11
tags:
	- 树莓派
	- vnc

---

我给树莓派安装了带界面的系统，但是我没有多余显示屏给树莓派用，所以就用vnc来进行远程桌面连接。

1、pc上安装vnc客户端。

2、树莓派安装vnc服务端。`sudo apt-get install tightvncserver`

3、树莓派启动服务器。`vncserver :1`。然后输入密码。

4、pc上启动vnc客户端。输入`192.168.0.101:1`，输入第3步设置的密码，就可以连接了。





# 参考资料

1、修改分辨率。

https://support.realvnc.com/knowledgebase/article/View/523