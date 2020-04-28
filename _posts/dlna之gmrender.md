---
title: dlna之gmrender
date: 2020-01-03 11:02:08
tags:
	- dlna

---

1

gmrender是一个开源的dlna播放器方案。

gm代表了Gstreamer Media。媒体播放是采用了gstreamer。

代码在这里：

https://github.com/hzeller/gmrender-resurrect

从项目介绍可以看到：

针对了树莓派进行优化。项目是从GMediaRenderer fork来的。

编译很简单：

```
./autogen.sh
./configure
make 
```

可执行文件生成在src目录下，叫gmediarender。

看看可以接受的参数：

```
-I
	指定ip地址。
-p
	指定端口号。
-u
	指定uuid
-f
	指定friendly name
-o
	指定输出模块。目前只实现了gstreamer的方式。所以不用管这个。
-P
	指定pidfile
-d
	后台模式。

```

另外还有针对gstreamer的参数：

```
./gmediarender --help-gst
./gmediarender --help-gstout
```

一条基本的命令：

```
sudo ./gmediarender -I 172.16.4.205 --logfile stdout
# 我之所以指定这个地之后，是因为我的笔记本有多张网卡，这个网卡才跟我的手机是在一个局域网的。
# 而需要sudo权限是因为，如果不sudo执行，那么没有声音。
```

加上--logfile stdout，这样就可以把很多信息打印出来。可以看收到的数据和发出的数据，调试很有用。



头文件：

```
output_gstreamer.h
	就声明了一个变量，extern struct output_module gstreamer_output;
output_module.h
	定义了一个结构体。struct output_module 
upnp_compat.h
	这个是为了兼容1.6版本和1.8版本的。
upnp_control.h
	声明了3个函数：都是upnp_control开头的。
	init
	get_service
	register_variable_listener。
upnp_renderer.h
	主要就是声明一个函数，返回了upnp_renderer_descriptor结构体指针。
upnp_transport.h
	跟upnp_control.h类型。声明了3个函数。都是upnp_transport开头。
	init
	get_service
	register_variable_listener
webserver.h
	声明了3个函数。都是webserver开头。
	register_callbacks
	register_buf
	register_file
	
xmlescape.h
	就声明了一个函数。xmlescape。
logging.h
	日志工具函数。
output.h
	各种播放器播放控制函数。
song-meta-data.h
	声明了结构体SongMetaData。
	4个函数，都是SongMetaData开头的。
	init
	clear
	to_DIDL
	parse_DIDL
upnp_connmgr.h
	声明了3个函数。
	upnp_connmgr_get_service。
	connmgr_init
	register_mime_type
	主要的对外接口就是connmgr_init。注册了支持的mime type。
upnp_device.h
	定义了结构体类型struct upnp_device_descriptor。
	9个函数。这些函数都是工具函数，需要掌握。
	upnp_get_string
		通过key获取value。
		这个用得最多。在这里面加打印。可以看出交互的信息过程。
	upnp_add_response
		回复的时候，添加内容到xml。
	upnp_append_variable
upnp_service.h
	全部是结构体定义。
variable-container.h
	都是函数声明。
xmldoc.h
	xml相关函数。
```



主函数流程：

```
main
	1、解析参数。
	2、创建upnp_renderer。
	3、output_init。
		创建gstreamer的pipeline。
	4、创建upnp_device，参数是upnp_renderer，ip地址，端口。
	5、upnp的transport和controller初始化。
		upnp_transport_init(device);
		upnp_control_init(device);
	6、output_loop
		这个就是g_main_loop_run。
```

上面涉及到4个概念：

render

device

transport

control



transport是一个service。

control也是一个service。

```
struct service transport_service_
struct service control_service_
```

另外还有一个connmgr，总共是3个服务。

```
service id："urn:upnp-org:serviceId:ConnectionManager"
service type："urn:schemas-upnp-org:service:ConnectionManager:1"
scpd_url：服务控制协议描述。"/upnp/renderconnmgrSCPD.xml"
control_url："/upnp/control/renderconnmgr1"
event_url："/upnp/event/renderconnmgr1"

actions有：
	获取协议信息
	获取当前连接id。
	获取当前连接信息。？还是设置？这里宏的名字是set，但是字符串是get，可能有错误。
	准备连接。
actions对应的参数有：
	获取协议信息的
		source 
		sink
	获取当前连接id
		ConnectionIDs
	设置当前连接信息
		ConnectionID
		RcsID
		AVTransportID
		ProtocolInfo
		PeerConnectionManager
		PeerConnectionID
		Direction
		Status
	准备连接
		RemoteProtocolInfo
		PeerConnectionManager
		PeerConnectionID
		Direction
		ConnectionID
		AVTransportID
		RcsID
		
```

Transport这个service的值：

