---
title: Linux驱动之LDT
date: 2018-03-08 14:13:03
tags:
	- Linux驱动

---



LDT是Linux Driver Template的缩写。

代码在这里：https://github.com/makelinux/ldt





使用了这些linux技术：

1、module。

2、platform driver。

3、file ops。

4、kfifo。

5、interrupt。

6、tasklet。

7、work。

8、kthread。

9、timer。

10、misc dev

11、char dev

12、device model

13、configfs

14、uart

15、hw loopback

16、sw loopback

17、ftracer。

# 运行测试

1、直接在Ubuntu下make就好了。

2、运行。ldt-test是一个脚本。

```
teddy@teddy-ubuntu:~/work/test/driver/ldt$ ./ldt-test 
[sudo] password for teddy: 
stty: /dev/ttyS0: Permission denied
No loopback behind /dev/ttyS0 detected, running ldt driver with UART in loopback mode
LDT nonblock read/write test failed
expected 123rw
received 
LDT blocking read/write test failed
expected 123bl
received 

LDT mmap test passed
LDT ioctl test passed
-r--r--r-- 1 root root 0 3月   8 14:21 /sys/kernel/debug/ldt
trace_stat.log saved
ftrace.log saved
trace_pipe.log saved
functrace.log saved
kernel.log saved
```

测试基本是通过的。

不对，我用sudo ./ldt-test来测试一次，就通过了。

```
teddy@teddy-ubuntu:~/work/test/driver/ldt$ sudo ./ldt-test 
No loopback behind /dev/ttyS0 detected, running ldt driver with UART in loopback mode
LDT nonblocking read/write test passed
LDT blocking read/write test passed
LDT mmap test passed
LDT ioctl test passed
-r--r--r-- 1 root root 0 3月   8 14:33 /sys/kernel/debug/ldt
trace_stat.log saved
ftrace.log saved
trace_pipe.log saved
functrace.log saved
kernel.log saved
```



我们现在看看ldt-test脚本的内容，看看做了些什么。

1、设置dmesg级别为7，就是都打印出来。

2、卸载ldt模块，避免重复加载。

3、清空dmesg。

4、配置uart。用来演示驱动。

```
stty -F /dev/ttyS0 115200
```

5、测试串口。

6、加载驱动

7、对/dev/ldt设备进行读写测试。

8、进行block读写测试。

9、进行mmap测试。

10、ioctl测试。

11、保存log。

# 看ldt.c里的内容

对照着生成的kernel.log文件来看看。

##了解定义的全局变量

先把文件从上到下读一遍。

port=0x3f8，这个是pc平台上的uart的串口号。

默认8个port。

irq是4.

定义FIFO大小为128 。一定要是2的幂。

bufsize是8页。

定义结构体ldt_data。

```
1、void *in_buf。
2、void *out_buf。
3、in_fifo
4、out_fifo。
5、spinlock_t ffio_lock。
6、work_queue_head_t readable，writeable。
7、mutex readlock，writelock。
8、void __iomem *port_ptr。
9、uart_detected。
```

一个tasklet，就是给串口的中断用的。

定义了一个ldt_timer。

是一个misc设备，次设备号是255 。

## 从ldt_init开始读

1、ldt_data_init。

```
1、drvdata这个全局指针，kzalloc，
2、把里面的成员都初始化。
	3对，
```

2、继续对drvdata的成员进行其他的初始化。

```
in_buf用alloc_page_exact来分配8个页。标记为PG_reserved。这个技术我看驱动用得不多。
out_buf一样处理。
```

3、uart_probe。取得串口的寄存器的虚拟地址，进行寄存器配置操作。

4、启动ldt_timer，每100ms执行一次。

5、debugfs创建文件。

6、注册ldt_miscdev。

## 结合ldt-test过程来看

1、insmod的时候，没有调用到任何函数。

2、`echo 123rw > /dev/ldt`调用了open和write函数。

```
open：就打印了一行东西。
write：用kfifo_from_user来拷贝数据。
	然后调度ldt_tasklet。
	到了ldt_tasklet_func函数里。
		
```

然后会调用close函数。

3、`cat/dev/ldt > R.tmp & `这个后面有个sleep，现在里面还没有东西，所以会阻塞。









