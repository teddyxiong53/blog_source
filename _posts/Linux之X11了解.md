---
title: Linux之X11了解
date: 2020-03-13 10:42:13
tags:
	- Linux

---

--

什么是X11？它的发展历史是怎样的？当前的发展情况是怎样的？

X11，是X Window System的简称，也可以叫做X，X-Windows。

之所以叫做X，是因为字母表里，X在W字母之后。

MIT开发过一套图形界面系统叫W。

之所以叫X11，是因为在1987年的时候，X Window System已经到了版本11了。

而后续的所有的X，都是基于版本11发展而来。而且没有很大的变化。

为了方便，我们都简称X。



X最开始是由X.org来维护。

后来基于X11R6发展出来专门给X86架构用的X。也叫做XFree86 。

XFree86占据了很大的份额，但是从2004年起，XFree86不再使用GPL协议。

所以很多Linux发行版本，开始弃用XFree86，转而使用Xorg。

现在xorg又称为主流。



X的设计理念是：

```
It is important to decide what a system is not as to what it is.
```

这句话的翻译是：决定一个系统不是什么，跟决定一个系统是什么，这两件事情一样重要。

X只提供实现GUI的框架，

它提供了绘制基本点线面的方法，跟鼠标键盘的交互。

但是不提示button这些具体控件。

X包括3个部分：

```
X server ：守护进程。
X client 
X protocol
```



Qt for embedd linux在这方面则完全不同，它并没有构建在X Window之上，

而是构建在Linux的Framebuffer之上，把在界面上需要显示的内容直接写入了framebuffer。

**因为在嵌入式系统上 把X System给省略了，这样会节省许多的系统开销。**

**而直接写framebuffer，又会加快显示速度。**



# 从fbtft探索x11

现在看fbtft的，看到可以在很小的tft屏幕上显示linux图形界面。

https://github.com/notro/fbtft-spindle/wiki/Appendix#x-windows-backlight-script

而且还提供了不少可操作的系统，我觉得这个可以作为一个了解x11的切入点。

可以同时有2个X windows会话，一个在lcd上，一个在hdmi上。

但是这样有一个问题，就是input device只能属于其中一个。

```
startx -- -layout HDMI &
startx -- -layout TFT &
```

startx 这个命令值得玩味。

# 简介

X11 是一个用于图形用户界面（GUI）的显示服务器协议，

也是一个基于该协议实现的开源图形系统。

它最初由麻省理工学院（MIT）开发，于 1987 年首次发布。

X11 在当时成为了几乎所有 UNIX 和类 UNIX 操作系统的标准图形系统。

以下是 X11 的一些主要特点和组成部分：

1. **显示服务器**：X11 定义了一个客户端-服务器模型，其中显示服务器负责管理图形硬件设备（如显示器、鼠标、键盘等），并提供图形显示的基本功能。

2. **客户端应用程序**：客户端应用程序通过 X11 协议与显示服务器进行通信，向服务器发送绘图请求，并接收服务器返回的图形数据。客户端应用程序可以是任何支持 X11 协议的程序，如窗口管理器、桌面环境、应用程序等。

3. **窗口管理器**：窗口管理器是运行在 X11 上的一个特殊类型的客户端应用程序，负责管理窗口的布局、大小、层叠顺序等。常见的窗口管理器包括 Xfwm、Metacity、Openbox 等。

4. **图形工具包（Toolkit）**：图形工具包是用于开发图形用户界面的库或框架。它们提供了一组 GUI 组件和功能，用于创建和管理窗口、按钮、文本框等元素。常见的图形工具包包括 GTK+、Qt、Motif 等。

5. **协议和扩展**：X11 协议定义了客户端和服务器之间的通信规则和命令格式。此外，X11 还支持一系列扩展，以增强其功能，如图形渲染、图像压缩、字体管理等。

6. **网络透明性**：X11 具有网络透明性，允许客户端应用程序在远程服务器上运行，并通过网络连接到显示服务器。这使得用户可以在远程服务器上运行图形应用程序，并在本地显示图形界面。

总的来说，X11 是一个功能强大且灵活的图形系统，为 UNIX 和类 UNIX 操作系统提供了可扩展的图形用户界面。虽然它在当今仍然广泛使用，但也面临着一些挑战，如性能问题、安全漏洞等，导致一些现代系统开始转向使用 Wayland 或其他替代方案。

