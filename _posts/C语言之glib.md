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



# 实用功能

glib包含了近20种实用功能。从简单的字符串处理到xml解析。

现在我们看看随机数和计时的。



# 实现异步

g_idle_add，添加一个空闲时执行的任务。

是被main_loop执行的。

gtk就是通过这些方式来刷新屏幕的。

串行化对ui的操作。



# 参考资料

1、浅析GLib

https://www.ibm.com/developerworks/cn/linux/l-glib/index.html

2、glib中的signal不是异步的，使用g_idle_add实现异步

https://blog.csdn.net/fingding/article/details/6866263