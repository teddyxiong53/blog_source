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

# 用chatgpt来分析源代码

## atomic.h分析

FreeRTOS的`atomic.h`文件提供了原子操作相关的功能。原子操作是一种在多线程或多任务环境中保持操作的完整性的机制，确保在执行期间不会被中断。这在并发编程中非常重要，因为它可以防止多个任务同时访问和修改共享资源而引发的竞态条件和数据不一致性问题。

`atomic.h`文件的主要功能包括以下几个方面：

1. 定义原子数据类型：
   - `Atomic_t`：原子类型，用于在原子操作中保持数据的完整性。

2. 原子操作函数：
   - `Atomic_Init`：用于初始化原子变量。
   - `Atomic_Get`：获取原子变量的值。
   - `Atomic_Set`：设置原子变量的值。
   - `Atomic_Add`：原子地将一个值添加到原子变量。
   - `Atomic_Subtract`：原子地从原子变量中减去一个值。
   - `Atomic_Increment`：原子地将原子变量增加1。
   - `Atomic_Decrement`：原子地将原子变量减少1。
   - `Atomic_CompareAndSwap`：原子地比较并交换操作，用于原子地修改变量的值。

这些原子操作函数通过使用底层的硬件特性（如原子指令）或特定的编译器扩展来确保操作的原子性。在不同的体系结构和编译器上，实现方式可能会有所不同。

使用`atomic.h`文件中提供的原子操作函数，可以在FreeRTOS中编写更安全、可靠的多线程代码，避免竞态条件和数据不一致性问题。

## event_groups.h分析

在FreeRTOS中，`event_groups.h`文件提供了事件组（Event Groups）的功能。事件组是一种同步机制，用于多任务或多线程之间的通信和协调。通过事件组，任务可以等待特定的事件发生或清除事件，并可以通过设置、等待、等待任意和等待所有等操作来进行事件的管理。

以下是`event_groups.h`文件的主要功能和相关函数：

1. 定义事件组数据类型：
   - `EventGroupHandle_t`：事件组句柄类型，用于引用事件组。

2. 事件组操作函数：
   - `xEventGroupCreate`：创建一个事件组，返回一个事件组句柄。
   - `xEventGroupWaitBits`：等待事件组中的一个或多个特定位的事件发生。
   - `xEventGroupSetBits`：设置事件组中的一个或多个位。
   - `xEventGroupClearBits`：清除事件组中的一个或多个位。
   - `xEventGroupSync`：等待事件组中的所有位都被设置或清除。
   - `vEventGroupDelete`：删除事件组及其关联的资源。

通过这些事件组操作函数，任务可以在事件组上等待特定的位或任意位的事件发生，也可以设置、清除或等待所有位的事件。这种机制允许任务按需等待和触发事件，实现任务之间的同步和通信。

事件组通常用于以下情况：
- 等待多个任务完成特定的操作后再继续执行。
- 任务间的同步和互斥。
- 事件驱动的任务调度。

`event_groups.h`文件为多任务或多线程的开发者提供了一种强大的同步机制，可用于构建可靠的并发系统。通过合理地使用事件组，可以实现任务之间的协调、同步和通信，提高系统的性能和可靠性。

## freertos.h分析

`FreeRTOS.h`是FreeRTOS实时操作系统中的主头文件，它包含了许多宏定义、函数原型和数据结构的声明。下面是对`FreeRTOS.h`文件中一些重要部分的分析：

1. 版本信息：
   - `FREERTOS_MAJOR_VERSION`：FreeRTOS的主要版本号。
   - `FREERTOS_MINOR_VERSION`：FreeRTOS的次要版本号。
   - `FREERTOS_PATCH_LEVEL`：FreeRTOS的修订级别。

2. 数据类型和常量定义：
   - `BaseType_t`：基本数据类型，通常是`int`或`long`。
   - `TickType_t`：时钟滴答计数器类型，用于表示时间和延迟。
   - `TaskHandle_t`：任务句柄类型，用于引用任务。
   - `QueueHandle_t`：队列句柄类型，用于引用队列。
   - `SemaphoreHandle_t`：信号量句柄类型，用于引用信号量。
   - `EventGroupHandle_t`：事件组句柄类型，用于引用事件组。
   - `TimerHandle_t`：定时器句柄类型，用于引用定时器。
   - `pdTRUE`、`pdFALSE`：布尔值常量，表示真和假。
   - `pdPASS`、`pdFAIL`：操作返回值常量，表示成功和失败。
   - `portMAX_DELAY`：最大延迟常量，表示无限延迟。

