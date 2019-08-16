---
title: C语言之glib
date: 2018-09-10 17:36:31
tags:
	- C语言

---



glib和glibc是2个东西。glib主要是给gnome用的。

但是因为封装得挺好，其他人在其他地方也会用。

主要就是定义了很多的基础链表这些常用的数据结构。



先看glib.h这个头文件。

```
#include <glib/galloca.h>
#include <glib/garray.h>
#include <glib/gasyncqueue.h>
#include <glib/gatomic.h>
#include <glib/gbacktrace.h>
#include <glib/gbase64.h>
#include <glib/gbitlock.h>
#include <glib/gbookmarkfile.h>
#include <glib/gbytes.h>
#include <glib/gcharset.h>
#include <glib/gchecksum.h>
#include <glib/gconvert.h>
#include <glib/gdataset.h>
#include <glib/gdate.h>
#include <glib/gdatetime.h>
#include <glib/gdir.h>
#include <glib/genviron.h>
#include <glib/gerror.h>
#include <glib/gfileutils.h>
#include <glib/ggettext.h>
#include <glib/ghash.h>
#include <glib/ghmac.h>
#include <glib/ghook.h>
#include <glib/ghostutils.h>
#include <glib/giochannel.h>
#include <glib/gkeyfile.h>
#include <glib/glist.h>
#include <glib/gmacros.h>
#include <glib/gmain.h>
#include <glib/gmappedfile.h>
#include <glib/gmarkup.h>
#include <glib/gmem.h>
#include <glib/gmessages.h>
#include <glib/gnode.h>
#include <glib/goption.h>
#include <glib/gpattern.h>
#include <glib/gpoll.h>
#include <glib/gprimes.h>
#include <glib/gqsort.h>
#include <glib/gquark.h>
#include <glib/gqueue.h>
#include <glib/grand.h>
#include <glib/gregex.h>
#include <glib/gscanner.h>
#include <glib/gsequence.h>
#include <glib/gshell.h>
#include <glib/gslice.h>
#include <glib/gslist.h>
#include <glib/gspawn.h>
#include <glib/gstrfuncs.h>
#include <glib/gstring.h>
#include <glib/gstringchunk.h>
#include <glib/gtestutils.h>
#include <glib/gthread.h>
#include <glib/gthreadpool.h>
#include <glib/gtimer.h>
#include <glib/gtimezone.h>
#include <glib/gtrashstack.h>
#include <glib/gtree.h>
#include <glib/gtypes.h>
#include <glib/gunicode.h>
#include <glib/gurifuncs.h>
#include <glib/gutils.h>
#include <glib/gvarianttype.h>
#include <glib/gvariant.h>
#include <glib/gversion.h>
#include <glib/gversionmacros.h>
#ifdef G_PLATFORM_WIN32
#include <glib/gwin32.h>
#endif

#ifndef G_DISABLE_DEPRECATED
#include <glib/deprecated/gallocator.h>
#include <glib/deprecated/gcache.h>
#include <glib/deprecated/gcompletion.h>
#include <glib/deprecated/gmain.h>
#include <glib/deprecated/grel.h>
#include <glib/deprecated/gthread.h>
#endif /* G_DISABLE_DEPRECATED */

#include <glib/glib-autocleanups.h>
```



看看GObject的定义。

```
struct  _GObject
{
  GTypeInstance  g_type_instance;
  
  /*< private >*/
  volatile guint ref_count;
  GData         *qdata;
};
```

GTypeClass

GType：这个就是ulong的。



这一套对象系统，靠的就是在最前面包含父类的方式实现继承。



安装：

```
编译安装libffi
编译安装glib
然后apt-get安装sudo apt-get install libdbus-glib-1-dev
```

编译例子

```
.PHONY: all clean

CFLAGS := -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include -I/usr/lib/i386-linux-gnu/glib-2.0/include/ \
	-L/usr/lib/x86_64-linux-gnu -lgobject-2.0 -lgthread-2.0 -lglib-2.0
all:
	gcc recv.c -o recv -ldbus $(CFLAGS)
	gcc send.c -o send -ldbus $(CFLAGS)

clean:
	rm -rf recv send
```



# 基本使用方法

glib由5个部分组成：

1、基础类型。

2、对核心应用的支持。

3、实用功能。

