---
title: Linux之进程间通信fifo编程
date: 2020-05-21 16:23:35
tags:
	- Linux

---

1

现在使用mpd来做一个功能。

需要往snapcast的/tmp/snapfifo里写入录音数据。

直接arecord来写入可以，但是声音偏小。所以我希望自己来写，然后把pcm数据进行放大后再写入。

所以就涉及到fifo的写入操作。

mpd往/tmp/snapfifo也是进行写入操作。所以我可以模仿它的来写。

操作方法跟普通文件很像。

fifowriter.c

```

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>



int main(int argc, char *argv[])

{
	int fd;
	int ret;
	ret = mkfifo("my_fifo", 0666);//创建命名管道
	if(ret != 0)
	{
		perror("mkfifo");
	}

	printf("before open\n");
	fd = open("my_fifo", O_WRONLY); //等着只读
	if(fd < 0)
	{
		perror("open fifo");
	}
	printf("after open\n");
	printf("before write\n");

	// 5s后才往命名管道写数据，没数据前，读端read()阻塞
	sleep(5);
	char send[100] = "Hello Mike";
	write(fd, send, strlen(send));
	printf("write to my_fifo buf=%s\n", send);
	return 0;

}
```

fiforeader.c

```

#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>



int main(int argc, char *argv[])
{
	int fd;
	int ret;
	ret = mkfifo("my_fifo", 0666); //创建命名管道
	if(ret != 0)
	{
		perror("mkfifo");
	}
	printf("before open\n");
	fd = open("my_fifo", O_RDONLY);//等着只写
	if(fd < 0)
	{
		perror("open fifo");
	}
	printf("after open\n");
	printf("before read\n");
	char recv[100] = {0};
	//读数据，命名管道没数据时会阻塞，有数据时就取出来
	read(fd, recv, sizeof(recv));
	printf("read from my_fifo buf=[%s]\n", recv);
	return 0;

}
```



参考资料

1、

https://blog.csdn.net/qq_35433716/article/details/86175020