3. 函数原型：
   - FreeRTOS内核和任务管理的函数原型，如任务创建、任务删除、任务挂起、任务恢复等。
   - 队列、信号量、事件组和定时器等各种对象的创建、删除和操作函数原型。

4. 宏定义：
   - FreeRTOS内核配置选项的宏定义，如调度器开关、堆栈溢出检测、时间片轮转调度等。
   - 中断和临界区管理的宏定义，如中断嵌套计数器、禁止/使能中断等。

`FreeRTOS.h`是使用FreeRTOS时必须包含的主要头文件，它提供了对FreeRTOS功能的访问、配置和控制。通过包含此头文件，开发者可以使用FreeRTOS提供的函数和数据类型，实现任务管理、内存管理、通信和同步等功能，构建可靠的嵌入式实时应用程序。

### pdTRUE的pd表示什么

pd是portable define的意思。

## list.h分析

`list.h`是FreeRTOS实时操作系统中的一个头文件，用于实现双向链表的数据结构和相关操作。双向链表在FreeRTOS中被广泛用于任务列表、队列和其他数据结构的实现。

以下是对`list.h`文件中一些重要部分的分析：

1. 数据结构定义：
   - `List_t`：双向链表的结构类型，表示一个链表。
   - `ListItem_t`：链表节点的结构类型，表示链表中的一个节点。

2. 宏定义：
   - `listSET_LIST_ITEM_OWNER`：将链表节点的拥有者指针与节点关联。
   - `listGET_LIST_ITEM_OWNER`：获取链表节点的拥有者指针。
   - `listGET_OWNER_OF_NEXT_ENTRY`：根据链表节点获取下一个节点的拥有者指针。
   - `listGET_ITEM_VALUE`：获取链表节点的值。
   - `listSET_ITEM_VALUE`：设置链表节点的值。

3. 链表操作函数：
   - `vListInitialise`：初始化链表。
   - `vListInitialiseItem`：初始化链表节点。
   - `vListInsertEnd`：将节点插入链表末尾。
   - `vListInsert`：将节点插入链表的指定位置。
   - `vListRemove`：从链表中移除节点。
   - `uxListRemove`：从链表中移除节点并返回链表长度。

这些函数和宏定义提供了对双向链表的创建、初始化、插入、删除和遍历等操作。通过使用`list.h`中定义的函数和数据结构，开发者可以方便地操作双向链表，实现任务列表、队列、定时器列表等各种数据结构。

双向链表的设计使得在FreeRTOS中能够高效地进行插入、删除和遍历操作，从而提供了一种灵活的数据结构，适用于实时操作系统的任务调度和通信需求。

## message_buffer.h 分析

`message_buffer.h`是FreeRTOS实时操作系统中的一个头文件，用于实现消息缓冲区的功能。消息缓冲区提供了一种在任务之间传递可变长度数据的机制，允许任务通过发送和接收消息进行通信。

以下是对`message_buffer.h`文件中一些重要部分的分析：

1. 数据类型定义：
   - `MessageBufferHandle_t`：消息缓冲区句柄类型，用于引用消息缓冲区。
   - `StreamBufferHandle_t`：流缓冲区句柄类型，与消息缓冲区共享。

2. 函数原型：
   - `xMessageBufferCreate`：创建一个消息缓冲区，返回一个消息缓冲区句柄。
   - `xMessageBufferCreateStatic`：创建一个静态消息缓冲区，使用静态分配的缓冲区内存。
   - `vMessageBufferDelete`：删除消息缓冲区及其关联的资源。
   - `xMessageBufferSend`：向消息缓冲区发送数据。
   - `xMessageBufferReceive`：从消息缓冲区接收数据。
   - `xMessageBufferSendFromISR`：从中断服务程序中向消息缓冲区发送数据。
   - `xMessageBufferReceiveFromISR`：从中断服务程序中接收消息缓冲区的数据。
   - `xMessageBufferReset`：重置消息缓冲区，清除缓冲区中的数据。

3. 宏定义：
   - `xMessageBufferIsEmpty`：判断消息缓冲区是否为空。
   - `xMessageBufferIsFull`：判断消息缓冲区是否已满。
   - `xMessageBufferSpacesAvailable`：获取消息缓冲区中剩余可用空间的数量。
   - `xMessageBufferBytesAvailable`：获取消息缓冲区中可读取的字节数量。

通过使用`message_buffer.h`文件中提供的函数和数据类型，开发者可以方便地创建、发送、接收和管理消息缓冲区。消息缓冲区是一种轻量级的通信机制，适用于任务之间传递可变长度数据的场景。它可以在任务之间实现异步通信，提供灵活的消息传递机制，用于构建复杂的任务间通信和同步方案。

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