# X11的11是什么意思

X11 的 "11" 实际上代表了其历史。在计算机科学中，X 系统是由麻省理工学院（MIT）开发的一系列图形显示系统，其中的 "X" 表示 "实验"（eXperimental）。X11 是 X 系统的第 11 个版本，因此被称为 X11。

X11 最初发布于 1987 年，成为几乎所有 UNIX 和类 UNIX 操作系统的标准图形系统。从那时起，X11 成为了大多数 Unix 系统中的默认图形系统，并为开源社区中的图形界面提供了一个通用标准。即便在现今，许多 Unix 和类 Unix 操作系统仍然使用 X11，尽管一些新兴的系统开始转向使用 Wayland 等现代的替代方案。

# X11协议说明

X11 协议是用于图形用户界面（GUI）的显示服务器协议，它定义了客户端和服务器之间的通信规则和命令格式。以下是 X11 协议的一些关键方面和说明：

1. **客户端-服务器模型**：X11 协议采用了客户端-服务器模型，其中客户端应用程序通过网络与显示服务器进行通信。显示服务器负责管理图形硬件设备，并提供图形显示的基本功能。

2. **网络透明性**：X11 具有网络透明性，允许客户端应用程序在远程服务器上运行，并通过网络连接到显示服务器。这意味着用户可以在远程服务器上运行图形应用程序，并在本地显示图形界面。

3. **基本概念**：X11 协议定义了一系列基本概念，如窗口、图形上下文、图像格式等。这些基本概念为客户端应用程序提供了操作图形界面的基础。

4. **图形绘制命令**：X11 协议定义了一系列图形绘制命令，用于在屏幕上绘制图形元素，如线条、矩形、圆形等。客户端应用程序可以向显示服务器发送这些绘制命令，并指定绘制的位置、颜色、线型等属性。

5. **事件和窗口管理**：X11 协议定义了一系列事件，用于表示用户输入、窗口状态变化等事件。客户端应用程序可以注册事件处理程序，并在事件发生时接收和处理这些事件。此外，X11 协议还定义了一些窗口管理相关的命令和协议，如创建窗口、移动窗口、改变窗口属性等。

6. **扩展和协议版本**：X11 协议支持一系列扩展，以增强其功能。这些扩展可以提供图像渲染、图像压缩、字体管理等额外的功能。此外，X11 协议有多个版本，每个版本都引入了新的特性和改进。

总的来说，X11 协议提供了一个标准的图形界面通信协议，使得客户端应用程序可以与显示服务器进行交互，并在屏幕上显示图形界面。它的网络透明性和灵活性使得它成为了 UNIX 和类 UNIX 系统中的标准图形系统。

# X11相关的软件有哪些

X11 是一个开源的图形系统协议，许多软件都是基于 X11 协议开发的。以下是一些与 X11 相关的常见软件：

1. **X.Org Server**：X.Org 项目是一个开源的 X11 实现，其中包括 X.Org 服务器（X.Org Server），它是 X11 协议的参考实现，用于管理图形硬件设备并提供图形显示功能。

2. **窗口管理器**：窗口管理器是运行在 X11 上的一类特殊的客户端应用程序，负责管理窗口的布局、大小、层叠顺序等。常见的窗口管理器包括：

   - **GNOME Shell**：GNOME 桌面环境的默认窗口管理器。
   - **KWin**：KDE 桌面环境的窗口管理器。
   - **Openbox**：一个轻量级的窗口管理器，常用于类 Unix 桌面环境中。

3. **图形工具包（Toolkit）**：图形工具包是用于开发图形用户界面的库或框架。它们提供了一组 GUI 组件和功能，用于创建和管理窗口、按钮、文本框等元素。常见的图形工具包包括：

   - **GTK+**：GNOME 桌面环境使用的图形工具包。
   - **Qt**：KDE 桌面环境使用的图形工具包。

4. **应用程序**：许多图形应用程序都是基于 X11 协议开发的，包括文件管理器、文本编辑器、终端仿真器、图像编辑器等。一些常见的 X11 应用程序包括：

   - **Nautilus**：GNOME 桌面环境的默认文件管理器。
   - **gedit**：GNOME 桌面环境的默认文本编辑器。
   - **GNOME Terminal**：GNOME 桌面环境的默认终端仿真器。

