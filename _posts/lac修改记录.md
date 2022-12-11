# lac

lac是我自己的一个开源项目。本文是对应的修改记录。



# cjson

这个不用写，但是以编译这个为入口，把autotools的编译链接过程走通。

现在可以编译通过。但是生成的只有la结尾的文件。没有看到a或者so文件。

# tinyparam

C语言切分字符串

https://blog.csdn.net/SweeNeil/article/details/84787945

```
char *strtok_r(char *str, const char *delim, char **saveptr);
```

这个才是线程安全的。

测试代码：

```
#include <stdio.h>
#include <string.h>

int main()
{
    char str[] = "system.audio.volume";
    char* ptr;
    char* p;
    printf("before strtok:  str=%s\n", str);
    printf("begin:\n");
    ptr = strtok_r(str, ".", &p);
    while (ptr != NULL) {
        printf("str=%s\n", str);
        printf("ptr=%s\n", ptr);
        ptr = strtok_r(NULL, ".", &p);
    }
    return 0;
}
```

这样打印出来是：

```
before strtok:  str=system.audio.volume
begin:
str=system
ptr=system
str=system
ptr=audio
str=system
ptr=volume
```

那我以ptr的作为取值对象。

代码这样：

```
#include <stdio.h>
#include <string.h>

int main()
{
    char str[] = "system.audio.volume";
    char* ptr;
    char* p;
    printf("before strtok:  str=%s\n", str);
    ptr = strtok_r(str, ".", &p);
    while (ptr != NULL) {
        printf("ptr=%s\n", ptr);
        ptr = strtok_r(NULL, ".", &p);
    }
    return 0;
}
```

写入的时候，进行truncate操作。前面会有一堆的NUL。

需要rewind一下。

现在tinyparam功能完成了。

# tinyev

接下来是实现tinyev。

这个就比较麻烦一点。需要先研究一下libev的内容。

我就用3个文件：ev.c、ev.h、ev_epoll.c。

看了一下代码风格，真的是非常别扭。但是回头看了一下libtuv。这个文件就是比较多。

相比之下，还是libev代码量算是少的。

我先保证可以把这个例子编译运行起来。

```
#include <ev.h>
#include <stdio.h>
#include <signal.h>
#include <sys/unistd.h>

ev_io io_w;
ev_timer timer_w;
ev_signal signal_w;

void io_action(struct ev_loop *main_loop, ev_io *io_w, int e)
{
    int ret;
    char buf[1024] = {0};
    puts("in io cb\n");
    read(STDIN_FILENO, buf, sizeof(buf));
    buf[1023] = '\0';
    printf("read a string:%s\n", buf);
    ev_io_stop(main_loop, io_w);
}
void timer_action(struct ev_loop *main_loop, ev_timer *timer_w, int e)
{
    puts("in timer cb\n");
    ev_timer_stop(main_loop, timer_w);
}
void signal_action(struct ev_loop *main_loop, ev_signal *signal_w, int e)
{
    puts("in signal cb\n");
    ev_signal_stop(main_loop, signal_w);
    ev_break(main_loop, EVBREAK_ALL);
}

int main(int argc, char const *argv[])
{
    struct ev_loop *main_loop = ev_default_loop(0);
    ev_init(&io_w, io_action);
    ev_io_set(&io_w, STDIN_FILENO, EV_READ);
    ev_init(&timer_w, timer_action);
    ev_timer_set(&timer_w, 2,0);
    ev_init(&signal_w, signal_action);
    ev_signal_set(&signal_w, SIGINT);

    ev_io_start(main_loop, &io_w);
    ev_timer_start(main_loop, &timer_w);
    ev_signal_start(main_loop, &signal_w);
    ev_run(main_loop, 0);
    return 0;
}
```

ev_default_loop实现

EV_USE_REALTIME 这个功能我不用。

我只用EV_USE_MONOTONIC

写了几个函数后，感觉思路清晰一些了。

```
#define NUMPRI (EV_MAXPRI - EV_MINPRI + 1)
```

这个优先级我不用。所以NUMPRI为1.

```
实现ev_init
	这个必须实现为宏。
	因为传递进来的类型是多种。只能用宏来模拟c++的模板。
	
```

# jsonrpc

想明白了jsonrpc的通知怎么做了，

进程A作为server，内部同时运行jsonrpc server1和连接自己的client代码，

