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

| 模块        | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| galloca     | 对外提供4个函数：<br />g_alloca<br />g_alloca0<br />g_newa<br />g_newa0 |
| garray      | 提供4个数据类型：<br />GBytes：这个没有看到配套的函数。在另外的gbytes.h文件里<br />GArray<br />GByteArray：跟GArray的区别是，内部数据是uint8类型，而不是char类型。<br />GPtrArray |
| gasyncqueue | 异步队列。用于线程间通信。                                   |
| gatomic     |                                                              |
| gbacktrace  |                                                              |
| gbase64     |                                                              |
| gbitlock    |                                                              |
| gbytes      |                                                              |
| gcharset    | 只有函数                                                     |


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

`GQuark` 是 GLib 库中的一个数据类型，用于管理和标识字符串的唯一符号。

它的名称 "Quark" 源自粒子物理学中的术语，

表示一种独特的标识符，==用于避免字符串比较的开销，提高性能。==

`GQuark` 具有以下特点：

1. **唯一性**：每个 `GQuark` 对象都关联了一个唯一的整数值，用于表示相应的字符串标识符。这确保了相同的字符串对应相同的 `GQuark` 值。

2. **快速比较**：由于 `GQuark` 对象是整数，因此比较两个 `GQuark` 值非常快速，远远快于字符串比较。

3. **用于优化**：`GQuark` 主要用于优化字符串处理，特别是在 GLib 和 GTK+ 等库中，用于加速操作。它可以用于加速字符串查找、哈希表操作等。

4. **避免内存泄漏**：通过使用 `GQuark`，可以避免字符串的内存分配和泄漏问题，因为字符串常量只会分配一次并保持不变。

在使用 `GQuark` 时，通常会涉及以下操作：

1. 创建 `GQuark` 对象：通过调用 `g_quark_from_static_string` 或 `g_quark_from_string` 来将字符串转换为 `GQuark` 对象。

2. 比较 `GQuark` 值：通过直接比较 `GQuark` 对象的整数值来判断字符串是否相等。

3. 优化哈希表和查找操作：`GQuark` 可以用于优化哈希表的键，以提高查找性能。

总之，`GQuark` 是 GLib 中的一种数据类型，用于管理字符串的唯一标识符，以提高性能和避免内存泄漏。它通常用于 GLib、GTK+ 和其他 GNOME 框架中，以加速字符串处理操作。



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



GQuark值是分配给字符串的数字，

并且很容易测试它们的等同性。

然而，它们并没有数字顺序。

你不能用quark值来进行字母顺序测试。

因此，你不能用它们作为排序关键字。

如果你想比较quark所代表的字符串，

你必须先用g_quark_to_string()来提取相应的字符串，然后才可以使用strcmp()或g_ascii_strcasecmp()。



参考资料

1、

https://blog.csdn.net/hiccupzhu/article/details/16832649

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

# GInitiallyUnowned

`GInitiallyUnowned` 是 GLib 库中的一个基类，

用于创建 GObject 对象的类。

GLib 是一个开源库，它提供了一种用 C 语言创建面向对象代码的方式，GObject 是其面向对象系统的一部分。

`GInitiallyUnowned` 是 GObject 的一个子类，==通常用于创建那些不需要立即初始化和管理生命周期的对象。==

具体来说，它的特点包括：

1. **不需要立即释放**：与其他 GObject 子类不同，`GInitiallyUnowned` 对象不需要立即释放（通过 `g_object_unref`）。==它们的释放通常由 GType 系统自动处理。==

2. **允许延迟初始化**：`GInitiallyUnowned` 对象可以被创建并保持在内存中，而不需要立即分配资源或初始化。这对于稍后在需要时初始化对象非常有用。

3. **支持延迟释放**：对象的释放通常是由 GObject 的引用计数机制管理的。然而，`GInitiallyUnowned` 对象的释放可能会延迟到稍后，例如，当对象不再被引用时。

4. **适用于构建控件和窗口**：==`GInitiallyUnowned` 对象通常用于构建 GUI 控件、窗口和其他用户界面元素，因为它们可以灵活地处理对象的生命周期。==

通常情况下，开发者不需要直接创建 `GInitiallyUnowned` 对象，而是使用它的子类，例如 `GtkWidget`（用于构建 GTK+ 用户界面）等。这些子类通常提供了更多的功能和适用于特定应用领域的接口。

总之，`GInitiallyUnowned` 是 GObject 类的一个子类，用于创建那些不需要立即初始化和释放的对象，通常用于构建 GUI 控件和窗口等应用程序界面元素。

# GInitiallyUnownedClass

`GInitiallyUnownedClass` 是 GLib/GObject 中的一个结构体，

用于描述 `GInitiallyUnowned` 类的类信息。

在 GObject 中，每个类都由一个类结构体（class structure）来定义，

该结构体包含了类的方法、属性和信号等信息。

`GInitiallyUnownedClass` 结构体中包含了一些字段，

这些字段定义了 `GInitiallyUnowned` 类的行为。

一些常见的字段包括：

- `parent_class`：指向父类的指针，它表示该类继承自哪个父类。父类的方法和属性可以在子类中被继承和重写。

- `finalize`：一个函数指针，用于在对象被销毁时执行一些最终清理工作。==这是一个析构函数==，用于释放对象的资源。

- `dispose`：==类似于 `finalize`，但更常用于在对象即将被销毁之前进行资源释放或断开连接等操作。==

- `set_property` 和 `get_property`：用于设置和获取对象属性的函数指针，这允许开发者定义对象的属性以及对这些属性的访问方式。

`GInitiallyUnownedClass` 结构体是 GObject 类系统的核心部分之一，它描述了类的行为和属性，

允许开发者创建自定义的 GObject 子类。

当开发者创建新的 GObject 子类时，通常需要填充和配置相应的 `GInitiallyUnownedClass` 结构体以定义类的行为。

这些类结构体通常在 GObject 子类的类初始化函数中进行设置。

总之，`GInitiallyUnownedClass` 结构体用于描述 `GInitiallyUnowned` 类的类信息，包括类的方法、属性和信号等，允许开发者创建自定义的 GObject 子类。

# GType

`GType` 是 GLib/GObject 库中的一个基本数据类型，

用于表示 GObject 类型。

GObject 是 GLib 库的面向对象系统，

它允许在 C 语言中创建和管理面向对象的程序。

`GType` 用于标识和区分不同的 GObject 类型，它是 GObject 类型系统的核心之一。

`GType` 具有以下特点：

1. **类型标识符**：每个 GObject 类型都与一个唯一的 `GType` 值相关联，用于标识该类型。这个值是一个整数，通常用于在运行时确定对象的类型。

2. **继承关系**：`GType` 值还包含有关类型继承关系的信息。它可以用于确定一个类型是否是另一个类型的子类型，从而支持多态性和继承。

3. **运行时类型检查**：`GType` 值允许在运行时检查对象的类型，这对于在面向对象程序中执行类型安全的操作非常重要。

4. **类型注册**：GObject 类型通常需要在应用程序中进行注册，以便在运行时使用。`GType` 值可以用于注册和查找类型，以确保正确的类型信息。

5. **类型系统的核心**：`GType` 是 GObject 类型系统的核心之一，它允许开发者创建自定义的 GObject 子类，并在 GObject 类型系统中进行管理和查找。

在使用 GObject 类型时，通常会涉及以下操作：

1. **定义类型**：开发者可以使用 GObject 类型系统定义新的 GObject 类型，包括创建类结构体、初始化类、注册类型等。

2. **创建对象**：通过 `g_object_new` 或其他方式创建特定类型的 GObject 对象。

3. **类型检查**：使用 `GType` 值进行类型检查，例如，`G_TYPE_IS_OBJECT` 或 `G_TYPE_CHECK_INSTANCE`。

4. **对象操作**：在对象上执行操作，调用方法，设置属性等。

总之，`GType` 是 GObject 类型系统的核心数据类型，用于标识、管理和操作 GObject 类型，以支持面向对象编程在 C 语言中的实现。

# G_TYPE_IS_FUNDAMENTAL

`G_TYPE_IS_FUNDAMENTAL` 是 GLib/GObject 库中的一个宏，

==用于检查给定的 `GType` 是否是基本数据类型。==

在 GLib/GObject 中，数据类型分为两种：

==基本数据类型和派生数据类型。==

基本数据类型是 GLib/GObject 提供的一组内置数据类型，

如整数、布尔值、字符串等。

派生数据类型是基于这些基本数据类型创建的用户自定义数据类型，

通常通过创建 GObject 类的子类来实现。



`G_TYPE_IS_FUNDAMENTAL` 宏用于检查给定的 `GType` 是否是基本数据类型。

如果是基本数据类型，则宏返回 `TRUE`，否则返回 `FALSE`。



以下是使用 `G_TYPE_IS_FUNDAMENTAL` 宏的示例：

```c
GType type = G_TYPE_STRING;

if (G_TYPE_IS_FUNDAMENTAL(type)) {
    g_print("This is a fundamental data type.\n");
} else {
    g_print("This is not a fundamental data type.\n");
}
```

在这个示例中，我们检查 `G_TYPE_STRING` 是否是一个基本数据类型。由于字符串是一个基本数据类型，所以 `G_TYPE_IS_FUNDAMENTAL` 将返回 `TRUE`。

这个宏通常用于在处理数据类型时进行条件检查，以确定如何处理不同类型的数据。

总之，`G_TYPE_IS_FUNDAMENTAL` 是 GLib/GObject 中的一个宏，用于检查给定的 `GType` 是否是基本数据类型。这有助于在编程中根据数据类型采取不同的操作。

# GTypeCValue

`GTypeCValue` 是 GLib/GObject 库中的一个数据结构，

