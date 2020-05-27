---
title: Linux之inotify
date: 2018-05-06 22:14:36
tags:
	- Linux

---

1

Linux的桌面体验，比不上macos和windows。

为了提升Linux的桌面使用体验。开源社区对内核提出了需求，要求内核提供一些机制，让用户态可以及时了解到内核或者硬件发生了什么变化。

从而可以更好地管理设备，为用户提供更好的服务。

hotplug、udev、inotify这3种机制，就是在这个背景下诞生的。

其中，inotify是一种文件系统的变化通知机制，文件的变化，可以及时通知到用户态。

对应的头文件是`<sys/inotify.h>`。

```
IN_ACCESS：文件被访问
IN_MODIFY：文件被修改
IN_ATTRIB，文件属性被修改
```



里面主要是3个接口.

```
inotify_init
inotify_add_watch
inotify_rm_watch
```

## inotify_init

```
原型：
	int inotify_init(void);
返回值：
	一个fd。表示一个inotify实例。
```

一个inotify实例，对应了一个独立的排序的队列。

文件系统的变化，是一个watch事件。队列里放的就是这种watch事件。

一个watch事件，是一个二元组。包括：目标、mask。目标可以是目录和文件。

mask表示事件类型，例如创建、删除、修改等。

## inotify_add_watch

```
原型：
	int inotify_add_watch(int fd, const char *pathname, uint32_t mask);
参数1：
	fd。就是inotify_init得到的fd。
参数2：
	pathname。
参数3：
	x。
返回值：
	> 0表示成功，-1表示失败。具体错误码用errno来表示。
	返回值在rm的时候需要用到。
函数作用：
	1、添加或者修改。
```

一个fd，可以添加多个wd。

所以在你的应用进程里，只需要一个fd。然后根据需要add一些你关注的文件或者目录就好了。



## inotify_rm_watch

```
原型：
	int inotify_rm_watch(int fd, int wd);
参数1：
	fd。inotify_init的返回值。
参数2：
	wd：inotify_add_watch的返回值。
```



## inotify_event

```
struct inotify_event {
  s32 wd;//watch fd
  u32 mask;
  u32 cookie;
  u32 len;//表示name字段的长度。
  char name[0];//会4字节对齐。len也包括对齐增加的字节数在内。
};
```

name 为被监视目标的路径名，**该结构的 name 字段为一个桩，**它只是为了用户方面引用文件名，文件名是变长的，它实际紧跟在该结构的后面，文件名将被 0 填充以使下一个事件结构能够 4 字节对齐。注意，len 也把填充字节数统计在内。







## 操作

```
size_t len = read(fd, buf, BUF_LEN);
```

一次read，可以获得多个事件，只要提供的buf足够大。

```
#include <stdio.h>
#include <sys/inotify.h>

int main(int argc, char const *argv[])
{
    int fd = inotify_init();
    printf("fd:%d\n", fd);
    int wd = inotify_add_watch(fd, "./1.txt", IN_MODIFY);
    printf("wd:%d\n", wd);
    char buf[1024] = {0};
    printf("before read:\n");
    size_t len = read(fd, buf, 1023);
    printf("read len:%d, sizeof(inotify_event):%d\n", len, sizeof(struct inotify_event));
    struct inotify_event *event = (struct inotify_event *)buf;
    printf("event->wd:%d, event->mask:0x%x, event->cookie:%d, event->len:%d, event->name:%s\n",
        event->wd, event->mask, event->cookie, event->len, event->name);

    return 0;
}
```

运行：

```
fd:3
wd:1
before read:
read len:16, sizeof(inotify_event):16
event->wd:1, event->mask:0x2, event->cookie:0, event->len:0, event->name:
```

为什么name是空的呢？



# 问题

我使用inotify来监听mpd的/var/lib/mpd/state文件的变化。

但是发现只能检查到第一次的变化。这就奇怪了。

后面发现是因为state这个文件每次有变化是被删除重新创建的。

用stat查看。可以看到inode一直在变化。

这个inotify就没法解决了。







# 参考资料

1、Linux inotify详解

https://blog.csdn.net/breakout_alex/article/details/8902886

2、inotify 心得

https://www.cnblogs.com/mywebnumber/p/5826767.html