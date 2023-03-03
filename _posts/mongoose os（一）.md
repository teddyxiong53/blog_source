---
title: mongoose os（一）
date: 2018-02-10 17:37:37
tags:
	- mongoose

---



看rt-thread的代码，看到mongoose os这个东西。

官网介绍在这里。

https://cesanta.com/docs/overview/intro.html

1、mongoose是一个用C语言写的网络库。

2、算是一个嵌入式网络编程的瑞士军刀。

3、它实现了事件驱动的非阻塞API。

4、**基于它事件驱动实现了tcp/udp/mqtt/coap/websocket的server和client。**代码量并不大，实现了这么多完善的功能，实在是很强大。

5、已经支持了PicoTCP 和lwip协议栈。

6、方便集成，就一个mongoose.c和一个mongoose.h文件。

官网在这里：

https://mongoose.ws/

这里是官方教程。

https://mongoose.ws/tutorials/

代码在这里

https://github.com/cesanta/mongoose

# 看一下提交日志

把代码clone到本地，用tortoisegit查看提交的历史。

这个是从2010年开始的。从svn的仓库转换过来。

# 代码目录情况

Makefile会把src目录下分开的文件，最终合并成mongoose.c和mongoose.h这2个文件。

所以，修改代码是在src下面修改。

## Makefile的target

Makefile的target有这些：（make，然后tab进行补全得到）

```
all  这个是进入到examples/http-server目录下进行编译，编译得到的就是http-server的可执行文件。
armhf
fuzz
mg_prefix
mip_test
musl
test
upload-coverage
vc98
arduino
clean
fuzz2
mingw
mkfs
riscv
test/
valgrind
arduino-xiao
coverage
install
mingw++
mongoose.c
s390
unamalgamated
vc17
arm
examples
linux-libs
mip_tap_test
mongoose.h
tall
uninstall
vc22
```

armhf这个target是这样的内容：

```
armhf: ASAN=
armhf: IPV6=0
armhf: CC = $(DOCKER) mdashnet/armhf cc
armhf: RUN = $(DOCKER) mdashnet/armhf
armhf: test
```

这种写法怎么理解？

执行一下make armhf看看有什么打印。

起作用的还是`armhf: test`这个。上面的几行，我觉得应该就是相当于make的时候传递变量的作用。

而test是做了这些：

```
test: Makefile mongoose.h $(SRCS)
	$(CC) $(SRCS) $(CFLAGS) $(LDFLAGS) -o unit_test
	ASAN_OPTIONS=$(ASAN_OPTIONS) $(RUN) ./unit_test
```

就是编译生成unit_test文件。

依赖了mongoose.h头文件。

```
mongoose.h: $(HDRS) Makefile
	(cat src/license.h; echo; echo '#ifndef MONGOOSE_H'; echo '#define MONGOOSE_H'; echo; cat src/version.h ; echo; echo '#ifdef __cplusplus'; echo 'extern "C" {'; echo '#endif'; cat src/arch.h src/arch_*.h src/net_*.h src/config.h src/str.h src/queue.h src/fmt.h src/log.h src/timer.h src/fs.h src/util.h src/url.h src/iobuf.h src/base64.h src/md5.h src/sha1.h src/event.h src/net.h src/http.h src/ssi.h src/tls.h src/tls_mbed.h src/tls_openssl.h src/ws.h src/sntp.h src/mqtt.h src/dns.h src/json.h src/rpc.h src/tcpip/tcpip.h src/tcpip/driver_*.h | sed -e '/keep/! s,#include ".*,,' -e 's,^#pragma once,,'; echo; echo '#ifdef __cplusplus'; echo '}'; echo '#endif'; echo '#endif  // MONGOOSE_H')> $@
```

所以每次都是会重新生成mongoose.h头文件的。

```
src/license.h
	里面全部是license注册
src/version.h
	里面就一行#define MG_VERSION "7.9"
src/arch.h
	这个就是包含了arch的宏定义。同时包含了所有其他的arch_xx.h文件。
src/config.h
	这个就是mongoose的配置。
src/str.h
	定义了mg_str结构体和配套函数。
src/queue.h
	mg_queue结构体和配套函数。
src/fmt.h 
	各种printf函数。
src/log.h
	mg_log函数。
src/timer.h
	mg_timer结构体和函数。
src/fs.h 
	mg_fs结构体和函数。
src/util.h
	基础函数，例如hton等。
src/url.h
	url函数。
src/iobuf.h 
	mg_iobuf结构体和函数。
src/base64.h
	base64函数。

```

make all，看看效果。是编译后直接运行在8000端口上。

会把当前目录在网页列出来可以访问。

```
cc main.c mongoose.c        -W -Wall -Wextra -g -I.   -DMG_HTTP_DIRLIST_TIME_FMT="%Y/%m/%d %H:%M:%S" -DMG_ENABLE_LINES=1 -DMG_ENABLE_IPV6=1 -DMG_ENABLE_SSI=1  -o example                                    
./example       
```

mg_http_serve_dir 这个函数。



## config.h配置

```
MG_ENABLE_LOG 1
MG_ENABLE_TCPIP 0
MG_ENABLE_LWIP 0
MG_ENABLE_FREERTOS_TCP 0
MG_ENABLE_RL 0
	这个是arm mdk里的tcp协议栈。
MG_ENABLE_SOCKET !MG_ENABLE_TCPIP
MG_ENABLE_POLL 0
MG_ENABLE_EPOLL 0
MG_ENABLE_FATFS 0
MG_ENABLE_MBEDTLS 0
MG_ENABLE_OPENSSL 0
MG_ENABLE_CUSTOM_TLS 0
MG_ENABLE_SSI 0
MG_ENABLE_IPV6 0
MG_ENABLE_MD5 1
MG_ENABLE_WINSOCK 1
MG_ENABLE_CUSTOM_RANDOM 0
MG_ENABLE_CUSTOM_MILLIS 0
MG_ENABLE_PACKED_FS 0
MG_IO_SIZE 2048 
MG_MAX_RECV_SIZE (3 * 1024 * 1024)
MG_DATA_SIZE 32 
MG_MAX_HTTP_HEADERS 30
MG_HTTP_INDEX "index.html"
MG_PATH_MAX PATH_MAX
MG_SOCK_LISTEN_BACKLOG_SIZE 3
MG_ENABLE_FILE 1
MG_INVALID_SOCKET (-1)
MG_SOCKET_TYPE int
MG_SOCKET_ERRNO errno

```



# 技巧：通过宏运算来判断大小端

```
#define MG_BIG_ENDIAN (*(uint16_t *) "\0\xff" < 0x100)
```

来自于这里：

http://esr.ibiblio.org/?p=5095



# 一个http server的例子

我们通过这个例子来看mg的简单用法。

```
#include "mongoose.h"

static const char * s_http_port = "8888";

static void ev_handler(struct mg_connection *conn, int ev, void  *p)
{
	if(ev == MG_EV_HTTP_REQUEST)
	{
		struct http_message *hm = (struct http_message *)p;
		mg_send_head(conn, 200, hm->message.len, "Content-Type: text/plain");
		mg_printf(conn, "%.*s", (int)hm->message.len, hm->message.p);
	}
}
int main()
{
	struct mg_mgr mgr;
	struct mg_connection *conn;
	mg_mgr_init(&mgr, NULL);
	conn = mg_bind(&mgr, s_http_port, ev_handler);
	mg_set_protocol_http_websocket(conn);
	while(1)
	{
		mg_mgr_poll(&mgr, 100);
		
	}
	mg_mgr_free(&mgr);
	return 0;
}
```

用法还是很简单的。

