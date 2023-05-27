---
title: gui之awtk
date: 2021-06-01 16:39:11
tags:
	- gui

---

--

这个是周立功公司开源的一个gui框架。

应该是李先静开发的。这个人之前把自己的gui框架捐给了rt-thread。在微博上接触过。

可以直接在linux上运行demo。效果还可以。

李先静在csdn上的博客，有不少是关于awtk的。

编译体系应该是从rt-thread里学来的，是用scons来进行编译。

先把编译逻辑理清楚。

框架代码：

https://github.com/zlgopen/awtk

示例代码：

https://github.com/zlgopen/awtk-c-demos

# 配置分析

awtk的顶层SConstruct文件

```
import awtk_config as awtk
```



awtk_config.py配置文件

```
INPUT_ENGINE='pinyin'
VGCANVAS='NANOVG'
NANOVG_BACKEND='GL3'
LCD='SDL_GPU'
NATIVE_WINDOW='sdl'
GRAPHIC_BUFFER='default'

OS_FLAGS='-g -Wall -fPIC ' 
OS_LIBS = ['GL', 'gtk-3','gdk-3','Xext', 'X11', 'sndio','stdc++', 'pthread', 'm', 'dl', 'asound']
OS_PROJECTS=['3rd/SDL/SConscript']
```



编译时的环境变量

```
WITH_MBEDTLS=1  
ENABLE_CURSOR=1  
WITH_TEXT_BIDI=1  
WITH_DATA_READER_WRITER=1  
WITH_EVENT_RECORDER_PLAYER=1  
WITH_ASSET_LOADER 
WITH_FS_RES 
WITH_ASSET_LOADER_ZIP  
STBTT_STATIC 
STB_IMAGE_STATIC 
WITH_STB_IMAGE  
WITH_VGCANVAS 
WITH_UNICODE_BREAK 
WITH_DESKTOP_STYLE  
WITH_SDL 
HAS_STDIO 
HAVE_STDIO_H 
HAS_GET_TIME_US64  
HAS_STD_MALLOC 
TK_MAX_MEM_BLOCK_NR=3  
WITH_IME_PINYIN  
WITH_NANOVG_GPU 
WITH_VGCANVAS_LCD 
WITH_STB_FONT  
WITH_NANOVG_GL3 
WITH_NANOVG_GL  
LINUX 
HAS_PTHREAD 
SDL_REAL_API 
SDL_TIMER_UNIX 
SDL_VIDEO_DRIVER_X11 
SDL_VIDEO_DRIVER_X11_SUPPORTS_GENERIC_EVENTS  
SDL_AUDIO_DRIVER_SNDIO 
SDL_VIDEO_OPENGL_GLX 
SDL_VIDEO_RENDER_OGL  
SDL_LOADSO_DLOPEN 
SDL_VIDEO_OPENGL_EGL 
SDL_VIDEO_OPENGL_ES2  
SDL_REAL_API 
SDL_HAPTIC_DISABLED 
SDL_SENSOR_DISABLED 
SDL_JOYSTICK_DISABLED
```



```
    'VGCANVAS': 'NANOVG',
    'TOOLS_NAME': '',
    'GTEST_ROOT': '/home/teddy/work/test/awtk-test/awtk/3rd/gtest/googletest',
    'TK_3RD_ROOT': '/home/teddy/work/test/awtk-test/awtk/3rd',
    'INPUT_ENGINE': 'pinyin',
    'NANOVG_BACKEND': 'GL3',
    'NATIVE_WINDOW': 'sdl',
    'GRAPHIC_BUFFER': 'default',
```



# binding

