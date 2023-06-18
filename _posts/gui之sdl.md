---
title: gui之sdl
date: 2021-06-03 14:48:11
tags:
	- gui

---

--

# 资源收集

https://tjumyk.github.io/sdl-tutorial-cn/

# 简介

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

api接口有些没有向前兼容了。

# 基于sdl的著名软件有哪些

基于SDL的著名软件有许多，以下是其中一些知名的例子：

1. 游戏软件：
   - "星际争霸"（StarCraft）：这是一款著名的即时战略游戏，最初使用SDL进行跨平台开发。
   - "炉石传说"（Hearthstone）：这是一款知名的在线卡牌游戏，最初也使用SDL进行开发。
   - "超级食肉男孩"（Super Meat Boy）：这是一款受欢迎的平台动作游戏，它使用SDL作为其底层引擎。

2. 模拟器软件：
   - DOSBox：这是一款用于在现代计算机上模拟旧版MS-DOS系统的软件，它使用SDL提供跨平台的图形和音频支持。
   - ScummVM：这是一款用于运行经典图形冒险游戏的模拟器，例如《疯狂大酒店》（Maniac Mansion）和《猴岛传奇》（Monkey Island），它使用SDL作为其底层库。

3. 多媒体应用软件：
   - VLC媒体播放器：这是一款广受欢迎的多媒体播放器，它使用SDL作为其底层渲染和音频输出引擎。
   - FFmpeg：这是一个强大的多媒体处理库，广泛用于音视频编解码、转码和处理，它也使用SDL来实现图形和音频的显示和输出。

这只是一小部分基于SDL的著名软件的例子，还有许多其他的应用程序和游戏也使用了SDL作为其开发框架。SDL的跨平台性、简单易用的API和丰富的功能使得它成为许多开发者选择的工具之一。

# 基于sdl的gui方案

基于SDL的GUI（图形用户界面）方案可以使用SDL的渲染功能和用户输入处理来实现。尽管SDL本身并没有提供完整的GUI库，但您可以结合SDL和其他库或框架来构建GUI应用程序。以下是一些基于SDL的常见GUI方案：

1. SDL_gfx：SDL_gfx是一个用于扩展SDL渲染功能的开源库。它提供了一系列绘图函数，例如绘制线条、矩形、圆形等，可以用于创建GUI元素。

2. Dear ImGui：Dear ImGui是一个轻量级、开源的GUI库，专注于快速创建调试工具和原型设计。它可以与SDL集成，提供一个简单的API来创建窗口、按钮、文本框等常见的GUI组件。

3. Nuklear：Nuklear是另一个轻量级的GUI库，适用于嵌入式系统和游戏开发。它支持多个后端，包括SDL，可以用于创建GUI应用程序和工具。

4. CEGUI：CEGUI是一个功能强大的跨平台GUI库，支持多种渲染器，包括基于SDL的渲染器。它提供了丰富的GUI组件和布局选项，适用于创建复杂的GUI应用程序。

这些是一些基于SDL的常见GUI方案的示例，但并不限于此。您还可以根据自己的需求选择其他库或框架，或者根据需要自行开发GUI组件和交互逻辑。重要的是要理解SDL提供的渲染和输入功能，以便在GUI开发中进行适当的集成和使用。

# 基于sdl的播放器

基于SDL的播放器可以用于播放音频和视频文件，并提供用户界面和交互控制。下面是一个简单的基于SDL的音频播放器的示例：

```c++
#include <SDL.h>

int main(int argc, char* argv[]) {
    // 初始化SDL
    SDL_Init(SDL_INIT_AUDIO);

    // 打开音频设备
    SDL_AudioSpec spec;
    spec.freq = 44100;
    spec.format = AUDIO_S16SYS;
    spec.channels = 2;
    spec.samples = 4096;
    SDL_OpenAudio(&spec, NULL);

    // 加载音频文件
    SDL_AudioSpec waveSpec;
    Uint32 waveLength;
    Uint8* waveData;
    if (SDL_LoadWAV("audio.wav", &waveSpec, &waveData, &waveLength) == NULL) {
        SDL_Log("Failed to load audio.wav: %s", SDL_GetError());
        return 1;
    }

    // 播放音频
    SDL_QueueAudio(1, waveData, waveLength);
    SDL_PauseAudio(0);

    // 等待播放结束
    while (SDL_GetAudioStatus() == SDL_AUDIO_PLAYING) {
        SDL_Delay(100);
    }

    // 清理资源
    SDL_CloseAudio();
    SDL_FreeWAV(waveData);
    SDL_Quit();

    return 0;
}
```

此示例程序使用SDL来初始化音频设备，加载音频文件（`audio.wav`），并将其加入音频队列进行播放。程序通过调用`SDL_PauseAudio(0)`来启动音频播放，并在播放结束后退出。

请注意，这只是一个简单的示例，用于演示基于SDL的音频播放器的基本结构。在实际应用中，您可能需要添加更多的功能和控制选项，例如音频格式转换、音量控制、播放列表管理等。

对于基于SDL的视频播放器，您需要结合SDL的图像渲染功能来实现视频的解码和显示。这通常需要使用其他库或框架，例如FFmpeg或libAV来进行视频解码，并使用SDL的渲染器和纹理功能来将解码后的视频帧呈现到屏幕上。

请注意，音频和视频播放器是相对复杂的应用程序，需要处理多线程、同步、格式转换等方面的问题。因此，在实际开发中，可能需要更复杂的架构和库来处理这些问题。以上示例仅提供了一个基本的起点，以帮助您了解基于SDL的播放器的基本原理。

# 参考资料

1、

https://baike.baidu.com/item/SDL/224181?fr=aladdin

2、

https://blog.csdn.net/leixiaohua1020/article/details/11954039

3、SDL1.2到2.0的迁移指南

https://www.cnblogs.com/lihaiping/p/4020248.html