5. **其他工具和库**：除了上述软件之外，还有许多其他与 X11 相关的工具和库，用于图形开发、窗口管理、图形渲染等。例如，Xlib 是一个用于编写 X11 客户端应用程序的 C 语言库。

总的来说，X11 相关的软件涵盖了图形系统的各个方面，包括显示服务器、窗口管理、图形工具包、应用程序等。它们共同构成了 UNIX 和类 UNIX 系统中的图形用户界面。

# freedesktop.org介绍

freedesktop.org 是一个旨在推动开放式标准和协作的开源项目的组织。

它由多个主要的自由软件项目组成，致力于创建和维护一组共享的技术规范和工具，

以改善 Linux 和其他开源操作系统的互操作性和用户体验。

以下是有关 freedesktop.org 的一些介绍：

1. **目标和使命**：freedesktop.org 的主要目标是通过制定和推广开放标准、协议和规范来改善 Linux 和类 Unix 操作系统的用户体验。它致力于通过促进开源软件项目之间的协作和共享来实现这一目标。

2. **组织结构**：freedesktop.org 是一个开放式的组织，由多个项目组成。这些项目包括 X.Org Foundation、Wayland、D-Bus、Fontconfig、Cairo、HarfBuzz 等。每个项目都有自己的社区和开发者团队，负责管理和维护相应的技术规范和工具。

3. **主要项目**：
   - **X.Org Foundation**：X.Org 是一个开源的图形系统项目，负责开发和维护 X Window 系统和相关的图形技术。它提供了 X11 协议的参考实现，以及用于构建图形用户界面的图形库和工具。
   - **Wayland**：Wayland 是一个现代的图形显示服务器协议，旨在取代 X11，并提供更好的性能、安全性和可扩展性。
   - **D-Bus**：D-Bus 是一个用于进程间通信的消息总线系统，广泛用于 Linux 和类 Unix 操作系统中的桌面和系统服务。
   - **Fontconfig**：Fontconfig 是一个字体配置和管理库，用于提供统一的字体配置和渲染功能。
   - **Cairo**：Cairo 是一个矢量图形渲染库，用于在不同的绘图设备上渲染图形元素。
   - **HarfBuzz**：HarfBuzz 是一个开源的文本排版引擎，用于处理复杂的文本布局和渲染。

4. **贡献和社区**：freedesktop.org 欢迎来自全球的开发者和贡献者参与其中。每个项目都有自己的社区网站、邮件列表、版本控制系统等，用于讨论技术问题、提交补丁和提出建议。

总的来说，freedesktop.org 是一个重要的开源组织，致力于推动开放标准和协作，以改善 Linux 和其他开源操作系统的用户体验和互操作性。其项目涵盖了图形系统、进程间通信、字体管理、文本排版等多个方面，对于开源社区的发展具有重要意义。

# buildroot下面的x11r7目录下的内容

Sure, here's a Markdown table with the first column filled with the provided English terms and the second column empty:

| package                          | 说明 |
| -------------------------------- | ---- |
| libxcb                           |      |
| mcookie                          |      |
| xapp_appres                      |      |
| xapp_bdftopcf                    |      |
| xapp_beforelight                 |      |
| xapp_bitmap                      |      |
| xapp_editres                     |      |
| xapp_fonttosfnt                  |      |
| xapp_fslsfonts                   |      |
| xapp_fstobdf                     |      |
| xapp_iceauth                     |      |
| xapp_ico                         |      |
| xapp_listres                     |      |
| xapp_luit                        |      |
| xapp_mkfontscale                 |      |
| xapp_oclock                      |      |
| xapp_rgb                         |      |
| xapp_rstart                      |      |
| xapp_scripts                     |      |
| xapp_sessreg                     |      |
| xapp_setxkbmap                   |      |
| xapp_showfont                    |      |
| xapp_smproxy                     |      |
| xapp_twm                         |      |
| xapp_viewres                     |      |
| xapp_x11perf                     |      |
| xapp_xauth                       |      |
| xapp_xbacklight                  |      |
| xapp_xbiff                       |      |
| xapp_xcalc                       |      |
| xapp_xclipboard                  |      |
| xapp_xclock                      |      |
| xapp_xcmsdb                      |      |
| xapp_xcompmgr                    |      |
| xapp_xconsole                    |      |
| xapp_xcursorgen                  |      |
| xapp_xdbedizzy                   |      |
| xapp_xditview                    |      |
| xapp_xdm                         |      |
| xapp_xdpyinfo                    |      |
| xapp_xdriinfo                    |      |
| xapp_xedit                       |      |
| xapp_xev                         |      |
| xapp_xeyes                       |      |
| xapp_xf86dga                     |      |
| xapp_xfd                         |      |
| xapp_xfindproxy                  |      |
| xapp_xfontsel                    |      |
| xapp_xfs                         |      |
| xapp_xfsinfo                     |      |
| xapp_xgamma                      |      |
| xapp_xgc                         |      |
| xapp_xhost                       |      |
| xapp_xinit                       |      |
| xapp_xinput                      |      |
| xapp_xinput-calibrator           |      |
| xapp_xkbcomp                     |      |
| xapp_xkbevd                      |      |
| xapp_xkbprint                    |      |
| xapp_xkbutils                    |      |
| xapp_xkill                       |      |
| xapp_xload                       |      |
| xapp_xlogo                       |      |
| xapp_xlsatoms                    |      |
| xapp_xlsclients                  |      |
| xapp_xlsfonts                    |      |
| xapp_xmag                        |      |
| xapp_xman                        |      |
| xapp_xmessage                    |      |
| xapp_xmh                         |      |
| xapp_xmodmap                     |      |
| xapp_xmore                       |      |
| xapp_xpr                         |      |
| xapp_xprop                       |      |
| xapp_xrandr                      |      |
| xapp_xrdb                        |      |
| xapp_xrefresh                    |      |
| xapp_xset                        |      |
| xapp_xsetmode                    |      |
| xapp_xsetpointer                 |      |
| xapp_xsetroot                    |      |
| xapp_xsm                         |      |
| xapp_xstdcmap                    |      |
| xapp_xvidtune                    |      |
| xapp_xvinfo                      |      |
| xapp_xwd                         |      |
| xapp_xwininfo                    |      |
| xapp_xwud                        |      |
| xcb-proto                        |      |
| xcb-util                         |      |
| xcb-util-cursor                  |      |
| xcb-util-image                   |      |
| xcb-util-keysyms                 |      |
| xcb-util-renderutil              |      |
| xcb-util-wm                      |      |
| xcursor-transparent-theme        |      |
| xdata_xbitmaps                   |      |
| xdata_xcursor-themes             |      |
| xdriver_xf86-input-evdev         |      |
| xdriver_xf86-input-joystick      |      |
| xdriver_xf86-input-keyboard      |      |
| xdriver_xf86-input-libinput      |      |
| xdriver_xf86-input-mouse         |      |
| xdriver_xf86-input-synaptics     |      |
| xdriver_xf86-input-tslib         |      |
| xdriver_xf86-input-vmmouse       |      |
| xdriver_xf86-video-amdgpu        |      |
| xdriver_xf86-video-ark           |      |
| xdriver_xf86-video-ast           |      |
| xdriver_xf86-video-ati           |      |
| xdriver_xf86-video-cirrus        |      |
| xdriver_xf86-video-dummy         |      |
| xdriver_xf86-video-fbdev         |      |
| xdriver_xf86-video-fbturbo       |      |
| xdriver_xf86-video-geode         |      |
| xdriver_xf86-video-glint         |      |
| xdriver_xf86-video-i128          |      |
| xdriver_xf86-video-imx           |      |
| xdriver_xf86-video-imx-viv       |      |
| xdriver_xf86-video-intel         |      |
| xdriver_xf86-video-mach64        |      |
| xdriver_xf86-video-mali          |      |
| xdriver_xf86-video-mga           |      |
| xdriver_xf86-video-neomagic      |      |
| xdriver_xf86-video-nouveau       |      |
| xdriver_xf86-video-nv            |      |
| xdriver_xf86-video-openchrome    |      |
| xdriver_xf86-video-qxl           |      |
| xdriver_xf86-video-r128          |      |
| xdriver_xf86-video-savage        |      |
| xdriver_xf86-video-siliconmotion |      |
| xdriver_xf86-video-sis           |      |
| xdriver_xf86-video-tdfx          |      |
| xdriver_xf86-video-tga           |      |
| xdriver_xf86-video-trident       |      |
| xdriver_xf86-video-vesa          |      |
| xdriver_xf86-video-vmware        |      |
| xdriver_xf86-video-voodoo        |      |
| xfont_encodings                  |      |
| xfont_font-adobe-100dpi          |      |
| xfont_font-adobe-75dpi           |      |
| xfont_font-adobe-utopia-100dpi   |      |



