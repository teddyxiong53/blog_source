---
title: directfb代码分析
date: 2021-07-15 09:58:33
tags:
	- gui

---

--

# 代码分析

桌面GUI系统涉及很多图像运算，

比如画点、画线、填充、透明度处理、平滑度处理、层的叠加、字体处理、贴图等等。

如果这些运算都由CPU来处理，那这将是对CPU的一个很大的负载。

在QT的文档中曾说到，

假如一个图形运算让加速设备来做需要1到2个CLK，

同样的图形运算让CPU来算则至少需要20个CLK，

而且，对于嵌入式SoC来说，CPU的频率和SDRAM/DRAM的带宽始终是图形运算的瓶颈。

所以这些芯片的图形加速能力有无、高低，最终决定其目标GUI的质量。



近两年嵌入式设备主芯片越来越多的嵌入了2D/3D加速功能，

由此软件可以搭建越来越复杂、炫酷、先进的桌面系统，如Qt/Android等。

这些加速硬件，通常也因其是否拥有私有内存、是否支持3D、加速接口是否可编程等特性而分为三六九等。

硬件的加速功能如果要在目标GUI系统中跑起来，

还得需要一些软件中间层为不同的硬件加速提供同一的接口，并且为上层GUI提供服务。

DirectFB就是这样一个软件中间层,它主要为上层提供2D加速服务。

**OpenGL/ES 主要为上层提供3D加速服务。**

DirectFB是一个专门针对Linux图形库设计的图形加速中间层。

它的上层直接面向图形库比如QT，提供如显示、画图、输入设备控制等服务，

他的下层直接面向GFX加速硬件，**要求硬件驱动实现全部或部分预定的画图函数**。



 DirectFB由超级接口IDirectFB为上层提供接口调用，其他所有接口都由此接口生成，这些接口内容包括：

  =========================
  . IDirectFBScreen
  . IDirectbFBDisplayLayer

   IDirectFBSurface



dfb由下面几个部分构造

```
基本库函数
	direct。这个目录下放的是一些公共函数。包括哈希表、链表、线程、调试信息、signal处理
	fusion。有2个版本。单进程版本和多进程版本。多进程版本需要linux-fusion这个内核模块支持。
	voodoo。不清楚。
对第三方组件库的包装。
	在interfaces目录下。
	interfaces这个名字容易引起误解，它并不是dfb对外提供的接口。
	而是把第三方接口纳入到dfb的接口。
	包括3个部分：
	字体。IDirectFBFont接口来处理字体。字体有点阵字体和矢量字体。freetype2就是矢量字体。
		DFB定义了IDirectFBFont接口来处理字体
	图片。
		DFB定义了IDirectFBImageProvider接口来处理图片
	视频。
		DFB定义了IDirectFBVideoProvider接口来处理视频，
核心代码
	在src目录下。
	DFB的core由多个部分组成，
	每个部分称为一个core_part，都实现同一个接口CorePart。
	这个接口并不描述它们的功能，而是用于管理的。
	初看这些函数时，可能会感到有些奇怪。
	最好要先了解DFB采用的master/slave模型：
	第一个运行应用程序是master进程，后来运行的应用程序是slave进程。
	master进程负责初始化和~初始化arena，它只能在所有slave退出之后才能退出。
	而slave进程则可以随时加入arena，也可以随时退出arena。
对外接口
	这主要是给上层应用程序使用的。
	IDirectFBInputDevice: 输入设备
    IDirectFBScreen: 屏幕。
    IDirectFBSurface: 绘图表面。
    IDirectFBPalette: 调色板。
    IDirectFBFont: 字体
    IDirectFBImageProvider：图片
    IDirectFBVideoProvider：视频
    IDirectFBWindow：窗口
    DirectFBEventBuffer: 事件缓冲
窗口管理器。
	在wm目录下。
	DFB实现了两个窗口管理器。
	default：实现了基本的窗口管理功能，支持一些快捷键。
	unique：功能也很弱，不过架构还可以，加入自己的功能很方便。
输入设备
	这部分代码在inputdrivers目录下。
	其实这些代码并不是真正的驱动，只是一个adapter层，
	它把从linux设备文件读到的事件，转换成DFB自己的事件格式，
	然后调用dfb_input_dispatch把事件分发出去。
	
输出设备。
	这部分代码在system目录下。这也是一个adapter层，主要对显示设备的抽象，
	有的也包括对输入事件的处理。其中包括：
```

