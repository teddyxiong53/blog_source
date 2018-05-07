---
title: Linux之inotify
date: 2018-05-06 22:14:36
tags:
	- Linux

---



inotify可以监测linux下的文件系统变化。

对应头文件是linux/inotify.h。

里面主要就是一个结构体inotify_event和几个宏。

```
struct inotify_event {
  s32 wd;//watch fd
  u32 mask;
  u32 cookie;
  u32 len;
  char name[0];
};
```

宏就是指定监控的行为，例如：

```
IN_ACCESS
IN_MODIFY这些。
```



示例程序：

```
#include <stdio.h>
#include <stdlib.h>

#include <linux/inotify.h>


int watch_inotify_events(int fd)
{
	int ret;
	char event_buf[512];
	struct inotify_event *event;
	int event_pos = 0;
	int event_size = 0;
	ret = read(fd, event_buf, sizeof(event_buf));
	while(ret >= sizeof(struct inotify_event)) {
		event = (struct inotify_event *)(event_buf + event_pos);
		if(event->len) {
			if(event->mask & IN_CREATE) {
				printf("create file:%s\n", event->name);
			} else if(event->mask & IN_DELETE) {
				printf("delete file:%s\n", event->name);
			}
		}
		event_size = sizeof(struct inotify_event) + event->len;
		ret -= event_size;
		event_pos += event_size;
	}
	return 0;
}


int main(int argc, char **argv)
{
	int fd;
	if(argc != 2) {
		printf("%s <dir> \n", argv[0]);
		return -1;
	}
	fd = inotify_init();
	if(fd == -1) {
		printf("init fail\n");
		return -1;
	}
	int ret;
	ret = inotify_add_watch(fd, argv[1], IN_CREATE | IN_DELETE);
	watch_inotify_events(fd);
	if(inotify_rm_watch(fd, ret) == -1) {
		printf("rm watch fail\n");
		return -1;
	}
	close(fd);
	return 0;
}

```

```
teddy@teddy-ubuntu:~/work/test/c-test$ ./a.out ./
create file:xx
```

