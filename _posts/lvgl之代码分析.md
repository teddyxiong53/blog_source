---
title: lvgl之代码分析
date: 2021-08-11 16:54:33
tags:
	- gui

---

--

代码目录结构分析，以v8.0.0为分析对象。

```
docs： md格式的文档，比较齐全。官网的就是这些文件生成的。直接看官网的就好了。
examples：例子程序。
scripts：工具脚本。
src
tests
```

编译可以是make和cmake的。

如果要做一个完整的程序，可以参考这个linuxfb的例子。

https://github.com/lvgl/lv_port_linux_frame_buffer

对我的头文件，就一个lvgl.h。

src目录

```
core：lv_obj、lv_obj_class这些基础结构体和函数
draw：就是fill-rect这些东西。
extra：控件那些就在这个下面。
	layouts：有flex和grid这2个。
	others：snapshot。
	themes：basic、default、mono
	widgets：控件都在这里。
font
	把字体的转成了c文件的。
gpu
	硬件加速的。
hal
	硬件抽象层。
misc
	log、async这些基础设施。
widgets
	跟extra目录下的是什么关系？
```



这个3个结构体就是系统的根基

```
struct _lv_obj_t;
struct _lv_obj_class_t;
struct _lv_event_t;
```

基本对象属性：就是所有空间都有的。

```
pos
size
parent
style
event handler
```

对象的属性可以用lv_obj_set_size这样的接口来设置。

通过lv_obj_get_size这样的接口来获取。

特殊属性，某些控件特有的属性。

例如slider特有的。就用类似lv_slider_set_range这样的接口来设置。

创建和删除对象：

lv_xx_create

lv_obj_del



# screen对象

screen对象特殊在于，它没有parent。

创建是这样：

```
lv_obj_t * scr1 = lv_obj_create(NULL);
```

相关接口是：lv_scr_xx



# layer

有2个自动生成的layer。

top layer

system layer

这2个layer是跟screen无关的。

top layer是在所有屏幕上object之上的

而system layer则还在top layer之上。

你可以在top layer上显示popup的窗口。

system layer则只能放系统的东西，例如鼠标。

lvgl默认是采取覆盖的策略。



可以在load screen的时候带上动画。



使用css的盒模型概念。

# event

给对象添加事件

```
lv_obj_t * btn = lv_btn_create(lv_scr_act());
lv_obj_add_event_cb(btn, my_event_cb, LV_EVENT_CLICKED, NULL);   /*Assign an event callback*/

...

static void my_event_cb(lv_event_t * event)
{
    printf("Clicked\n");
}
```

# fbdev

头文件对外只提供了4个接口：

```
init
exit：就一行，调用close fd。
flush：这个感觉是主要接口，但是为什么没有找到调用的地方。
get_size：就是把宽高信息给出去。
```

init逻辑

```
1、打开fb设备，得到fd。
2、得到fix info和var info。
3、mmap显示内存。然后清空。

这个只是设备，不是驱动。
```

flush是靠这里注册进去的。

```
/*Initialize and register a display driver*/
    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);  这个没有做什么，就是memset了一下，给几个成员赋值。
    disp_drv.draw_buf   = &disp_buf;
    disp_drv.flush_cb   = fbdev_flush;//这个是重点。
    disp_drv.hor_res    = 720;
    disp_drv.ver_res    = 720;
    lv_disp_drv_register(&disp_drv);
```

flush函数逻辑：

```
2个参数：一个area，一个是color。
这参数很简单。
不是color，是相当于显示数据指针
执行一次memcpy，就没有了。就这么简单。
```

# evdev

对外接口也很简单，就2个：

evdev_init：就是打开对应的/dev/input/event1

evdev_read：读取输入数据。

## touchscreen的校正

很简单的逻辑，就是一个偏移相减。不知道在实际中是否够用。



# timer

刷新屏幕，是靠这个定时器来做的。

```
disp->refr_timer = lv_timer_create(_lv_disp_refr_timer, LV_DISP_DEF_REFR_PERIOD, disp);
```

# display buffer

当前buffer给这么大的。128K的。

```c
/*A small buffer for LittlevGL to draw the screen's content*/
    static lv_color_t buf[DISP_BUF_SIZE];

    /*Initialize a descriptor for the buffer*/
    static lv_disp_draw_buf_t disp_buf;
    lv_disp_draw_buf_init(&disp_buf, buf, NULL, DISP_BUF_SIZE);
```

这个buffer具体是怎么被使用的？大小决定的依据是什么？

lv_disp_draw_buf_init 函数可以接受2个buf。

所以就可能有这么几种情况：

1、只给一个buf。当前就是这种情况。buf可以比屏幕小，这样就需要绘制多次。

2、给2个buf，且buf的大小跟屏幕大小不一致。就是一个双缓冲机制。

3、给2个buf，且buf的大小跟屏幕一致。这种方式是最高效的。

但是我对比了一下，用benchmark测试了一下，并没有提高性能。

所以，还是维持之前的吧。



# style

这个我觉得是非常核心的一个部分。

style枚举的分组