**用于表示 C 值的通用容器。**

它用于在不同数据类型之间进行转换和传递参数，

是 GObject 类型系统中的一部分，用于处理 GObject 的属性、信号、方法等。

`GTypeCValue` 具有以下特点：

1. **通用容器**：`GTypeCValue` 可以用于存储不同数据类型的值，如整数、浮点数、指针等。这使得它非常灵活，可以用于处理各种数据类型。

2. **类型信息**：每个 `GTypeCValue` 包含有关存储的值的类型信息。这有助于确保在转换和操作值时进行正确的类型检查。

3. **GObject 集成**：`GTypeCValue` 是 GObject 类型系统的一部分，通常与 GObject 的属性系统一起使用。它可以用于获取和设置 GObject 的属性值。

使用 `GTypeCValue` 通常涉及以下操作：

1. 创建 `GTypeCValue` 对象，并为其分配适当的内存。

2. 设置或获取值：使用函数如 `g_value_init`、`g_value_set_int`、`g_value_get_double` 等来设置或获取值。

3. 类型转换：将值从一个类型转换为另一个类型。

4. 销毁：在不再需要时，应使用 `g_value_unset` 或 `g_value_reset` 等函数来释放 `GTypeCValue` 对象的资源。

`GTypeCValue` 主要用于 GObject 的属性操作和信号处理，以确保正确的类型转换和数据交换。这在图形用户界面开发和多媒体处理等领域非常有用。

总之，`GTypeCValue` 是 GLib/GObject 中的一个数据结构，用于表示 C 值的通用容器，用于处理不同数据类型的值。它是 GObject 类型系统的一部分，用于属性操作和信号处理。

# GTypeInterface

`GTypeInterface` 是 GLib/GObject 库中的一个重要概念，

用于实现接口（interface）和多继承。

它是 GObject 类型系统的一部分，

用于创建可共享的接口和允许多个类实现这些接口，==从而实现多继承的一种机制。==

以下是关于 `GTypeInterface` 的一些关键概念：

1. **接口（Interface）**：接口是一种抽象规范，定义了一组方法或函数的签名，但没有提供具体的实现。接口允许多个类共享相同的方法规范，从而实现一种形式的多继承。在 GObject 类型系统中，接口是由 `GTypeInterface` 表示的。

2. **多继承**：多继承是一种编程范例，允许一个类继承多个父类的属性和行为。==由于 C 语言不直接支持多继承，因此 GObject 类型系统使用接口和 `GTypeInterface` 来实现这种机制。==

3. **`GTypeInterface` 结构**：`GTypeInterface` 结构用于表示接口，它包含了一组函数指针，这些函数指针定义了接口的方法。不同的类可以实现相同的接口，以共享相同的方法规范。

4. **接口实现**：类可以实现一个或多个接口，从而获得接口定义的方法。这使得类可以共享多个接口的行为，而不必继承多个父类。

5. **多态性**：接口和多继承机制使得对象能够以多态的方式调用方法，即在运行时根据对象的实际类型调用适当的方法。

在 GObject 类型系统中，`GTypeInterface` 是实现多继承和接口的关键机制之一。它使得开发者能够创建可重用的接口，并使多个类实现这些接口，以共享方法规范和行为。这对于构建复杂的对象层次结构和促进代码重用非常有用。

总之，`GTypeInterface` 是 GLib/GObject 类型系统中的一部分，用于实现接口和多继承的机制，以支持面向对象编程的灵活性和代码重用。

# g_param_spec_enum

`g_param_spec_enum` 是 GLib 库中的一个函数，

用于创建 GObject 参数规范，

这些参数可以用于描述枚举类型的属性。



在使用 `g_param_spec_enum` 时，

你可以定义一个参数规范，

用于描述一个 GObject 属性，该属性的值是一个枚举类型的成员。

这对于表示某种状态或选项的属性非常有用。



以下是 `g_param_spec_enum` 的一些重要参数和特性：

1. **名字和详细描述**：你可以指定参数的名字和详细描述，以便更好地理解参数的用途。

2. **枚举类型**：通过提供一个枚举类型的 `GType`（GObject 类型），你可以指定此参数允许的枚举类型。

3. **默认值**：你可以定义参数的默认值，它将在创建对象时设置为参数的初始值。

4. **标志**：可以设置参数的各种标志，例如是否可读、可写、是否为类属性等。

5. **校验函数**：你可以指定一个自定义校验函数，用于检查用户提供的值是否有效。

使用 `g_param_spec_enum` 创建参数规范的示例：

```c
GParamSpec *param_spec;
GType enum_type = MY_ENUM_TYPE;  // 用你自己的枚举类型替换 MY_ENUM_TYPE

param_spec = g_param_spec_enum("my-enum-property",  // 参数名
                              "My Enum Property",   // 参数描述
                              "Description of my enum property", // 详细描述
                              enum_type,            // 枚举类型
                              MY_ENUM_DEFAULT,      // 默认值
                              G_PARAM_READWRITE);   // 可读可写标志
```

这将创建一个参数规范，用于描述一个名为 "my-enum-property" 的属性，其值是指定枚举类型 `enum_type` 的成员之一。该属性可以读取和写入，并具有默认值 `MY_ENUM_DEFAULT`。

一旦创建了参数规范，它可以用于创建对象的属性，使你能够设置和检索枚举类型的值。

总之，`g_param_spec_enum` 是 GLib 库中用于创建 GObject 参数规范的函数，用于描述枚举类型属性的规范。这对于创建具有不同状态和选项的对象属性非常有用。

# g_signal_new

`g_signal_new` 是 GLib/GObject 库中的一个函数，

用于创建新的 GObject 信号（Signal）。 

GObject 信号是一种机制，

==用于在对象之间传递事件和通知，使对象能够响应和处理事件。==

以下是 `g_signal_new` 函数的一些关键参数和特性：

1. **信号名（Signal Name）**：你需要指定一个唯一的信号名称，以便在后续代码中引用该信号。

2. **信号类型（Signal Type）**：你需要指定信号的数据类型。这表示信号可以传递的数据类型。

3. **标志（Flags）**：可以设置各种标志，如是否是详细信号、是否是用户驱动信号等。

4. **类（Class）**：你需要指定将该信号附加到的 GObject 类。

5. **紧密度（Closures）**：你可以定义信号的紧密度，用于确定信号的执行顺序。紧密度越高的信号将在紧密度较低的信号之前执行。

6. **函数指针（Handler Function）**：你需要指定一个函数指针，用于处理信号。这个函数将在信号触发时执行。

7. **用户数据（User Data）**：你可以传递用户自定义数据给信号处理函数，以便在信号处理中使用。

使用 `g_signal_new` 函数通常涉及以下操作：

1. 创建一个新的信号，其中包括指定的信号名称、信号类型、类等。

2. 指定信号处理函数，这是一个用户编写的函数，用于处理信号触发时的操作。

3. 可选地指定信号的标志、紧密度和用户数据。

4. 将新信号附加到 GObject 类中，使该类的对象能够连接和处理该信号。

一旦信号创建并附加到类中，类的对象可以使用 `g_signal_connect` 来连接信号并注册信号处理函数，以响应信号的触发。

总之，`g_signal_new` 是 GLib/GObject 中的一个函数，用于创建新的 GObject 信号，这是一种机制，用于在对象之间传递事件和通知。通过创建和连接信号，你可以实现对象之间的协作和通信。

# gobject类的`_init和_class_init`在什么时候被调用

在 GObject 类的生命周期中，`_init` 和 `_class_init` 方法都有特定的时机被调用：

1. **_class_init 方法**：`_class_init` 方法是在一个类（Class）第一次被创建时调用。这个方法通常在类初始化时执行，一般只执行一次，用于初始化类级别的属性、信号和方法。在 GObject 类的继承体系中，父类的 `_class_init` 方法通常在子类的 `_class_init` 方法之前调用，以确保父类的初始化操作完成。

2. **_init 方法**：`_init` 方法是在每个对象（Instance）创建时调用。每次创建一个类的对象时，都会执行对象的 `_init` 方法。这个方法通常用于初始化对象特定的属性。因此，每个对象都有自己的 `_init` 方法的实例。通常情况下，`_init` 方法在构造函数内部被调用。

下面是一些简单示例来说明这两个方法的调用时机：

```c
// _class_init 方法示例
static void my_object_class_init(MyObjectClass *klass) {
    GObjectClass *gobject_class = G_OBJECT_CLASS(klass);

    gobject_class->finalize = my_object_finalize;
    gobject_class->my_class_member = 42;
    // 更多类级别的初始化操作
}

// _init 方法示例
static void my_object_init(MyObject *object) {
    // 初始化对象级别的属性
    object->my_instance_member = 0;
}
```

在上面的示例中，`_class_init` 方法用于初始化类级别的属性，如类成员变量和方法。而 `_init` 方法用于初始化对象特定的属性，如对象的实例成员变量。在实际使用中，这两个方法通常用于确保类和对象都正确初始化，以使 GObject 类能够正常工作。

总之，`_class_init` 方法在类首次被创建时调用，用于初始化类级别的属性，而 `_init` 方法在每个对象创建时调用，用于初始化对象特定的属性。这两个方法在 GObject 类的生命周期中具有不同的作用和调用时机。

以gstbasesrc的为例：

这个get_type函数里，就注册了这个信息。