进程B作为纯的client。

当进程A有状态需要通知时，A内部的client向自己的server发通知，这个信息就会被server转给所有的client.

这样就实现了进程A主动给进程B发送通知的机制。

有了这个，jsonrpc就可以替代dbus的功能来实现进程通信了。

代码规划：

```
jsonrpc_server.c
	里面的对外接口：jrpc_server作为前缀
jsonrpc_client.c
	里面的对外接口，jrpc_client作为前缀。
	
无论server还是client，都以libev作为通信基础。
json库使用cjson。

至于消息的内容，需要后续编写过程中进行优化整理。

```

server端参考jsonrpc-c。

client端我刚无意中发现opensips里有一个实现，代码也很简练。可以参考一下。

我不太在意rpc的传递计算功能。

我只希望传递一个json命令过去。

所以在命令的制定上，我要再看一下snapcast里的做法。

从example切入。

先实现jrpc_server_init函数和jrpc_server结构体。

一个jrpc_server，应该有哪些属性呢？

```
作为server，应该有：
	port。
	一个evloop指针。
	一个ev_io来监听listen_watcher，监听连接。
	一个注册表，注册自己可以处理的所有命令。
		注册的命令用一个jrpc_procedure来表示。
		jrpc_procedure就一个name，一个函数，一个void *data。
		这个回调函数，需要一个jrpc_context。这个context包含了void *data，另外包含了错误信息。
		
```

作为一个server，还有有一个结构体来表示connection。

```
jrpc_connection
	一个connection，是一个io，所以有一个ev_io。
	对应了一个fd。
	有一个buffer来存放收到的消息。buffer配套了2个参数：pos和size。
```

主要的结构体都有了。

现在可以开始看jrpc_server_init做了什么。

server里只有一个ev_loop，用的是默认的。

那么如果要创建多个server实例，会怎么样呢？

应该也没事。

而且还提供了一个jrpc_server_init_with_ev_loop版本让你自己另外传递loop进去。

jrpc_server_init只是一个常用的简单版本而已。

因为每个server都有个ev_loop指针。

发现我用的cjson没有cJSON_Parse_Stream这个函数。

直接把这个函数的实现拷贝过来。不改版本。

jsonrpc_server实现了。整个流程还是非常清晰直观的。都是同步的行为。



今天出现很奇怪的现象，昨天我在另外一台电脑上完全正常的测试程序。

现在换了一台电脑编译运行，就不对了。

问题是ev_default_loop得到的是空指针。

为什么会这样？

if (ev_backend (EV_A)) 这个条件不满足了。

我知道了。因为我gitignore把config.h给忽略了。

而我目前是让libev里直接放了config.h。所以当前就缺失这个文件了。

加上config.h重新编译就好了。

现在测试接收json字符串。结果不对。

怎么收到的数据解析处理不对呢？

```
root->type:3
```

会不会是cjson解析这一步的不对呢？

我直接替换cjson的文件看看。

的确是的。

cjson代码里没有没有版本号呢？

这样很不便于版本管理啊。

现在是提示参数错误。

```
{"id":1,"jsonrpc":"2.0","method":"sayHello"}
{
        "error":        {
                "code": -32600,
                "message":      "request is invalid"
        }
}
```

按道理不应该。

参数是可以不带的吧。

应该是我处理上有不对的地方。

是我判断的条件不对。改了就好了。

现在有个问题，就是只要有一次发送错了json。那么后面解析都不对了。

测试一下jsonrpc-c的。发现这个在解析出错后，client就退出了。

我是没有退出的。

我把jsonrpc-c也改成不退出的看看。

碰到一次错误解析后，之后还是正常的。

那就是我的代码还有问题。

从connection_cb开始看。

目前测试简单的几个字符发送。不会触发解析。我觉得这个符合预期。

但是随便发了几个字符，再发一个正常的json。

后面就一直错误无法恢复了。

当前对buffer这一块的处理，不是很直观。

需要把jsonrpc-c的调试一下。

也是一样的问题。

这个时候的buffer内容是这样。

```
fdfdf
{"id":1,"jsonrpc":"2.0","method":"sayHello"}
{"id":1,"jsonrpc":"2.0","method":"sayHello"}
```

需要在出错的时候，把buffer整个复位一下。

现在把server的destroy的逻辑写一下。

写好了。

现在开始写client端。