核心组件包括下面几个组件：

dfb_core_clipboard: 剪切板。
dfb_core_colorhash：调色板。
  dfb_core_gfxcard：图形卡，主要完成基本的绘图功能，如绘直线、填充等等。
dfb_core_input：输入设备。
dfb_core_layers：分层功能，好像要硬件支持，通常都只有一个层。
dfb_core_screens：逻辑屏幕(可能像X一样支持多个屏幕吧，不太清楚，有时间再研究)。
dfb_core_system：显示输出，把gfxcard绘制后的图形数据输出到屏幕上，即可以通过fbdev输出到本机屏幕上，也可以通过sdl/x11/vnc输出到远程主机的屏幕上。对于像sdl/x11等，也包括对输入事件的处理。
dfb_core_wm：窗口管理器。

以上这些*core_part*，有的是直接实现的，比如*clipboard*。有的只是一层包装，具体的实现在一个独立的共享库中，在运行时通过参数来控制加载具体的实现，如*system*。



```
master/slave模型。
	master/slave是DFB的基本模型，一定要先了解它，否则很难了解DFB的基本架构。
reactor模式。
	DFB中的消息，无论是进程内的，还是进程间的，都是通过reactor来传递的。
	这是一种简单的发布-订阅机制，谁关心谁就注册。
	不先弄清楚reactor的机制，很容易就被消息的流向搞糊涂了。
加锁术语。
	加锁/解锁动作常用lock/unlook、acquire/release、 wait/release等术语，
	而DFB里使用skirmish_prevail/skirmish_dismiss。
	
引用计数术语。
	增加/减少引用计数常用ref/unref、addref/release等术语。
	DFB里使用了ref/unref，同时增加了几个动作：
	link/unlink用于增加和减少全局引用计数，
	ref增加的计数，只要应用程序退出，fusion自动释放这个引用计数。
	而link增加的引用计数非要用unlink减少才行，应用程序退出时不会自动减少。
	inherit: 继承另外一个对象的引用计数，即把被继承的对象的引用计数加到继承者身来，
	不但如此，当被继承的对象的引用计数增减时，自动增减继承者的引用计数。
注册/注销术语。
	注册/注销常用register/unregister等术语，DFB使用了attach/detatch。
	
内核对象的宏。
	DFB用宏FUSION_OBJECT_METHODS去实现一个fusion object的子类，
	FUSION_OBJECT_METHODS是在object.h里定义的。
	像CoreWindow和CoreSurface等内核对象，都调用这个宏去实现自己的方法。

```



核心组件都是以共享库形式存在的，这里主要是加载这些共享库，并调用相应的初始化函数。为了避免框架与组件之间的耦合，DirectFB是通过遍历目录去加载的，删除不必要插件可以提高加载速度。

## 对外头文件

### directfb.h

这个文件在7500行左右。

这样声明了接口。

```
D_DECLARE_INTERFACE( IDirectFB )
展开是：
typedef struct _IDirectFB IDirectFB;
```

对应的定义是：

```
#define D_DEFINE_INTERFACE( IFACE, ... )          \
     struct _ ## IFACE {                          \
          void          *priv;                    \
          int            magic;                   \
          int            refs;                    \
                                                  \
          DirectResult (*AddRef)( IFACE *thiz );  \
          DirectResult (*Release)( IFACE *thiz ); \
                                                  \
          __VA_ARGS__                             \
     };
```

