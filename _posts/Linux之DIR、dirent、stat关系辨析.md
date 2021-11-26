---
title: Linux之DIR、dirent、stat关系辨析
date: 2021-11-26 10:34:33
tags:
	- Linux

---

--

DIR、dirent都来自于dirent.h，我们以musl这个C库的来进行分析。

# DIR

```
struct __dirstream
{
	off_t tell;
	int fd;
	int buf_pos;
	int buf_end;
	volatile int lock[1];
	char buf[2048];
};

typedef struct __dirstream DIR;
```

DIR类似于FILE。是一个内部结构，给下面这些函数用来保存当前操作的目录的信息。

作为对照，FILE的结构体定义是这样，这个是给fopen等函数用的。

```
struct _iobuf {  
        char *_ptr;  
        int   _cnt;  
        char *_base;  
        int   _flag;  
        int   _file;  
        int   _charbuf;  
        int   _bufsiz;  
        char *_tmpfname;  
        };  
typedef struct _iobuf FILE;  
```

回到DIR。使用DIR的函数有这些：

```
DIR           *opendir(const char *);
int            closedir(DIR *);
struct dirent *readdir(DIR *);//这里开始涉及到dirent
int            readdir_r(DIR *__restrict, struct dirent *__restrict, struct dirent **__restrict);
long telldir(DIR *dp);   
void seekdir(DIR *dp,long loc);  
```

关于DIR结构，我们知道这么多就可以了，没必要去再去研究他的结构成员。



# dirent

从定义能够看出，dirent不仅仅指向目录，还指向目录中的具体文件，readdir函数同样也读取目录下的文件，这就是证据。

```
struct dirent {
	ino_t d_ino;
	off_t d_off;
	unsigned short d_reclen;
	unsigned char d_type;
	char d_name[256];
};
```

从上述定义也能够看出来，dirent结构体存储的关于文件的信息很少，

所以dirent同样也是起着一个索引的作用，

如果想获得类似ls -l那种效果的文件信息，必须要靠stat函数了。

通过readdir函数读取到的文件名存储在结构体dirent的d_name成员中，而函数

int stat(const char *file_name, struct stat *buf);

的作用就是获取文件名为d_name的文件的详细信息，存储在stat结构体中。



# 参考资料

1、

https://blog.csdn.net/zhuyi2654715/article/details/7605051

2、

https://blog.csdn.net/qq_36532097/article/details/72588206