看看怎么用libev写tcp client。

这个例子可以参考。

https://github.com/coolaj86/libev-examples/blob/master/src/unix-echo-client.c



关键是搞清楚什么时候需要外往发送。

简单点，可以用一个event_handler来做一个event来触发。

但是我当前是首选的libev的方式。

我看的这个例子。是以stdin读取一行数据为触发条件。

逻辑是这样：

```
stdin收到一行数据。
把sockfd对应的watcher先进行ev_io_stop
然后设置
ev_io_set(&wather, sockfd, EV_READ|EV_WRITE)
然后
ev_io_start(loop, &watcher)

这样就会马上触发可写事件。
然后在send_cb里，真正send之后，马上要去掉对EV_WRITE的关注。
（必须要去掉，不然这个事件会一直触发的）。
ev_io_stop(loop, &watcher);
ev_io_set(&watcher, sockfd, EV_READ);
ev_io_start(loop, &watcher);

这个逻辑还是清晰的。
```

搞清楚这个。就可以开始设计我的逻辑。

```
我需要在什么时候，开始关注sockfd的EV_WRITE事件？
在jrpc_client_send_cmd里，把内容解析成字符串，填入到send_buf里之后，就可以用关注EV_WRITE的方式来触发调用到send_cb函数。

send_cb的可读事件，就是在收到server发来的数据之后。
可以在这里处理执行的命令的返回值。
需要根据返回值来决定是不是要重新发送命令。

接收消息还可能来自于server的主动通知。

可能出现这种情况：
server的主动通知跟自己发送命令的返回值同时被收到。这样就可能导致解析出问题吧。
但是这个现在不管。后面在仔细考虑这个场景。
我觉得关键是要server端进行序列化操作。
排队处理。

```

现在总的逻辑理清楚了。可以开始写这部分逻辑了。

现在connect失败。

```
connect fail: Operation now in progress
```

这个是要把设置非阻塞放在connect之后。

现在的问题是，trigger之后，没有触发EV_WRITE。

那这个是不是跟epoll的设置有关系？

我直接拿这个例子来测试看看。

https://github.com/coolaj86/libev-examples/blob/master/src/unix-echo-client.c

这个需要server和client配套一起跑。

这个运行是正常的。说明libev和epoll没有问题。

那关键应该还是ev_io的设置问题。

需要梳理一下例子的逻辑：

```
remote_w
send_w
	这2个分别代表了什么？关系是什么？
	remote_w实际上用来表示connect的状态。
	connect成功后，就没有作用了。
	remote_W一上来就是关注它的EV_WRITE。如果可以write了。说明连接已经成功。
	
	send_w。就是socket的发送和接收用途。
	默认只关注EV_READ。
```

我暂时换一种方式来做这个发送的触发条件。

如果用pthread_cond。那还不如用eventfd来做触发。

刚好还可以跟libev结合起来。

但是eventfd是ev_async这个。所以我发现我对libev的用法还是没有完全掌握。

所以先不用这个机制。

我先解决我当前的问题。

notification怎么发送呢？

我自己加server的这个行为，就借用jsonrpc的消息格式和tcp的连接。

其实发的内容跟jsonrpc已经没有关系了。



测试用例用这么几条。

```
{"id":1,"jsonrpc":"2.0","method":"sayHello"}
{"method": "add", "params": [1,2], "id":1}
```

我现在的server应该不管有没有id，都进行了回复的吧。

看看jsonrpc的规格书标准是怎么说的。

通知不允许被回复。

好像当前没有处理批量调用的情况吧。

测试一下看看能不能处理。

不能，因为只处理了object的类型。

其实要处理也可以。但是我先不支持吧。必要性不大。上层自己做一个for循环发送一下不就可以了吗？

测试一下多个client连接的情况。

我目前写的是限制了3个client。为什么连了4个也连上了呢？

我的代码写得有问题。改好了。

# mqtt

纯C语言实现一个mqtt client。

基于libev来做。

用libemqtt。

我看我之前用的是paho mqtt的。



# tinythpool

一个基于pthread的线程池。

这里有一个。就基于这个来改吧。

https://github.com/Pithikos/C-Thread-Pool

# file和string、time的util

怎么怎么放呢？如何命名呢？

要简单，但是也要有识别度，不要跟其他的库的命名冲突了。

就叫：

```
file_util_xx
str_util_xx
time_util_xx
misc_util_xx
```

