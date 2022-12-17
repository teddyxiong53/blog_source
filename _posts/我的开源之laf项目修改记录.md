laf是lua App framework的缩写。

目标是做一个lua和C混合编程的基础框架，方便自己后续扩展写一下小的项目。

受到cfadmin项目的启发。

# eventloop实现

觉得libev还是复杂了点。我决定使用另外一个更加精简的eventloop方案：ev.h。

然后自己实现一下ev.h，只选择自己需要的那部分功能，让代码更加精简。

还是基于autotools来组织编译。



选择把epoll的代码写了。调试一下。发现不能接受和发送数据。

要调试一下看看卡在哪里了。

从添加的打印看，整个循环都卡住了。

在client连接上来后，就卡住了。

这2个fd怎么不一样？而且为什么中间的4被跳过去了？

```
[DEBUG][ev_epoll.c][ev_api_fetch_event][91]: fd:3
[DEBUG][tinyev.c][ev_process_event][91]: mask:0x00000001
[DEBUG][tinyev.c][ev_process_event][117]: 
[DEBUG][test-tinyev.c][on_connection][120]: get connection fd:5
[DEBUG][test-tinyev.c][connection_init][21]: conn->fd:5
```

这个没有关系。

这个时候，再开一个shell，还可以连接上来的。

但是为什么循环不会继续运转呢？我是设置2s的超时的。

现在不知道问题在哪里。

是在tinyev还是在ev_epoll？

还是在test里？

跟fd的设置nonblock也没有关系。

算了。

我直接把本来的代码拷贝过来测试一下。

发现问题就是出在test里。

用默认的测试代码测试，至少是不会卡住循环的。

但是我代码还是有一个错误打印：

```
[ERROR][tinyev.c][ev_fire_event][180]: ev_api_fire_event fail
```

epoll_ctl 函数说明时候会出错？

我的条件写错了

```
if (mask & xx)
写成了
if (mask | xx) 这样条件就一定满足了。所以逻辑不对。
```

现在要看test里之前是什么问题导致我的卡住的问题。

知道了

```
static void on_data (ev_context *ctx, void *data)
{
    int n = 0;
    struct connection *conn = data;

    mylogd("");
    do {
        mylogd("");
        n = read(conn->fd, conn->buf + conn->bufsize, conn->capacity - conn->bufsize);
        mylogd("read data len:%d", n);
        if (n < 0) {
            if (errno == EAGAIN || errno == EWOULDBLOCK) {
                continue;//这里写错了。应该是要break掉。因为非阻塞没有数据，就是这个情况。
            } else {
```

但是现在还是卡住。

找到原因了，就是listenfd没有设置为nonblock模式。

设置了就好了。

得出结论，就是在eventloop里，所有的fd都要是nonblock的。



目前感觉eventfd的还是比较混乱的。

总之目标是希望可以实现libev的基本功能。



仔细回顾了当前的功能，发现有这些不合理的地方：

1、没有signalfd的管理。

2、eventfd被特殊处理了。没有必要特殊处理啊。



## 实现一个libev兼容层

兼容感觉做起来工作量不小。

先看cfadmin里用到的内容，我用我的代码进行对等实现就好。

需要这几种情况

```
typedef ev_io core_io;
typedef ev_idle core_task;
typedef ev_timer core_timer;
typedef ev_signal core_signal;
typedef ev_child core_child;
typedef struct ev_loop core_loop;
```

这个其实不是我当前的关键。



# 然后就可以开始添加lua的相关代码

先从lac那边把lua的目录弄过来。

## 先做sys这个模块

lua标准库没有sys模块，我们做一个简单的。

可以加进去并使用。

## 然后加一个lualib的例子

就先做class的。这个很基础很独立，不依赖其他的。

可以加进去，并用lua解释器进行测试。

## 然后看在C代码里查找并调用到自定义lua模块的方法

可以先把src目录下的main入口这一块的C代码写好。

这个不依赖其他的。

把libev代码直接加进来。

从src/core的代码开始写。

core_start.c的，我只考虑一个进程的情况。

参数解析基本先不做。

现在安装cfadmin的做法，注册进去的模块require不行。

我决定先把debug的模块加进去，这个不依赖C模块的。

现在lualib下面的xx/init.lua可以正常导出符合进行使用。

现在把这个加进来。

https://github.com/cfadmin-cn/debug

直接用xpcall来执行代码吧。不用dofile。

这样来看到详细的出错信息。

现在看到的出错信息是这样：

```
[DEBUG][core_start.c][traceback][11]: msg:/home/teddy/work/test/laf/script/main.lua:18: module 'sys' not found:
        no field package.preload['sys']
        no file '/home/teddy/work/test/laf/lualib/sys.lua'
        no file '/home/teddy/work/test/laf/lualib/sys/init.lua'
        no file '/home/teddy/work/test/laf/luaclib/.libs/sys.so'
        no file '/home/teddy/work/test/laf/luaclib/libsys.so'
```

这找的路径不对啊。

把路劲改对。

现在又报这个错误。

```
 dynamic libraries not enabled; check your Lua installation
```

原来我一直编译的lua都不对的。

LUA_USE_LINUX 这个宏一直没有定义。

现在加上这个定义。

除了dlopen的通过-ldl来解决。

还有这个：

```
undefined reference to `add_history'
undefined reference to `readline'
```

这个需要：

```
sudo apt-get install libreadline-dev
```

还需要加上：-lreadline

可以了。

现在动态库的require一切正常了。

## 增加可执行文件的参数，方便测试

```
./cfadmin test.lua
```

自动去执行script下面的同名文件。

## 写Co

把这个写了。

lualib\internal\Co.lua

大概理解了。

写一个测试程序。

test-Co.lua

这个只能通过cfadmin来运行，因为加入自定义的模块task。

但是我运行有些问题，感觉我没有完全理解。所以还是先把cf这个lua写了再测试。

又依赖了Timer.lua。所以先完成这个。

这个又依赖了c模块的timer。



timer的start函数接受2个参数：

参数1：一个double的时间值。

参数2：一个co。



timer的写完了。

## 开始写cf的

是为了写loggging的，但是logging依赖了cf。

所以先写cf的。

写好了。测试一下。

报了这个错误。

```
attempt to yield from outside a coroutine
```

是我写错了一些变量导致的。

但是还是有问题。但是看原版的是没有这个错误的。

我把cf文件替换了还是一样。

那应该的Co里面有问题。

我把Co和Timer都替换了。还是有。

那问题可能出在C代码里。

不管了。先把logging写了。

这个太繁琐了。没有什么特别的技术在里面。先不写了logging了。

可以先写utils的。

里面调试工具写一下。

