---
title: Linux内核打开dev_dbg打印
date: 2020-04-10 16:29:51
tags:
	- Linux

---

--

```
/* If you are writing a driver, please use dev_dbg instead */
```



dev_dbg本质是上是调用了printk KERN_DEBUG。

要打开dev_dbg，需要2步：

第一步：

```
你调试的文件中必然包含了<linux/device.h>，或者<linux /paltforam_device.h>，后者包含了前者，在包含此头文件之前，使用#define DEBUG 1 来打开调试开关
```

第二步：

调整打印级别。



原来，三个宏作为判断条件决定了pr_debug到底采用哪种用法：

第一种用法，如果定义了CONFIG_DYNAMIC_DEBUG，就使用动态debug机制dynamic_pr_debug();

第二种用法，如果定义了DEBUG，就使用printk(KERN_DEBUG...)

第三种用法，默认情况下，不打印。



两条路可选了：要么动态debug，要么定义DEBUG宏。

先说一下如何定义DEBUG宏：

其实在kernel中很多driver已经定义好了这样的DEBUG选项，

前人栽树，后人乘凉，我们可以先看看有没有现成的。

例如，我们经常可以看到这样的配置选项和宏定义：

以DMA为例，在drivers/dma/Makefile中定义了编译选项

ccflags-$(CONFIG_DMADEVICES_DEBUG) := -DDEBUG
其作用相当于在drivers/dma/所有子文件定义了宏#define DEBUG

小伙伴们赶紧把CONFIG_DEBUG选项选上吧，然后重新编译kernel。

先别急，这样还不够，默认的console级别是7（在kernel/printk/printk.c中定义了#define DEFAULT_CONSOLE_LOGLEVEL7）

只有那些级别“小于7”的调试信息才能打印出来，

而printk(KERN_DEBUG...)的级别是7，那就还需要提高console打印级别。

如果要查看dma初始化的debug信息，那就直接改代码，

#defineDEFAULT_CONSOLE_LOGLEVEL 8。

如果是runtime，可以直接通过printk的sys接口调整打印级别 



下面再简单说一下kernel的动态调试

打开Enable dynamic printk() support（DYNAMIC_DEBUG），

那么所有的pr_debug()/dev_debug() 之类的函数在runtime就可以动态地使用了。

kernel动态调试提供一个debugfs接口:`<debugfs>/dynamic_debug/control `

```
这个文件可以用来获取已完成的调试信息列表，例如你要显示文件'svcsock.c'的1603行内容,你可以这样做：

nullarbor:~ # echo 'file svcsock.c line 1603 +p' >

        <debugfs>/dynamic_debug/control  

// 提供文件svcsock.c所有信息 

nullarbor:~ # echo -n 'file svcsock.c +p' >

        <debugfs>/dynamic_debug/control 
```

```
如果你想执行多个命令，你需要为每个加入“echo”分割，像这样：

nullarbor:~ # echo 'file svcsock.c line 1603 +p' >/proc/dprintk ;\

> echo 'file svcsock.c line 1563 +p' >/proc/dprintk

 

或者甚至是这样： 

nullarbor:~ # (

> echo 'file svcsock.c line 1603 +p' ;\

> echo 'file svcsock.c line 1563 +p' ;\

> ) > /proc/dprintk 

 

file可以替换成module,format等匹配方式，具体用法请参考Documentation/dynamic-debug-howto.txt
```



# 参考资料

1、

https://blog.csdn.net/renlonggg/article/details/79467437

2、

https://blog.csdn.net/helloanthea/article/details/25330809

3、

https://www.cnblogs.com/pengdonglin137/p/4621576.html

4、

https://blog.csdn.net/firstlai/article/details/52755115