啰嗦了点，但是可以保证唯一性。

写起来也比较顺手。

至于提取哪些函数放进来。还没有想好，先占个坑位吧。

# app

最后可以写一个app。是一个大的顶层结构体，把所有的其他库，都统一管理起来。

可以从avs sdk里找一些代码，写对应的C语言版本。

模仿实现一下bgservice和uiapp先。

```
bgservice
	jrpc_server *server
		注册处理命令
	tp_open 参数读写
	event_handler
		处理一下事件。
	tinythpool
	tinyutils
	http_client
	stream_player
	
uiapp
	jrpc_client
		也要注册一些处理函数，用来处理收到的通知。
		连接到server。
	显示
```

只有一个比较贴近真实场景的应用，才能驱动相关功能的完善。



# http工具库

基于libcurl进行封装。

# event_handler

这个还是需要的。跟线程池还是不一样。侧重点不一样。

能不能用libev来实现呢？

不是很合适。

跟线程池也不是完全重合。这个还是比较关注事件本身的。

线程池就是扔出去就不管了。

这个相当于给每个模块可以自己用于一个单独的事件处理线程。



# 增加模块

```
网络相关
	http client：基于libcurl。
	http server：基于libev
	websocket 客户端
audio媒体相关
	tinyalsa
	wav解码
	mp3解码
	stream_player：基于ffmpeg
脚本语言
	嵌入lua解释器。
	嵌入micropython解释器。
数据库
	基于sqlite封装一个简单的接口。
	
```

# 代码风格

```
风格一：
struct xx_server *server =  xx_server_create();
server->run(server)

风格二：
struct xx_server *server =  xx_server_create();
xx_server_run(server);
```

风格一看起来更加面向对象。

到底哪种好一些呢？

还是选择风格二吧。

风格一的代码找函数实现更加麻烦一点。不那么直观。

风格一也不是大多数C语言的风格。

# 调试方法

当前因为生成的库都没有install到指定目录。

所以默认是用libtool的包装脚本来运行程序。

例如app/bgservice就是一个脚本。真正的二进制文件是在app/.libs/bgservice。

如果需要gdb、valgrind的时候，就需要直接使用二进制的版本。

直接运行二进制版本会找不到库。

需要这样指定库的路径。

```
export LD_LIBRARY_PATH=~/work/test/linux-app-component/jsonrpc/.libs:\
~/work/test/linux-app-component/cjson/.libs:\
~/work/test/linux-app-component/libev/.libs:\
~/work/test/linux-app-component/tinyparam/.libs
```



# 问题解决

## 一个错误的json导致jrpc_server挂掉

```
{"id":1, "methods":"version"}
```

这个测试把method错误写错了methods。会导致jrpc-server crash掉。

是因为下面判断method的括号写错了。

改了就好了。

## bgservice内存泄漏

现在bgservice的exit逻辑已经有了。

顺便用valgrind测试一下bgservice是否有内存泄漏。

还真有问题。

```
==35319== HEAP SUMMARY:
==35319==     in use at exit: 2,508 bytes in 6 blocks
==35319==   total heap usage: 84 allocs, 80 frees, 10,235 bytes allocated
==35319== 
==35319== LEAK SUMMARY:
==35319==    definitely lost: 0 bytes in 0 blocks
==35319==    indirectly lost: 0 bytes in 0 blocks
==35319==      possibly lost: 0 bytes in 0 blocks
==35319==    still reachable: 2,508 bytes in 6 blocks
==35319==         suppressed: 0 bytes in 0 blocks
```

有4个block没有释放。

我是这样启动：

```
valgrind --leak-check=full ./bgservice
```

然后用nc localhost 1234连上来。发送一个

```
{"id":1, "method":"version"}
{"id":1, "method":"exit"}
```

然后bgservice就自动退出了。

这样才能进行检查。

看看生成的报告。

```
==35319== Invalid free() / delete / delete[] / realloc()
==35319==    at 0x483CA3F: free (in /usr/lib/x86_64-linux-gnu/valgrind/vgpreload_memcheck-amd64-linux.so)
==35319==    by 0x484DA10: jrpc_procedure_destroy (jsonrpc_server.c:423)
==35319==    by 0x484DA10: jrpc_server_destroy (jsonrpc_server.c:436)
==35319==    by 0x1096C9: bgservice_destroy (bgservice.c:95)
==35319==    by 0x10928F: main (main.c:11)
```

