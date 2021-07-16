---
title: gui之sdl
date: 2021-06-03 14:48:11
tags:
	- gui

---

--

看awtk在ubuntu上的模拟运行，使用的是sdl作为显示接口。

了解一下sdl。

SDL（Simple DirectMedia Layer）是一套开放源代码的跨平台多媒体开发库，使用C语言写成。

SDL提供了数种控制图像、声音、输出入的函数，

让开发者只要用相同或是相似的代码就可以开发出跨多个平台（Linux、Windows、Mac OS X等）的应用软件。

目前SDL多用于开发游戏、模拟器、媒体播放器等多媒体应用领域。



SDL内置了调用OpenGL的函数。
通过使用SDL_image、SDL_ttf、SDL_mixer、SDL_net等外部扩展库，

可以轻松实现JPG、PNG、TIFF图像的加载使用，TrueType字体的使用，MP3文件的使用、网络相关的使用等。

SDL也有其他语言的包装，可以在这里查看　SDL用C语言写成，但是可以很容易在C++下面工作，并且SDL绑定了许多其它的语言，

这其中就包括Ada, C#, Eiffel, Erlang, Euphoria, Guile, Haskell, Java, Lisp, Lua, ML, Objective C, Pascal, Perl, PHP, Pike, Pliant, Python, Ruby, and Smalltalk。

**包装得比较好的是python语言的pygame。**

不过仍然建议你熟悉c/c++环境下的SDL后再使用，会得心应手许多。



虽然SDL时常被比较为‘跨平台的DirectX’，

然而事实上SDL是定位成以精简的方式来完成基础的功能，

它大幅度简化了控制图像、声音、输出入等工作所需撰写的代码。

**但更高级的绘图功能或是音效功能则需搭配OpenGL和OpenAL等API来达成。**

另外它本身也没有方便创建图形用户界面的函数。

![img](../images/random_name/20130923233206828)



```
static VideoBootStrap *bootstrap[] = {
#if SDL_VIDEO_DRIVER_COCOA
    &COCOA_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_X11
    &X11_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_MIR
    &MIR_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_WAYLAND
    &Wayland_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_VIVANTE
    &VIVANTE_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_DIRECTFB
    &DirectFB_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_WINDOWS
    &WINDOWS_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_WINRT
    &WINRT_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_HAIKU
    &HAIKU_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_PANDORA
    &PND_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_UIKIT
    &UIKIT_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_ANDROID
    &Android_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_PSP
    &PSP_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_KMSDRM
    &KMSDRM_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_RPI
    &RPI_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_NACL
    &NACL_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_EMSCRIPTEN
    &Emscripten_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_QNX
    &QNX_bootstrap,
#endif
#if SDL_VIDEO_DRIVER_DUMMY
    &DUMMY_bootstrap,
#endif
    NULL
};
```

当前awtk里，是怎么编译sdl的呢？是哪种显示类型？

SDL_VIDEO_DRIVER_X11

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



# sdl和sdl2的区别

就是一个较大的版本改动。

api接口有些每一向前兼容了。



# 参考资料

1、

https://baike.baidu.com/item/SDL/224181?fr=aladdin

2、

https://blog.csdn.net/leixiaohua1020/article/details/11954039

3、SDL1.2到2.0的迁移指南

https://www.cnblogs.com/lihaiping/p/4020248.html