这个是最基础的interface。

```
/*
 * Declare base interface
 */
D_DECLARE_INTERFACE( IAny )
```

然后是一些简单的基础结构体类型定义。例如point、color。以及配套的工具宏。

接口函数：

```
DirectFBInit
DirectFBSetOption
	参数是键值对。char *类型。
DirectFBCreate
	得到IDirectFB指针。
	
```



接口的设计风格：

函数返回值都是DFBResult类型。其他的返回值，通过指针参数来进行返回。



工程组织

DirectFB使用C语言实现了面向对象思想，

源码中大量的使用函数指针，

**加上一些关键变量、函数的申明和定义都使用宏来完成，**

源代码的可读性不是很好。

在阅读DirectFB源码之前必须先明白它的源码组织方式。

**所有对外接口的定义都在directfb.h中，**

接口申明使用DECLARE_INTERFACE宏，定义使用DEFINE_INTERFACE。

**每个接口的实现单独成一个C文件，文件名与接口名相同。**

接口的方法采用函数指针的方式实现，

**方法名与其所指的实际函数之间的对应关系是：“函数名=接口名_方法名”，**

如IDirectFBWindow_CreateEventBuffer为IDirectFBWindow接口CreateEventBuffer方法的具体实现。



*fusion*使用了*reactor*设计模式，

简单的说就是订阅－发布模式。

*reactor*是事件宿主，所有关心它的模块都向其注册*reaction*，

当*reactor*有事件产生时，它会将事件发布给所有关心它的模块。

对于*reactor*的理解，以下几点需要注意：

1、reactor不是消息循环。

2、reactor不是消息队列。

3、reactor不是通信的实体。

*reactor*的本质是消息代理，是消息过滤装置。

类似于MiniGUI的进程版和线程版，

fusion也支持进程和线程两种通讯模型，

通过编译宏FUSION_BUILD_MULTI控制。

但在进程模型下，fusion没有区分通信的双方是在进程内还是进程间，没有对线程间通讯做优化。

同时，进程模型是与操作系统绑定的——需要在Linux内核中插入fusion模块。

fusion只提供了最基本的事件通知机制，

它本身不提供消息队列，也不区分同步和异步消息。

对于这些传统消息队列的特性，需要在reaction的基础上来封装实现。

实际上这与MiniGUI的消息机制已经有很大的不同，

fusion的原则是“关心则来注册”，

MiniGUI是“主动将消息发送到关心的窗口”。

fusion将消息处理分为全局和局部两种。

在消息dispatch时指定该消息是全局还是局部有效，

全局消息会先进入全局处理函数，之后才是局部函数。

局部消息则不会进入全局处理函数。


他们之间的关系主要是一些一对一或是一对多的关系：

1 IDirectFB (顶层) <--> N 屏幕(Screens)
1 屏幕(Screen) <--> N 层(Layers)
1 层(Layer) <--> 1 主表面(Primary Surface)
1 层(Layer) <--> N 窗口(Windows)
1 窗口(Window) <--> 1 窗口表面(Window Surface)
1 表面(Surface) <--> N 子表面(Subsurfaces)



**通常的状况是一个屏幕有一个显示层，但是DFB支持他们每个有多个实例**



++dfb这个lib，是不是必须的？

有没有被编译？

能够把C++的部分全部去掉吗？

看了一下lib目录下的Makefile.am

```
SUBDIRS = direct fusion $(ONE_DIR) $(VOODOO_DIR) $(FUSIONDALE_DIRS) $(FUSIONSOUND_DIRS)
```

并没有编译++dfb的。

但是搜索.o文件，可以看到++dfb里的文件都被编译了。

得到的是这个库：lib++dfb-1.7.so.7.0.0

也被安装到板端了。

我去掉这个库，看看能不能运行起来。

