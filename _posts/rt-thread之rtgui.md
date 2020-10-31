---
title: rt-thread之rtgui
date: 2020-10-28 15:05:30
tags:
	- rt-thread
---

1

demo程序逻辑：

```
//创建app
struct rtgui_app *app = rtgui_app_create("gui_demo");
//创建window
struct rtgui_win *main_win = rtgui_mainwin_create(RT_NULL, "UiWindow", RTGUI_WIN_STYLE_NO_TITLE);
//设置事件处理
rtgui_object_set_event_handler(RTGUI_OBJECT(main_win), dc_event_handler);
//设置显示
rtgui_win_show(main_win, RT_FALSE);
//运行
rtgui_app_run(app);
//销毁
rtgui_win_destroy(main_win);
rtgui_app_destroy(app);
```

点：

```
struct rtgui_point
{
    rt_int16_t x, y;
};
```

线：

```
struct rtgui_line
{
    rtgui_point_t start, end;
};
```

面：

```
struct rtgui_rect
{
    rt_int16_t x1, y1, x2, y2;
};
```

颜色：

```
typedef unsigned long rtgui_color_t;
```

图形上下文

```
struct rtgui_gc
{
    /* foreground and background color */
    rtgui_color_t foreground, background;

    /* text style */
    rt_uint16_t textstyle;
    /* text align */
    rt_uint16_t textalign;

    /* font */
    struct rtgui_font *font;
};
```

重要的头文件。

```
rtgui_app.h  
	rtgui_app结构体及函数。
rtgui_config.h  
	配置。
rtgui_object.h  
	rtgui_object一切rtgui对象的父类。
	它自己没有继承rt_object。
	风格有点像gobject。
	依靠宏展开来定义	DEFINE_CLASS_TYPE
rtgui_server.h  
rtgui_system.h
```

我先只分析demo里用到的东西。

rtgui_app

rtgui_object

```
只有4个成员
type：一个指针，指向静态的结构体。
event_handler。事件处理。
flag：枚举。
id
```



rtgui_server_app

这个是C/S架构的吗？

这个会提前初始化。

```
int rtgui_system_server_init(void)
{
    rt_mutex_init(&_screen_lock, "screen", RT_IPC_FLAG_FIFO);

    /* init image */
    rtgui_system_image_init();
    /* init font */
    rtgui_font_system_init();

    /* init rtgui server */
    rtgui_topwin_init();
    rtgui_server_init();

    /* use driver rect for main window */
    rtgui_graphic_driver_get_rect(rtgui_graphic_driver_get_default(), &_mainwin_rect);

    return 0;
}
```



参考资料