```
GType
gst_base_src_get_type (void)
{
  static volatile gsize base_src_type = 0;

  if (g_once_init_enter (&base_src_type)) {
    GType _type;
    static const GTypeInfo base_src_info = {
      sizeof (GstBaseSrcClass),
      NULL,
      NULL,
      (GClassInitFunc) gst_base_src_class_init,
      NULL,
      NULL,
      sizeof (GstBaseSrc),
      0,
      (GInstanceInitFunc) gst_base_src_init,
    };

    _type = g_type_register_static (GST_TYPE_ELEMENT,
        "GstBaseSrc", &base_src_info, G_TYPE_FLAG_ABSTRACT);

    private_offset =
        g_type_add_instance_private (_type, sizeof (GstBaseSrcPrivate));

    g_once_init_leave (&base_src_type, _type);
  }
  return base_src_type;
}
```

# 文章

对象的实现包含了公有成员。

GObject 也提供了私有成员的方法。

这实际上是 C 源文件中的一个结构，而不是在头文件。该类通常只包含函数指针。



https://zhuanlan.zhihu.com/p/567751966

# autoptr的实现原理

`__attribute__((cleanup(func)))` 是 GCC 提供的一个特性，

用于指定在变量作用域结束时自动调用指定的清理函数。

这个特性通常用于在 C 语言中进行资源管理，

确保在变量生命周期结束时执行必要的清理操作，

比如释放动态分配的内存或关闭文件描述符等。

下面是关于 `__attribute__((cleanup(func)))` 特性的一些说明：

- **语法**：`__attribute__((cleanup(func)))` 中的 `func` 是一个函数名，用于指定在变量作用域结束时要调用的清理函数。

- **工作原理**：当声明一个变量时，在变量的声明中使用 `__attribute__((cleanup(func)))`，会使得编译器在变量作用域结束时自动调用指定的清理函数。

- **示例**：

  ```c
  void cleanup_func(void *ptr) {
      free(ptr); // 释放内存
  }

  void example_function() {
      void *data __attribute__((cleanup(cleanup_func))) = malloc(10); // 在变量作用域结束时自动调用 cleanup_func
  }
  ```

- **注意事项**：
  
  - 清理函数的参数类型应该匹配被管理资源的类型。
  - 如果变量具有静态存储期（如全局变量），在程序结束时可能不会调用清理函数。

这个特性非常有用，可以帮助程序员避免忘记释放资源而导致内存泄漏等问题。在 C 语言中，没有自动垃圾回收机制，因此手动管理资源是至关重要的，而 `__attribute__((cleanup(func)))` 特性提供了一种方便的方式来管理资源的生命周期。

# 函数的I、W、U后缀的含义

这段代码是关于静态函数的锁定处理的说明。它指出，当调用静态函数时，锁定问题的处理方式由大写字母后缀指示。所有的静态函数都必须具有以下后缀之一：

- _I：[不关心锁定]
函数不关心锁定。

- _U：[未锁定调用]
调用期间不需要持有读写锁，但是在调用期间可以获取和释放锁。

- _L：[已锁定调用]
调用期间需要持有写锁或读锁数量大于0。

- _W：[已锁定写调用]
调用期间需要持有写锁。

- _Wm：[可变的已锁定写调用]
类似于_W，但在调用期间可以释放和重新获取写锁，需要注意指针。

- _WmREC：[可变的已锁定写调用，递归]
类似于_Wm，但还会获取递归互斥锁class_init_rec_mutex。

这些后缀用于指示静态函数在调用期间需要持有哪种类型的锁。





# glib的TypeNode的作用

在 GLib 中，`TypeNode` 主要用于表示类型系统中的节点。它

在类型注册和管理中扮演重要角色，具体作用包括：

1. **类型定义**：`TypeNode` 用于定义和存储类型的信息，包括类型的名称、父类型等。

2. **类型层次结构**：它帮助构建类型之间的层次结构，使得类型可以继承和扩展。

3. **类型查找**：通过 `TypeNode`，GLib 可以快速查找和访问已注册的类型信息。

4. **类型属性**：存储与类型相关的属性和元数据，便于在运行时操作。

总之，`TypeNode` 是 GLib 类型系统的核心组件，支持类型的创建、管理和查询。

# glib的类型系统

GLib 的类型系统是一个强大而灵活的机制，用于管理和操作不同的数据类型。以下是其主要特点和功能：

### 1. 类型注册
- GLib 允许开发者注册新的类型，支持自定义数据结构和对象。

### 2. 类型层次结构
- 支持继承和多态，通过父类和子类的关系组织类型，使得类型可以共享属性和方法。

### 3. 类型查询
- 提供接口用于查询类型信息，如类型名称、父类型、属性等，方便在运行时进行操作。

### 4. 类型安全
- 通过类型检查，确保在运行时只使用正确的数据类型，减少错误。

### 5. 动态类型
- 支持动态创建和操作类型，使得应用程序在运行时能够灵活地处理不同的数据。

### 6. 结合 GObject
- GLib 的类型系统与 GObject（对象系统）紧密结合，支持面向对象编程的特性，如信号、属性和接口。

### 使用示例
- 在创建自定义数据类型时，开发者可以通过 `GType` 系统注册类型并定义其行为和属性。

### 总结
GLib 的类型系统为开发者提供了一种结构化的方式来管理复杂数据类型，增强了代码的可维护性和可扩展性。

# 如何在 GLib 中注册自定义类型？

在 GLib 中注册自定义类型通常涉及以下步骤：

### 1. 定义结构体
首先，定义一个结构体来表示你的自定义类型。

```c
typedef struct {
    int some_property;
} MyCustomType;
```

### 2. 定义类型的函数
创建类型的相关函数，包括初始化、清理和其他必要的操作。

```c
static void my_custom_type_init(MyCustomType *self) {
    self->some_property = 0; // 初始化
}

static void my_custom_type_class_init(MyCustomTypeClass *klass) {
    // 类初始化代码
}
```

### 3. 注册类型
使用 `g_type_register_static` 或 `g_define_type` 宏来注册类型。

```c
G_DEFINE_TYPE(MyCustomType, my_custom_type, G_TYPE_OBJECT);
```

### 4. 使用类型
注册后，可以使用 `G_TYPE` 系列宏来创建和操作你的自定义类型。

```c
MyCustomType *obj = g_object_new(MY_CUSTOM_TYPE, NULL);
```

### 5. 编译和链接
确保在编译时链接到 GLib 库，并包含相应的头文件。

### 示例代码
以下是一个简单的完整示例：

```c
#include <glib-object.h>

typedef struct {
    GObject parent_instance;
    int some_property;
} MyCustomType;

G_DEFINE_TYPE(MyCustomType, my_custom_type, G_TYPE_OBJECT);

static void my_custom_type_init(MyCustomType *self) {
    self->some_property = 0;
}

static void my_custom_type_class_init(MyCustomTypeClass *klass) {
    // 类初始化
}

int main(int argc, char *argv[]) {
    g_type_init(); // 初始化类型系统
    MyCustomType *obj = g_object_new(MY_CUSTOM_TYPE, NULL);
    // 使用 obj
    g_object_unref(obj); // 释放对象
    return 0;
}
```

### 总结
通过以上步骤，你可以在 GLib 中成功注册和使用自定义类型。

# G_DECLARE_TYPE和G_DEFINE_TYPE的关系是什么

`G_DECLARE_TYPE` 和 `G_DEFINE_TYPE` 是 GLib 中用于定义自定义类型的宏，它们在类型系统中扮演不同的角色：

### 1. **G_DECLARE_TYPE**
- **作用**：用于声明一个类型的结构和类的定义。
- **使用场景**：通常在头文件中使用，以便其他文件可以引用该类型。
- **示例**：
  
  ```c
  G_DECLARE_FINAL_TYPE(MyCustomType, my_custom_type, MY, CUSTOM_TYPE, GObject);
  ```

### 2. **G_DEFINE_TYPE**
- **作用**：用于定义一个类型，包括初始化和类的实现。
- **使用场景**：在源文件中使用，实际实现类型的逻辑。
- **示例**：
  ```c
  G_DEFINE_TYPE(MyCustomType, my_custom_type, G_TYPE_OBJECT);
  ```

### 关系
- **结合使用**：`G_DECLARE_TYPE` 用于声明，而 `G_DEFINE_TYPE` 用于定义。通常在头文件中声明类型，在源文件中定义类型。
- **编译过程**：声明确保类型在其他模块中可见，而定义则提供具体的实现。

通过这两个宏，开发者可以方便地管理自定义类型的声明和定义，使代码结构更清晰。

# boxed type

```
G_DEFINE_BOXED_TYPE(WpProperties, wp_properties, wp_properties_ref, wp_properties_unref)

```

### 逐步分解

1. **G_DEFINE_BOXED_TYPE**
   - 这是一个宏，用于定义一个 boxed type。**Boxed type 是 GLib 中的一种类型，它可以被复制和引用计数，但不像对象那样有继承层次结构。**
2. **WpProperties**
   - 这是 boxed type 的名称，即我们定义的 boxed type 类型的名字。在这个例子中，`WpProperties` 是我们定义的 boxed type 的类型名。
3. **wp_properties**
   - 这是 boxed type 的小写形式名称，通常用于函数和变量命名。在这个例子中，`wp_properties` 是 `WpProperties` 的小写形式。
4. **wp_properties_ref**
   - 这是引用函数，用于增加 boxed type 实例的引用计数。在这个例子中，`wp_properties_ref` 是用于增加 `WpProperties` 实例引用计数的函数。
5. **wp_properties_unref**
   - 这是取消引用函数，用于减少 boxed type 实例的引用计数。当引用计数减少到零时，实例将被释放。在这个例子中，`wp_properties_unref` 是用于减少 `WpProperties` 实例引用计数的函数。

### 详细解释

- **G_DEFINE_BOXED_TYPE** 宏的作用是定义一个新的 boxed type，并为其生成必要的函数和类型信息。具体来说，它会生成以下内容：
  - 一个类型注册函数，用于在 GLib 类型系统中注册 `WpProperties` 类型。
  - 一个类型结构体，包含类型信息和函数指针。
  - 引用和取消引用函数，用于管理 `WpProperties` 实例的引用计数。
