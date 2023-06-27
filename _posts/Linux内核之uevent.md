---
title: Linux内核之uevent
date: 2019-12-05 16:05:28
tags:
	- Linux
---

--

# 简介

什么是uevent机制？

这个问题需要从设备的热插拔说起。

典型的就是U盘的热插拔。

当我们在设备上插入U盘时，系统的usb hub就会检测到U盘插入，并且完成设备枚举过程。

所谓枚举，就是从U盘上读取出对应的信息。

然后在内核里创建相应的结构体。

但是usb设备千奇百怪，内核不可能预先把所有usb设备驱动都load到内存里。

也就说，插入设备的时候，系统里对应该usb设备的驱动可能还没有被加载到内存。

驱动ko文件，是放在硬盘上 。

那么我们就需要从用户态来载入这个驱动。

当前你可以手动来加载驱动，但是这个无疑是很麻烦的。

为了解决这种问题，就推出了uevent机制。

uevent机制是指：

当有新的设备加入时，内核将设备的消息发送到用户态，用户态有一个udev进程一直在监听这一类消息。

udev检测到消息后，会做一些之前配置好的工作，包括加载驱动。



uevent是kobject的一部分。

用于在kobject状态发生变化时，通知用户空间。

通知的途径有两种：

1、kmod。

2、netlink。

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/types.h>
#include <asm/types.h>
//该头文件需要放在netlink.h前面防止编译出现__kernel_sa_family未定义
#include <sys/socket.h>  
#include <linux/netlink.h>

void MonitorNetlinkUevent()
{
    int sockfd;
    struct sockaddr_nl sa;
    int len;
    char buf[4096];
    struct iovec iov;
    struct msghdr msg;
    int i;

    memset(&sa,0,sizeof(sa));
    sa.nl_family=AF_NETLINK;
    sa.nl_groups=NETLINK_KOBJECT_UEVENT;
    sa.nl_pid = 0;//getpid(); both is ok
    memset(&msg,0,sizeof(msg));
    iov.iov_base=(void *)buf;
    iov.iov_len=sizeof(buf);
    msg.msg_name=(void *)&sa;
    msg.msg_namelen=sizeof(sa);
    msg.msg_iov=&iov;
    msg.msg_iovlen=1;

    sockfd=socket(AF_NETLINK,SOCK_RAW,NETLINK_KOBJECT_UEVENT);
    if(sockfd==-1)
        printf("socket creating failed:%s\n",strerror(errno));
    if(bind(sockfd,(struct sockaddr *)&sa,sizeof(sa))==-1)
        printf("bind error:%s\n",strerror(errno));

    len=recvmsg(sockfd,&msg,0);
    if(len<0)
        printf("receive error\n");
    else if(len<32||len>sizeof(buf))
        printf("invalid message");
    for(i=0;i<len;i++)
        if(*(buf+i)=='\0')
            buf[i]='\n';
    printf("received %d bytes\n%s\n",len,buf);
}