```
def genIdlAndDef():
    cmds = [
            'node tools/idl_gen/tkc.js tools/idl_gen/tkc.json',
            'node tools/idl_gen/index.js tools/idl_gen/idl.json',
            'node tools/dll_def_gen/index.js tools/idl_gen/idl.json  dllexports/awtk.def false',
            'node tools/dll_def_gen/index.js tools/idl_gen/tkc.json  dllexports/tkc.def false'
    ];

    for cmd in cmds:
        print(cmd)
        if os.system(cmd) != 0:
            print('exe cmd: ' + cmd + ' failed.')

```

上面这个函数的理解。

idl：是生成其他的语言的binding。



这个是python的binding。

https://github.com/zlgopen/awtk-python

运行方法：

```
在awtk同一层目录，下载awtk-python的代码
git clone https://github.com/zlgopen/awtk-python.git
cd awtk-python
生成资源
python ./scripts/update_res.py all
编译
scons
运行
./bin/awtkRun demos/button.py
```

awtkRun就相当于一个python解释器？

这里有几个很大的源代码文件，应该是自动生成的吧。如何自动生成的？

先只管C语言的版本。其他语言的暂时不看。



awtk designer怎么用？

https://awtk.zlg.cn/index.html#/Login

从这里下载，有ubuntu版本的。需要注册登录。

使用非常简单。我直接新建项目，拖入一个仪表盘的控件。打包编译，并模拟运行。可以看到效果。

但是就这么小的东西，居然有14M。

strip后，是4.5M。

不过哪些复杂的例子，有是这么大。

如果一般大小在4M左右。还是可以接受的。

看看默认生成了什么代码。

代码没有多少。资源文件不少。

还是看看复杂的例子，跟这个相比，多了什么。

主要是在window_main.c里改了，加了几百行代码。



中英文替换如何实现的？



# binding代码的生成

https://github.com/zlgopen/awtk-binding

都是靠这个工具生成的binding代码。确实很强大。

总的流程是：C语言代码导出了idl和json文件。通过idl和json文件生成了python、js等语言的binding代码。

```
getJsonIDL() {
    return '../../../../awtk/tools/idl_gen/idl.json';
  }
```



在awtk的tools/idl_gen/index.js里，用法是这样：

```
node index.js outputIDL sourcesPath
```

outputIDL就是idl.json。

sourcesPath就是src目录。

idl_gen.js的逻辑

关键是这段代码，是靠注释里的特殊字段来进行解析的。

```
if (comment.indexOf('* @') >= 0) {
            if (comment.indexOf(' @method') >= 0) {
              this.parseMethod(comment);
            } else if (comment.indexOf(' @class') >= 0) {
              this.parseClass(comment);
            } else if (comment.indexOf(' @property') >= 0) {
              this.parseProperty(comment);
            } else if (comment.indexOf(' @event') >= 0) {
              this.parseEvent(comment);
            } else if (comment.indexOf(' @const') >= 0) {
              this.parseConst(comment);
            } else if (comment.indexOf(' @enum') >= 0) {
              this.parseEnum(comment);
            }
          }
```

符号分为了这些种类：

method

class

property

event

const

enum

以src/tkc/event.h里的event_cast函数为例。

在头文件里是这样：

```
/**
 * @method event_cast
 * 转换为event对象。
 *
 * > 供脚本语言使用
 * @annotation ["cast", "scriptable"]
 * @param {event_t*} event event对象。
 *
 * @return {event_t*} event对象。
 */
event_t* event_cast(event_t* event);
```

在idl.json里，是这样的

```
[
  {
    "type": "class",
    "methods": [
      {
        "params": [
          {
            "type": "event_t*",
            "name": "event",
            "desc": "event对象。"
          }
        ],
        "annotation": {
          "cast": true,
          "scriptable": true
        },
        "desc": "转换为event对象。\n\n> 供脚本语言使用",
        "name": "event_cast",
        "return": {
          "type": "event_t*",
          "desc": "event对象。"
        }
      },
```

最后转成的python代码