- **wp_properties_ref** 函数通常会调用 `g_ref_count_inc` 来增加引用计数，并返回增加引用计数后的实例。
- **wp_properties_unref** 函数通常会调用 `g_ref_count_dec` 来减少引用计数，并在引用计数减少到零时释放实例。



在 GLib 中，**boxed 类型**（Boxed Types）是指用户定义的复杂数据类型，它们通常不直接映射到 C 语言的基本数据类型。相较于简单的类型（如整数、字符等），boxed 类型允许开发者定义自己的数据结构，并在 GLib 的类型系统中注册和使用。

### 特点

1. **内存管理**: Boxed 类型通常由 GLib 提供的内存管理函数管理，这样可以确保在使用这些类型时避免内存泄漏或重复释放。

2. **封装**: Boxed 类型的数据被封装在一个指针中，这种封装提供了一种抽象方式，使得可以在不同的上下文中使用这些数据。

3. **自定义类型**: 开发者可以根据需要定义自己的数据结构，例如结构体，并通过 GLib 的机制将其注册为 boxed 类型。

### 如何定义 Boxed 类型

定义 boxed 类型一般包括以下几个步骤：

1. **定义结构体**: 创建一个 C 语言结构体来表示你的数据。

2. **实现复制和释放函数**: 实现用于复制和释放该数据类型的函数。

3. **注册类型**: 使用 GLib 宏（如 `G_DEFINE_BOXED_TYPE`）注册这个类型。

### 示例

以下是一个简单的 boxed 类型定义示例：

```c
#include <glib.h>

typedef struct {
    int x;
    int y;
} MyBoxedType;

G_DEFINE_BOXED_TYPE(MyBoxedType, my_boxed_type,
                     my_boxed_type_copy, my_boxed_type_free)

void my_boxed_type_copy(MyBoxedType *src, MyBoxedType *dest) {
    dest->x = src->x;
    dest->y = src->y;
}

void my_boxed_type_free(MyBoxedType *data) {
    g_free(data);
}
```

### 使用 Boxed 类型

在 `GValue` 中使用 boxed 类型，您可以像使用其他基本类型一样，以安全的方式存储和访问数据：

```c
GValue value = G_VALUE_INIT;
g_value_init(&value, MY_TYPE_BOXED);

MyBoxedType *data = g_new(MyBoxedType, 1);
data->x = 10;
data->y = 20;

g_value_set_boxed(&value, data);
MyBoxedType *retrieved_data = g_value_get_boxed(&value);

g_print("x: %d, y: %d\n", retrieved_data->x, retrieved_data->y);

// 记得释放内存
g_free(data);
g_value_unset(&value);
```

### 总结

Boxed 类型在 GLib 中允许开发者创建和管理复杂数据类型，提供了灵活性和安全性，尤其是在需要存储和处理自定义结构时。如果您还有其他问题，欢迎继续提问！

# gthread是不是不再推荐使用了？

是的，`gthread`在GLib中并不是推荐的线程处理方式。GLib提供了`GThread`用于基本的线程支持，但随着Glib和GTK的发展，推荐使用更高级的线程和并发机制。

### 现代推荐

1. **GAsyncQueue** 和 **GTask**：用于异步处理，适合处理需要在后台执行的任务。
2. **GMutex** 和 **GCond**：用于线程同步和条件变量，提供了更灵活的线程控制方式。
3. **GMainContext** 和 **GMainLoop**：用于事件驱动编程，能够处理异步事件和回调。

### 结论

虽然`gthread`仍然可用，但对于新项目，建议使用更现代的异步和事件驱动方法，以提高代码的可维护性和性能。如果你有更具体的使用场景或代码示例，可以提供更多细节，我可以帮助你更好地理解和选择合适的工具。

# GKeyFile

`GKeyFile` 是GTK+库中的一个数据结构，用于读写和管理INI风格的配置文件。它提供了一种方便的方式来存储和检索配置数据。

`GKeyFile` 的主要特点包括：

1. 支持INI风格的配置文件：`GKeyFile` 可以读写INI风格的配置文件，包括支持分组、键值对和注释。
2. 支持多种数据类型：`GKeyFile` 支持多种数据类型，包括字符串、整数、浮点数、布尔值等。
3. 支持本地化：`GKeyFile` 支持本地化，允许存储和检索不同语言的配置数据。
4. 支持列表和数组：`GKeyFile` 支持列表和数组数据类型，允许存储和检索多个值。

`GKeyFile` 的常用函数包括：

* `g_key_file_new()`: 创建一个新的 `GKeyFile` 对象。
* `g_key_file_load_from_file()`: 从文件中加载配置数据。
* `g_key_file_load_from_data()`: 从内存中加载配置数据。
* `g_key_file_get_string()`: 获取字符串值。
* `g_key_file_get_integer()`: 获取整数值。
* `g_key_file_get_boolean()`: 获取布尔值。
* `g_key_file_set_string()`: 设置字符串值。
* `g_key_file_set_integer()`: 设置整数值。
* `g_key_file_set_boolean()`: 设置布尔值。

`GKeyFile` 在GTK+应用程序中常用于存储和检索配置数据，例如用户设置、应用程序状态等。

# gslice介绍

`g_slice` 是 GLib 库中的一种内存分配机制，用于高效地分配和管理小块内存。

它是 GLib 库中的一部分，用于替代传统的 `malloc` 和 `free` 函数。

`g_slice` 的主要特点是：

1.  **高效的内存分配**：`g_slice` 使用一种称为 "切片" 的数据结构来管理内存块。切片是一种连续的内存块集合，每个切片都有相同的大小。这种结构使得 `g_slice` 可以高效地分配和释放内存块。
2.  **小块内存优化**：`g_slice`专门针对小块内存（通常小于几千字节）的分配进行了优化。它使用一种称为 "杂志" 的数据结构来管理小块内存，这种结构可以减少内存碎片和分配的开销。
3.  **线程安全**：`g_slice` 是线程安全的，这意味着多个线程可以同时使用 `g_slice` 来分配和释放内存块，而不会出现竞争条件或其他线程安全问题。
4.  **内存重用**：`g_slice` 会重用已经释放的内存块，以减少内存碎片和分配的开销。

`g_slice` 提供了以下函数来分配和释放内存块：

*   `g_slice_alloc`：分配一个新的内存块。
*   `g_slice_free`：释放一个已经分配的内存块。
*   `g_slice_alloc0`：分配一个新的内存块，并将其初始化为零。

`g_slice` 是 GLib 库中的一部分，用于替代传统的 `malloc` 和 `free` 函数。它提供了高效的内存分配和管理机制，特别适合于小块内存的分配和管理。



这段代码描述了GLib内存分配器（GSlice） 的实现原理。GSlice分为四层：

1. 线程杂志（Thread Magazines）：每个线程维护一个最近释放和即将分配的内存块列表。
2. 杂志缓存（Magazine Cache）：全局维护一个杂志缓存，用于分配和释放内存块。
3. Slab分配器（Slab Allocator）：分配大块内存，分成小块，用于满足上层分配请求。
4. 页分配器（Page Allocator）：使用posix_memalign或memalign分配内存块，或者使用valloc或malloc作为fallback。

这些层次的设计目的是为了提高内存分配效率，减少内存碎片，适应多线程和多CPU环境。

# PROP_0

在 GLib 库中，`PROP_0` 是一个常量，用作属性系统的占位符。它的主要作用是提供一个初始值，通常用于表示没有有效的属性 ID。

### 主要用途

1. **属性 ID 的起始值**：在定义属性时，`PROP_0` 可以作为属性 ID 的起始值，确保后续定义的属性都有唯一的 ID。

2. **简化代码**：使用 `PROP_0` 可以避免未初始化的属性 ID 导致的潜在错误。

3. **与 GObject 兼容**：在 GObject 的属性系统中，属性的 ID 从 1 开始，`PROP_0` 作为 0 使得代码在逻辑上更清晰。

### 示例

在定义属性时，通常会用到类似下面的代码：

```c
g_object_class_install_property(
    gobject_class,
    PROP_0, // 占位符
    g_param_spec_string("my-property", "My Property", "Description", NULL, G_PARAM_READWRITE));
```

### 小结

`PROP_0` 主要是为了保持属性系统的整洁和一致性，避免使用未初始化的属性 ID，确保代码的可读性和可维护性。

# g_steal_pointer函数的原理

`g_steal_pointer` 是 GLib 中的一个实用函数，用于管理指针的所有权。以下是它的基本原理和用途：

### 原理

- **所有权转移**：`g_steal_pointer` 接受一个指针参数，并返回该指针，同时将其所有权转移给调用者。这意味着调用者现在负责释放该指针所指向的内存，而原始指针被置为 `NULL`。

- **避免双重释放**：通过将原指针置为 `NULL`，`g_steal_pointer` 防止了在后续代码中意外释放同一内存区域，从而避免了潜在的双重释放错误。

### 用法

```c
#include <glib.h>

void example() {
    gpointer data = g_malloc(100); // 分配内存
    data = g_steal_pointer(&data);  // 转移所有权，原指针置为 NULL

    // 现在可以安全使用 data
    
    g_free(data); // 释放内存
}
```

### 适用场景

- **内存管理**：在需要将资源从一个地方转移到另一个地方时，`g_steal_pointer` 是一个方便的工具，特别是在处理动态内存分配时。

- **避免内存泄漏**：确保资源在转移后不会由于未正确管理而造成内存泄漏。

### 小结

`g_steal_pointer` 的设计旨在简化内存管理，使得指针的所有权转移更加安全和明确，是 GLib 提供的内存管理功能之一。

# g_clear_pointer

