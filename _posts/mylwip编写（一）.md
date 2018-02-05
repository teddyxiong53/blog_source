---
title: mylwip编写记录
date: 2018-02-04 12:07:49
tags:
	- lwip

---



lwip为了兼容各种情况，代码里各种宏嵌套，让代码逻辑显得很不清晰。

为了可以深入理解lwip，我决定自己来实现一个简单的lwip，先实现ping通，再实现udp功能。

名字就叫mylwip。

# 1. 环境准备

还是借助vexpress、qemu、rt-thread的环境。

在把lwip-2.0.2目录替换为我的mylwip目录。逐步往里面加东西。

因为重点还是lwip，所以其他内容采用拷贝的方式来做。以免分散太多精力。

可以上传到github上，也许可以逐步完善。

# 2.目录建立

```
api  apps  arch  core    include   netif
```

先建立这些目录。

````
teddy@teddy-ubuntu:~/work/rt-thread/rt-thread/components/net/mylwip/src$ tree
.
├── api
├── apps
├── arch
├── core
├── include
└── netif
````

第一步应该做什么。

1、把arch目录的内容拷贝过去。整理一下。

里面文件结构这样：

```
├── include
│   └── arch
│       ├── bpstruct.h：bp是begin pack，这个为了把struct pack一下而定义的。对于gcc没有用。清空。
│       ├── cc.h：与编译器相关的，只留下gcc的情况的。
│       ├── epstruct.h：ep是end pack。清空。
│       ├── perf.h：留下2个空宏。PERF_START，PERF_STOP。
│       └── sys_arch.h：定义了sem、Mutex、mbox、thread类型。
└── sys_arch.c
```

#3. sys_arch.c整理

这个整理就涉及到很多的东西了。

从include的头文件开始看。

1、lwip/sys.h。定义了sys_mutex_new等函数。拷贝过来。删除多余的东西。

包含了lwip/opt.h。这个是系统默认的配置。如果你不在外面的lwipopt.h里定义，就用这里的默认值。

lwipopt.h放在src根目录。放进去，改。

包含了lwip/err.h。char类型的错误。错误枚举。0到-16 。

lwip/sys.h里的函数都是以sys_xxx这样形式。

> include/lwip目录下的头文件的保护宏都是：
>
> LWIP_HDR_XXX_H这种格式。

lwip/debug.h：包含了DEBUG_ON等宏。

2、lwip/opt.h：这个完全不改。

3、lwip/stats.h。全部改成空宏。

4、lwip/netif.h。这个设计到具体内容了。包含的内容就大大增加。

```
1、lwip/ip_addr.h。
	lwip/opt.h
	lwip/def.h：提供了几个hton函数。
	ip4_addr.h：定义一堆的ip地址工具宏。
		lwip/arch.h
			包括arch/cc.h。
			我要手动把所有#define PACK_STRUCT_STRUCT __attribute__((packed))这个宏手动替换。
	ip6_addr.h：去掉这个。
 2、pbuf.h。
 	删除复杂的情况。
 把netif.h里ipv6的都删掉，ipv4的宏也去掉。让代码显得清晰。
 
```

5、netifapi.h。这个在ethernetif.c里有用到。

把特别的变量声明方式改为普通的。

把dhcp和autoip的头文件去掉。

```
lwip/priv/tcpip_priv.h
	lwip/tcpip.h：tcpip_xxx函数。例如tcpip_init函数。
	lwip/timeouts.h：
	定义了tcpip_msg结构体。
	
```

6、netif/ethernetif.h。

```
定义了eth_device结构体。
eth_device_xxx函数。
```

7、lwip/opt.hsio.h不要了。这个串口的。

8、lwip/init.h。版本宏定义。lwip_init函数。

9、lwip/dhcp.h。去掉。

10、lwip/inet.h。

```
定义inet地址宏。跟ip的类似。
```

## sys_arch.c函数

按照从上到下的顺序来看。

1、netif_device_init。

```
可以看到netif->state这个void指针，被用来存放eth_device了。
```

2、tcpip_init_done_callback。

```
这个是tcpip初始化完成之后的回调。实际上做的是把netif类型的device遍历一遍，初始化掉。
```

3、lwip_system_init。这个是lwip的初始化入口。当然是rt-thread的适配的。

4、sys_init。空的。lwip要求必须有的。

5、剩下的就是os内容适配了。



> 接下来，就还是从sys-arch.c出发。从init函数开始进去。逐步补全里面的实现。
>
> 接下来的c语言部分，就主要用写的方式来进行。



# tcpip_init函数实现

在api/tcpip.c里。

tcpip_init需要lwip_init和tcpip_thread。thread先实现一个死循环。里面等一个邮箱。不干任何事情。

lwip_init先来一个空的实现。

现在要改一改编译文件，保证可以编译过。保证线程可以起来。