```
#
# 事件基类。
#
#
class TEvent(object):
  def __init__(self, nativeObj):
    self.nativeObj = nativeObj;


  #
  # 转换为event对象。
  #
  #> 供脚本语言使用
  # 
  # @param event event对象。
  #
  # @return event对象。
  #
  @classmethod
  def cast(cls, event): 
    return  TEvent(event_cast(awtk_get_native_obj(event)));
```

要形成这样一套代码，的确是需要很仔细全面的架构设计。

所以，awtk总体还是比较完备的。



# buildroot里运行

看网上的文章，也只是直接scons编译，只是改了一下工具链的名字。

那么还是基于x11？

先运行一下再说。

改工具链的名字没用。

不对，我搞错了。

要在qemu里跑，是要编译下面这个代码。而不是默认的awtk。

https://github.com/zlgopen/awtk-linux-fb

感觉占用CPU还比较高。非常卡。



# demo1_app.c分析

#include "awtk_main.inc"

这一行包含的这个公共文件，就是main入口函数所在文件。

```
#ifndef APP_DEFAULT_FONT
#define APP_DEFAULT_FONT "default"
#endif /*APP_DEFAULT_FONT*/

#ifndef APP_TYPE
#define APP_TYPE APP_SIMULATOR
#endif /*APP_TYPE*/

#ifndef LCD_WIDTH
#define LCD_WIDTH 320
#endif /*LCD_WIDTH*/

#ifndef LCD_HEIGHT
#define LCD_HEIGHT 480
#endif /*LCD_HEIGHT*/
#ifndef APP_NAME
#define APP_NAME "awtk"
#endif /*APP_NAME*/

#ifndef APP_RES_ROOT
#define APP_RES_ROOT NULL
#endif /*APP_RES_ROOT*/
```



```
tk_init(lcd_w, lcd_h, APP_TYPE, APP_NAME, APP_RES_ROOT);
```



mainloop的实现

```
main_loop_t
	成员变量
		running
		quit_num
		app_quited
		last_loop_time
		widget_t *wm
	接口
		run
		quit
		step
		sleep
		wakeup
		recv_event
		queue_event
		get_event_source_manager
		destroy
```

事件

```
event_queue_req_t：是一个共用体。
	包括了：
	event_t event
		type
		size
		time
		void *target
		void *native_window_handle
	key_event_t key_event
		第一个成员是event_t，相当于继承了event_t。
		u32 key
		bool alt
		bool lalt
		bool ralt
		bool ctl
		bool shift
		bool cmd
		bool menu
		bool capslock
	wheel_event_t wheel_event
		鼠标滚轮事件
		int y 滚轮滚动的距离。
		bool alt
		bool ctrl
		bool shift
	pointer_event_t 
		鼠标指针事件。
		
	multi_gesture_event_t
		多点触摸手势。
	add_idle_t
	add_timer_t
	exec_in_ui_t 
```



mainloop当前只有sdl的真的实现了。

main_loop_sdl.c

```
main_loop_simple_t
	第一个成员是main_loop，相当于继承。
	
```



```
object_t
	emitter_t emitter
	ref_count
	name
	object_vtable_t *vt
```

tk_init

```
platform_prepare
	stm_time_init
	预分配了12M的内存。
tk_mem_init_stage2
system_info_init
tk_init_internal
	这个是真正干活的函数。里面调用了很多的初始化函数。
	tk_widgets_init 这个注册了组件。
```

object_vtable_t

```
这个是对象设计的关键。
object_t* object_create(const object_vtable_t* vt) 
	创建每一种对象，都提供一个这样的结构体。
	
对象继承了emitter。
所以对象都可以进行事件的发送。

```



vgcanvas



字体功能的实现



# darray

表示动态数组。

# 头文件层次分析

```
基础头文件的层次关系
tkc：自己实现的基础库。

action_queue.h
action_thread.h
	执行action的线程。难道是类似线程池的操作？
action_thread_pool.h
async.h
	借助action_thread来进行非阻塞操作。
	
我觉得一定程度上对glib进行了实现。
例如darray动态数组。

```

