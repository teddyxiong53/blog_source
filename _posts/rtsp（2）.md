---
title: rtsp（2）
date: 2018-04-29 21:49:06
tags:
	- rtsp

---

1、从这里下载代码。是一个简单的rtsp服务器代码。

https://github.com/iskey/rtsp_rtp_server

2、编译，出错。提示：

```
gst/gst.h: No such file or directory
```

安装gstreamer相关。

```
sudo apt-get install libgstreamer0.10-dev gstreamer-tools gstreamer0.10-tools gstreamer0.10-doc
```

再编译。还是不行，我还是用源代码的方式编译安装gstreamer把。

这个源代码的方式，很麻烦，代码都是分散的。

```
No package 'gstreamer-interfaces-0.10' found
```

```
sudo apt-get install libgstreamer-plugins-base1.0-dev libgstreamer-plugins-good1.0-dev
```

```
pkg-config --libs gtk+-2.0
-lgtk-x11-2.0 -lgdk-x11-2.0 -lpangocairo-1.0 -latk-1.0 -lcairo -lgdk_pixbuf-2.0 -lgio-2.0 -lpangoft2-1.0 -lpango-1.0 -lgobject-2.0 -lglib-2.0 -lfontconfig -lfreetype
```

```
teddy@teddy-ubuntu:~/tools$ echo $PKG_CONFIG_PATH 
:/usr/local/lib/pkgconfig
```

还是继续看包安装的方式。

我再执行一下这个，就可以了。

```
sudo apt-get install libgstreamer-plugins-base0.10-dev
```

3、执行rtsp_server。

```
teddy@teddy-ubuntu:~/work/rtsp/rtsp_rtp_server$ ./rtsp_server 
^C

Closing main socket - closed
Starting killing workers ....................- killed
Killing threads - killed
Deleting session hash - deleted
Destroying mutex - destroyed
Finished
```

没有什么提示。怎么测试，还需要摸索一下。



# 代码分析

```
teddy@teddy-ubuntu:~/work/rtsp/rtsp_rtp_server$ tree
.
├── common.h
├── hashtable
│   ├── hashfunction.c
│   ├── hashfunction.h
│   ├── hashtable.c
│   └── hashtable.h
├── internal_rtp.h
├── internal_rtsp.h
├── Makefile
├── parse_rtp.c
├── parse_rtp.h
├── parse_rtsp.c
├── parse_rtsp.h
├── parse_sdp.c
├── parse_sdp.h
├── rtcp.c
├── rtcp.h
├── rtp_server.c
├── rtp_server.h
├── rtsp.c
├── rtsp.h
├── rtsp_server.c
├── rtsp_server.h
├── server.c
├── server_client.c
├── server_client.h
├── server.h
├── servers_comm.h
├── socketlib
│   ├── socketlib.c
│   └── socketlib.h
├── strnstr.c
├── strnstr.h
├── test_parse_rtp.c
├── test_parse_rtsp.c
├── test_parse_sdp.c
└── test_rtsp.c
```



test_rtsp.c相当于一个单元测试，构造一下url，传递进行处理，再比较预期结果与实际结果。



