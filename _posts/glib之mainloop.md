---
title: glib之mainloop
date: 2019-08-07 18:01:19
tags:
	- glib

---

1

GMainContext代表了一组被一个mainloop处理的资源。

GMainLoop代表glib或者gtk应用里的主事件循环。

GSource代表了一个事件源。

本质还是select这种机制。

最简单的例子。

```
#include <glib.h>
#include <stdio.h>
#include <unistd.h>

gboolean idle_proc(gpointer userdata)
{
    printf("idle print\n");
}
int main()
{
    GMainLoop *loop = g_main_loop_new(NULL, TRUE);//如果这里是FALSE，那么就不会执行。
    g_idle_add(idle_proc, NULL);
    g_main_loop_run(loop);
}
```

Makefile这样写：

```
CFLAGS:=`pkg-config --cflags --libs gobject-2.0 `
all:
	gcc test.c $(CFLAGS)
```

运行效果是一直打印idle print。

修改一些，打印一些次数后，停止打印。

```
#include <glib.h>
#include <stdio.h>
#include <unistd.h>
int count = 0;
gint source_id = 0;
gboolean idle_proc(gpointer userdata)
{
    printf("idle print:%d\n", count++);
    if(count > 5) {
        g_source_remove(source_id);//靠这个remove来做到。
        printf("remove idle proc\n");
    }
}
int main()
{
    GMainLoop *loop = g_main_loop_new(NULL, TRUE);
    source_id = g_idle_add(idle_proc, NULL);
    g_main_loop_run(loop);
    printf("end of code\n");
}

```



参考资料

1、

