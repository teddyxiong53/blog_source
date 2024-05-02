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

SDL（Simple DirectMedia Layer）是一个跨平台的开源多媒体库，

用于在计算机上创建图形、音频和输入设备的应用程序。

它提供了一个简单而高效的接口，

使开发人员能够轻松地在不同的操作系统上编写多媒体应用程序，

如游戏、模拟器、媒体播放器等。

以下是SDL的一些主要特点和功能：

1. **跨平台性**：SDL可以在多个操作系统上运行，包括Windows、Mac OS、Linux以及一些嵌入式系统。这使得开发者可以在不同平台上编写一次代码，而无需担心特定平台的细节。

2. **简单易用**：SDL提供了简洁、易于理解的API，使开发者能够快速入门并快速开发应用程序。它封装了许多底层的多媒体功能，使得开发者可以更专注于应用程序的逻辑而不是底层实现细节。

3. **支持多媒体功能**：SDL提供了对图形、音频、输入设备等多种多媒体功能的支持。开发者可以使用SDL来创建2D图形、播放音频文件、处理键盘和鼠标输入等。

4. **轻量级**：SDL的设计目标之一是保持轻量级和高效。它的核心库相对较小，但仍提供了足够的功能来满足大多数应用程序的需求。此外，SDL还允许开发者根据需要选择性地使用附加模块，以满足特定的需求。

5. **活跃的社区支持**：SDL拥有一个活跃的开发社区，提供了丰富的文档、示例代码和支持资源。开发者可以在社区中获取帮助、分享经验，并参与到SDL的开发和改进中。

总的来说，SDL是一个强大而灵活的多媒体库，适用于各种类型的应用程序开发。无论是初学者还是经验丰富的开发者，都可以通过使用SDL来快速构建跨平台的多媒体应用程序。



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

# 发展历史

SDL的发展历史可以追溯到1998年，当时由Sam Lantinga创建。以下是SDL的一些主要发展里程碑：

1. **1998年**：SDL首次发布。最初，SDL是为了帮助游戏开发者更容易地在不同平台上编写游戏而创建的。

2. **1999年**：SDL 1.0发布。第一个稳定版本的SDL提供了基本的图形、音频和输入功能，使得开发者可以在Windows、Linux和其他操作系统上编写跨平台的游戏。

3. **2001年**：SDL 1.2发布。这个版本增加了更多的功能和改进，包括对OpenGL图形API的支持、更好的音频管理和更广泛的输入设备支持。

4. **2006年**：SDL 1.2.11发布。这是SDL 1.2系列的最后一个官方发布版本，后续的维护工作主要由社区维护。

5. **2013年**：SDL 2.0发布。这是一个重大的版本更新，引入了许多新功能和改进，包括对硬件加速的2D图形渲染、多窗口支持、更强大的音频功能、更好的输入设备管理等。SDL 2.0还采用了更现代化的设计和API，使其更适合于当前的硬件和软件环境。

6. **2018年**：SDL 2.0.8发布。这个版本带来了一些重要的改进和修复，包括对高DPI显示器的支持、对Android和iOS平台的改进等。

自从SDL 2.0发布以来，SDL继续保持活跃的开发和更新。开发者可以从SDL的官方网站上获取最新的版本和文档，并参与到SDL的开发和改进中。SDL已经成为许多游戏开发者和多媒体应用程序开发者的首选库之一，因其简单易用、跨平台性和丰富的功能而备受青睐。

# sdl和sdl2的区别

就是一个较大的版本改动。

api接口有些没有向前兼容了。

SDL和SDL2是两个不同版本的Simple DirectMedia Layer库，它们之间有一些显著的区别：

1. **功能和性能**：SDL2相对于SDL来说提供了更丰富和更现代化的功能。SDL2引入了许多新的特性，如对硬件加速的2D图形渲染、多窗口支持、更强大的音频功能、更好的输入设备管理等，这些功能使得SDL2在功能和性能上都比SDL更优秀。

2. **API设计**：SDL2在设计上进行了一些改进，使得API更现代化、更一致，并且更适合于当前的硬件和软件环境。SDL2的API相对于SDL来说更清晰、更易于理解和使用。

3. **跨平台支持**：SDL2相对于SDL来说在跨平台支持方面也有所改进。SDL2可以在更多的操作系统和硬件平台上运行，包括Windows、Mac OS、Linux、iOS、Android等。

4. **硬件加速**：SDL2引入了对硬件加速的支持，这使得图形渲染更加高效和流畅。SDL2可以利用现代图形硬件的特性来加速2D图形渲染，从而提高应用程序的性能和体验。

5. **更好的扩展性和灵活性**：SDL2相对于SDL来说具有更好的扩展性和灵活性。SDL2采用了模块化的设计，允许开发者根据需要选择性地使用不同的模块，以满足特定的需求。这使得SDL2更适合于大型项目和复杂应用程序的开发。

总的来说，SDL2是SDL的一个重大更新版本，引入了许多新的功能和改进，使得它在功能、性能和跨平台支持方面都比SDL更优秀。因此，对于新的项目和应用程序来说，通常推荐使用SDL2来获得更好的体验和性能。

# 基于sdl的项目一般是做什么的

基于SDL的项目可以涵盖各种不同的领域，但主要集中在游戏开发和多媒体应用程序开发方面。以下是一些常见的基于SDL的项目示例：

1. **2D游戏开发**：SDL提供了简单而强大的2D图形渲染功能，使得开发者可以轻松地创建各种类型的2D游戏，包括平台游戏、射击游戏、益智游戏等。许多经典的独立游戏和游戏引擎都是基于SDL开发的。

2. **媒体播放器**：SDL可以用来播放音频和视频文件，因此可以用于创建简单的媒体播放器应用程序。开发者可以利用SDL的音频和视频功能来实现播放、暂停、停止、音量控制等功能。

3. **模拟器**：由于SDL提供了对图形、音频和输入设备的统一抽象，因此可以用于创建各种类型的模拟器，如游戏机模拟器、计算机模拟器等。开发者可以利用SDL来模拟硬件设备的行为，并实现相关的游戏或应用程序。

4. **图形和多媒体工具**：SDL可以用于创建各种图形和多媒体工具，如图像编辑器、音频编辑器、动画工具等。开发者可以利用SDL的图形和音频功能来实现工具的各种功能，并提供友好的用户界面。

5. **教育和学习应用**：SDL可以用于创建教育和学习应用程序，如交互式教程、学习游戏等。开发者可以利用SDL来实现应用程序的图形、音频和用户交互功能，从而帮助用户更好地学习和理解知识。

总的来说，基于SDL的项目可以涵盖各种不同的领域，但通常都与游戏开发和多媒体应用程序开发有关。SDL的简单易用性、跨平台性和丰富的功能使其成为开发者的首选之一，特别是对于那些希望快速构建跨平台多媒体应用程序的开发者来说。

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

# api文档

https://wiki.libsdl.org/SDL2/APIByCategory

# 相关的软件

https://wiki.libsdl.org/SDL2/Libraries

# 以Micro UI为切入点



# 参考资料

1、

https://baike.baidu.com/item/SDL/224181?fr=aladdin

2、

https://blog.csdn.net/leixiaohua1020/article/details/11954039

3、SDL1.2到2.0的迁移指南

https://www.cnblogs.com/lihaiping/p/4020248.html