以df_input为例，看看链接了哪些动态库

```
# ldd ./df_input 
        libstdc++.so.6 => /lib/libstdc++.so.6 (0xf733d000)
        libz.so.1 => /usr/lib/libz.so.1 (0xf731a000)
        libdirectfb-1.7.so.7 => /usr/lib/libdirectfb-1.7.so.7 (0xf70d9000)
        libfusion-1.7.so.7 => /usr/lib/libfusion-1.7.so.7 (0xf70ae000)
        libdirect-1.7.so.7 => /usr/lib/libdirect-1.7.so.7 (0xf7062000)
        libpthread.so.0 => /lib/libpthread.so.0 (0xf703c000)
        libc.so.6 => /lib/libc.so.6 (0xf6f50000)
        libm.so.6 => /lib/libm.so.6 (0xf6ed6000)
        /lib/ld-linux-armhf.so.3 (0xf7447000)
        libgcc_s.so.1 => /lib/libgcc_s.so.1 (0xf6eac000)
        libdl.so.2 => /lib/libdl.so.2 (0xf6e97000)
        librt.so.1 => /lib/librt.so.1 (0xf6e7f000)
```

没有用++dfb的。

但是dfbshow的就用到了。

```
# ./dfbshow 
./dfbshow: error while loading shared libraries: lib++dfb-1.7.so.7: cannot open shared object file: No such file or directory
# 
```

因为dfbshow就是在examples/++dfb目录下的。

基本是没有用++dfb的。++dfb的可以不管。

把代码从source insight里去掉，避免影响我分析代码。

```
#ifdef __cplusplus
#include <directfb++.h>
#endif
```



没有使能multi的时候，fusion/shm使用的是fake.c的。

voodoo这个东西应该也是没有用的。

```
if ENABLE_VOODOO
PROXY_DIR = proxy
endif
```

proxy是为voodoo服务的，那么也应该是没有用的。



既然opendfb，是在directfb上精简了。那么看opendfb可能会更清晰一些。

虽然我不一定使用opendfb。



这些宏层层嵌套展开，实在是非常麻烦。

DIRECT_INTERFACE_IMPLEMENTATION

这个就是给interfaces目录下的用的。给图片、字体这些库适配对接用的。

我以这个为例。

idirectfbimageprovider_bmp.c

这个是处理bmp图片的。

相对来说是比较简单的。

总共500行代码左右。

文件的前面：

```
#include <direct/interface_implementation.h>

DIRECT_INTERFACE_IMPLEMENTATION( IDirectFBImageProvider, BMP )
```

这个展开得到的是：

```
static DirectInterfaceFuncs interface_funcs = {
     /* GetType */            GetType,
     /* GetImplementation */  GetImplementation,
     /* Allocate */           Allocate,
     /* Deallocate */         Deallocate,
     /* Probe */              (void*) Probe,    //FIXME
     /* Construct */          (void*) Construct //FIXME
};
static const char *       
GetType( void )           
{                         
     return "IDirectFBImageProvider";        
}                         
static const char *        
GetImplementation( void )  
{                          
     return "BMP";         
}                          
void                                              
IDirectFBImageProvider_BMP_ctor( void )                      
{                                                 
     DirectRegisterInterface( &interface_funcs ); 
}                                                 
void IDirectFBImageProvider_BMP_dtor()
{
	DirectUnregisterInterface( &interface_funcs ); 
}
```

然后就看Probe、Construct这些实现入口函数。

Probe什么时候被调用？

```
DirectResult
DirectProbeInterface( DirectInterfaceFuncs *funcs, void *ctx )
{
     return (funcs->Probe( ctx ) == DR_OK);
}
```

这个是被这里调用：

```
thiz->GetInterface = IDirectFB_GetInterface;
```

GetInterface看看这个指针是怎么被使用的。

没有被调用的地方。

只有几个test程序里有用到。

