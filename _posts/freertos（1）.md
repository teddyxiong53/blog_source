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



# 其他在qemu里跑freertos的方式

https://github.com/Victor-Y-Fadeev/vexpress-a9

参考这个，在vexpress+qemu上跑freertos。

我打算基于freertos打造一个自己的rtos简单框架。

看.gitmodules里写着依赖xvisor。我把对应的工程复制到gitee.com上 。这样clone的时候就会快一些。

依次执行下面的脚本：

```
$ ./scripts/install.sh
$ ./scripts/xvisor.sh
```

然后执行：

```
$ ./scripts/make.sh
$ ./scripts/qemu.sh
```

可以顺利运行，没有什么错误。

只是起来后，没有shell。

入口是在src/main.c里。

```
#include "FreeRTOS.h"
#include "task.h"


void app_main(void)
{
        basic_puts("xhl --- hello \n");
        return;
}
```

没有实现printf。

打印是用basic_puts函数。

运行效果。

![1593421906072](/images/random_name/1593421906072.png)

仔细看看这套方案的细节。

## 脚本分析

install.sh

```
这个没有什么特别的，就是安装工具链和qemu。
gcc-arm-none-eabi qemu-system-arm
还安装了genext2fs
```

xvisor.sh

```
先git clone xvisor
然后打补丁，修改配置。
patch -f $XVISOR/arch/arm/board/generic/dts/arm/vexpress-v2p-ca9.dts < $PATCH/vexpress-v2p-ca9.patch
然后编译xvisor
make ARCH=arm generic-v7-defconfig
make
```

make.sh

```
把freertos的代码拷贝到xvisor目录下去编译。
cp -rf $FREERTOS $XVISOR/tests/arm32/vexpress-a9/freertos
cp -rf $PORT $XVISOR/tests/arm32/vexpress-a9/freertos
cp -f $CONFIG $XVISOR/tests/arm32/vexpress-a9/freertos
把src目录下的代码拷贝到xvisor的目录下去编译。
# Copy application source
cp -rf $SRC $XVISOR/tests/arm32/vexpress-a9/freertos
执行make
cd $XVISOR/tests/arm32/vexpress-a9/freertos
if ! make ; then
	exit 1
fi
生成disk.img文件
genext2fs -B 1024 -b 32768 -d ./build/disk ./build/disk.img
```

qemu.sh

```
这个就是运行qemu。时延disk.img文件。

qemu-system-arm -M vexpress-a9 -m 512M -nographic \
	-kernel build/vmm.bin \
	-dtb    build/arch/arm/board/generic/dts/arm/vexpress-v2p-ca9.dtb \
	-initrd build/disk.img
```

vmm.bin 这个文件是作为kernel。应该相当于uboot的作用。



# 配置

```
节拍是1ms的。
配置抢占。
最大优先级为7 
最小的栈配置为128字节。
使用时间片
使用mutex和递归mutex
不使用idle hook
不使用tick hook

#define vPortSVCHandler		SVC_Handler
#define xPortPendSVHandler	PendSV_Handler
#define xPortSysTickHandler	SysTick_Handler

```

# api梳理

```
任务创建
xTaskCreate
	返回值：pdSUCCESS成功。
	句柄是通过指针返回的。
xTaskDelete
	通过句柄删除。
xEventGroupCreate
	创建一个event group。
	返回的就是handle。
xQueueCreate
	创建队列，返回handle。
	输入参数是len和size。
	
```

```
任务控制
vTaskSuspend
	通过handle挂起任务。
vTaskResume
xTaskResumeFromISR
vTaskDelay
```

```
调度器控制
vTaskStartScheduler
	初始化的最后一步。
vTaskEndScheduler
	基本不用。
vTaskSuspendAll
xTaskResumeAll
```

```
定时器
xTimerCreate
xTimerStart 
xTimerStop
pvTimerGetTimerID 
```



```
变量有严格的前缀标识变量类型属性：

c – char 字符型变量
s – short 短型变量
l – long  长整型变量
x – portBASE_TYPE 在 portmacro.h 中定义，便于移植的数据类型转定义
u – unsigned 无符号整型
p - pointer 指针
```

```
函数前缀：

v ：void 无返回类型
x ：返回portBASE_TYPE
prv ：私有函数，模块内使用
```

