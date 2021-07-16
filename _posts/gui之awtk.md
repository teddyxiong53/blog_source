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



# 参考资料

1、在 qemu 中运行 awtk-linux-fb

https://blog.csdn.net/absurd/article/details/117195727

2、

https://blog.csdn.net/a232664/article/details/103943789/