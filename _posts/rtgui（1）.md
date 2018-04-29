---
title: rtgui（一）
date: 2018-04-28 20:47:52
tags:
	- rt-thread
typora-root-url: ..\
---



现在开始看rtgui。

实验环境是qemu里运行rt-thread。vexpress-a9的板子。

先跑起来看看。

我在menuconfig里选配上rtgui。就用默认配置，不打开多余的配置。

然后在Ubuntu的图形界面下运行。

默认效果是这样的。

![](/images/rtgui（一）-默认例子.png)

我们看看是怎么跑出这个效果的。

搜索一下，

```
teddy@teddy-ubuntu:~/work/rt-thread$ grep -nwr "Hello RT-thread" .
./rt-thread/components/gui/example/gui_demo.c:59:        char *text_buf = "Hello RT-thread!";
```

示例的入口是这样：

```
int rt_gui_demo_init(void)
{
    rt_thread_t tid;
    
    tid = rt_thread_create("mygui",
        rt_gui_demo_entry, RT_NULL,
        2048, 25, 10);

    if (tid != RT_NULL)
        rt_thread_startup(tid);

    return 0;
}
INIT_APP_EXPORT(rt_gui_demo_init);
```

还支持鼠标操作的。

```
[ DBG][line]:117 motion event id:202199 x:799 y:479
[ DBG][line]:117 motion event id:202199 x:799 y:479
[ DBG][line]:154 up event id:202199 x:799 y:479
[ DBG][line]:117 motion event id:202199 x:799 y:479
[ DBG][line]:136 down event id:205257 x:799 y:479
[ DBG][line]:117 motion event id:205257 x:799 y:479
[ DBG][line]:117 motion event id:205257 x:799 y:479
[ DBG][line]:154 up event id:205257 x:799 y:479
[ DBG]flag:0x00000084 value:0x11 key:UNKNOWN status:DOWN
[ DBG]flag:0x00000080 value:0x11 key:UNKNOWN status:UP
```

鼠标的代码在：

```
./bsp/qemu-vexpress-a9/drivers/drv_mouse.c:136:    dbg_log(DBG_LOG, "[line]:%d down event id:%d x:%d y:%d\n", __LINE__, emouse.id, x, y);
```

鼠标是PL050。应该是ARM的标准。

rtgui的系统入口是在rtgui_system.c里。

rtgui_server_init



手动定义#define RTGUI_USING_MOUSE_CURSOR

但是还是看不到鼠标的图形。

我在qemu的启动命令里加上：

```
-show-cursor
```

这样就可以显示了鼠标图形了。



```
teddy@teddy-ubuntu:~/work/rt-thread/rt-thread/components/gui$ tree include/ src
include/
├── rtgui
│   ├── blit.h
│   ├── color.h
│   ├── dc_draw.h
│   ├── dc.h
│   ├── dc_trans.h
│   ├── driver.h
│   ├── event.h
│   ├── filerw.h
│   ├── font_fnt.h
│   ├── font_freetype.h
│   ├── font.h
│   ├── image_bmp.h
│   ├── image_container.h
│   ├── image.h
│   ├── image_hdc.h
│   ├── kbddef.h
│   ├── list.h
│   ├── matrix.h
│   ├── region.h
│   ├── rtgui_app.h
│   ├── rtgui_config.h
│   ├── rtgui.h
│   ├── rtgui_object.h：这个是最基础的。
│   ├── rtgui_server.h
│   ├── rtgui_system.h
│   ├── tree.h
│   └── widgets
│       ├── box.h
│       ├── container.h
│       ├── title.h
│       ├── widget.h
│       └── window.h
└── SConscript
src
├── asc12font.c
├── asc16font.c
├── blit.c
├── box.c
├── color.c
├── container.c
├── dc_blend.c
├── dc_buffer.c
├── dc.c
├── dc_client.c
├── dc_hw.c
├── dc_rotozoom.c
├── dc_trans.c
├── filerw.c
├── font_bmp.c
├── font.c
├── font_fnt.c
├── font_freetype.c
├── font_hz_bmp.c
├── font_hz_file.c
├── hz12font.c
├── hz16font.c
├── image_bmp.c
├── image.c
├── image_container.c
├── image_hdc.c
├── image_jpg.c
├── image_png.c
├── image_xpm.c
├── matrix.c
├── mouse.c
├── mouse.h
├── region.c
├── rtgui_app.c
├── rtgui_driver.c
├── rtgui_object.c
├── rtgui_system.c
├── SConscript
├── server.c
├── title.c
├── topwin.c
├── topwin.h
├── widget.c
└── window.c
```



```
rtgui_object
rtgui_type_t

```



截图出来。

finsh里有个screenshot(“/test.bmp")。截图出来。可以在windows里打开。