`g_clear_pointer` 是 GLib 中的一个实用函数，主要用于安全地释放指针所指向的内存。以下是它的基本原理和用途：

### 原理

- **释放内存**：`g_clear_pointer` 接受一个指向指针的指针（如 `gpointer*`）和一个释放函数（通常是 `g_free`），它会调用该释放函数来释放指针所指向的内存。

- **置空指针**：在释放内存后，`g_clear_pointer` 会将指针设置为 `NULL`，以避免悬空指针的出现。

### 用法

```c
#include <glib.h>

void example() {
    gpointer data = g_malloc(100); // 分配内存

    // 使用 data ...

    g_clear_pointer(&data, g_free); // 释放内存并置空指针

    // 此时 data 为 NULL，安全无误
}
```

### 适用场景

- **内存管理**：在需要释放动态分配的内存时，`g_clear_pointer` 提供了一种安全的方式，避免了手动管理指针可能带来的错误。

- **避免悬空指针**：通过将指针置为 `NULL`，可以有效避免后续对已释放内存的访问。

### 小结

`g_clear_pointer` 是一个便捷的内存管理工具，简化了指针的释放过程，并提高了代码的安全性和可维护性。它在 GLib 的内存管理中扮演着重要角色，特别是在处理动态内存时。

# G_DEFINE_AUTO_CLEANUP_CLEAR_FUNC

`G_DEFINE_AUTO_CLEANUP_CLEAR_FUNC` 是 GLib 中用于定义自动清理函数的宏。它的主要目的是简化资源管理，特别是在使用自动清理（auto-cleanup）机制时。

### 原理

- **自动清理**：该宏用于定义一个清理函数，该函数会在相应的自动清理类型被释放时被调用。这通常用于管理动态分配的内存或其他资源。

- **类型安全**：通过使用这个宏，确保清理函数与特定类型匹配，减少了类型不匹配的风险。

### 用法

一般来说，使用 `G_DEFINE_AUTO_CLEANUP_CLEAR_FUNC` 的步骤如下：

1. **定义清理函数**：首先定义一个清理函数，该函数负责释放或清理资源。

2. **使用宏定义**：使用 `G_DEFINE_AUTO_CLEANUP_CLEAR_FUNC` 来定义这个清理函数的自动清理行为。

### 示例

```c
#include <glib.h>

// 定义一个清理函数
void my_resource_clear(gpointer data) {
    g_free(data); // 释放内存
}

// 使用宏定义自动清理
G_DEFINE_AUTO_CLEANUP_CLEAR_FUNC(MyResource, my_resource_clear)

void example() {
    MyResource resource = g_new(gpointer, 1); // 分配资源
    // 使用 resource...

    // 当 resource 超出作用域时，会自动调用 my_resource_clear
}
```

### 适用场景

- **简化代码**：使用 `G_DEFINE_AUTO_CLEANUP_CLEAR_FUNC` 可以减少手动清理资源的代码，使得代码更加简洁和易于维护。

- **防止内存泄漏**：通过自动清理机制，确保资源在不再需要时被正确释放，降低了内存泄漏的风险。

### 小结

`G_DEFINE_AUTO_CLEANUP_CLEAR_FUNC` 是 GLib 提供的一个方便的宏，用于简化自动清理的实现，增强代码的可读性和安全性。在处理动态资源时，它是一个非常有用的工具。

# g_type_ensure

`g_type_ensure` 是 GLib 中的一个函数，用于确保特定类型（`GType`）已经被注册。它通常用于 GObject 类型系统，以确保在使用某个类型之前，该类型已经存在于系统中。

### 原理

- **类型检查**：`g_type_ensure` 接受一个 `GType` 参数，并检查该类型是否已经注册。如果未注册，它会自动注册该类型。

- **防止重复注册**：如果该类型已经注册，`g_type_ensure` 不会再次注册，从而避免了潜在的错误和资源浪费。

### 用法

典型的用法包括：

1. **确保类型存在**：在使用某个类型（如创建实例或访问属性）之前，调用 `g_type_ensure` 以确保该类型已经被注册。

2. **类型安全**：通过确保类型的存在，可以避免在运行时出现未定义行为。

### 示例

```c
#include <glib-object.h>

// 假设 MyType 是一个自定义类型
G_DEFINE_TYPE(MyType, my_type, G_TYPE_OBJECT)

void example() {
    g_type_ensure(MY_TYPE); // 确保 MyType 类型已注册

    MyType *instance = g_object_new(MY_TYPE, NULL); // 创建实例
    // 使用 instance...
}
```

### 适用场景

- **GObject 类型系统**：在使用自定义 GObject 类型时，确保类型的注册状态是很重要的。

- **动态插件**：在动态加载插件或模块时，确保相关类型已被注册。

### 小结

`g_type_ensure` 是 GLib 中的一个便利函数，用于确保特定类型已注册，避免类型未定义的错误，增强代码的安全性和稳定性。

# g_autofree 和g_autoptr区别

`g_autofree` 和 `g_autoptr` 是 GLib 中的两个宏，用于自动管理内存，但它们适用于不同的场景和类型。以下是它们的主要区别：

### g_autofree

- **用途**：`g_autofree` 用于普通指针，尤其是动态分配的内存（如使用 `g_malloc` 或 `g_new` 分配的内存）。

- **原理**：当使用 `g_autofree` 定义的指针超出作用域时，指向的内存会自动被释放，通常通过调用 `g_free()`。

- **示例**：

  ```c
  #include <glib.h>
  
  void example() {
      g_autofree gchar *data = g_malloc(100); // 自动管理的内存
      // 使用 data...
      // 超出作用域后，data 会被自动释放
  }
  ```

### g_autoptr

- **用途**：`g_autoptr` 用于 GObject 对象，确保对象的引用计数在超出作用域时自动减少。

- **原理**：当使用 `g_autoptr` 定义的 GObject 类型的指针超出作用域时，会自动调用 `g_object_unref()`，从而释放对象。

- **示例**：

  ```c
  #include <glib-object.h>
  
  void example() {
      g_autoptr(GObject) obj = g_object_new(G_OBJECT_TYPE, NULL); // 自动管理的 GObject
      // 使用 obj...
      // 超出作用域后，obj 会被自动释放
  }
  ```

### 主要区别

1. **适用类型**：
   - `g_autofree` 适用于普通指针（如 `gchar*`、`gint*` 等）。
   - `g_autoptr` 适用于 GObject 类型的指针。

2. **释放方式**：
   - `g_autofree` 通过 `g_free()` 来释放内存。
   - `g_autoptr` 通过调用 `g_object_unref()` 来管理 GObject 的引用计数。

### 小结

- 使用 `g_autofree` 来管理常规动态内存，使用 `g_autoptr` 来管理 GObject 对象。这两个宏都简化了内存管理，减少了手动释放的复杂性，降低了内存泄漏的风险。

# g_signal_connect_swapped的swapped怎么理解？

`g_signal_connect_swapped` 是 GLib/GObject 中用于连接信号的一个函数，与 `g_signal_connect` 类似，但其参数的顺序是反向的。这种“交换”意味着在信号发射时，回调函数的第一个参数和第二个参数被反转。

### 理解 `swapped`

- **标准连接**：通常使用 `g_signal_connect`，连接信号时，回调函数的第一个参数是发射信号的对象，第二个参数是信号的附加数据（如事件或者其他上下文信息）。

- **交换连接**：使用 `g_signal_connect_swapped` 时，回调函数的第一个参数是信号的附加数据，而第二个参数是发射信号的对象。这在某些情况下非常有用，特别是当你想要直接使用某些上下文信息而不需要引用发射对象时。

### 示例

假设你有一个按钮和一个回调函数，想要在按钮被点击时传递一些额外的数据：

```c
#include <gtk/gtk.h>

void on_button_clicked(gpointer data, GtkWidget *button) {
    g_print("Button clicked! Data: %s\n", (char *)data);
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    GtkWidget *window = gtk_window_new(GTK_WINDOW_TOPLEVEL);
    GtkWidget *button = gtk_button_new_with_label("Click me");

    // 使用 g_signal_connect_swapped
    g_signal_connect_swapped(button, "clicked", G_CALLBACK(on_button_clicked), "Hello, World!");

    gtk_container_add(GTK_CONTAINER(window), button);
    gtk_widget_show_all(window);
    
    g_signal_connect(window, "destroy", G_CALLBACK(gtk_main_quit), NULL);
    
    gtk_main();
    return 0;
}
```

### 输出示例

当你点击按钮时，输出将是：

```
Button clicked! Data: Hello, World!
```

### 总结

- **`g_signal_connect`**：第一个参数是发射信号的对象，第二个参数是附加数据。
- **`g_signal_connect_swapped`**：第一个参数是附加数据，第二个参数是发射信号的对象。

这种交换在某些情况下可以使代码更简洁，特别是当你只关心附加数据而不需要引用发射对象时。

# gobject的函数跟面向对象的c++的各个特性对比

GObject 是 GLib 的一部分，提供了一种面向对象的编程模型，用于 C 语言。尽管 C++ 是一种真正的面向对象语言，GObject 在 C 语言中实现了一些类似于 C++ 的特性。以下是 GObject 的一些功能与 C++ 的各个面向对象特性的比较：

### 1. 类和对象

- **C++**：使用 `class` 关键字定义类，通过构造函数创建对象。
  
  ```cpp
  class MyClass {
  public:
      MyClass() {} // 构造函数
  };
  
  MyClass obj;
  ```

- **GObject**：使用 `G_DEFINE_TYPE` 宏定义类，通过 `g_object_new()` 创建对象。

  ```c
  typedef struct {
      GObject parent_instance;
  } MyClass;
  
  G_DEFINE_TYPE(MyClass, my_class, G_TYPE_OBJECT);
  
  MyClass *obj = g_object_new(MY_TYPE_CLASS, NULL);
  ```

