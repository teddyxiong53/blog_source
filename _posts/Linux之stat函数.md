---
title: Linux之stat函数
date: 2018-03-22 12:56:46
tags:
	- Linux

---



stat函数的使用。

```
#include <sys/types.h>
#include <sys/stat.h>
//#include <linux/time.h>

void main()
{
    struct stat stat1;
    stat("./test.c", &stat1);
    printf("dev:%d\n", stat1.st_dev);
    printf("mode:%o\n",stat1.st_mode);
    printf("nlink:%d\n", stat1.st_nlink);
    printf("uid:%d\n", stat1.st_uid);
    printf("gid:%d\n",stat1.st_gid);
    printf("rdev:%d\n",stat1.st_rdev);
    printf("blksize:%d\n",stat1.st_blksize);
    printf("blks:%d \n",stat1.st_blocks);
    printf("atime:%ul\n", stat1.st_atim.tv_sec);
    printf("mtime:%ul\n", stat1.st_mtim.tv_sec);
    printf("ctime:%ul\n", stat1.st_ctim.tv_sec);
    printf("ino:%d\n", stat1.st_ino);
    
}
```

```
/mnt/test # ./a.out 
dev:575028600  
mode:100766
nlink:1
uid:1000
gid:1000
rdev:0
blksize:1048576
blks:8 
atime:1521694549l
mtime:1521694542l
ctime:1521694542l
ino:1739307
```