在完整的directfb里，在proxy/dispatcher里有用到。

Dispatch_GetInterface

但是不对，这个其实也是间接调用。

lib/direct/interface.c。应该是这里面调用了。

DirectGetInterface

Probe确实没怎么用。

Construct有用。

这样实现的继承，实在是非常拧巴。



最关键，还是要把fusion流程梳理清楚。



在传统的DirectFB应用中，所有的应用程序都在一个进程中，

在性能上，有一些优势，

然而一个应用程序不稳定会造成整个系统的不稳定。

若采用C/S模型，无疑是重蹈X Widnow的覆辙，会丧失性能上的优势。

所以DirectFB采用了另外一种方式，

与C/S相区别，称之为主从模型（Master/Slave）。

**它加了一个称之为fusion的内核模块。**

Fusion是熔化的意思，

多个应用程序在不的进程空间里，

通过这个内核模块通信，在这里，一切都溶为一体了。

Master应用程序负责初始化一个称为竞技场的东西，

**其它Slave应用程序可以加入或者退出竟技场。**

**当Master退出时，则其它所有Slave都必须退出。**



Fusion里采用了Reactor模式，

每个应用程序可以通过ioctl向reactor注册事件处理器，

当有事件发生时，reactor会把事件写入到所注册了的应用程序的fusion文件描述符时，

之后应用程序可以从fusion文件描述符里读取到事件数据。



下面以触摸屏为例介绍笔点事件的过程：

\1. 初始化时，driver_open_device创建一个进程，挂在/dev/input/event0上，等待笔点事件。

\2. 初始化时，应用程序创建另外一个线程，挂在/dev/fusionN(不同的应用程序N值不同)上。

\3. 当有笔点事件时，通过函数调用dfb_input_dispatch–>fusion_reactor_dispatch->ioctl (FUSION_REACTOR_DISPATCH)把消息丢给内核模块。

\4. 内核模块中的Reactor把事件数据写入到各个所注册的事件处理器的/dev/fusionN里。

\5. 应用程序从/dev/fusionN文件中取得事件数据，并调用应用程序内部的reactor处理函数，一般是IDirectFBEventBuffer_InputReact/IDirectFBEventBuffer_WindowReact两个函数。

\6. 然后，在IDirectFBEventBuffer_InputReact/IDirectFBEventBuffer_WindowReact两个函数中，调用IDirectFBEventBuffer_AddItem把事件加入到窗口的事件队列中。

\7. 在应用程序的主线程中，就可以通过调用窗口的GetEvent函数从事件队列中获取事件了，最后，把获取的事件分发到各个窗口事件处理函数中。

```
typedef enum {
     FER_ANY,
     FER_MASTER,
     FER_SLAVE
} FusionEnterRole;
```

加锁：

```
fusion_skirmish_prevail
```

解锁：

```
fusion_skirmish_dismiss
```

对于非multi的情况，就是mutex 的行为。

fusion_enter

这个是一个关键函数，create或者join一个fusion。

对非multi的情况：

```
malloc FusionWorld结构体
malloc FusionWorldShared结构体
fusion_shm_pool_create
	创建一个1M的内存池。
	对于fake.c的实现，只是malloc FusionSHMPoolShared， 1M这个值没用。
然后初始化一些mutex。
创建一个线程，函数是：event_dispatcher_loop
```

上面这个World这个单词挺奇怪的，理解成Context就好了。

event_dispatcher_loop函数的处理逻辑：

```
while(1)
{
	direct_waitqueue_wait//等待队列
	取出FusionEventDispatcherBuffer类型的消息。
	reaction->func
}
```

谁会往队列里放消息呢？

```
direct_waitqueue_signal( &world->event_dispatcher_cond );
```

fusion_call_execute

这个被调用的地方有几处。

例如：fbdev_ioctl里。

fusion_call_execute3 这个是被用得最多的。

被其他函数间接调用。