对外的头文件层次

```
awtk.h
	awtk_tkc.h：基础库。
	awtk_base.h: 基础组件。
	awtk_global.h: 全局工具函数。
	awtk_widgets.h: 各组组件。
```



# tkc目录分析

这个是基础库实现。

```
action_queue_t
action_queue_create
action_queue_recv
action_queue_send
action_queue_destroy


action_thread_pool_t
action_thread_pool_create
action_thread_pool_exec
action_thread_pool_destroy


action_thread_t
action_thread_create
action_thread_exec
action_thread_set_on_idle
action_thread_set_on_quit
action_thread_destroy


asset_type_t
asset_font_type_t
asset_data_type_t
asset_script_type_t
asset_image_type_t
asset_ui_type_t
asset_info_t
asset_info_create
asset_info_destroy
asset_info_unref
asset_info_ref
asset_info_get_type
asset_info_get_name


```



```
async_call
async_call_init
async_call_deinit


wbuffer_t
wbuffer_init
wbuffer_rewind
wbuffer_init_extendable
wbuffer_extend_capacity
wbuffer_deinit
wbuffer_skip
wbuffer_write_uint8
wbuffer_write_uint16
wbuffer_write_uint32
wbuffer_write_binary
wbuffer_write_string
wbuffer_has_room

rbuffer_t
rbuffer_init
...

color_parse

rgba_t
color_t
color_init
color_create
color_from_str
color_r
color_g
color_b
color_destroy

```



```
compressor_t
compressor_compress
compressor_uncompress
compressor_destroy


tk_cond_var_t
tk_cond_var_create
tk_cond_var_wait
tk_cond_var_awake
tk_cond_var_destroy


tk_cond_t
tk_cond_create
tk_cond_wait
tk_cond_wait_timeout
tk_cond_signal
tk_cond_destroy

```

## mem.c

这个主要是为了对接不同的os来做的抽象层。



# types_def.h

这个定义了基本类型和工具宏。

bool类型的定义。

```
#if defined(__GNUC__) && !defined(__cplusplus)
typedef _Bool bool_t;
#else
typedef uint8_t bool_t;
#endif
```

尺寸的定义。

```
typedef int32_t xy_t;
typedef int32_t wh_t;
```

对象类型

```
struct _value_t;
typedef struct _value_t value_t;

struct _object_t;
typedef struct _object_t object_t;
```

返回值

```
ret_t
```

包含log.h头文件

```
#include "tkc/log.h"
```

返回工具

```
goto_error_if_fail
break_if_fail
return_if_fail
return_value_if_fail
```

大小范围

```
#define tk_min(a, b) ((a) < (b) ? (a) : (b))
#define tk_abs(a) ((a) < (0) ? (-(a)) : (a))
#define tk_max(a, b) ((a) > (b) ? (a) : (b))
#define tk_roundi(a) (int32_t)(((a) >= 0) ? ((a) + 0.5f) : ((a)-0.5f))
#define tk_clamp(a, mn, mx) ((a) < (mn) ? (mn) : ((a) > (mx) ? (mx) : (a)))
#define tk_clampi(a, mn, mx) 
```

ARRAY_SIZE

一些基础的函数类型。

```
typedef void* (*tk_create_t)(void);
typedef ret_t (*tk_destroy_t)(void* data);
typedef ret_t (*tk_on_done_t)(void* data);
typedef ret_t (*tk_on_result_t)(void* ctx, const void* data);
typedef bool_t (*tk_is_valid_t)(void* data);
```



# str类型实现

类型：

```
str_t
	3个成员。
	size。
	capacity。
	char *str。
	
```



接口：

