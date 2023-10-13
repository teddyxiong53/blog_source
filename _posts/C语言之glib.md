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