4、数据类型。

5、对象系统。



glib是gtk的一套函数库。是gnome工程的基础。

是一个轻量级的实用的C程序库。

可以跨平台使用。

有3个子系统：

```
1、线程gthread。
2、插件gmodule
3、对象gobject。
```

需要这样来链接对应的库：

```
`pkg-config --cflags --libs gthread-2.0 gmoudle-2.0 gobject-2.0`
```



GObject是glib的精华所在。

glib用C语言实现，提供了动态数组、链表、哈希表、平衡二叉树、字符串等常用容器。



编译一个最简单的使用glib的程序。

这个需要加入一些目录。所以写一个Makefile来做。

```
.PHONY: all clean
INCLUDE := -I/usr/include/glib-2.0 -I/usr/lib/x86_64-linux-gnu/glib-2.0/include \
	-L/usr/lib/x86_64-linux-gnu -lgobject-2.0 -lgthread-2.0 -lglib-2.0
	
CFLAGS := -g -Wall -O3  $(INCLUDE)
all:
	gcc test.c $(CFLAGS)
```

```
#include <glib.h>

int main()
{
	gint i = 0;
	
}
```

现在加入事件循环、内存操作、线程这3种功能。

```
#include <glib.h>

GMutex *mutex = NULL;
static gboolean t1_end = FALSE;
static gboolean t2_end = FALSE;
struct _Arg {
	GMainLoop *loop;
	gint max;
};
typedef struct _Arg Arg;

void run_1(Arg *arg)
{
	int i;
	for(i=0;i<arg->max;i++) {
		if(g_mutex_trylock(mutex) == FALSE) {
			g_print("run_2 lock the mutex\n");
			g_mutex_unlock(mutex);
		} else {
			g_usleep(10);
		}
	}
	t1_end = TRUE;
}
void run_2(Arg *arg)
{
	int i;
	for(i=0; i<arg->max; i++) {
		if(g_mutex_trylock(mutex) == FALSE) {
			g_print("run_1 lock the mutex\n");
			g_mutex_unlock(mutex);
		} else {
			g_usleep(10);
		}
	}
	t2_end = TRUE;
}

void run_3(Arg * arg)
{
	for(;;) {
		if(t1_end && t2_end) {
			g_main_loop_quit(arg->loop);
			break;
		} else {
			g_usleep(10);
		}
	}
}
int main()
{
	GMainLoop *main_loop;
	Arg *arg;
	if(!g_thread_supported()) {
		g_thread_init(NULL);
	}
	main_loop = g_main_loop_new(NULL, FALSE);
	arg = g_new(Arg, 1);
	arg->loop = main_loop;
	arg->max = 11;
	mutex = g_mutex_new();
	g_thread_create(run_1, arg, TRUE, NULL);
	g_thread_create(run_2, arg, TRUE, NULL);
	g_thread_create(run_3, arg, TRUE, NULL);
	
	g_main_loop_run(main_loop);
	g_print("run_3 has exited\n");
	g_mutex_free(mutex);
	g_free(arg);
	
}
```

# 常用函数和宏

```
MIN(a,b)
MAX(a,b)
ABS(a)
CLAMP(x, low, high)
	限制x在low到high之间。
GINT_TO_POINTER
GPOINTER_TO_INT

g_return_if_fail(cond);
g_return_val_if_fail(cond, retval);

g_malloc
	总是返回gpointer类型。
	失败时会退出进程。
	所以没有必要检查是否为NULL。
	
GString
	字符串类型。跟c++的string比较像。
```

# 对核心应用的支持

包括：

1、事件循环。

2、内存操作。

3、线程操作。

4、动态库操作。

5、错误处理。

6、日志。



# 实用功能

glib包含了近20种实用功能。从简单的字符串处理到xml解析。

现在我们看看随机数和计时的。



# 实现异步

g_idle_add，添加一个空闲时执行的任务。

是被main_loop执行的。

gtk就是通过这些方式来刷新屏幕的。

串行化对ui的操作。



glib main loop最大的特点就是支持多事件源。使用非常方便。

包括：键盘鼠标事件、系统定时事件、socket事件等。

还支持一种叫idle的事件源。这个主要是实现异步的。



# 例子

我把代码放在这里：

https://github.com/teddyxiong53/c_code/tree/master/glib_test