现在编译有一大堆的错误。解决起来比较费劲。

这个编译体系是scons做的。不能子目录编译。先不管。

现在是其他文件包括了netdb.h。我先把这个文件写出来。

这个文件里的内容全部被DNS的宏包起来了。我前面犯了一个错误，就是把DNS宏的内容都去掉了。

没事，加回来就行了。

看了一下，目前我还没有改动相关内容。把配置打开。

现在改了这些配置。

```
1、//#define BSP_DRV_EMAC 这样就不会编译以太网驱动，我暂时就不用写这一块的。
2、net目录下的SConscript：
#list = os.listdir(cwd)
list = ['mylwip']，强制编译我的mylwip。
```

现在挨个处理错误。现在的错误比较可控了。

1、` fatal error: lwip/sockets.h: No such file or directory`。

加入这个文件。

```
1、依赖了lwip/errno.h。加入。
```

2、`fatal error: lwip/api.h: No such file or directory`

加入，简单整理，不删太多。

3、lwip/netbuf.h:

4、lwip/dns.h

5、lwip/mem.h

6、lwip/memp.h。这个就是很绕的。但是我暂时不动它。

同时需要把memp_std.h放到priv目录下。还有memp_priv.h。

还有tcpip-priv.h。

到现在编译就到了链接阶段了。找函数定义了。

1、list_if和set_if。这个是给ifconfig用的。先给个空的。

在ethernetif.c里。

这个文件要依赖ethernetif.h文件。拷贝过来。

2、dns的dns_getserver、、set_dns。

在src/core/dns.c里。空实现先。

3、ip4addr_ntoa在src/core/ipv4_addr.c里。

4、然后就是socket函数的实现了。

在src/api目录下新建sockets.c文件。都都空实现。

现在链接，报了重复定义的错误。我的函数明显只有一个。发现是我在SConscript里一个文件写了2次，所以就重复定义了。

解决其他的链接问题。

1、在tcpip.c里增加tcpip_input的空实现。

2、netif_add找不到。在netif.c里空实现。这个文件都还没有。在src/core下面。

现在终于编译过了。

当前目录是这样的：

```
├── api
│   ├── netdb.c
│   ├── netifapi.c
│   ├── sockets.c
│   └── tcpip.c
├── apps
├── arch
│   ├── include
│   │   └── arch
│   │       ├── bpstruct.h
│   │       ├── cc.h
│   │       ├── epstruct.h
│   │       ├── perf.h
│   │       └── sys_arch.h
│   └── sys_arch.c
├── core
│   ├── def.c
│   ├── dns.c
│   ├── ipv4
│   │   └── ip4_addr.c
│   ├── netif.c
│   └── timeouts.c
├── include
│   ├── lwip
│   │   ├── api.h
│   │   ├── arch.h
│   │   ├── debug.h
│   │   ├── def.h
│   │   ├── dns.h
│   │   ├── err.h
│   │   ├── errno.h
│   │   ├── inet.h
│   │   ├── init.h
│   │   ├── ip4_addr.h
│   │   ├── ip_addr.h
│   │   ├── mem.h
│   │   ├── memp.h
│   │   ├── netbuf.h
│   │   ├── netdb.h
│   │   ├── netifapi.h
│   │   ├── netif.h
│   │   ├── opt.h
│   │   ├── pbuf.h
│   │   ├── priv
│   │   │   ├── memp_priv.h
│   │   │   ├── memp_std.h
│   │   │   └── tcpip_priv.h
│   │   ├── sockets.h
│   │   ├── stats.h
│   │   ├── sys.h
│   │   ├── tcpip.h
│   │   └── timeouts.h
│   └── netif
│       └── ethernetif.h
├── lwipopts.h
├── lwippools.h
└── netif
    └── ethernetif.c
```

把这个版本先上传到github。然后逐步上传。



运行出错。

```
initialize rti_board_end:0 done
initialize lwip_system_init(mutex != RT_NULL) assertion failed at function:rt_mutex_take, line number:650 
QEMU: Terminated
```

调试一下，发现几个问题：

1、前面还不能用printf，只能用rt_kprintf。不然打印不出来。

现在初始化这里走不下去。

完善一下。

我把这个注释掉。就走下去了。

```
//sys_thread_new("tcpip", tcpip_thread, NULL, 1024, 8);
```

我觉得这里逻辑会走不下去才对啊。

lwip_system_init里等一个sem。rt_sem_take在os没有启动之前，肯定是拿不到的。

但是这里拿不到。os应该就启动不了。但是实际上却是可以启动的。

现在只能调试一下我改动之前的代码看看。

这个是只有eth0时的打印。