例如：CoreDFB_Call



coredfb.h头文件



input逻辑

头文件是src/core/input_driver.h

靠构造调用direct_modules_register



# 系统能力

```
CSCAPS_ACCELERATION 具有硬件加速
CSCAPS_ALWAYS_INDIRECT  所有的调用都不直接调用？

```

对于fbdev，只设置了硬件加速这个标志。

```
static void
system_get_info( CoreSystemInfo *info )
{
     info->type = CORE_FBDEV;
     info->caps = CSCAPS_ACCELERATION;

     snprintf( info->name, DFB_CORE_SYSTEM_INFO_NAME_LENGTH, "FBDev" );
}
```

# fusion机制

 Fusion是DFB实现的一个进程间通信的机制。它提供了一系列抽象模块/对象的实现。这些抽象模块都是使用多线程、多进程编程必要的模块。这些模块主要有以下几种：

（1）共享内存（shared memory）;

fusion的共享内存是基于GNU malloc在用户空间实现的，

但是它mmap到一个基于ram的文件系统（tmpfs或shmfs），

该文件系统可作为共享堆内存(share heap)的后备仓库（backing store）.

每个进程的mmap的起始地址都是0x20000000，

**因此指向内存分配的指针就可以方便的在进程间传递，而不需要经过复杂的转换。**

（2）竞技场(Arena),它是共享内存的指针注册中心。

可以理解为它是一个跨进程的仓库，

用来存储所有指向共享内存的指针。

通常，我们把这些指针按域fields分类存放在竞技场里。

指针通过fields取得。fields域名和竞技场都由你选择的一个竞技场内唯一的名字name来区分。

可见，**竞技场的的主要功能是对共享数据的管理，**

通过一个名称与一块数据关联起来，放到hash表中，

每个进程都可以通过名字取相应的数据。

.fusion_arena_enter()负责创建或者访问指定的Arena,

并可以使用回调函数 initialize()和 join() (分别创建新的field和访问field)。



理解Fusion，**需要从用户空间和内核空间两个方面去把握**：

（1）在用户空间，fusion library库被DFB或其他程序调用；

 （2）在内核空间，实现了fusion device,这些device被库使用，从而实现进程间的通信。

 FUSION通常配置成一个支持多进程的库，

**它使用内核模块的软设备实现多进程通信。**

**Fusion也可以配置成使用单进程，使用pthread的mutex等构建相关的概念。**

**单进程的情况下，只用到了用户空间的fusion library，它与内核空间的fusion device无关。**

  使用fusion library的一个进程通常被称为一个fusionee.

Fusionee可以访问它自己创建的fusion item项，也可以访问同处一个fusion world的其他fusionee.

多进程环境下，一个world可以包含任意多的进程,而一个系统最多可以有8个world。

单进程环境下，每个fusionee都在它自身的world里运作，因此自使用fusion作为内部通信（可能是线程间的通信，但都是限制于同一个进程的线程）。

 每个fusion world 拥有一个file-backed heap（请参看前面讲到的共享内存模块）.

每个fusion library实例只有一个shared heap. 





fusionee_rpc.c
该程序会创建一个简单的进程。

它通过竞技场共享一个过程调用。

为了实现这个共享，我们必须按步骤完成以下工作：

创建一个fusion world.
创建一个共享内存池
初始化一个竞技场
在共享内存里通过调用fusion_call_init()注册一个 FusionCall结构。

把该结构添加到竞技场； 

把fusioncall初始化为一个普通的函数。

发布一个指向该fusioncall函数的指针；



# 命名规律

```
src/core目录
	这个下面的，C文件里的函数都是dfb_xx的命名方式。
	c文件名都是蛇形的。c++文件都是驼峰的。
	有一些core part。
	DFB_CORE_PART
	数据结构还是驼峰的。
	数据结构的成员变量是蛇形的。
	CoreDFB.h的例外，这个是c++的。
	类之外的函数也是驼峰的。
	CoreDFB_Roundtrip 这种风格。
	
	
应用使用的接口
类型都是DirectFB开头的。
```