## helloworld

这个简单

## GSList

单链表。

结构体是这样：

```
struct {
	gpointer *data;
	GSList *next;
};
```

## GList

双向链表。

## 双向队列GQueue

## 哈希表

GHashTable

## 字符串

GString

## 动态数组

GArray。

## 动态指针数组

GPtrArray。

## 动态字节数组

GByteArray。

## 平衡二叉树

GTree。

## 关系和元组

GRelation

类似数据库，但是只限于2个字段。

GTuple

关系的每条记录对应一个GTuple。

## 随机数

GRand

## 线程池

GThreadPool。

## 警告和断言

## 线程

GThread

只实现了pthread的基本功能。有些没有覆盖到。所以有时候会混用pthread。

mutex。这个是用一些宏来做的。也可以用GMutex直接来定义变量。

```
G_LOCK_DEFINE (thread_mutex);
	定义一个mutex。
G_LOCK (thread_mutex)
	加锁
G_UNLOCK (thread_mutex)
	解锁。
```

GCond

GPrivate 私有数据。

GOnce 一次性初始化

## 线程异步通信

GAsyncQueue。

## 字符串函数

## 主事件循环

这个是重中之重。需要重点搞清楚这个。



# 打印

我看代码里g_debug没有打印出来。

输出这个环境变量。

```
export G_MESSAGES_DEBUG=all
```

然后就可以了。

```
int main(int argc, char **argv)
{
    //g_log_set_handler(G_LOG_DOMAIN, G_LOG_LEVEL_WARNING| G_LOG_LEVEL_CRITICAL|G_LOG_LEVEL_DEBUG|G_LOG_LEVEL_INFO, g_log_default_handler, NULL);
    g_warning("This is warning\n");
    g_message("This is message\n");
    g_debug("This is debug\n");
    g_critical("This is critical\n");
    g_log(NULL, G_LOG_LEVEL_INFO , "This is info\n");
    return 0;
}
```

要调整为其他的值，可以这样改：

```
export G_MESSAGES_DEBUG=debug
```



# 代码

代码目录下，有这么几个目录：

```
glib
gmodule
gobject
gthread
```

我们先重点看glib目录。下面有个tests目录。

编译方法是，make xx。xx是对应xx.c这种文件名的。

这样就可以一个个进行测试。



# 主循环

主循环涉及到3个结构体。

```
GMainLoop
GMainContext
GSource

它们之间的关系是这样的：
    GMainLoop -> GMainContext -> {GSource1, GSource2, GSource3......}
    
每个GmainLoop都包含一个GMainContext成员，而这个GMainContext成员可以装各种各样的GSource，GSource则是具体的各种Event处理逻辑了。在这里，可以把GMainContext理解为GSource的容器。（不过它的用处不只是装GSource）

```

GMainLoop通过g_main_loop_new来创建。

这个函数需要2个参数：

```
参数1：
	一个GMainContext指针。
	如果传递NULL，会分配一个默认的Context给这个loop。
	我们也可以这样来明确指定一个GMainContext。
	main_context = g_main_context_new();
	main_loop = g_main_loop_new(main_context, FALSE);
参数2：
	bool类型。is_running。一般是给false。
	而在后面通过g_main_loop_run(main_loop);在这里面把is_running设置为TRUE。
```

g_main_loop_run

这个函数会阻塞，然后处理各种事件。

mainloop支持多种事件源。

比较特殊的一种叫idle是事件源。这个主要是用来处理异步的。



GMainContext可以在多个GMainLoop之间共享。

下面是一个简单的例子。实现的效果是100ms的定时。

```
#include <glib.h>

gboolean count_calls(gpointer *data)
{
    mylogd("");
    gint *i = (gint *)data;
    (*i)++;
    return TRUE;
}
void test_timeouts()
{
    GMainContext *ctx;
    GMainLoop *loop;
    GSource *source;
    gint a, b, c;
    a = b = c = 0;

    ctx = g_main_context_new();
    loop = g_main_loop_new(ctx, FALSE);

    source = g_timeout_source_new(100);
    g_source_set_callback(source, count_calls, &a, NULL);
    g_source_attach(source, ctx);
    g_source_unref(source);
    g_main_loop_run(loop);

}
int main()
{
    test_timeouts();
}
```



idle任务。

