---
title: openwrt（八）luci分析
date: 2018-04-11 21:59:43
tags:
	- openwrt

---



luci是openwrt的web管理系统。是用lua写的。

代码在/www目录下。

```
/usr/sbin/uhttpd -f -h /www -r LEDE -
```

web server是uhttpd。这个web server又是谁写的呢？跟thttpd区别何在呢？

github地址在这：

https://github.com/lewischeng-ms/uhttpd



暂时不深入看luci的代码了。



uhttpd的配置在/etc/config/uhttpd里。

```
option home '/www'
list lua_prefix '/cgi-bin/luci=/usr/lib/lua/luci/sgi/uhttpd.lua'
list index_page 'cgi-bin/luci'
```

cgi程序的作用

CGI即通用网关接口，是外部应用程序（即CGI程序）与WEB服务器之间的接口标准，负责在CGI程序和Web服务器之间传递信息。

下图中的r = luci.http.Request(…)函数主要的作用是用来获取客户端提交的信息如图1 图2 所示

其中luci.dispather.httpdispatch(…)函数，主要用来解析相应的http指令，执行相应的脚本，同时组建http相关的帧



res为协同程序的状态

id=1，响应消息比如200OK

id为2,3组建相应的消息头部，http的格式里的 如图3所示

id为4时，是向uhttpd发送相关的html代码  如图4所示

id为5时，刷新缓冲区

io.write(…)是向uhttpd服务器发送信息



参考资料

1、openwrt--luci学习记录3 登录页面分析

https://blog.csdn.net/xiaohu1996/article/details/108190424

2、openwrt luci学习记录1--启动流程

https://blog.csdn.net/xiaohu1996/article/details/104463221

3、openwrt之修改Luci界面

https://blog.csdn.net/robothj/article/details/80636398

4、开发OpenWrt路由器上LuCI的模块

https://www.cnblogs.com/mayswind/p/3468124.html

5、OpenWrt Luci编写小技巧

https://blog.csdn.net/lvshaorong/article/details/54925266