调用方式有：拒绝、直接、间接。默认是直接调用。

```
typedef enum {
     COREDFB_CALL_DENY,
     COREDFB_CALL_DIRECT,
     COREDFB_CALL_INDIRECT
} CoreDFBCallMode;
```

以Core开头的类型，这个应该是对内的。

以DFB开头的类型，这个是对外的。

在src/core/coretypes.h头文件里。统一进行了规范typedef定义。

```
Core开头的类型有：
最核心的：
CoreDFB
CoreDFBShared

CoreGraphicsDevice
CoreGraphicsState
CoreGraphicsStateClient

CoreScreen
CoreInputDevice
CoreLayer
CoreSurface
CoreWindow
```

CoreDFB

```
系统最核心的数据结构
在src/core/core.h里。
包含了：
FusionWorld             *world;
DirectLink              *cleanups;
init_handler
signal_handler
cleanup_handler
```

CoreDFBShared

```
一系列的FusionObjectPool

```

dfb_core_initialize 

```
被ICore_Real::Initialize调用
被CoreDFB_Initialize
dfb_core_arena_initialize
dfb_core_create
IDirectFB_Construct
DirectFBCreate
```



XX_Real相当于XX_Impl的意思。接口的实现。



# CallBuffer

这个是什么调用机制？

```
class IGraphicsState_Requestor : public IGraphicsState, public CallBuffer
```

非直接调用的方式。

```
case COREDFB_CALL_INDIRECT: {
            DirectFB::IGraphicsState_Requestor requestor( core_dfb, obj );
```

类似线程池一样的操作。

相对于的是直接同步调用的方式。

DirectFB::IGraphicsState_Real

但是从打印中看，这个确实有打印。为什么呢？

ILayerContext_Requestor

是打印写错了。是直接调用的方式，打印写成了间接的。

```
ILayerContext_Real::GetPrimaryRegion(
                    DFBBoolean                                 create,
                    CoreLayerRegion                          **ret_region
)
{
    D_DEBUG_AT( DirectFB_CoreLayerContext, "ILayerContext_Requestor::%s()\n", __FUNCTION__ );

    D_ASSERT( ret_region != NULL );

    return dfb_layer_context_get_primary_region( obj, create, ret_region );
}
```



# State的调用

```
IDirectFB_CreateSurface
IDirectFBSurface_Construct
CoreGraphicsStateClient_Init
CoreGraphicsStateClient_init_state
CoreDFB_CreateState
ICore_Real::CreateState
dfb_graphics_state_create
```

但是当前打印中找不到dfb_graphics_state_create的日志。

CoreGraphicsStateClient_Init 这个的打印有。

的确是没有调用。分支进不去。

靠这个来初始化的

```
dfb_state_init( &data->state, core );
dfb_state_set_destination( &data->state, surface );
```

看state.c里的函数。

# direct库

direct_trace_lookup_symbol_at( direct_trace_get_caller() )

这个可以获取调用者的名字。不错。





```
dfb->SetCooperativeLevel
IDirectFB_SetCooperativeLevel
CoreLayer_CreateContext
ILayer_Real::CreateContext
dfb_layer_context_init
dfb_windowstack_create
```

dfb_windowstack_create里加上trace打印，看看调用栈是怎样的。

实际调用栈是这样

```
dfb_windowstack_create () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
dfb_layer_context_init () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
dfb_layer_create_context () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
dfb_layer_get_primary_context () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
DirectFB::ILayer_Real::GetPrimaryContext(DFBBoolean, __DFB_CoreLayerContext**) () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
CoreLayer_GetPrimaryContext () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
InitIDirectFB_Async () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
IDirectFB_Construct () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
DirectFBCreate () from /usr/lib/libdirectfb-1.7.so.7 [0xf702b000]
```