```
#include <glib.h>

gboolean test_idle(gpointer data)
{
    gchar *s = (gchar *)data;
    g_printf("data:%s\n", s);
    g_usleep(1000*1000);
    return TRUE;
}
int main()
{
    GMainLoop *loop;
    loop = g_main_loop_new(NULL, FALSE);
    g_idle_add(test_idle, "xxx");
    g_main_loop_run(loop);
}
```

改成这样也可以。

```
#include <glib.h>

gboolean test_idle(gpointer data)
{
    gchar *s = (gchar *)data;
    g_printf("data:%s\n", s);
    g_usleep(1000*1000);
    return TRUE;
}
int main()
{
    g_idle_add(test_idle, "xxx");
    g_main_context_iteration (NULL, FALSE);
}
```



# GVariant

这个代表了什么？做什么用的？

可以用来实现数据的序列化。

这个还是比较复杂的一个东西。

这个的内涵是，任意类型。

相当于弱类型一样。

这个知识点非常大。暂时不管。



# GQuark

quark这个词的字面含义，是一种物理单位。

在glib里，用这个来表示什么含义呢？

在程序里标识一块代码，有两种方式可以做到：

1、用数字。

2、用字符串。

数字比较节省空间，但是可读性差。

字符串可读，但是速度慢。

GQuark就是结合这2者的长处。

主要的接口是：

```
g_quark_from_string
g_quark_to_string
```



学习方法

把glib/tests目录下的一个个自己写一遍。

# signal用途





GArray跟C语言默认的数组比较像。但是GArray可以自增长。

GAsyncQueue是用来做线程之间异步通信的。



glib靠一个800K的动态库，还是还易于使用的。

比标准C库函数名更加有规律，易于使用。



简单测试代码：

```
int main()
{
    //字符串操作
    {
        GString *s = g_string_new(NULL);
        g_string_assign(s, "new value");
        g_printf("str:%s, len:%d, allocated_len:%d\n", s->str, s->len, s->allocated_len);
        g_string_append(s, "11111111111111111");
        g_printf("after append:\n");
        g_printf("str:%s, len:%d, allocated_len:%d\n", s->str, s->len, s->allocated_len);
        g_printf("after prepend:\n");
        g_string_prepend(s, "222222222222222");
        g_printf("str:%s, len:%d, allocated_len:%d\n", s->str, s->len, s->allocated_len);
        g_free(s);
    }
    //array操作
    {
        GArray *a = g_array_new(FALSE, FALSE, sizeof(gint));
        g_array_set_size(a, 60);//必须指定长度，不然下面操作就会越界导致段错误。
        gint index = 17;
        gint value = 55;
        g_array_append_val(a, value);
        g_array_insert_val(a, index, value);
        g_array_free(a, FALSE);
    }
    //获取目录。
    g_printf("user config dir:%s\n", g_get_user_config_dir());
    g_printf("user data dir:%s\n", g_get_user_data_dir());
    g_printf("user cache dir:%s\n", g_get_user_cache_dir());
    //检查文件存在性
    g_printf("1.txt is exist:%d\n", g_file_test("1.txt", G_FILE_TEST_EXISTS));

    //读文件。
    {
        gssize length;
        gchar *content;
        gchar *filename = "1.txt";
        if(g_file_get_contents(filename, &content, &length, NULL)) {
            g_printf("content:%s\n", content);
            g_free(content);
        }
    }
    //写文件
    {
        g_file_set_contents("1.txt", "aaaa", 4, NULL);
    }

}
```



# glib-genmarshal



# once的用法

```
g_once_init_enter 
	这个是在临界区初始化的时候用的。
	它的参数是一个static gsize inited=0;这样的一个初始化值为0的static变量。
	在完成的时候，inited会被赋值为非0值。
```

实例代码是这样：

```
void xx_init()
{
	static gsize inited = 0;
	if(g_once_init_enter(&inited) {
		g_once_init_leave(&inited, TRUE);
	}
	//code
}
```

# slice

这个是分配大小相同的多个内存块。

# gspawn

这个支持比posix接口更加好用的fork机制。

在gio里，还进一步封装了GSubprocess。



# 使用了glib的开源项目

## bluez