```
service id："urn:upnp-org:serviceId:AVTransport"
service type："urn:schemas-upnp-org:service:AVTransport:1"
#define TRANSPORT_SCPD_URL "/upnp/rendertransportSCPD.xml"
#define TRANSPORT_CONTROL_URL "/upnp/control/rendertransport1"
#define TRANSPORT_EVENT_URL "/upnp/event/rendertransport1"

actions有：
	拿到当前传输。
	获取设备能力。
	获取媒体信息。
	设置avtransport的url
	设置下一个avtransport的url。
	获取传输信息。
	获取position。
	获取传输设置。
	stop
	play
	pause
	seek
```

control这个服务的：

```
service id："urn:upnp-org:serviceId:RenderingControl"
service type："urn:schemas-upnp-org:service:RenderingControl:1"
 #define CONTROL_SCPD_URL "/upnp/rendercontrolSCPD.xml"
 #define CONTROL_CONTROL_URL "/upnp/control/rendercontrol1"
 #define CONTROL_EVENT_URL "/upnp/event/rendercontrol1"

actions有：
	列出preset
	获取亮度
	获取对比度
	获取锐度。
	设置音量
```

有个关键基础结构叫variable_container。

```
output_gstreamer_init
	scan_mime_list
		scan_pad_templates_info
			scan_caps 这里扫描出来非常多。
				register_mime_type 
					形成一个单链表。
```



connection id固定为0的。



使用QQ音乐和酷狗来进行测试。

QQ音乐是自己修改的qplay协议，数据量要少一些。

而酷狗的，多一些数据。

qplay还是有一些优化的，控制反应更快一些。



# 使用mpd来做output_module

当前的项目里，需要结合单机和多机的情况。

所以gstreamer是不够的。

而且当前gstreamer跑起来问题不少，代码繁杂。

所以要替换为mpd的实现方式。

看了一下output_module结构体的构成。mpd完全可以对接上。

经过对接，现在可以用mpd进行播放了。

当前有的问题：

```
1、不能自动下一首。
	这个是因为我没有处理set_next_uri函数。
	看看可以怎样来处理。
2、播放完之后，就停止了，这个应该也是跟set_next_uri有关系。
	也不是一定的。有时候还是可以自动切换到下一首。
3、手机上更新时间比较慢。
	当前是2到3秒更新一下。
	另外进度时间还有点错乱。
4、系统里有大量的timed wait的端口。
5、seek操作不太对。
	拖到中间，显示133%这样的值。
```

这个6600，是mpd的默认端口。我当前是在本机播放，不要走tcp socket，而要走unix socket。

```
tcp        0      0 127.0.0.1:43560         127.0.0.1:6600          TIME_WAIT
tcp        0      0 127.0.0.1:43848         127.0.0.1:6600          TIME_WAIT
tcp        0      0 127.0.0.1:43342         127.0.0.1:6600          TIME_WAIT
tcp        0      0 127.0.0.1:43666         127.0.0.1:6600          TIME_WAIT
tcp        0      0 127.0.0.1:43832         127.0.0.1:6600          TIME_WAIT
```

看看怎么可以禁用6600 端口。

在mpd的代码目录下搜索bind_to_address

```
./doc/mpdconf.example:85:#bind_to_address               "~/.mpd/socket"
```

只需要把这一行注释掉：

```
# bind_to_address		"any"
```

就只会走unix socket了。

测试一下，发现mpd不正常了。

```
/ # mpc                       
mpd error: Connection refused 
```

看一下代码。发现不能注释掉socket的那一个。

现在出现这么多的timed wait，是不是因为mpd启动比较晚导致？

应该还是我频繁调用mpc命令导致的。这个应该是每次都建立socket连接，然后端口。

这个效率就真的很低了。那我还是必须自己实现mpc的。保持长连接。



mpd的很多socket的问题，已经通过自己实现mpc相关接口解决了。

现在gmrender跟手机之间也会产生大量这种socket。

```
tcp        0      0 192.168.0.102:49495     192.168.0.101:36832     TIME_WAIT
tcp        0      0 192.168.0.102:49495     192.168.0.101:36682     TIME_WAIT
tcp        0      0 192.168.0.102:49495     192.168.0.101:36504     TIME_WAIT
tcp        0      0 192.168.0.102:49495     192.168.0.101:36620     TIME_WAIT
tcp        0      0 192.168.0.102:49495     192.168.0.101:36594     TIME_WAIT
tcp        0      0 192.168.0.102:49495     192.168.0.101:36596     TIME_WAIT
```

这样来统计看看。没有持续增加，而是在慢慢减少。

```
netstat -ant |grep TIME_WAIT | wc -l
```



# 问题解决

## db值计算有问题

```
这个我自己用mixer接口来实现了音量的设置和获取。
```

## 不能自动连续播放下一首

直接原因是set_next_uri没有被调用。
手机上试了酷狗和QQ音乐都是一样。
但是我觉得应该不至于。

直接用未修改的gmrender，可以自动播放下一首。

虽然也不完全正常。手机这边歌曲显示不对，但是确实播放下一首了。

先在笔记本上用未修改的gmrender来调试看看。

也是不能自动切换下一首的。

这个需要我把协议仔细理解一下，看看能不能想办法实现。

## 板端按键调节音量没有自动同步给手机端



参考资料

1、

