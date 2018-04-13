---
title: openwrt（十三）libubox
date: 2018-04-13 17:04:07
tags:
	- openwrt

---



libubox是openwrt的一个核心库。提供了一系列的基础功能。包括：

1、事件循环。

2、二进制格式处理。

3、链表实现。

4、json辅助。



代码下载地址在这：

```
git clone git://git.openwrt.org/project/libubox.git
```

总共52个文件。

```
teddy@teddy-ubuntu:~/work/ubus/libubox$ tree
.
├── avl.c
├── avl-cmp.c
├── avl-cmp.h
├── avl.h：自平衡二叉查找树。
├── base64.c
├── blob.c：生成和解析二级制数据。
├── blob.h
├── blobmsg.c
├── blobmsg.h
├── blobmsg_json.c
├── blobmsg_json.h
├── CMakeLists.txt
├── examples
│   ├── blobmsg-example.c
│   ├── CMakeLists.txt
│   ├── json_script-example.c
│   ├── json_script-example.json
│   ├── json_script-tests.sh
│   ├── runqueue-example.c
│   ├── shunit2
│   ├── uloop-example.lua
│   ├── uloop_pid_test.sh
│   └── ustream-example.c
├── jshn.c：json相关。
├── json_script.c
├── json_script.h
├── kvlist.c：键值对。
├── kvlist.h
├── list.h
├── lua
│   ├── CMakeLists.txt
│   └── uloop.c
├── md5.c
├── md5.h
├── runqueue.c：任务排队。
├── runqueue.h
├── safe_list.c
├── safe_list.h
├── sh
│   └── jshn.sh
├── ulog.c
├── ulog.h
├── uloop.c
├── uloop-epoll.c
├── uloop.h
├── uloop-kqueue.c
├── usock.c：对socket的封装，我感觉没有什么用。
├── usock.h
├── ustream.c
├── ustream-fd.c
├── ustream.h
├── utils.c
├── utils.h
├── vlist.c
└── vlist.h

3 directories, 52 files
```





# 参考资料

1、libubox

http://www.cnblogs.com/embedded-linux/p/6791544.html