```
分组0：空间信息，宽高尺寸
width
min width
max width
height及min、max
x、y
align
transform width、height、x、y、zoom、angle。

分组1：pad信息
pad top/bottom/left/right/row/colume

分组2：bg信息
bg color/opa/img/

分组3：border信息和outline信息
border color/opa/width/side/post
outline width/color/opa/pad

分组4：shadow信息、img信息、line信息
shadow width/offset/spread/color/opa
img opa/recolor
line width/color/opa

分组5：arc信息、text信息
arc width/color/opa
text color/opa/font/decor/align/letter space/line space

分组6：其他
radius
opa
anim
blend
layout
base_dir
```

## lv_style_t结构体

```
uint16_t prop1 :15; 对应属性的那个枚举。
uint16_t is_const :1;
uint8_t has_group;
uint8_t prop_cnt;
除了上面这4个属性，另外就是主要的一个属性。
v_p
是一个union类型。
union {
        lv_style_value_t value1;
        uint8_t * values_and_props;
        const lv_style_const_prop_t * const_props;
    } v_p;
```

主要就是这个类型

```
typedef struct {
    lv_style_prop_t prop;//就是枚举
    lv_style_value_t value;//一个union，包括3种可能：int、void *、lv_color_t
} lv_style_const_prop_t;
```

2个重要接口

```
void lv_style_set_prop(lv_style_t * style, lv_style_prop_t prop, lv_style_value_t value);
lv_res_t lv_style_get_prop(lv_style_t * style, lv_style_prop_t prop, lv_style_value_t * value);
```

有一个h文件和c文件是脚本生成的。

lv_style_gen.h、lv_style_gen.c。

里面的函数是这样的：

```
void lv_style_set_width(lv_style_t * style, lv_coord_t value);
void lv_style_set_min_width(lv_style_t * style, lv_coord_t value);
void lv_style_set_max_width(lv_style_t * style, lv_coord_t value);
```

# theme

在extra/themes目录下，有3个子目录

basic

default

mono

代表了3种主题。

## 结构体lv_theme_t

```
三种字体，
const lv_font_t * font_small;
const lv_font_t * font_normal;
const lv_font_t * font_large;
2种色调
lv_color_t color_primary;
lv_color_t color_secondary;
```

函数：

lv_theme_default_init

lv_theme_default

lv_theme_mono：这个是单色的，应该是只有黑白。

lv_theme_basic

这3个的区别是什么？

对外的接口，都是一个lv_theme_xx_init。

内部实现，复杂一些的就是theme_apply函数。这个是在修改theme的时候被回调到。



# core部分代码

## lv_disp

函数以lv_disp_开头，函数的参数有lv_disp_t *disp。

## lv_event

事件枚举

```
==========input事件
pressed
pressing
press_lost
short_clicked
long_pressed
long_pressed_repeat
clicked
released
scroll_begin
scroll_end
scroll
gesture
key
focused
defocused
leave
=======绘制事件
draw_main_begin
draw_main
draw_main_end
post_begin
post
post_end
part_begin
part_end

========特殊事件
value_changed
insert
refresh
ready
cancel
=========其他事件
delete
child_changed
size_changed
style_changed
layout_changed
get_self_size
```

lv_event_t

```
lv_event_code_t 事件枚举
事件的目标对象
struct _lv_obj_t * target;
struct _lv_obj_t * current_target;
```

主要接口：

lv_event_send

## lv_obj



# 颜色

颜色深度的宏

透明度枚举，从0到100%，10%为一个步进值。

调色板，就是预设的各种颜色吧。

# lv_style_t

属性键值对。可以看做css。



# grid desc

这个具体是指什么？

分析lv_demo_widgets里的代码。

这个是如何对布局进行指定的？

```
if(disp_size == DISP_LARGE) {
        static lv_coord_t grid_main_col_dsc[] = {LV_GRID_FR(1), LV_GRID_FR(1), LV_GRID_TEMPLATE_LAST};
        static lv_coord_t grid_main_row_dsc[] = {LV_GRID_CONTENT, LV_GRID_CONTENT, LV_GRID_TEMPLATE_LAST};

        /*Create the top panel*/
        static lv_coord_t grid_1_col_dsc[] = {LV_GRID_CONTENT, 5, LV_GRID_CONTENT, LV_GRID_FR(2), LV_GRID_FR(1), LV_GRID_FR(1), LV_GRID_TEMPLATE_LAST};
        static lv_coord_t grid_1_row_dsc[] = {LV_GRID_CONTENT, LV_GRID_CONTENT, 10, LV_GRID_CONTENT, LV_GRID_CONTENT, LV_GRID_TEMPLATE_LAST};

        static lv_coord_t grid_2_col_dsc[] = {LV_GRID_FR(1), LV_GRID_FR(1), LV_GRID_TEMPLATE_LAST};
        static lv_coord_t grid_2_row_dsc[] = {
                LV_GRID_CONTENT,  /*Title*/
                5,                /*Separator*/
                LV_GRID_CONTENT,  /*Box title*/
                30,               /*Boxes*/
                5,                /*Separator*/
                LV_GRID_CONTENT,  /*Box title*/
                30,               /*Boxes*/
                LV_GRID_TEMPLATE_LAST
        };
```

# vscode sdl sim的makefile分析

值得作为简单的C语言Makefile模板来使用。

简单清晰。



# 参考资料

1、官网文档

https://docs.lvgl.io/latest/en/html/widgets/obj.html