int main(int argc,char **argv)
{
    MonitorNetlinkUevent();
    return 0;
}
```



实际上这里实现的类似于对 kobject 的派生，

**包含不同 kobj_type 的kobject 可以看做不同的子类。**

通过实现相同的函数来实现多态。

在这样的设计下，

每一个内嵌Kobject的数据结构(如kset、device、device_driver等)，

都要实现自己的 kobj_type ，并定义其中的回调函数。



**总结，Ktype以及整个Kobject机制的理解。**

Kobject的核心功能是：

保持一个引用计数，当该计数减为0时，自动释放（由本文所讲的kobject模块负责） Kobject所占用的meomry空间。

**这就决定了Kobject必须是动态分配的（只有这样才能动态释放）**。 

而Kobject大多数的使用场景，

是内嵌在大型的数据结构中（如Kset、device_driver等），

因此这些大型的数据结构，也必须是动态分配、动态释放的。

那么释放的时机是什么呢？

是内嵌的Kobject释放时。

但是Kobject的释放是由Kobject模块自动完成的（在引用计数为0时），那么怎么一并释放包含自己的大型数据结构呢？ 

  这时Ktype就派上用场了。

我们知道，Ktype中的release回调函数负责释放Kobject（甚至是包含Kobject的数据结构）的内存空间，那么Ktype及其内部函数，是由谁实现呢？

是由上层数据结构所在的模块！

因为只有它，才清楚Kobject嵌在哪个数据结构中，并通过Kobject指针以及自身的数据结构类型，找到需要释放的上层数据结构的指针，然后释放它。 

  讲到这里，就清晰多了。

所以，每一个内嵌Kobject的数据结构，例如kset、device、device_driver等等，都要实现一个Ktype，并定义其中的回调函数。

同理，sysfs相关的操作也一样，必须经过ktype的中转，因为sysfs看到的是Kobject，而真正的文件操作的主体，是内嵌Kobject的上层数据结构！ 

  **顺便提一下，Kobject是面向对象的思想在Linux kernel中的极致体现，但C语言的优势却不在这里，所以Linux kernel需要用比较巧妙（也很啰嗦）的手段去实现。**



现在我们就要结合代码分析uevent机制了，

而要分析这个机制我们就要从class_create和class_device_create这两个函数

来分析这个过程是怎么实现的。

我们现在先分析class_create：

下面是**class_create函数的层级关系**：

 从上面我们可以看出kobject在sysfs中对应的是目录（dir），

当我们注册一个kobject时，

会调用kobject_add(&k->kobj);

然后在其后创建class设备目录。

而同时我们可以看出class_create函数是为class_device_create函数做了目录的准工作。



下面我们从**class_device_create函数**开始分析，

看他是如何走到kobject_uevent函数的。

我们看class_device_create函数的层级关系：



 uevent模块通过kmod上报uevent时，

会通过call_usermodehelper函数，

调用用户空间的可执行文件（或者脚本，简称uevent helper）处理该event。

而该uevent helper的路径保存在uevent_helper数组中。

可以在编译内核时，通过CONFIG_UEVENT_HELPER_PATH配置项，静态指定uevent helper。

  **但这种方式会为每个event fork一个进程，**

随着内核支持的设备数量的增多，

**这种方式在系统启动时将会是致命的（可以导致内存溢出等）。**

因此只有在早期的内核版本中会使用这种方式，现在内核不再推荐使用该方式。

**因此内核编译时，需要把该配置项留空。**

在系统启动后，大部分的设备已经ready，

**可以根据需要，重新指定一个uevent helper，**

**以便检测系统运行过程中的热拔插事件。**

  这可以通过把helper的路径写入到"/sys/kernel/uevent_helper"文件中实现。

实际上，内核通过sysfs文件系统的形式，将uevent_helper数组开放到用户空间，

供用户空间程序修改访问，具体可参考"./kernel/ksysfs.c”中相应的代码。

**在/etc/init.d/rcS脚本中添加 echo "/sbin/mdev" > /proc/sys/kernel/hotplug，**

**会发现cat /sys/kernel/uevent_helper 即是/sbin/mdev。说明/proc/sys/kernel/hotplug中的可执行文件路径最终还是会写到/sys/kernel/uevent_helper中。**

自己手动echo "/kernel/main" > uevent_helper(之前的/sbin/mdev会被覆盖)，

当lsmod、rmmod时，/sys/kernel/uevent_helper中的/kernel/main会执行，表明事件已经上报给用户空间。



轮到mdev出场了，前面的描述都是在sysfs文件系统中创建目录或者文件，

**而应用程序访问的设备文件则需要创建在/dev/目录下。**

该项工作由mdev完成。

  mdev的原理是解释/etc/mdev.conf文件定义的命名设备文件的规则，

并在该规则下根据环境变量的要求来创建设备文件。

mdev.conf由用户层指定，因此更具灵活性。本文无意展开对mdev配置脚本的分析。



# 手动改uevent文件的方式触发事件

以下是一个示例，展示如何使用sysfs中的"uevent"文件来处理U盘插入和拔出事件：

1. 找到U盘对应的sysfs路径。可以通过以下命令找到U盘的设备路径：

   ```shell
   lsblk -o NAME,TYPE,MOUNTPOINT
   ```

   在输出中找到U盘对应的设备名称，例如"/dev/sdb"，然后在/sys/devices目录下找到相应的设备路径，如"/sys/devices/pci0000:00/0000:00:0a.0/usb1/1-1/1-1.2/1-1.2:1.0/host7/target7:0:0/7:0:0:0/block/sdb".

2. 进入U盘设备的sysfs路径：

   ```shell
   cd /sys/devices/pci0000:00/0000:00:0a.0/usb1/1-1/1-1.2/1-1.2:1.0/host7/target7:0:0/7:0:0:0/block/sdb
   ```

3. 打开"uevent"文件进行编辑：

   ```shell
   sudo nano uevent
   ```

4. 在"uevent"文件中输入以下内容：

   ```
   ACTION=add
   DEVPATH=/devices/pci0000:00/0000:00:0a.0/usb1/1-1/1-1.2/1-1.2:1.0/host7/target7:0:0/7:0:0:0/block/sdb
   SUBSYSTEM=block
   DEVNAME=sdb
   ```

   这些键值对描述了U盘插入事件的属性。"ACTION"指示设备的操作是添加（插入），"DEVPATH"是设备的路径，"SUBSYSTEM"指示设备所属的子系统，"DEVNAME"是设备的名称。

5. 保存并关闭"uevent"文件。

此时，内核会将U盘插入事件通知发送到用户空间。可以使用udev守护进程监听该事件并执行相应的规则或脚本，例如自动挂载U盘文件系统、启动特定应用程序等。

请注意，以上示例仅演示了使用sysfs中的"uevent"文件触发设备事件通知的基本流程。在实际应用中，通常会结合udev规则和自定义脚本来实现更灵活的设备事件处理。

# 参考资料

1、内核Uevent事件机制 与 Input子系统

https://www.cnblogs.com/sky-heaven/p/6394267.html

2、

http://www.wowotech.net/device_model/uevent.html

3、Netlink实现热拔插监控

https://blog.csdn.net/findaway123/article/details/53122437

4、

https://blog.csdn.net/W1107101310/article/details/80211885