这个就是构造dfb的时候就调用了的。

而且demo_qt为什么没有调用到这个？

# coretypes.h

这个头文件里定义了重要的CoreXX的结构体。

```
DFBLayerCore;
DFBScreenCore;
DFBSystemCore;
DFBWMCore;

下面的结构体，从底层往上层
显卡
CoreGraphicsDevice
CoreGraphicsState
CoreGraphicsStateClient

屏幕
CoreScreen
显示层
CoreLayer;
CoreLayerContext;
CoreLayerRegion;
CoreLayerRegionConfig;

显示surface
CoreSurface;
CoreSurfaceAccessor;
CoreSurfaceAllocation;
CoreSurfaceBuffer;
CoreSurfaceBufferLock;
CoreSurfaceClient;
CoreSurfacePool;
CoreSurfacePoolBridge;
CoreSurfacePoolTransfer;

显示window
CoreWindow;
CoreWindowConfig;
CoreWindowStack;
```



```
CoreGraphicsDevice 显卡设备
主要包括2个函数结构体：
驱动函数
	Probe、Init这些。
设备函数
	FillRect这些。
还有caps能力。
```

```
CoreGraphicsState 显卡状态
主要是包含一个renderer指针。
还包含CardState结构体。
CardState结构体内容较多。
	GenefxState 软件显卡的状态。
```

```
CoreGraphicsStateClient
主要包含几个指针。
CardState
CoreGraphicsState
```

```
CoreScreen
包含
CoreGraphicsDevice 显卡设备指针
ScreenFuncs 屏幕处理函数结构体。
```

```
CoreLayer
包含显卡设备、屏幕的指针。
DisplayLayerFuncs 显示层函数结构体
	主要是Init、TestRegion、SetRegion、FlipRegion这些函数。
	还有AllocateSurface
	
```

```
CoreLayerContext

CoreWindowStack 每个Layer有自己的窗口栈。
```

```
CoreLayerRegion
状态标志
CoreLayerRegionConfig
id
```

```
CoreLayerRegionConfig
宽高、格式、颜色空间、buffermode。
Rect的src、dst

```

```
CoreSurface
CoreSurfaceStateFlags 状态，当前状态很少。
CoreSurfaceTypeFlags 类型。
	layer、window、cursor、font。
	internal（表示system memory）、external（表示video memory）
	preallocate
CoreSurfaceNotificationFlags
	通知。宽高变化、flip等。
	
CoreSurfaceBuffer
	有多个buffer。
	
```



```
CoreWindow 
id
flags。表示状态。
caps能力。
CoreWindowConfig 配置。
CoreSurface            *surface;  后备surface。
CoreWindowStack 所属的窗口栈。

```

```
CoreWindowConfig
范围
透明度
窗口栈类型。
窗口事件
```

```
CoreWindowStack

```

通过读取显卡硬件加速能力，来决定window policy。

如果有blit能力，而且还支持blend，那么优先使用video memory。

```
/* Examine the hardware capabilities. */
               dfb_gfxcard_get_capabilities( &card_caps );

               if (card_caps.accel & DFXL_BLIT && card_caps.blitting & DSBLIT_BLEND_ALPHACHANNEL)
                    policy = CSP_VIDEOHIGH;
```



# 参考资料

1、

https://blog.csdn.net/absurd/article/details/2596080

2、DirectFB分析

https://blog.csdn.net/alenwelkin/article/details/1649473

3、

https://blog.csdn.net/dotphoenix/article/details/4762623

4、基于fusion的DirectFB消息流

https://blog.csdn.net/hope_learn/article/details/5567644

5、

https://blog.csdn.net/acs713/article/details/7963964

6、

https://blog.csdn.net/acs713/article/details/7975830

7、

https://wenku.baidu.com/view/11842c0af78a6529647d5385.html