### 2. 继承

- **C++**：可以通过 `:` 继承类。

  ```cpp
  class Base {};
  class Derived : public Base {};
  ```

- **GObject**：通过 `G_DEFINE_TYPE` 的父类参数实现继承。

  ```c
  G_DEFINE_TYPE(Derived, derived, BASE_TYPE);
  ```

### 3. 封装

- **C++**：使用 `private` 和 `protected` 关键字控制访问权限。

  ```cpp
  class MyClass {
  private:
      int privateVar;
  };
  ```

- **GObject**：通过定义私有数据结构并在接口中隐藏它们实现封装。

  ```c
  typedef struct {
      int private_var; // 私有变量
  } MyClassPrivate;
  
  struct _MyClass {
      GObject parent_instance;
      MyClassPrivate *priv; // 指向私有数据
  };
  ```

### 4. 多态

- **C++**：使用虚函数实现多态。

  ```cpp
  class Base {
      virtual void func() {}
  };
  ```

- **GObject**：通过信号和虚函数表（VTable）实现多态。

  ```c
  void my_class_func(MyClass *self) {
      // 具体实现
  }
  ```

### 5. 方法和属性

- **C++**：使用类的方法访问和操作对象的属性。

  ```cpp
  class MyClass {
  public:
      void setValue(int v) { value = v; }
  private:
      int value;
  };
  ```

- **GObject**：通过 getter 和 setter 方法以及属性系统来访问和设置对象属性。

  ```c
  g_object_set(obj, "property-name", value, NULL);
  g_object_get(obj, "property-name", &value, NULL);
  ```

### 6. 信号和事件

- **C++**：使用回调函数和事件处理机制。

  ```cpp
  // 通过函数指针或 std::function 实现回调
  ```

- **GObject**：使用信号系统，允许对象发出信号并连接到回调函数。

  ```c
  g_signal_connect(obj, "signal-name", G_CALLBACK(callback_function), NULL);
  ```

### 7. 内存管理

- **C++**：使用构造函数和析构函数进行内存管理，支持 RAII。

  ```cpp
  class MyClass {
  public:
      ~MyClass() {} // 析构函数
  };
  ```

- **GObject**：使用引用计数管理对象的生命周期，通过 `g_object_unref()` 释放对象。

  ```c
  g_object_unref(obj);
  ```

### 总结

虽然 GObject 在 C 语言中实现了一些面向对象的特性，但与 C++ 的语法和功能相比，它的实现更为基础和繁琐。GObject 提供的面向对象特性包括类、继承、封装、多态、信号和属性等，使得 C 语言能够更好地支持面向对象的编程风格。

# GObjectClass主要函数

`GObjectClass` 是 GObject 类型系统中的一个结构体，用于定义 GObject 类型的类。它包含了多个函数指针，用于实现类的行为和特性。以下是 `GObjectClass` 中主要的函数和它们的用途：

### 主要函数

1. **`finalize`**
   - **类型**：`void (*finalize)(GObject *object);`
   - **说明**：在对象的生命周期结束时调用，用于释放对象所占用的资源。通常在自定义类型中重载，以清理私有数据。

2. **`get_property`**
   - **类型**：`void (*get_property)(GObject *object, guint prop_id, GValue *value, GParamSpec *pspec);`
   - **说明**：用于获取对象的属性值。当调用 `g_object_get()` 时，此函数将被调用。

3. **`set_property`**
   - **类型**：`void (*set_property)(GObject *object, guint prop_id, const GValue *value, GParamSpec *pspec);`
   - **说明**：用于设置对象的属性值。当调用 `g_object_set()` 时，此函数将被调用。

4. **`dispose`**
   - **类型**：`void (*dispose)(GObject *object);`
   - **说明**：在对象被销毁之前调用，用于释放可被重复使用的资源。与 `finalize` 不同，`dispose` 允许资源的重用。

5. **`class_init`**
   - **类型**：`void (*class_init)(MyClassClass *klass);`
   - **说明**：在类被创建时调用，用于初始化类的静态数据和方法。这是定义类的主要初始化函数。

6. **`instance_init`**
   - **类型**：`void (*instance_init)(GTypeInstance *instance, gpointer g_class);`
   - **说明**：在每个对象实例被创建时调用，用于初始化实例的状态和属性。

### 示例

下面是一个创建自定义 GObject 类型的示例，展示了如何定义和实现 `GObjectClass` 的主要函数：

```c
#include <glib-object.h>

typedef struct {
    GObject parent_instance;
    int my_property;
} MyObject;

typedef struct {
    GObjectClass parent_class;
} MyObjectClass;

G_DEFINE_TYPE(MyObject, my_object, G_TYPE_OBJECT)

static void my_object_finalize(GObject *object) {
    // 释放资源
    G_OBJECT_CLASS(my_object_parent_class)->finalize(object);
}

static void my_object_get_property(GObject *object, guint prop_id, GValue *value, GParamSpec *pspec) {
    MyObject *self = MY_OBJECT(object);
    switch (prop_id) {
        case 1: // 假设 1 是 my_property 的 ID
            g_value_set_int(value, self->my_property);
            break;
        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
            break;
    }
}

static void my_object_set_property(GObject *object, guint prop_id, const GValue *value, GParamSpec *pspec) {
    MyObject *self = MY_OBJECT(object);
    switch (prop_id) {
        case 1: // 假设 1 是 my_property 的 ID
            self->my_property = g_value_get_int(value);
            break;
        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
            break;
    }
}

static void my_object_class_init(MyObjectClass *klass) {
    GObjectClass *gobject_class = G_OBJECT_CLASS(klass);

    gobject_class->finalize = my_object_finalize;
    gobject_class->get_property = my_object_get_property;
    gobject_class->set_property = my_object_set_property;

    // 定义属性
    g_object_class_install_property(gobject_class, 1,
        g_param_spec_int("my-property", "My Property", "An integer property",
                         0, G_MAXINT, 0, G_PARAM_READWRITE));
}

static void my_object_instance_init(MyObject *self) {
    self->my_property = 0; // 初始化为默认值
}

int main() {
    g_type_init(); // 初始化 GType 系统

    MyObject *obj = g_object_new(MY_TYPE_OBJECT, "my-property", 42, NULL);
    int value;
    g_object_get(obj, "my-property", &value, NULL);
    g_print("My Property: %d\n", value); // 输出: My Property: 42

    g_object_unref(obj); // 释放对象
    return 0;
}
```

### 小结

`GObjectClass` 中的这些主要函数提供了对象的生命周期管理、属性访问、资源释放等功能，使得 GObject 类型能够有效地管理其状态和行为。通过实现这些函数，开发者可以创建功能丰富、可重用的 C 语言对象。

# constructed函数呢

在 GObject 中，`constructed` 函数是一个特定的虚拟函数，用于在对象实例被构造完成后调用。它用于执行对象构造的最后初始化步骤，通常在类的 `instance_init` 函数之后被调用。

### `constructed` 函数

- **定义**：
  - 类型：`void (*constructed)(GObject *object);`
  - 说明：这个函数在对象完全构造后被调用，允许开发者在构造完成后执行额外的初始化。

### 用法

1. **初始化完成**：在 `constructed` 中，你可以执行任何需要在对象所有初始化步骤完成后进行的操作，比如设置默认值、连接信号等。

2. **重载**：通常在类的初始化过程中重载这个函数，以添加具体的初始化逻辑。

### 示例

以下是一个使用 `constructed` 函数的示例：

```c
#include <glib-object.h>

typedef struct {
    GObject parent_instance;
    int value;
} MyObject;

typedef struct {
    GObjectClass parent_class;
} MyObjectClass;

G_DEFINE_TYPE(MyObject, my_object, G_TYPE_OBJECT)

static void my_object_constructed(GObject *object) {
    MyObject *self = MY_OBJECT(object);
    // 在对象构造完成后执行额外的初始化
    self->value = 100; // 设置默认值
    g_print("MyObject constructed! Value set to: %d\n", self->value);
}

static void my_object_class_init(MyObjectClass *klass) {
    GObjectClass *gobject_class = G_OBJECT_CLASS(klass);
    gobject_class->constructed = my_object_constructed; // 连接 constructed 函数
}

static void my_object_instance_init(MyObject *self) {
    // 这里可以设置其他初始化逻辑
}

int main() {
    g_type_init(); // 初始化 GType 系统

    MyObject *obj = g_object_new(MY_TYPE_OBJECT, NULL);
    // 此时会调用 constructed 函数，输出 "MyObject constructed! Value set to: 100"

    g_object_unref(obj); // 释放对象
    return 0;
}
```

### 小结

- `constructed` 函数在对象构造完成后被调用，允许开发者进行最后的初始化。
- 通过重载 `constructed` 函数，可以为对象提供额外的初始化逻辑，确保对象在使用前处于正确的状态。

这种机制使得 GObject 的对象构造更加灵活和可扩展。

# dispose函数

在 GObject 中，`dispose` 函数是一个重要的虚拟函数，用于资源管理和对象的生命周期管理。它允许开发者在对象被销毁之前执行清理操作，以释放资源或进行其他必要的处理。

### `dispose` 函数

- **定义**：
  - 类型：`void (*dispose)(GObject *object);`
  - 说明：该函数在对象被销毁之前调用，主要用于释放非必要的资源或进行清理操作。

### 主要特点

1. **资源释放**：`dispose` 函数通常用于释放可以被重用的资源，比如信号连接、动态分配的内存等。

