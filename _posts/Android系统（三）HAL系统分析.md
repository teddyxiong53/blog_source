---
title: Android系统（三）HAL系统分析
date: 2018-01-23 14:45:07
tags:
	- Android系统

---



Android系统的HAL层在用户空间运行。

# hal出现的背景

在Android系统中，推出hal层是为了保护一些硬件厂商的知识产权，用来避开linux的GPL协议的。

谷歌的架构师的思路是把控制硬件的动作都放到HAL层里。而Linux Driver进负责一些简单的数据交互。**甚至把硬件寄存器都映射到用户控件来操作。**

**Android系统是基于Apache协议的，厂家可以只提供二进制的文件。所以Android只是一个开放平台，而不是一个开源平台。**

也因为Android不遵守GPL，linux内核维护者就把Android驱动从linux内核里移除了。不过后面Linux又把Android接纳进来了。

**GPL和硬件厂商之间的分歧很难弥合。**

# hal分类

Android系统里的hal可以分为下面6类：

1、上层软件。

2、内部以太网。

3、内部通信client。

4、用户接入口。

5、虚拟驱动。

6、内部通信server。

# hal主要存放的目录

1、libhardware_legacy。之前的目录。**采取了链接库模块的观念来进行架构的。**

2、libhardware。新的 目录，**采用HAL stub的观念来架构。**

3、ril。是Radio接口层。

4、msm7k。qual平台相关的信息。

# hal的基本架构

基本层次关系是这样：

```
库、Android运行环境
---------------------
HAL层
----------------------
linux内核
```

**hal层把Android框架跟linux内核隔离开了。**





# 分析hal module架构

Android5.0的hal采用hal module和hal stub结合的方式来架构。

hal stub不是一个so文件。

hal module主要包括3个结构体：

```
struct hw_module_t;
struct hw_module_methods_t;
struct hw_device_t;
```

对应的so文件的命名规则是：

id.varient.so

例如：

gralloc.msm7k.so

```
/**
 * There are a set of variant filename for modules. The form of the filename
 * is "<MODULE_ID>.variant.so" so for the led module the Dream variants 
 * of base "ro.product.board", "ro.board.platform" and "ro.arch" would be:
 *
 * led.trout.so
 * led.msm7k.so
 * led.ARMV6.so
 * led.default.so
 */
 static const char *variant_keys[] = {
    "ro.hardware",  /* This goes first so that it can pick up a different
                       file on the emulator. */
    "ro.product.board",
    "ro.board.platform",
    "ro.arch"
};
```



hal层的通用结构，可以总结为“321”结构。

3表示3个结构体。

2表示2个常量。

1表示1个函数。

所有的硬件抽象模块都遵循321架构。在这个基础上进行扩展。

3个结构体是：

```
硬件模块
	
硬件模块方法
	被硬件模块包含。只有一个open方法。
硬件设备
```

2个常量是：

```
#define HAL_MODULE_INFO_SYM HMI
#define HAL_MODULE_INFO_SYM_AS_STR "HMI"
```

1个函数：

```
int hw_get_module(const char *id, const struct hw_module_t **module);
```



# led 的hal分析

我们以led的为例子分析一下hal。

led.h

```
struct led_module_t {
	struct hw_module_t common;
	int (*init_led)(struct led_control_device_t *dev);
};

struct led_control_device_t {
	struct hw_device_t common;
	int fd;
	int (*set_on)(struct led_control_device_t *dev, int32_t led);
	
};
#define LED_HARDWARE_MODULE_ID "led"
static inline int led_control_open(const struct hw_module_t *module, struct led_control_device_t **device)
{
	return module->methods->open(module, LED_HARDWARE_MODULE_ID, (struct hw_device_t **)device);
}
```

led.cpp

```
int led_device_open(const struct hw_module_t *module, const char *name, struct hw_device_t ** device)
{
	struct led_control_device_t *dev;
	dev = (struct led_control_device_t *)malloc(sizeof(*dev));
	memset(dev, 0, sizeof(*dev));
	dev->common.tag = HARDWARE_DEVICE_TAG;
	dev->common.version = 0;
	dev->common.module = const_cast<struct hw_module_t *>(module);
	dev->common.close = led_device_close;
	
	dev->set_on = led_on;
	dev->fd = open("/dev/led-test", O_RDWR);
	return 0;
}

struct hw_module_methods_t led_module_methods = {
	.open = led_device_open
};
const struct led_module_t HAL_MODULE_INFO_SYM = {
	common: {
		tag: HARDWARE_MODULE_TAG,
		version_major: 1,
		version_minor: 0,
		id: LED_HARDWARE_MODULE_ID,
		name: "simple led stub",
		author: "xhl",
		methods: &led_module_methods,
	}
};
```



上层调用

这个的查看，就以SoundTrigger的为例来看吧。

hal层在：aosp\hardware\libhardware\modules\soundtrigger

上层在：Z:\work3\aosp\frameworks\base\core\jni\android_hardware_SoundTrigger.cpp



参考资料

1、【Android】HAL层浅析

https://blog.csdn.net/flappy_boy/article/details/81150290