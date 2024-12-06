---
title: Pipewire之pipewire-media-session
date: 2024-06-05 13:47:28
tags:
	- 音频
---



pipewire-media-session是之前pipewire的session管理工具。

现在被wireplumber取代了。

但是media-session这个看起来简单清晰一些。所以可以作为session管理的研究对象。

这里的代码前缀是sm，可以理解为session manage。

入口文件是src\media-session.c

# 主要结构体

```
struct sm_media_session

struct sm_object_events

struct sm_object_methods

struct sm_object

struct sm_param 

struct sm_client 

struct sm_device 

struct sm_node 
struct sm_port
struct sm_session

struct sm_endpoint

struct sm_endpoint_stream

struct sm_endpoint_link

struct sm_media_session_events 
struct sm_media_session 
```



```
sm_object
^
|
sm_session
^
|
sm_media_session
	
```

sm_object的主要属性

```
u32 id
char * type
	这2个好理解。
spa_list link
	所有的对象串起来。
sm_media_session *session
	指向全局对象。
pw_properties *props
	属性列表。
u64	serial
	对象的uuid？
pw_proxy *proxy
	跟pw通信的代理对象
spa_hook proxy_listener
	proxy状态变化监听器。
spa_hook object_listener
	对象变化监听器。
pw_destroy_t destroy
	销毁函数。
pw_proxy *handle
	这个也是一个pw_proxy指针，主要用途是什么？
spa_callbacks methods
	方法列表。
	
```



# src\media-session.c



# media-session怎么跟pw关联起来的

sm_device持有pw_device_info指针。

所有这种结构体都是类似这样做的。

sm_xx持有pw_xx_info指针。



