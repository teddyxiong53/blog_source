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
sudo ./gmediarender -I 172.16.4.205
# 我之所以指定这个地之后，是因为我的笔记本有多张网卡，这个网卡才跟我的手机是在一个局域网的。
# 而需要sudo权限是因为，如果不sudo执行，那么没有声音。
```



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



参考资料

1、

