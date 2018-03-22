---
title: thttpd（二）
date: 2018-03-22 11:41:49
tags:
	- thttpd
typora-root-url: ..\
---



现在看一下代码。

我重点关注这几点：

阈值机制。

文件mmap机制。

发送缓冲区的处理。

定时处理。

fd的监听机制。

cgi的实现。

# 文件mmap

这个是为了提高文件访问的效率。

这个总共提供了5个接口。

1、mmc_map。

2、mmc_unmap。

3、mmc_cleanup。定时清理无效的。

4、mmc_term

5、mmc_logstats。

最重要的就是mmc_map。看懂了这个，其他的也就懂了。

```
mmc_map函数。
参数就是文件名，返回的是一个void *指针。
调用的地方，也就是一个。
就是curl http://192.168.0.2/index.html的时候。
把index.html这个文件跟一个指针关联起来。后面发送的时候，不用read，直接从指针处拷贝就好了。
看一下实现。
如果系统不支持mmap，是直接分配一块内存，把文件内容read进去的。
```

这里还使用了hash表来组织。

把所有的mmap串成一个单链表。

数据结构是：

```
typedef struct MapStruct {
    ino_t ino;
    dev_t dev;
    off_t size;
    time_t ct;
    int refcount;
    time_t reftime;
    void* addr;
    unsigned int hash;
    int hash_idx;
    struct MapStruct* next;
    } Map;
```

求的hash值，是用ino、dev、size、time这几个值求得的int数。

求出来的值，是0到1023之间，当前认为这个表的大小是1024 来讨论。

# 接收缓冲区

每个连接有自己的接收缓冲区。

所以放在http_conn结构体里。

除了buf指针，还有3个变量来辅助处理。

```
char* read_buf;
size_t read_size, read_idx, checked_idx;
```

相关的处理主要是在handle_read函数里。

```
1、httpd_get_conn 新建连接的时候，
	read_size为0，read_buf分配了600字节。
	read_idx和checked_idx都是0
2、handle_read里
	read_idx += read_size。
```

我的疑问是：read_idx一直是增加的，没有看到减少的地方。

应该要重复利用才对啊。

我连续两次访问。是一样的打印。

```
c:0x76dab008, read_index:0, read_size:600
c:0x76dab008, read_index:0, read_size:600
```

这就是所谓的http是无连接的服务了。

在handle_send里。

```
/* Are we done? */
    if ( c->next_byte_index >= c->end_byte_index )
	{
		printf("before finish_connection\n");
	/* This connection is finished! */
	finish_connection( c, tvP );
	return;
	}
```

每次正常发送都会调用这个。

我看里面的实现，是把tcp连接都断开了的。有必要吗？

确实是的。

如果受到的请求有一个keepalive选项，就不会断开的。

不过，为什么每次分配的连接的指针是一样的呢？

因为是全局的内存。不会清空的。



# 发送缓冲区

发送缓冲区的变量分布在2个结构体里。

一个connecttab。一个是http_conn。（我看了一下，接受缓冲区也用到了connecttab里的变量）

connecttab里有2个变量来管理。

```
    off_t end_byte_index;
    off_t next_byte_index;
```

http_conn里也有2个变量。

```
    off_t bytes_to_send;
    off_t bytes_sent;
```

另外，缓冲区的内容是mmap得到的一个地址。

```
char* file_address;
```



它们是如何进行配合工作的呢？

```
c:0x76d81008, read_index:0, read_size:600
xhl -- func:handle_read, line:1668 , c->next_byte_index:0,c->end_byte_index:311 
xhl -- func:handle_send, line:1790 ,hc->responselen:235
xhl -- func:handle_send, line:1814 ,c->next_byte_index:311, c->end_byte_index:311
xhl -- func:really_clear_connection, line:2047 
```

bytes_to_send是hc->sb.st_size,就是index.html的文件长度。

header的长度是235字节。内容的长度是311字节。

```
iv[0].len:235, iv[1].len:311
```



# io复用

nfiles:4096

接口：

1、fdwatch_get_nfiles(); 得到4096个nfiles。建立对应的表。

2、fdwatch_add_fd和fdwatch_del_fd。

3、fdwatch。

4、fdwatch_check_fd

5、fdwatch_get_next_client_data



fdwatch_add_fd

```
调用的地方：
1、fdwatch_add_fd( hs->listen4_fd, (void*) 0, FDW_READ );
	监听的listenfd。只读。
2、建立连接的时候，fdwatch_add_fd( c->hc->conn_fd, c, FDW_READ );只读。
3、解析完请求，在handle_read函数是最后面。
	fdwatch_del_fd( hc->conn_fd );
    fdwatch_add_fd( hc->conn_fd, c, FDW_WRITE );
    //从读里面删除，添加到写。
```

看实现：

```
1、调用ADD_FD宏。
	select_add_fd( fd, rw )
		FD_SET( fd, &master_rfdset )
		FD_SET( fd, &master_wfdset )
2、fd_rw里对应的表项，写入FDW_READ或者FDW_WRITE。
3、fd_data对应的表项，写入指针。例如connecttab
```

![thttpd（二）-图1](/images/thttpd（二）-图1.png)





# CGI实现

调用的入口是解析的时候，

```
/* Is it world-executable and in the CGI area? */
    if ( hc->hs->cgi_pattern != (char*) 0 &&
	 ( hc->sb.st_mode & S_IXOTH ) &&
	 match( hc->hs->cgi_pattern, hc->expnfilename ) )
	return cgi( hc );
```

cgi函数：

```
{
	r = fork();
	if (r == 0) {
      http_unlisten(hc->hs);
      cgi_child(hc);
      	继续fork。处理比较复杂，值得分析。
	}
	//parent process
	syslog( LOG_DEBUG, "spawned CGI process %d for file '%.200s'", r, hc->expnfilename );
}
```

我先弄一个helloworld程序进去看看。

1、在/var/www/html目录下，新建cgi-bin目录。

2、把printenv放进去。

3、重启，访问。

curl http://192.168.0.2/cgi-bin/printenv

```
    <h2>403 Forbidden</h2>
The requested URL '/cgi-bin/printenv' resolves to a file which is marked executable but is not a CGI file; retrieving it is forbidden.
    <hr>
```

把权限改成0766就好了。