2. **与 `finalize` 的区别**：
   - `dispose` 允许对象在被销毁之前释放资源，但对象仍然可以被重用。
   - `finalize` 函数在对象完全销毁时调用，主要用于释放对象的所有资源。当 `finalize` 被调用时，对象的状态不再可用。

3. **自动调用**：当对象的引用计数降至零时，`dispose` 和 `finalize` 会自动被调用。

### 示例

以下是一个使用 `dispose` 函数的示例：

```c
#include <glib-object.h>

typedef struct {
    GObject parent_instance;
    GList *connections; // 用于存储信号连接
} MyObject;

typedef struct {
    GObjectClass parent_class;
} MyObjectClass;

G_DEFINE_TYPE(MyObject, my_object, G_TYPE_OBJECT)

static void my_object_dispose(GObject *object) {
    MyObject *self = MY_OBJECT(object);

    // 释放信号连接
    for (GList *l = self->connections; l != NULL; l = l->next) {
        g_signal_handler_disconnect(l->data, GPOINTER_TO_INT(l->next->data));
    }
    g_list_free(self->connections);
    self->connections = NULL; // 防止悬挂指针

    // 调用父类的 dispose 方法
    G_OBJECT_CLASS(my_object_parent_class)->dispose(object);
}

static void my_object_class_init(MyObjectClass *klass) {
    GObjectClass *gobject_class = G_OBJECT_CLASS(klass);
    gobject_class->dispose = my_object_dispose; // 连接 dispose 函数
}

static void my_object_instance_init(MyObject *self) {
    self->connections = NULL; // 初始化连接列表
}

int main() {
    g_type_init(); // 初始化 GType 系统

    MyObject *obj = g_object_new(MY_TYPE_OBJECT, NULL);
    // 使用对象 ...

    g_object_unref(obj); // 释放对象，调用 dispose 和 finalize
    return 0;
}
```

### 小结

- `dispose` 函数是 GObject 生命周期管理中的一个关键部分，允许开发者在对象被销毁之前执行清理操作。
- 它与 `finalize` 不同，`dispose` 主要用于释放可重用的资源，而 `finalize` 用于完全清理对象状态。
- 通过实现 `dispose` 函数，开发者可以确保资源得以正确管理，避免内存泄漏和其他资源管理问题。

# g_param_spec_boxed

`g_param_spec_boxed` 是 GObject 中用于定义参数规格（`GParamSpec`）的一种方式，特别用于处理自定义的复合数据类型（boxed types）。这种参数规格允许对象的属性以自定义类型的形式存在。

### 主要特点

- **用途**：`g_param_spec_boxed` 主要用于定义属性，这些属性的值是自定义的 C 结构体类型，而不是基本数据类型（如整数、字符串等）。

- **数据管理**：使用 `g_param_spec_boxed`，可以确保 GObject 正确管理对象的属性，包括复制、比较和清理等。

### 函数原型

```c
GParamSpec* g_param_spec_boxed(const gchar *name,
                               const gchar *nick,
                               const gchar *blurb,
                               GType boxed_type,
                               GParamFlags flags);
```

### 参数说明

- **`name`**：属性的名称（字符串）。
- **`nick`**：属性的简短名称（字符串，通常用于用户界面）。
- **`blurb`**：属性的描述（字符串，提供额外信息）。
- **`boxed_type`**：自定义数据类型的 GType，必须是一个已经注册的 boxed type。
- **`flags`**：属性的标志，指示属性的可读性和可写性等特性（如 `G_PARAM_READWRITE`）。

### 示例

以下是如何使用 `g_param_spec_boxed` 定义一个自定义属性的示例：

```c
#include <glib-object.h>

typedef struct {
    int x;
    int y;
} MyBoxedType;

G_DEFINE_BOXED_TYPE(MyBoxedType, my_boxed_type, my_boxed_type_copy, my_boxed_type_free)

MyBoxedType* my_boxed_type_copy(MyBoxedType* boxed) {
    return g_new(MyBoxedType, 1);
}

void my_boxed_type_free(MyBoxedType* boxed) {
    g_free(boxed);
}

typedef struct {
    GObject parent_instance;
    MyBoxedType *position; // 使用自定义类型
} MyObject;

typedef struct {
    GObjectClass parent_class;
} MyObjectClass;

G_DEFINE_TYPE(MyObject, my_object, G_TYPE_OBJECT)

static void my_object_class_init(MyObjectClass *klass) {
    g_object_class_install_property(G_OBJECT_CLASS(klass),
                                    1,
                                    g_param_spec_boxed("position", 
                                                       "Position", 
                                                       "The position of the object", 
                                                       MY_TYPE_BOXED_TYPE, 
                                                       G_PARAM_READWRITE));
}

static void my_object_instance_init(MyObject *self) {
    self->position = g_new(MyBoxedType, 1); // 初始化
    self->position->x = 0;
    self->position->y = 0;
}

int main() {
    g_type_init(); // 初始化 GType 系统

    MyObject *obj = g_object_new(MY_TYPE_OBJECT, NULL);
    
    MyBoxedType *pos = g_new(MyBoxedType, 1);
    pos->x = 10;
    pos->y = 20;

    g_object_set(obj, "position", pos, NULL); // 设置属性

    g_object_unref(obj); // 释放对象
    return 0;
}
```

### 小结

- `g_param_spec_boxed` 用于定义 GObject 属性，以自定义的 boxed 类型作为属性值。
- 它确保属性的读写操作符合 GObject 的类型系统，提供了内存管理和数据复制等功能。
- 使用这种方式可以很好地集成复杂数据类型到 GObject 的属性系统中。

# G_DEFINE_TYPE 和G_DECLARE_TYPE必须成对出现吗

`G_DEFINE_TYPE` 和 `G_DECLARE_FINAL_TYPE`（或 `G_DECLARE_TYPE`）是 GObject 类型系统中的两个宏，它们通常是成对使用的，但并不是严格要求的。

### 说明

1. **`G_DECLARE_TYPE`/`G_DECLARE_FINAL_TYPE`**：
   - **作用**：用于声明一个 GObject 类型。这种声明让编译器知道这个类型的存在，并允许其他代码引用这个类型。
   - **使用场景**：在头文件中使用，以便其他模块可以使用该类型。

2. **`G_DEFINE_TYPE`**：
   - **作用**：用于定义一个 GObject 类型的实现，包括类型的初始化和注册。
   - **使用场景**：在源文件中使用，提供具体的实现细节。

### 成对使用的理由

- **声明和定义分离**：
  - 使用 `G_DECLARE_TYPE` 或 `G_DECLARE_FINAL_TYPE` 声明类型，可以在其他文件中引用这个类型，而不需要知道它的具体实现。
  - `G_DEFINE_TYPE` 提供了该类型的具体实现，通常是在实现文件中。

### 不是强制成对使用的情况

- **单独使用**：在某些情况下，如果你只需要定义一个类型而不打算在其他地方引用它，可能只需要使用 `G_DEFINE_TYPE`。但是，这种情况比较少见，因为大多数情况下，你会希望能够在其他模块中引用这个类型。

### 示例

以下是一个简单的示例，展示了如何使用这两个宏：

#### 头文件（`my_object.h`）

```c
#include <glib-object.h>

G_DECLARE_FINAL_TYPE(MyObject, my_object, MY, OBJECT, GObject)

struct _MyObject {
    GObject parent_instance;
    // 自定义字段
};
```

#### 源文件（`my_object.c`）

```c
#include "my_object.h"

G_DEFINE_TYPE(MyObject, my_object, G_TYPE_OBJECT)

static void my_object_class_init(MyObjectClass *klass) {
    // 类初始化逻辑
}

static void my_object_init(MyObject *self) {
    // 实例初始化逻辑
}
```

### 总结

- **通常成对使用**：为了保持类型的声明和定义分离，通常会在头文件和源文件中成对使用这两个宏。
- **不是严格要求**：在某些特定情况下，可以只使用其中一个宏，但这通常不符合 GObject 的最佳实践。

# G_DEFINE_ABSTRACT_TYPE_WITH_PRIVATE

`G_DEFINE_ABSTRACT_TYPE_WITH_PRIVATE` 是 GObject 中的一个宏，用于定义一个抽象类型，同时为该类型提供私有数据结构。这种宏常用于创建不能被实例化的基类，允许子类继承并实现具体的功能。

### 用法

`G_DEFINE_ABSTRACT_TYPE_WITH_PRIVATE` 结合了抽象类型的定义和私有数据的管理。以下是这个宏的基本结构和参数解释：

```c
G_DEFINE_ABSTRACT_TYPE_WITH_PRIVATE(TypeName, type_name, ParentType)
```

- **`TypeName`**：要定义的抽象类型的名称（大写）。
- **`type_name`**：类型的实例名称（小写）。
- **`ParentType`**：父类的 GType，表示这个抽象类型的基类。

### 主要特点

1. **抽象类型**：使用该宏定义的类型不能直接实例化，通常作为其他具体类型的基类。
2. **私有数据**：该宏会为类型自动生成一个私有数据结构，使得实现细节可以封装在实现文件中，防止外部直接访问。

### 示例

以下是一个使用 `G_DEFINE_ABSTRACT_TYPE_WITH_PRIVATE` 的示例，展示如何定义一个抽象类型和私有数据结构。

#### 1. 头文件（`my_abstract.h`）

```c
#include <glib-object.h>

G_DECLARE_ABSTRACT_TYPE(MyAbstract, my_abstract, MY, ABSTRACT)

struct _MyAbstractClass {
    GObjectClass parent_class;

    void (*my_method)(MyAbstract *self); // 抽象方法
};

// 定义私有数据结构
typedef struct {
    int some_private_data;
} MyAbstractPrivate;

G_DEFINE_ABSTRACT_TYPE_WITH_PRIVATE(MyAbstract, my_abstract, G_TYPE_OBJECT)
```