```
 \ | /
- RT -     Thread Operating System
 / | \     3.0.2 build Feb  4 2018
 2006 - 2017 Copyright by rt-thread team
func:rtthread_startup, line:253 
do components intialization.
initialize rti_board_end:0 done
initialize lwip_system_initfunc:lwip_system_init, line:160 
func:lwip_system_init, line:162 
func:tcpip_init_done_callback, line:76 
func:tcpip_init_done_callback, line:96 , device->type:0
func:tcpip_init_done_callback, line:96 , device->type:0
func:tcpip_init_done_callback, line:135 
func:lwip_system_init, line:170 
lwIP-2.0.2 initialized!
:0 done
initialize dfs_init:0 done
initialize rt_mmcsd_blk_init:0 done
initialize rt_mmcsd_core_init:0 done
initialize pl180_init:0 done
initialize dfs_romfs_init:0 done
initialize dfs_ramfs_init:0 done
initialize elm_init:0 done
initialize libc_system_init:0 done
initialize pthread_system_init:0 done
initialize clock_time_system_init:0 done
initialize rt_i2c_core_init:0 done
initialize mnt_init:0 done
initialize smc911x_emac_hw_init:0 done
initialize finsh_system_init:0 done
hello rt-thread
```

这个顺序跟代码里调用函数的顺序差别很大啊。

没什么。我把rt_components_board_init跟rt_components_init 这2个弄混了。

rt_components_init这个里面才调用了lwip的初始化。是在main_thread_entry里调用的。所以就是lwip是在os完全启动之后才调用的。所以就不存在那个sem拿不到的情况了。

另外，启动的时候，遍历device的时候，还没有找到任何的netif 。

最后是smc911x_emac_hw_init这个里才发现的。而这个是init.6的。是排在最后的。

发现问题是sys_timeouts_mbox_fetch这个是空实现，导致线程一直没有阻塞狂运行。

先把tcpip_thread这个线程里留空。

现在可以正常进入到shell了。

> 接下来怎么做呢？开始补全lwip_init里的内容。

# lwip_init实现

1、新建src/core/init.c文件。

2、加入core/mem.c。

分配给lwip用的内存，是给16000字节。

3、加入core/memp.c。把多余宏的分支都去掉。整理一下。

4、加入core/pbuf.c。整理好。

5、core/netif.c完善。

我知道第二步应该完成什么了。应该保证可以看到loop这个netif。

netif_init。

为了方便定位问题，我加入我自己的调试函数。myprintf。目前因为是在mylwip里用。而所有c文件都包含了lwip/opt.h这个文件。我在这个文件最后加上：

```
extern char *basename(char *s);


#define myprintf(...) do {\
                        rt_kprintf("[%s][%s][%d]: ", basename(__FILE__), __func__, __LINE__);\
                        rt_kprintf(__VA_ARGS__);\
                        rt_kprintf("\n");\
                       }while(0)
#define mylogd(...) do {\
                            rt_kprintf("[DEBUG][%s][%s][%d]: ", basename(__FILE__), __func__, __LINE__);\
                            rt_kprintf(__VA_ARGS__);\
                            rt_kprintf("\n");\
                           }while(0)
#define myloge(...) do {\
                            rt_kprintf("[ERROR][%s][%s][%d]: ", basename(__FILE__), __func__, __LINE__);\
                            rt_kprintf(__VA_ARGS__);\
                            rt_kprintf("\n");\
                           }while(0)
#define mylogw(...) do {\
                            rt_kprintf("[WARN][%s][%s][%d]: ", basename(__FILE__), __func__, __LINE__);\
                            rt_kprintf(__VA_ARGS__);\
                            rt_kprintf("\n");\
                           }while(0)         
```

另外需要定义一个basename的函数。本来这个是标准C函数，但是现在就是找不到，就从musl里找来一个。

```
char *basename(char *s)
{
	size_t i;
	if (!s || !*s) return ".";
	i = strlen(s)-1;
	for (; i&&s[i]=='/'; i--) s[i] = 0;
	for (; i&&s[i-1]!='/'; i--);
	return s+i;
}
```

实际效果是这样：

```
[init.c][lwip_init][11]: test myprintf
[ERROR][init.c][lwip_init][12]: test myloge
[WARN][init.c][lwip_init][13]: test mylogw
[DEBUG][init.c][lwip_init][14]: test mylogd
```

接下来，希望可以用ifconfig看到loop的信息。

在ethernetif.c里。实现list_if函数。先只实现查询是否up，ip地址这些基本信息。

需要访问netif_list。所以netif_add需要实现。不然这个netif_list就是空的。

进行编译，现在发现错误增加了很多，memp.c引入了很多。暂时把udp的关闭。

arp也暂时关闭。

不得不改opt.h里一个点。

现在core/init.c里：

```
void lwip_init(void)
{
    mem_init();
    memp_init();
    pbuf_init();
    netif_init();
}
```

现在可以查询到loop的信息了。上传版本。

另外开一篇文章。



