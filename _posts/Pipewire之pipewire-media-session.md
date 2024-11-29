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