```
GTypePlugin是什么？主要用途是什么？
1、是一个interface，用来实现类型的动态加载。
2、它的父类是GInterface。
3、实现的子类是GTypeModule。

GTypeXxx
Xxx有：
Class
	成员就是一个GType（本质是u64）
Instance
	成员就是一个GTypeClass指针。
	之所以是指针，是因为所有的实例，共用了一个Class结构体。
Interface
	2个成员。
	都是GType类型。
	1、g_type。
	2、g_instance_type。
	为什么要比Class的还要多一个成员呢？
Query
	用来保存一种类型对应的信息的。
	4个成员。
	1、GType type
	2、char * type_name。
	3、class大小。
	4、instance大小。
	
Info
	这个结构体成员较多。是创建类型时的重要结构体。
	1、u16的class_size。这就决定了类的尺寸不能超过64K了。
	2、base的init和finalize函数。
		这2个函数的唯一参数都是klass。
	3、class的init和finalize函数。
		这2个函数的参数2个：klass和class_data。
	4、instance相关的3个成员。
		instance_size。也是u16的。
		预分配个数。
		instance的init函数。
	5、GTypeValueTable指针。
		这个很多时候，都是NULL。
		g_boxed_type_register_static
			这里面用到了，不是空的。
		_g_enum_types_init
			不是空的。
	可以通过搜索GTypeInfo来看系统里定义了哪些类型。
	看看这些类型。
	
GTypeValueTable
	这个的作用是什么？
	提供GValue实现需要的函数。
	这样GValue就可以存放类型的值了。
	
	有这些成员：
	1、value的init、free、copy这3个函数。
		init：
			分配的时候，会把对应的空间清零。
			
gboxed类型
一种机制，用来保证C结构体，这些结构体是通过类型系统注册到glib的。
类型系统只需要知道怎样去copy和free这些结构体。
基于这个，只需要把结构体当成内存块来处理就好了。
适合对Point这些简单结构体进行定义。

GApplication
	这个是一个应用的基础类。
	是GtkApplication的基础。
	你不应该直接使用GApplication类。
	通过引用计数来实现生命周期管理。
```



# 参考资料

1、浅析GLib

https://www.ibm.com/developerworks/cn/linux/l-glib/index.html

2、glib中的signal不是异步的，使用g_idle_add实现异步

https://blog.csdn.net/fingding/article/details/6866263

3、g_main_loop_new (NULL, FALSE) 原理分析

https://blog.csdn.net/arag2009/article/details/17095361

4、

https://blog.csdn.net/dj0379/article/details/7667399

5、glib学习笔记

https://blog.csdn.net/hpu11/article/details/62237142

6、GTK+ 2.0 教程

http://www.huzheng.org/ebook/gtk2-tut/book1.html

7、系列教程

https://blog.csdn.net/andylauren/article/category/6219334

8、快速上手Gobject

https://blog.csdn.net/acs713/article/details/7778051

9、Glib Log的使用

https://blog.csdn.net/mhpmii/article/details/50594295

10、glib 简介

https://www.cnblogs.com/wangkangluo1/archive/2011/07/10/2102178.html

11、How to control level of debugging info in glib?

https://stackoverflow.com/questions/7518620/how-to-control-level-of-debugging-info-in-glib

12、使用GVariant实现数据的序列化处理

https://blog.csdn.net/coroutines/article/details/38496145

13、C++变体数据类型—— VARIANT

https://blog.csdn.net/yousss/article/details/79555821

14、Glib中Gquark浅析

https://blog.csdn.net/wfreehorse/article/details/70238231

15、如何使用Glib工具集管理C数据

https://wenku.baidu.com/view/29d6911ffc4ffe473368abb8.html?sxts=1563870816369

16、glib中的signal不是异步的，使用g_idle_add实现异步

https://blog.csdn.net/fingding/article/details/6866263

17、Glib Examples

这些例子都很简洁。值得看一遍。

https://lzone.de/examples/Glib

18、Glib学习（15） 线程之间的异步通信 Asynchronous Queues

https://blog.csdn.net/andylauren/article/details/79313181

19、glib-genmarshal的使用

https://www.cnblogs.com/super119/archive/2011/01/03/1924442.html

20、

https://blog.csdn.net/fanzirong_/article/details/83069062

21、GObject 参考手册：概念：GLib 动态类型系统

https://hev.cc/445.html