我觉得之前这个

jrpc_server_register_procedure的逻辑并不直观。

我还是改成我比较习惯的逻辑。

因为我现在需要jrp_client也处理server发过来的消息，所以其实client也需要有一个procedure。

所以把jrpc_procedure单独提取出来。

就叫jrpc_procedure.c文件。

提供这些接口：

```
jrpc_procedure_create
jrpc_procedure_destroy
```

调整了一些参数的前后顺序，变得更加合理。

### 调试内存泄漏问题

一个shell窗口执行：

```
cd ~/work/test/linux-app-component/test/.libs

export LD_LIBRARY_PATH=~/work/test/linux-app-component/jsonrpc/.libs:\
~/work/test/linux-app-component/cjson/.libs:\
~/work/test/linux-app-component/libev/.libs:\
~/work/test/linux-app-component/tinyparam/.libs

valgrind --leak-check=full ./test-jsonrpc-server
```

另外一个shell窗口执行：

```
# 直接用nc来测试
nc localhost 1234
# 然后输入：这个命令是直接让server退出。server必须正常退出，才能打印valgrind的检测结果。
{"id":1, "method":"exit"}
```

看报告内容，我的broadcast_send函数有泄漏的。

看看。

这个是在test-jsonrpc-server.c里。

这个线程没有退出机制。

先去掉这发送广播的。

再测试一下。

这次的就比较隐蔽了。

需要加参数来查看：

```
valgrind  --leak-check=full --show-leak-kinds=all ./test-jsonrpc-server
```

还有这么多内存泄漏：

```
still reachable: 2,508 bytes in 6 blocks
```

现在都是显示在ev_run这个调用栈里面。

libev有销毁机制吗？

没有看到。这个先不管。不是运行中持续增加的那种情况。

# 重新调整readme

模块要进行分类。可以分为哪些大类：

```
基础库
网络库
多媒体库
脚本语言库

```

# toybox

就用0.8.8的这个最新的release版本。

https://github.com/landley/toybox/releases/tag/0.8.8

先下载下来编译运行一下看看。

# 以snapcast驱动组件的补全

单独写组件动力不足，还是以snapcast的编写为驱动力来补全需要的模块。

## 双向链表

首先就是需要一个双向链表。

我记得rtt里有一个。找过来看看。是在rtservice.h里。

不要太复杂。先只加常用功能。

```
init
insert
remove
find
```

rtservice.h里list有的功能：

```
init
insert_after
insert_before
remove
isempty
len
entry
foreach
```

好吧。那还是用rtservice这个，比较这个经过考验了。

我的双向链表的名字就叫dl_list吧。dl是double link

这个实现了。

现在看看queue是否需要实现。

不需要，这个就是队列。

# libevent

在思考eventloop和线程的关系的时候，网上找了一些资料，是基于libevent进行分析的。

然后看了一下libevent的代码，发现内置了websocket和http支持。

那这个岂不是更加适合我的需求？

可以把我需要的代码提取出来编译一个库进行测试看看。

我 选择最新的2.1.12版本。

configure.ac是写得挺长的。

编译时只涉及这些文件：

```
  GEN      include/event2/event-config.h
  CC       buffer.lo
  CC       bufferevent.lo
  CC       bufferevent_filter.lo
  CC       bufferevent_pair.lo
  CC       bufferevent_ratelim.lo
  CC       bufferevent_sock.lo
  CC       event.lo
  CC       evmap.lo
  CC       evthread.lo
  CC       evutil.lo
  CC       evutil_rand.lo
  CC       evutil_time.lo
  CC       listener.lo
  CC       log.lo
  CC       strlcpy.lo
  CC       select.lo
  CC       poll.lo
  CC       epoll.lo
  CC       signal.lo
  CC       evdns.lo
  CC       event_tagging.lo
  CC       evrpc.lo
  CC       http.lo
```

把这些文件提取出来。加上include目录。

加入编译系统。测试代码验证正常。提交了。

# micropython

看看怎么加入micropython的。

最新的是1.19的。

只能通过git clone的方式来取，因为有些模块是通过git module的方式包含进来的。

编译standard版本是会失败。

我编译minimal版本。

在ports/unix/Makefile里，把VARIANT=minimal

编译了这些内容：