#### 2. 源文件（`my_abstract.c`）

```c
#include "my_abstract.h"

static void my_abstract_class_init(MyAbstractClass *klass) {
    // 类初始化逻辑
}

static void my_abstract_init(MyAbstract *self) {
    MyAbstractPrivate *priv = my_abstract_get_instance_private(self);
    priv->some_private_data = 0; // 初始化私有数据
}
```

#### 3. 具体实现（`my_implementation.c`）

```c
#include "my_abstract.h"

typedef struct {
    MyAbstract parent_instance;
    // 其他实现特有的数据
} MyImplementation;

void my_implementation_my_method(MyAbstract *self) {
    MyAbstractPrivate *priv = my_abstract_get_instance_private(self);
    g_print("Private data: %d\n", priv->some_private_data);
}

G_DEFINE_TYPE(MyImplementation, my_implementation, MY_TYPE_ABSTRACT)

static void my_implementation_class_init(MyImplementationClass *klass) {
    MyAbstractClass *abstract_class = MY_ABSTRACT_CLASS(klass);
    abstract_class->my_method = my_implementation_my_method; // 实现抽象方法
}

static void my_implementation_init(MyImplementation *self) {
    MyAbstractPrivate *priv = my_abstract_get_instance_private(self);
    priv->some_private_data = 42; // 设置私有数据
}
```

### 使用示例

在 `main` 函数中，你可以创建具体的实现并调用其方法：

```c
int main() {
    g_type_init(); // 初始化 GType 系统（在新版本中通常不需要）

    MyImplementation *impl = g_object_new(MY_TYPE_IMPLEMENTATION, NULL);
    MyAbstractClass *abstract_class = MY_ABSTRACT_CLASS(impl);

    abstract_class->my_method(impl); // 调用实现的方法

    g_object_unref(impl); // 释放对象
    return 0;
}
```

### 总结

- `G_DEFINE_ABSTRACT_TYPE_WITH_PRIVATE` 允许你定义一个抽象类型，并在其内部管理私有数据。
- 这种方式有助于封装实现细节，增强代码的可维护性和可扩展性，特别是在面向对象的编程中。

# GTask

```c
#include <glib.h>
#include <gio/gio.h>
typedef struct {
    int number;
    GTask *task;
} TaskData;

void compute_square(
    GTask *task,
    gpointer source_object,
    gpointer task_data,
    GCancellable *cancellable
)
{
    TaskData *data = (TaskData *)task_data;
    int result = data->number * data->number;
    g_usleep(1000*1000);
    g_task_return_int(task, result);
}
void on_task_completed(
    GObject *source_object,
    GAsyncResult *res,
    gpointer userdata
)
{
    GError *error = NULL;
    int result = g_task_propagate_int(G_TASK(res), &error);
    if (error) {
        g_printerr("Error:%s\n", error->message);
        g_error_free(error);
    } else {
        g_printf("The square is:%d\n", result);
    }
}
int main() {
    g_type_init();
    GTask *task;
    TaskData data = {
        .number = 5,
        .task = NULL
    };
    task = g_task_new(
        NULL, NULL,
        on_task_completed,
        NULL
    );
    g_task_set_task_data(task, &data, NULL);
    g_printf("before run \n");
    g_task_run_in_thread(task, compute_square);
    g_object_unref(task);
    g_printf("after unref\n");
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);
    g_main_loop_run(loop);
    g_main_loop_unref(loop);
    return 0;
}


```

编译：

```
gcc -o async_task_example async_task_example.c `pkg-config --cflags --libs gio-2.0 glib-2.0`
```



这个代码片段定义了几个宏常量，用于控制任务池（task pool）的大小和等待时间。

当任务池满了并阻塞时，程序会逐渐添加更多的线程到池中，直到任务开始完成。这些“溢出”线程只会运行一个任务，然后退出，因此池的大小最终会回到基础大小。

这些宏常量的值如下：

*   `G_TASK_POOL_SIZE`: 任务池的初始大小，设为 10。
*   `G_TASK_WAIT_TIME_BASE`: 等待时间的基数，设为 100000（单位为微秒）。
*   `G_TASK_WAIT_TIME_MULTIPLIER`: 等待时间的乘数，设为 1.03。
*   `G_TASK_WAIT_TIME_MAX_POOL_SIZE`: 最大池大小，设为 330。

这些值的组合可以实现以下效果：

*   大约 1 秒钟后，池大小增加 10 个线程。
*   大约 5 秒钟后，池大小增加 30 个线程。
*   大约 1 分钟后，池大小增加 100 个线程。
*   大约 20 分钟后，池大小增加 200 个线程。

最大池大小为 330，可以让等待时间增加到大约 30 分钟。

# g_main_context_get_thread_default和g_main_context_default区别

`g_main_context_get_thread_default()` 和 `g_main_context_default()` 是 GLib 中用于处理主循环的两个不同函数，主要用于获取 `GMainContext` 的实例，但它们的用途和上下文有所不同。

### 1. `g_main_context_default()`

- **用途**：返回全局的默认 `GMainContext` 实例。
- **线程安全**：该函数返回的 `GMainContext` 是与主线程相关的，通常用于 GUI 应用程序或需要处理主事件循环的场景。
- **示例**：
  ```c
  GMainContext *context = g_main_context_default();
  ```

### 2. `g_main_context_get_thread_default()`

- **用途**：返回当前线程的默认 `GMainContext` 实例。
- **线程安全**：这个函数非常重要，因为在多线程程序中，每个线程可能有自己的主上下文。调用此函数可以获取与当前线程相关的上下文。
- **示例**：
  ```c
  GMainContext *context = g_main_context_get_thread_default();
  ```

### 主要区别

- **上下文**：
  - `g_main_context_default()` 提供的是全局的默认上下文，适用于单线程或主线程处理。
  - `g_main_context_get_thread_default()` 提供的是特定于调用线程的上下文，适合多线程环境。

- **使用场景**：
  - 如果你的应用程序是单线程的，通常使用 `g_main_context_default()`。
  - 如果你的应用程序是多线程的，并且每个线程可能会处理事件，应该使用 `g_main_context_get_thread_default()` 来确保你获取到该线程的正确上下文。

### 例子

在多线程编程中，你可能会在不同的线程中使用 `g_main_context_get_thread_default()` 来确保事件处理是正确的：

```c
#include <glib.h>
#include <glib/gprintf.h>

void thread_function() {
    GMainContext *context = g_main_context_get_thread_default();
    // 使用这个上下文进行事件处理
}

int main() {
    GThread *thread = g_thread_new("my_thread", (GThreadFunc)thread_function, NULL);
    g_thread_join(thread);
    return 0;
}
```

### 总结

- 使用 `g_main_context_default()` 获取全局的默认上下文，适合单线程。
- 使用 `g_main_context_get_thread_default()` 获取当前线程的上下文，适合多线程应用程序。选择合适的函数可以帮助确保事件处理的正确性和有效性。



# **GMainDispatch**

`GMainDispatch` 是 GLib 中的一个概念，通常与 `GMainContext` 和 `GMainLoop` 一起使用，涉及事件的调度和处理。以下是对 `GMainDispatch` 的详细介绍。

### GMainDispatch 的作用

- **事件调度**：`GMainDispatch` 负责在事件循环中调度和执行回调函数，允许应用程序响应各种事件，例如 I/O 事件、定时器和信号。
- **异步处理**：它使得异步操作能够在主循环中被处理，而不阻塞主线程，确保应用程序的响应性。

### 主要组件

1. **GMainContext**:
   - 这是事件的上下文，负责管理事件源（如文件描述符、定时器等）及其相关的回调。
   - `GMainDispatch` 在此上下文中运行，处理所有调度的事件。

2. **GMainLoop**:
   - 这是一个包含 `GMainContext` 的循环结构，通常用于运行主事件循环。
   - 通过调用 `g_main_loop_run()` 启动事件循环，进入调度和处理状态。

### 使用示例

以下是一个简单的示例，展示如何在主事件循环中使用 `GMainDispatch` 来处理定时器事件。

```c
#include <glib.h>
#include <glib/gprintf.h>

gboolean timeout_callback(gpointer user_data) {
    g_printf("Timeout occurred!\n");
    return G_SOURCE_CONTINUE; // 返回 TRUE 以继续调用此回调
}

int main() {
    GMainLoop *loop = g_main_loop_new(NULL, FALSE);

    // 添加一个定时器事件，每秒调用一次
    g_timeout_add_seconds(1, timeout_callback, NULL);

    // 运行主循环
    g_main_loop_run(loop);

    // 释放主循环
    g_main_loop_unref(loop);
    return 0;
}
```

### 编译命令

确保链接 GLib 库，并使用以下命令编译：

```bash
gcc -o main_dispatch_example main_dispatch_example.c `pkg-config --cflags --libs glib-2.0`
```

### 总结

- **GMainDispatch** 是 GLib 中的一个重要概念，负责调度和处理事件。
- 它与 `GMainContext` 和 `GMainLoop` 一起使用，确保异步操作能够在主事件循环中被有效处理。
- 通过使用定时器、I/O 事件等，`GMainDispatch` 能够帮助开发者构建响应式的应用程序。

# GLibPrivateVTable

这是一个C语言结构体的定义，名为`GLibPrivateVTable`。这个结构体包含了许多函数指针，用于访问GLib库的私有函数。这些函数指针被分组到不同的类别中，如`gwakeup.c`、`gmain.c`、`glib-init.c`等，表明它们与相应的源文件相关。

这个结构体的作用是提供一个统一的接口，允许其他部分的代码访问GLib库的私有函数，而不需要直接包含这些函数的源文件。通过这种方式，可以实现模块化和封装，提高代码的可维护性和可重用性。

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