```
定义宏所属文件，也即在哪个文件内定义的：

port：比如portable.h中portMAX_DELAY
task：比如task.h中task_ENTER_CRITICAL
pd ：例如projdefs.h中定义的pdTRUE
config：例如 FreeRTOSConfig.h中定义的configUSE_PREEMPTION
err：例如 projdefs.h中定义的errQUEUE_FULL
```

至于这么严格的代码规范是否值得推崇，这个见仁见智，个人比较喜欢Linux代码风格，对于过于复杂的代码规范，在实际开发中个人觉得有时候会让人不爽。

# 中断管理

这时候我们就需要确定在 ISR Code 和 NON-ISR Code 中的运行时间的分配问题以及ISR程序如何与NON-ISR程序进行通讯的问题。



需要说明一下，

系统API函数和宏定义以 FromISR 和 FROM_ISR 结尾的

才能在中断处理函数ISR中使用，

其余的API或者宏定义如果在ISR中使用可能会导致错误。



FreeRTOS允许中断嵌套，

这里首先说明一下处理器中断系统中的

数值优先级Numberic prioirty 和 

逻辑优先级Logical priority，

数值优先级是写入在中断优先级寄存器中的

用于计算中断的优先级的数值，

逻辑优先级表示的是通过计算数值优先级得到的中断的实际优先级，

有的系统是数值优先级和逻辑优先级呈正比，

但是有的是呈反比，

比如ARM Cortex-M处理器就是后者，

中断的数值优先级越高表示的实际的逻辑优先级就越低，相反，数值优先级越小，表示的逻辑优先级越高。



中断嵌套指的是在某个中断正在处理的时候，

发生一个更高优先级的中断，

这就发生了中断嵌套。

在FreeRTOS系统中，要支持完整的中断嵌套，

需要将configMAX_SYSCALL_INTERRUPT_PRIORITY（或configMAX_API_CALL_INTERRUPT_PRIORITY）

表示的逻辑优先级设置成高于configKERNEL_INTERRUPT_PRIORITY表示的逻辑优先级。

处理器有7个优先级1 - 7，数值优先级越高代表的逻辑优先级越高。

configKERNEL_INTERRUPT_PRIORITY is set to one. 内核中断优先级设置为1，也就是最低优先级。

configMAX_SYSCALL_INTERRUPT_PRIORITY is set to three. 设置系统调用FreeRTOS API的中断优先级最高为3。



（1）建立一个全面的中断嵌套模型需要设置 configMAX_SYSCALL_INTERRUPT_PRIRITY为比 configKERNEL_INTERRUPT_PRIORITY 更高的优先级

如上假定常量 configMAX_SYSCALL_INTERRUPT_PRIRITY 设置为 3，configKERNEL_INTERRUPT_PRIORITY 设置为 1

（2）假定这种情形基于一个具有七个不同中断优先及的微控制器。这里的七个优先级仅仅是本例的一种假定，并非对应于任何一种特定的微控制器架构

（3）处于中断优先级 1 到 3(含)的中断会被内核或处于临界区的应用程序阻塞执行， 但是它们可以调用中断安全版本的 FreeRTOS API 函数

（4）处于中断优先级 4 （高于configMAX_SYSCALL_INTERRUPT_PRIRITY）及以上的中断不受临界区影响，所以其不会被内核的任何行为阻塞，可以立即得到执行

注：这是由微控制器本身对中断优先级的限定所决定的。通常 需 要 严 格 时 间 精 度 的 功 能 ( 如 电 机 控 制 ) 会 使 用 高 于configMAX_SYSCALL_INTERRUPT_PRIRITY 的优先级，

以保证调度器不会对其中断响应时间造成抖动

（5）不需要调用任何 FreeRTOS API 函数的中断，可以自由地使用任意优先级



# 参考资料

1、Lab32: QEMU + FreeRTOS

http://wiki.csie.ncku.edu.tw/embedded/Lab32

2、FreeRTOS 任务优先级说明

https://blog.csdn.net/sty124578/article/details/80534276

3、

https://www.cnblogs.com/iot-dev/p/11681067.html

4、

https://www.eet-china.com/mp/a35448.html

5、

https://blog.51cto.com/u_12956289/2916953

6、

https://www.cnblogs.com/smartjourneys/p/7939736.html