```

str_init
str_extend
str_eq
str_set
str_clear
str_set_with_len
str_append
str_append_more
str_append_with_len
str_insert
str_insert_with_len
str_remove
str_append_char
str_append_int
str_append_double
str_append_json_str
str_append_json_int_pair
str_append_json_str_pair
str_append_json_double_pair
str_append_json_bool_pair
str_pop
str_unescape
str_decode_xml_entity
str_decode_xml_entity_with_len
str_from_int
str_from_float
str_from_value
str_from_wstr
str_from_wstr_with_len
str_to_int
str_to_float
str_encode_hex
str_decode_hex
str_end_with
str_start_with
str_trim
str_trim_left
str_trim_right
str_replace
str_to_lower
str_to_upper
str_expand_vars
str_reset
```

# 关于使用的LGPL license的问题

https://github.com/zlgopen/awtk/issues/715

# 控件层级树结构

```
window_base
	window
		dialog
	
widget

theme

children_layouter

clip_board

event_type
event
	wheel_event：滚轮的值，alt/ctrl/shift键是否按下。
	orientation_event：旋转事件。0/90/180/270
	value_change_event：new_value、old_value。
	pointer_event：x/y。其他按键是否按下。
	key_event：key_value。
	paint_event：一个canvas指针。
	window_event：一个widget_t指针。
	multi_gesture_event：x/y。rotation。
	assets_event：
	
font

input_engine
input_method

main_loop

shortcut
```



# vtable_t

# object系统

```
object_t
object_vtable_t
emitter_t 事件分发器，用来实现观察者模式。
```

src\tkc\object_default.c

这个提供了vtable的实现。

跟object_default.c对等还有什么文件？

src\tkc\object_compositor.c

```
object_default_t
对象接口的缺省实现。
相当于object_t的子类。
多了属性个数，属性容量和属性表这3个成员。
```

# conf_io

这个的对xml、ini、json、ubjson这些配置文件的抽象。



# 绘制原理

AWTK 提供了两种画布：

普通（canvas）和矢量图画布（vgcanvas），

通过调用这两种画布提供的画图接口，可以实现不同的绘图功能。



canvas：

普通画布可以实现一些简单的绘制功能，

如：绘制水平或垂直直线、文本、图片、矩形等。

如果需要绘制比较复杂一点的图形就需要使用矢量图画布，

如：绘制椭圆、圆弧等。

vgcanvas：

与 canvas 相比 vgcanvas 的效率要低一些，

但功能也丰富些。

绘制一些简单的图形，如线条、矩形等可以用 canvas；

复杂一点图形，如圆角矩形就用 vgcanvas。

备注：即使是渲染同一个效果，vgcanvas 也会比 canvas 慢。



AWTK 常用的渲染模式有两种，

分别为 AGGE 和 OpenGL。

前者是软件渲染，

主要通过 CPU 来计算界面数据并将其拷贝到显存中实现显示，兼容性比较好，

但渲染效果一般，速度慢，适合没有 GPU 的嵌入式平台；

后者基于 OpenGL/GLES 实现，渲染效果好，适合有 GPU 的平台，常用于 PC。


NANOVG 是第三方的矢量画布库，默认只提供 OpenGL 的适配，

但它本身是支持重载的，

因此，后面 AWTK 中自行增加了 AGGE 的适配。

在 AWTK 中，存在 NANOVG 前后端的概念，具体定义如下：

NANOVG 前端：指 NANOVG 对外提供的抽象接口，供画布类型调用。

NANOVG 后端：指 NANOVG 的具体实现，即真正的将图像数据绘制到屏幕上，比如默认提供的 OpenGL，以及 AWTK 后来增加 AGGE。

NANOVG 的作用其实就是给 AWTK 提供了矢量画布的功能。



参考资料

1、

https://blog.csdn.net/weixin_40026797/article/details/124831631

# demos分析



# 参考资料

1、在 qemu 中运行 awtk-linux-fb

https://blog.csdn.net/absurd/article/details/117195727

2、

https://blog.csdn.net/a232664/article/details/103943789/