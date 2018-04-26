---
title: freertos（一）
date: 2018-04-25 17:38:00
tags:
	- freertos
typora-root-url: ..\
---



先在qemu里跑起来。

1、下载stm32代码。

https://github.com/beckus/stm32_p103_demos

2、下载对应的qemu。只有11M。不大。

https://codeload.github.com/beckus/qemu_stm32/zip/stm32

3、安装一个依赖的软件。

```
sudo apt-get install libfdt-dev
```

4、编译qemu。进入到qemu目录。

```
./configure --disable-werror --enable-debug \
        --target-list="arm-softmmu" \
        --extra-cflags=-DDEBUG_CLKTREE \
        --extra-cflags=-DDEBUG_STM32_RCC \
        --extra-cflags=-DDEBUG_STM32_UART \
        --extra-cflags=-DSTM32_UART_NO_BAUD_DELAY \
        --extra-cflags=-DSTM32_UART_ENABLE_OVERRUN \
        --disable-gtk
```

然后直接make -j4就好了。

5、编译stm32 。

```
cd ../stm32_p103_demos
make all
```

6、运行测试。仍然在stm32的目录下执行。需要在Ubuntu的图像界面下运行这些命令。

```
make blink_flash_QEMURUN
make button_QEMURUN
make uart_echo_QEMURUN
```

效果如下。

![](/images/freertos（一）-stm32-qemu运行.png)



7、前面没有涉及到freertos，现在下载freertos。

https://github.com/embedded2014/freertos-plus

编译。

```
make
```

执行。

```
make qemu
```

可以看到运行，但是原文作者也写着是有问题的。





# 参考资料

1、Lab32: QEMU + FreeRTOS

http://wiki.csie.ncku.edu.tw/embedded/Lab32