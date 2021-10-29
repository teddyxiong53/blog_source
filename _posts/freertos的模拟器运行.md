---
title: freertos的模拟器运行
date: 2021-10-28 17:14:25
tags:
	- 模拟

---

--

https://github.com/alxhoff/FreeRTOS-Emulator

基于 POSIX 的 FreeRTOS 与 SDL2 图形组合的实现。

旨在为学生教授 FreeRTOS 提供 x86 仿真解决方案，无需嵌入式硬件。

在慕尼黑工业大学“嵌入式系统编程实验室”的教学中使用。

如果您不是我的学生之一，请原谅对“学生”或“课程”的任何提及。

基于由 William Davy 开发的 FreeRTOS (V5.X) 模拟器。

更新为使用 FreeRTOS V9.0.0。

先不细看，直接按readme快速跑起来看看效果。

安装工具链：

```
sudo apt-get install build-essential libsdl2-ttf-dev libsdl2-mixer-dev libsdl2-image-dev libsdl2-gfx-dev libsdl2-dev 
```

下载代码：

```
git clone --recursive https://github.com/alxhoff/FreeRTOS-Emulator
```



编译：

```
cd build
cmake ..
make
```

编译得到bin/FreeRTOS_Emulator，但是一运行，我的虚拟机就挂了。

算了。不管了。



参考资料

1、