## xcb

在 freedesktop.org 中，XCB（X C Bindings）是一个用于 X Window 系统的低级编程接口，旨在取代传统的 Xlib 库。

XCB 是基于网络透明的 X11 协议的轻量级、高效的 C 语言绑定库。

XCB 的设计目标是提供对 X11 协议的直接访问，同时尽可能减少资源消耗和延迟。

与传统的 Xlib 不同，XCB 使用异步和并发的方式处理请求和响应，

使得客户端应用程序能够更有效地利用系统资源，并在网络延迟较高的情况下表现更好。

XCB 由多个库组成，每个库对应于 X11 协议中的一个扩展或一组相关的请求。这些库包括：

1. **libxcb-core**：包含了 XCB 的核心功能，如连接管理、事件处理等。

2. **libxcb-atom**：用于处理原子属性和相关操作的库。

3. **libxcb-aux**：提供了一些辅助函数和工具，简化了 XCB 的使用。

4. **libxcb-image**：用于处理图像数据的库。

5. **libxcb-keysyms**：用于处理按键符号和键码的库。

6. **libxcb-render**：用于图形渲染的库。

7. **libxcb-shape**：用于处理窗口形状的库。

8. **libxcb-util**：提供了一些实用工具和辅助函数，简化了 XCB 的使用。

通过使用 XCB，开发者可以直接访问 X11 协议的底层细节，从而更灵活地控制图形系统的行为。XCB 的异步和并发设计使得它在处理大量请求和事件时具有较好的性能表现，尤其适用于高性能计算和网络应用场景。

总的来说，XCB 是 freedesktop.org 中的一个重要项目，为开发者提供了一个高效、灵活的 X11 编程接口，促进了图形应用程序在 Linux 和其他类 Unix 系统中的发展。

## mcookie

`mcookie` 是一个用于生成随机的 X11 魔术 Cookie（magic cookie）的命令行工具。

X11 魔术 Cookie 是一种用于身份验证的令牌，

用于在 X11 显示服务器和客户端之间进行安全通信。

在 X11 中，当客户端应用程序连接到显示服务器时，

它需要提供一个魔术 Cookie 作为身份验证的凭证。

服务器会验证客户端提供的魔术 Cookie，并决定是否允许客户端访问图形资源。

`mcookie` 工具用于生成一个随机的魔术 Cookie，并将其输出到标准输出。

生成的魔术 Cookie 是一个 128 位的十六进制字符串，可以用作 X11 客户端的身份验证凭证。

使用 `mcookie` 命令的基本语法如下：

```
mcookie
```

运行上述命令将生成一个随机的魔术 Cookie，并将其输出到标准输出。你可以将生成的魔术 Cookie 复制并粘贴到 X11 客户端的配置文件中，以便客户端能够成功连接到显示服务器。

魔术 Cookie 在 X11 中是一种常见的身份验证机制，用于确保图形会话的安全性。通过使用随机生成的魔术 Cookie，可以有效地防止未经授权的客户端访问图形资源。

# 用buildroot构建一个桌面系统用于研究

```
Target packages --->
    Graphic libraries and applications --->
        [*] x11r7
        [*] xterm
        [*] xdm
        [*] twm
```

## xdm



## twm

# 参考资料

1、

https://www.cnblogs.com/yuanqiangfei/p/11612815.html

2、linux-x11架构

https://www.cnblogs.com/xuzhaoping/p/11074290.html

3、Qt for destop Linux 和 Qt/E最大的区别

https://blog.csdn.net/sh_danny/article/details/6115902