```

teddy@teddy-VirtualBox:~/work/test/micropython/ports/unix$ make
Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
mkdir -p build-minimal/genhdr
GEN build-minimal/genhdr/mpversion.h
GEN build-minimal/genhdr/qstr.i.last
GEN build-minimal/genhdr/qstr.split
GEN build-minimal/genhdr/qstrdefs.collected.h
QSTR updated
GEN build-minimal/genhdr/qstrdefs.generated.h
GEN build-minimal/genhdr/moduledefs.split
GEN build-minimal/genhdr/moduledefs.collected
Module registrations updated
GEN build-minimal/genhdr/moduledefs.h
GEN build-minimal/genhdr/root_pointers.split
GEN build-minimal/genhdr/root_pointers.collected
Root pointer registrations updated
GEN build-minimal/genhdr/root_pointers.h
GEN build-minimal/genhdr/compressed.split
GEN build-minimal/genhdr/compressed.collected
Compressed data updated
GEN build-minimal/genhdr/compressed.data.h
mkdir -p build-minimal/extmod/
mkdir -p build-minimal/py/
mkdir -p build-minimal/shared/libc/
mkdir -p build-minimal/shared/runtime/
mkdir -p build-minimal/shared/timeutils/
CC ../../py/mpstate.c
CC ../../py/nlr.c
CC ../../py/nlrx86.c
CC ../../py/nlrx64.c
CC ../../py/nlrthumb.c
CC ../../py/nlraarch64.c
CC ../../py/nlrpowerpc.c
CC ../../py/nlrxtensa.c
CC ../../py/nlrsetjmp.c
CC ../../py/malloc.c
CC ../../py/gc.c
CC ../../py/pystack.c
CC ../../py/qstr.c
CC ../../py/vstr.c
CC ../../py/mpprint.c
CC ../../py/unicode.c
CC ../../py/mpz.c
CC ../../py/reader.c
CC ../../py/lexer.c
CC ../../py/parse.c
CC ../../py/scope.c
CC ../../py/compile.c
CC ../../py/emitcommon.c
CC ../../py/emitbc.c
CC ../../py/asmbase.c
CC ../../py/asmx64.c
CC ../../py/emitnx64.c
CC ../../py/asmx86.c
CC ../../py/emitnx86.c
CC ../../py/asmthumb.c
CC ../../py/emitnthumb.c
CC ../../py/emitinlinethumb.c
CC ../../py/asmarm.c
CC ../../py/emitnarm.c
CC ../../py/asmxtensa.c
CC ../../py/emitnxtensa.c
CC ../../py/emitinlinextensa.c
CC ../../py/emitnxtensawin.c
CC ../../py/formatfloat.c
CC ../../py/parsenumbase.c
CC ../../py/parsenum.c
CC ../../py/emitglue.c
CC ../../py/persistentcode.c
CC ../../py/runtime.c
CC ../../py/runtime_utils.c
CC ../../py/scheduler.c
CC ../../py/nativeglue.c
CC ../../py/pairheap.c
CC ../../py/ringbuf.c
CC ../../py/stackctrl.c
CC ../../py/argcheck.c
CC ../../py/warning.c
CC ../../py/profile.c
CC ../../py/map.c
CC ../../py/obj.c
CC ../../py/objarray.c
CC ../../py/objattrtuple.c
CC ../../py/objbool.c
CC ../../py/objboundmeth.c
CC ../../py/objcell.c
CC ../../py/objclosure.c
CC ../../py/objcomplex.c
CC ../../py/objdeque.c
CC ../../py/objdict.c
CC ../../py/objenumerate.c
CC ../../py/objexcept.c
CC ../../py/objfilter.c
CC ../../py/objfloat.c
CC ../../py/objfun.c
CC ../../py/objgenerator.c
CC ../../py/objgetitemiter.c
CC ../../py/objint.c
CC ../../py/objint_longlong.c
CC ../../py/objint_mpz.c
CC ../../py/objlist.c
CC ../../py/objmap.c
CC ../../py/objmodule.c
CC ../../py/objobject.c
CC ../../py/objpolyiter.c
CC ../../py/objproperty.c
CC ../../py/objnone.c
CC ../../py/objnamedtuple.c
CC ../../py/objrange.c
CC ../../py/objreversed.c
CC ../../py/objset.c
CC ../../py/objsingleton.c
CC ../../py/objslice.c
CC ../../py/objstr.c
CC ../../py/objstrunicode.c
CC ../../py/objstringio.c
CC ../../py/objtuple.c
CC ../../py/objtype.c
CC ../../py/objzip.c
CC ../../py/opmethods.c
CC ../../py/sequence.c
CC ../../py/stream.c
CC ../../py/binary.c
CC ../../py/builtinimport.c
CC ../../py/builtinevex.c
CC ../../py/builtinhelp.c
CC ../../py/modarray.c
CC ../../py/modbuiltins.c
CC ../../py/modcollections.c
CC ../../py/modgc.c
CC ../../py/modio.c
CC ../../py/modmath.c
CC ../../py/modcmath.c
CC ../../py/modmicropython.c
CC ../../py/modstruct.c
CC ../../py/modsys.c
CC ../../py/moduerrno.c
CC ../../py/modthread.c
CC ../../py/vm.c
CC ../../py/bc.c
CC ../../py/showbc.c
CC ../../py/repl.c
CC ../../py/smallint.c
CC ../../py/frozenmod.c
CC ../../extmod/machine_bitstream.c
CC ../../extmod/machine_i2c.c
CC ../../extmod/machine_mem.c
CC ../../extmod/machine_pinbase.c
CC ../../extmod/machine_pulse.c
CC ../../extmod/machine_pwm.c
CC ../../extmod/machine_signal.c
CC ../../extmod/machine_spi.c
CC ../../extmod/modbluetooth.c
CC ../../extmod/modbtree.c
CC ../../extmod/modframebuf.c
CC ../../extmod/modlwip.c
CC ../../extmod/modnetwork.c
CC ../../extmod/modonewire.c
CC ../../extmod/moduasyncio.c
CC ../../extmod/modubinascii.c
CC ../../extmod/moducryptolib.c
CC ../../extmod/moductypes.c
CC ../../extmod/moduhashlib.c
CC ../../extmod/moduheapq.c
CC ../../extmod/modujson.c
CC ../../extmod/moduos.c
CC ../../extmod/moduplatform.c
CC ../../extmod/modurandom.c
CC ../../extmod/modure.c
CC ../../extmod/moduselect.c
CC ../../extmod/modusocket.c
CC ../../extmod/modussl_axtls.c
CC ../../extmod/modussl_mbedtls.c
CC ../../extmod/modutimeq.c
CC ../../extmod/moduwebsocket.c
CC ../../extmod/moduzlib.c
CC ../../extmod/modwebrepl.c
CC ../../extmod/network_cyw43.c
CC ../../extmod/network_ninaw10.c
CC ../../extmod/network_wiznet5k.c
CC ../../extmod/uos_dupterm.c
CC ../../extmod/utime_mphal.c
CC ../../extmod/vfs.c
CC ../../extmod/vfs_blockdev.c
CC ../../extmod/vfs_fat.c
CC ../../extmod/vfs_fat_diskio.c
CC ../../extmod/vfs_fat_file.c
CC ../../extmod/vfs_lfs.c
CC ../../extmod/vfs_posix.c
CC ../../extmod/vfs_posix_file.c
CC ../../extmod/vfs_reader.c
CC ../../extmod/virtpin.c
CC ../../shared/libc/abort_.c
CC ../../shared/libc/printf.c
CC main.c
CC gccollect.c
CC unix_mphal.c
CC mpthreadport.c
CC input.c
CC modmachine.c
CC modtime.c
CC moduselect.c
CC alloc.c
CC fatfs_port.c
CC mpbthciport.c
CC mpbtstackport_common.c
CC mpbtstackport_h4.c
CC mpbtstackport_usb.c
CC mpnimbleport.c
CC modtermios.c
CC modusocket.c
CC modffi.c
CC modjni.c
CC ../../shared/runtime/gchelper_generic.c
CC ../../shared/timeutils/timeutils.c
LINK build-minimal/micropython
   text    data     bss     dec     hex filename
 176848   14984    5328  197160   30228 build-minimal/micropython
teddy@teddy-VirtualBox:~/work/test/micropython/ports/unix$ 
```

尝试编译standard版本。

但是出错。必须在linux下clone micropython代码才能正常。

暂时不弄了。

# lua集成进来



# 这里有一些小型的实现，还有lua

https://github.com/nodemcu/nodemcu-firmware/blob/release/app/