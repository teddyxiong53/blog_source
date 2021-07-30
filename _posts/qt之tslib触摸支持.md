---
title: qt之触摸支持
date: 2021-06-23 09:55:33
tags:
	- qt

---

--

```
配置ts.conf
module_raw input
module pthres pmin=1
module variance delta=30
module dejitter delta=100
module linear


配置环境变量
打开目标板文件系统/etc/profile文件
export LD_LIBRARY_PATH=/usr/lib/    --库文件目录
export TSLIB_ROOT=/usr/       --tslib库文件/头文件根目录
export TSLIB_TSDEVICE=/dev/input/touchscreen0 --触摸屏设备文件路径
export TSLIB_CALIBFILE=/etc/pointercal   --校正文件路径 运行ts_calibrates会自动生成
export TSLIB_CONFFILE=/etc/ts.conf    --配置文件路径
export TSLIB_CONSOLEDEVICE=none     --
export TSLIB_FBDEVICE=/dev/fb0     --fb显示设备文件路径
export TSLIB_TSEVENTTYPE=INPUT     --触摸事件类型 input子系统
export TSLIB_PLUGINDIR=/usr/lib/ts    --
```

tslib测试
运行ts_calibrate

校验完在/etc目录下生成/etc/pointercal

ts_calibrate可能会遇到一些问题

提示不是支持的触摸屏:查看TSLIB_TSDEVICE环境变量是否设置对

没点击方块就自动校正了:

1.驱动BTN_TOUCH或者ABS_PRESSURE的值固化成1了(有上报按下事件没上报松开事件)

2.库文件放错位置

运行ts_test

点击Drag按钮 可以拖动小方块


配置qt

.configure 后面加上 -no-mouse-linuxtp -qt-mouse-tslib

在test的过程中打印

Mouse driver(qt) ......pc tslib

表示库安装成功并成功检测到

example里面选择应用程序(推荐qt-everywhere-opensource-src-4.8.1/examples/widgets/calculator)
拷贝到目标板文件系统里



```
配置环境变量
打开目标板文件系统/etc/profile文件,添加以下
export LD_LIBRARY_PATH=/usr/lib/ ----库文件目录
export QWS_SIZE=1920x1080   ----分辨率
export QWS_MOUSE_PROTO="tslib:/dev/input/touchscreen0 mouseman:/dev/input/mouse0" ----"鼠标"类型
```



看amlogic的A113D S400的板子。接显示屏的。

 cat /proc/bus/input/devices 看到的信息

```
I: Bus=0018 Vendor=0000 Product=0000 Version=0000
N: Name="fts_ts"
P: Phys=
S: Sysfs=/devices/platform/soc/ff800000.aobus/ff805000.i2c/i2c-1/1-0048/input/input1
U: Uniq=
H: Handlers=event1
B: PROP=2
B: EV=b
B: KEY=400 0 0 0 0 0 0 0 0 0 0
B: ABS=2618000 0
```

从上面的信息可以看出，是在i2c1上，i2c地址是0x48 

屏幕是AXS040TG，720*720的屏幕。自带了触摸芯片。

AXS9621 。支持多点触控。

lsmod没有看到，说明是编译进内核了。

看下设备树里的信息。在这个目录下。

```
/sys/firmware/devicetree/base/soc/aobus@ff800000/i2c@5000/focaltech@48
```

```
compatible     
	内容是focaltech,fts
focaltech,display-coords     
focaltech,irq-gpio           
focaltech,max-touch-number   
focaltech,reset-gpio         
name                         
reg                          
status                       

```

focaltech 这个在代码里默认就有的。

驱动代码 ./drivers/amlogic/input/touchscreen/focaltech_touch

设备树里的完整信息

```
focaltech@48 {
                                        compatible = "focaltech,fts";
                                        reg = <0x00000048>;
                                        focaltech,irq-gpio = <0x0000000f 0x00000000 0x00000000>;
                                        focaltech,reset-gpio = <0x0000000f 0x00000001 0x00000000>;
                                        focaltech,max-touch-number = <0x00000001>;
                                        focaltech,display-coords = <0x00000000 0x00000000 0x000002d0 0x000002d0>;
                                        status = "okay";
                                };
```



./arch/arm/boot/dts/amlogic/g12a_s905d2_u200.dts 以这个为例看看。

我先直接改设备树，保证触摸板的驱动可以起来。

先看当前正常的板子的中断情况。

对应的是这个中断

```
 15:        650          0          0          0     GIC-0 227 Edge      ff805000.i2c
```

触摸一下，中断数增加了20 。

我先加入设备树，编译看看触摸会不会让这个中断增加。

等等，不太对。

当前的普通S400板子，这个中断已经有这么多。而且一直在增加。

这个是哪个设备导致的中断？

应该是这个。我看带显示的板子，把这个改成了disabled了。

```
aml_pca9557: aml_pca9557@0x1f {
		compatible = "aml, ledring";
		reg = <0x1f>;
                mode = <0>; /*0: 6-led 1: 4key+2led */
                key_num = <4>;
                led_dev_name = "aml_ledring";
                key_dev_name = "aml_pca_key";
                key_name = "mute", "pause", "vol+", "vol-";
                key_value = <200 201 202 203>;
		status = "okay";
	};
```



```
12:     115948          0          0          0     GIC-0 227 Edge      ff805000.i2c
```

设备树改好了。编译试一下。

没有中断产生。

看一下focaltech的代码。

Makefile里

```
obj-$(CONFIG_AMLOGIC_TOUCHSCREEN_FTS)	+=  focaltech_core.o
```

kernel下面搜索一下

```
./aml-4.9/arch/arm64/configs/meson64_defconfig:239:CONFIG_AMLOGIC_TOUCHSCREEN_FTS=y
./aml-4.9/arch/arm/configs/meson64_a32_defconfig:240:CONFIG_AMLOGIC_TOUCHSCREEN_FTS=y
```

那么默认就是选配的了。

里面有这些相关的配置

```
CONFIG_AMLOGIC_TOUCHSCREEN=y
CONFIG_AMLOGIC_TOUCHSCREEN_FTS=y
CONFIG_AMLOGIC_TOUCHSCREEN_GT1X=y
CONFIG_AMLOGIC_TOUCHSCREEN_GT9XX=y
CONFIG_AMLOGIC_TOUCHSCREEN_HYN_CST2XX=y
```

但是我们用的好像不是meson64_defconfig。应该是meson64_smarthome_defconfig

而这个里面没有配置触摸相关的。

看看buildroot里的是怎么配置S400的编译的。

在.config里可以看到

```
BR2_LINUX_KERNEL_DEFCONFIG="meson64_smarthome"
```

来自于

```
./a113_base.config:14:BR2_LINUX_KERNEL_DEFCONFIG="meson64_smarthome"
```

那么我需要对S400的配置改一下了。

不能用meson_defconfig，会导致编译不过。

那就单独打开触摸屏那几个配置。

怎么改比较好？

直接在aml-4.9\arch\arm64\configs\meson64_smarthome_defconfig里改。

现在编译可以过。

但是运行有打印一下内核错误，没有死机。但是触摸也没有反应。

```
gpio_to_desc+0xd8/0xe0
fts_reset_proc+0x2c/0x70
fts_ts_probe+0x2d4/0x8c8
i2c_device_probe+0x17c/0x230
driver_probe_device+0x204/0x2a8
__driver_attach+0xbc/0xc0
bus_for_each_dev+0x74/0xb0
driver_attach+0x30/0x40
bus_add_driver+0x110/0x220
driver_register+0x68/0x100
i2c_register_driver+0x4c/0x90
fts_ts_driver_init+0x18/0x20
do_one_initcall+0x44/0x130
kernel_init_freeable+0x13c/0x1dc
kernel_init+0x18/0x108
ret_from_fork+0x10/0x20
```

这个看起来像是gpio没有申请到。

是reset 这个gpio。

设备树里我写了这个。但是代码里没有看到使用的地方。

而且，我设备树里写的也不对。

gpio在设备树里的写法是：

```
gpio_demo: gpio_demo {
	            status = "okay";
	            compatible = "rk3328,gpio_demo";
	            firefly-gpio = <&gpio0 12 GPIO_ACTIVE_HIGH>;          /* GPIO0_B4 */
	            firefly-irq-gpio = <&gpio2 29 IRQ_TYPE_EDGE_RISING>;  /* GPIO2_D5 */               
	            };
```

是一个3元组：所在gpio组、gpio编号、特征。

我在amlogic的里面，应该这样写：

```
reset-gpio = <&gpio GPIOZ_10 GPIO_ACTIVE_HIGH>;
```

代码里用到是这里

```
./drivers/amlogic/input/touchscreen/focaltech_touch/focaltech_core.c:974:    pdata->reset_gpio = of_get_named_gpio_flags(np, "reset-gpio", 0, &pdata->reset_gpio_flags);
```

当前的错误就是：

```
[    6.585440@3]- [FTS][Error]Unable to get reset_gpio
[    6.589603@3]- [FTS][Error]Unable to get irq_gpio
[    6.594243@3]- [FTS][Info]CHIP TYPE ID = 0x8006
[    6.598712@3]- [FTS][Error][GPIO]reset is not valid
```

所以是我设备树里写的有问题。改了再试一下。

算了，暂时不管触摸屏的了。

```
GPIO_ACTIVE_HIGH = (0 << 0),
GPIO_ACTIVE_LOW = (1 << 0),
```

触摸屏中断好了。

其实问题很简单，就是驱动代码里和设备树里的名字对不上导致的。改一下设备树里的名字就好了。

可以正常触发中断了。

现在这个设备也出来了。

```
I: Bus=0018 Vendor=0000 Product=0000 Version=0000
N: Name="fts_ts"
P: Phys=
S: Sysfs=/devices/platform/soc/ff800000.aobus/ff805000.i2c/i2c-1/1-0048/input/input1
U: Uniq=
H: Handlers=event1 
B: PROP=2
B: EV=b
B: KEY=400 0 0 0 0 0 0 0 0 0 0
B: ABS=6618000 0
```



然后呢？

编译qt和tslib。让qt支持触摸。

tslib默认已经编译了。因为我之前选配了的。

```
BR2_PACKAGE_QT5BASE_TSLIB=y
BR2_PACKAGE_TSLIB=y
```

那么在板端需要怎么配置呢？

先看tslib的。

ts.conf，好像不用改宽高。好像是根据fb的来的。那就不管。

先改ts.conf的内容如下：

```
module_raw input
module pthres pmin=1
module variance delta=30
module dejitter delta=100
module linear
```

然后在/etc/profile.d目录下，新增一个set_ts.sh脚本。内容如下：

```
export LD_LIBRARY_PATH=/usr/lib/
export TSLIB_ROOT=/usr/lib
export TSLIB_TSDEVICE=/dev/input/event1
export TSLIB_CALIBFILE=/etc/pointercal
export TSLIB_CONFFILE=/etc/ts.conf
export TSLIB_CONSOLEDEVICE=none
export TSLIB_FBDEVICE=/dev/fb0
export TSLIB_TSEVENTTYPE=INPUT
export TSLIB_PLUGINDIR=/usr/lib/ts
```

然后重启板子，直接就工作正常了。也是出乎我的预料。



但是触摸时，有这样的打印：

```
Unknown system cursor
```



# qt需要设置什么

export QT_QPA_FB_TSLIB=1
export QT_QPA_FONTDIR=/usr/share/fonts/ttf
export QT_QPA_GENERIC_PLUGINS=“tslib:/dev/input/event1”
export QT_QPA_EVDEV_TOUCHSCREEN_PARAMETERS=/dev/input/event1:inverty//可以翻转X或者Y轴坐标，如果上下或者左右坐标相反，可使用此句（inverty/invertx）
export QT_QPA_PLATFORM=linuxfb:tty=/dev/fb0

QT_QPA_FB_TSLIB 这个环境变量在：

src/plugins/platforms/linuxfb/qlinuxfbintegration.cpp

createInputHandlers



那directfb呢？

看qdirectfbinput.cpp。

是这样来等待输入事件的

```
void QDirectFbInput::run()
{
    while (!m_shouldStop) {
        if (m_eventBuffer->WaitForEvent(m_eventBuffer.data()) == DFB_OK)
            handleEvents();
    }
}
```

qt里对接tslib的代码：src/platformsupport/input/tslib

```
static bool get_sample(struct tsdev *dev, struct ts_sample *sample, bool rawMode)
{
    if (rawMode)
        return (ts_read_raw(dev, sample, 1) == 1);
    else
        return (ts_read(dev, sample, 1) == 1);
}
```

是否使用rawmode，是看这里

```
m_rawMode(!key.compare(QLatin1String("TslibRaw"), Qt::CaseInsensitive))
```



现在在qt的tslib里加打印。

运行qt程序，有2个事件。

```
xhl -- qt dfb get event
xhl -- qt dfb event type:3 xxxyyy
xhl -- qt dfb before event
xhl -- qt dfb get event
xhl -- qt dfb event type:16777216 xxxyyy
```

3这个事件表示：DWET_POSITION |DWET_SIZE，就是创建窗口的事件。

16777216，对应0x0100 0000，DWET_UPDATE

这都是2个窗口绘制事件。

触摸并没有事件过来。

为什么没有过来？

现在跟qt都还没有关系。

问题还是回到了pressure。

因为directfb里的tslib，就是要这个东西。

```
if (ts_event.pressure) {
```



使用directfb的时候，ts_read这个函数，在directfb和qt里的qtslib.cpp里都有使用。

会不会相互影响？

是不是应该把qt里的tslib关闭呢？

我觉得是应该关闭的。

qt是否使用tslib，由什么来决定？

由环境变量控制？

查看wearable的动态库，并没有链接到tslib的动态库。

但是这个应该对于dlopen这一种方式的，查询不到。

我手动去掉当前qt里的tslib库，运行wearable，并不会报缺失动态库。

所以当前并没有直接用到。

但是我使用linuxfb，触摸又是完全正常的。

这个又怎么解释呢？

```
# ldd ./wearable
        libatomic.so.1 => /lib/libatomic.so.1 (0xf7470000)
        libQt5QuickControls2.so.5 => /usr/lib/libQt5QuickControls2.so.5 (0xf744c000)
        libQt5Quick.so.5 => /usr/lib/libQt5Quick.so.5 (0xf71b4000)
        libQt5Gui.so.5 => /usr/lib/libQt5Gui.so.5 (0xf6ef7000)
        libQt5Qml.so.5 => /usr/lib/libQt5Qml.so.5 (0xf6c2c000)
        libQt5Network.so.5 => /usr/lib/libQt5Network.so.5 (0xf6b2f000)
        libQt5Core.so.5 => /usr/lib/libQt5Core.so.5 (0xf67b3000)
        libpthread.so.0 => /lib/libpthread.so.0 (0xf678d000)
        librt.so.1 => /lib/librt.so.1 (0xf6775000)
        libdl.so.2 => /lib/libdl.so.2 (0xf6760000)
        libstdc++.so.6 => /lib/libstdc++.so.6 (0xf6656000)
        libm.so.6 => /lib/libm.so.6 (0xf65dc000)
        libgcc_s.so.1 => /lib/libgcc_s.so.1 (0xf65b2000)
        libc.so.6 => /lib/libc.so.6 (0xf64c6000)
        libQt5QuickTemplates2.so.5 => /usr/lib/libQt5QuickTemplates2.so.5 (0xf63e2000)
        libpng16.so.16 => /usr/lib/libpng16.so.16 (0xf63ab000)
        libz.so.1 => /usr/lib/libz.so.1 (0xf6388000)
        libicui18n.so.65 => /usr/lib/libicui18n.so.65 (0xf6168000)
        libicuuc.so.65 => /usr/lib/libicuuc.so.65 (0xf5ffc000)
        libicudata.so.65 => /usr/lib/libicudata.so.65 (0xf454b000)
        libpcre2-16.so.0 => /usr/lib/libpcre2-16.so.0 (0xf44f7000)
        libgthread-2.0.so.0 => /usr/lib/libgthread-2.0.so.0 (0xf44e4000)
        libglib-2.0.so.0 => /usr/lib/libglib-2.0.so.0 (0xf43e3000)
        /lib/ld-linux-armhf.so.3 (0xf7488000)
        libpcre.so.1 => /usr/lib/libpcre.so.1 (0xf4397000)
```



梳理一下linuxfb方式的触摸事件流程。

肯定是一个ts_read得到了触摸事件。

我把libts.so的库文件都放到tmp下面。再运行wearable，就跑步起来。说明有去使用libts。

```
# ./wearable
qt.qpa.plugin: Could not load the Qt platform plugin "linuxfb" in "" even though it was found.
This application failed to start because no Qt platform plugin could be initialized. Reinstalling the application may fix this problem.

Available platform plugins are: directfbegl, directfb, linuxfb, minimal, offscreen, vnc.
```

还是这里调用的。

```
void QLinuxFbIntegration::createInputHandlers()
{
#if QT_CONFIG(libinput)
    if (!qEnvironmentVariableIntValue("QT_QPA_FB_NO_LIBINPUT")) {
        new QLibInputHandler(QLatin1String("libinput"), QString());//这里面调用了ts_open。
        return;
    }
#endif

#if QT_CONFIG(tslib)
    bool useTslib = qEnvironmentVariableIntValue("QT_QPA_FB_TSLIB");
    if (useTslib)
        new QTsLibMouseHandler(QLatin1String("TsLib"), QString());
#endif
```

环境变量是这个：QT_QPA_FB_TSLIB

但是当前并没有这个环境变量。

那又是怎么使用的呢？

加打印确认了一下，的确是没有进上面代码分支。

那触摸为什么有效果？

那可能就是因为触摸有发出通用的key事件导致的？

我现在特意设置这个环境变量，

```
# export QT_QPA_FB_TSLIB=1
# ./wearable
```

反而触摸没有效果了。

read函数返回了-1 。

也不是每次都返回-1 。

大多数时候还是返回16的。

还是去掉QT_QPA_FB_TSLIB。

当前qt是收到了一个什么event？肯定是带上了坐标信息的。

应该是mouse。

这个要看一下wearable的代码。处理了哪些事件。





tslib利用QSocketNotifier来关联read触摸消息(event).

思路是,能够监视触摸屏(usb)插拔消息,然后构造函数重新建立绑定关系.

所以关键是能够watch插拔消息.



# 鼠标隐藏

而且当前有显示鼠标指针，我并不需要。怎么隐藏掉？

1、编译Qt库的时候添加编译选项QT_NO_CURSOR，这样cursor相关的代码统统不会被编译进去，自然鼠标光标也不会出现在程序中。

2、只希望在某个QWidget下不出现鼠标光标，则只要对这个widget调用

 QWidget::setCursor(QCursor(Qt::BlankCursor))，其它的窗口仍将出现鼠标。
3、在main函数中，实例化了APPLICATION后，调用

 QApplication::setOverrideCursor(Qt::BlankCursor);

4、任一控件下显示与关闭鼠标

 this->setCursor(Qt::BlankCursor);  //隐藏鼠标
 this->setCursor(Qt::ArrowCursor); //显示正常鼠标
 this改为需要隐藏鼠标的部件，就可以令当鼠标移动到该部件时候，效果生效。

 有人说 以上的都需要动一下鼠标才会消失，不知道不是我没有搞好，下面一启动就可以隐藏起来

我的测试是两个Qt进程，A启动B，A不显示，B显示。在A中如果不使用方法5，无论B怎么处理，都会显示鼠标。如果A使用了方法5，则不会显示鼠标指针。

5、调用下面函数

QWSServer::setCursorVisible(false);

这是一个静态函数，可以在main()函数中，实例化QApplication以后调用，这样整个程序将不会出现鼠标的光标。
注意必须包含头文件。

# 虚拟键盘输入

当前需要跑浏览器的。那么怎么输入网址，只能靠虚拟键盘来输入了。

怎么使用虚拟键盘呢？

使用qt自带的软键盘有两种集成方式：桌面方式以及应用方式。

- 桌面：键盘出现在桌面，即系统的屏幕上，键盘的宽度等于屏幕的宽度，不依赖于app的宽度。
- 应用：键盘嵌入到我们的app中去，键盘的宽度等于我们app的宽度



# 浏览器

当前的基础上，加上这3个配置。

```
BR2_PACKAGE_QT5QUICKCONTROLS2=y
BR2_PACKAGE_QT5WEBKIT_EXAMPLES=y
BR2_PACKAGE_QT_WEBKIT_KIOSK=y
```

/usr/lib/qt/examples/webkitwidgets/browser 这个浏览器可以正常运行。

但是浏览器带了窗口，怎么全屏运行呢？

module "QtWebKit" is not installed

这个错误是因为qtwebkit是过时的了。现在改成新的模块，叫webengineview了。

qtwebkit从qt5.6就移除了。







# fb设置

```
If you don't want to reinstall linux kernel you can do:
# fbset -xres 800 -yres 480
```



# 按键

看看按键的响应。

我这里指的是几个按钮的那个，不是标准键盘。

```
4.7之前的Qt版本，若是是PS2圆孔键盘，Qt编译时需加上选项：-qt-kbd-vr41xx（未测试）；若是是USB键盘，需加上-qt-kbd-usb选项。
Qt4.7.3默认的是tty，对于USB键盘可用，不须要配置。
```

我觉得应该是这个思路：

按键驱动，发送一个标准的keycode就好了。一般就实现方向键、确定键、退出键这些。



# tslib代码分析

以ts_caliberate这个为例进行分析。

tslib默认提供的ts.conf文件里，就这几行是有效的代码：

```
module_raw input
module pthres pmin=1
module dejitter delta=100
module linear
```

有这几个够用了。

核心数据结构：

```
struct tsdev {
	int fd;
	char *eventpath;
	struct tslib_module_info *list;
	struct tslib_module_info *list_raw;
	unsigned int res_x;
	unsigned int res_y;
	int rotation;
};
```

首先就是创建这个结构体

```
ts = ts_setup(NULL, 0);
```

如果没有指定名字，先从环境变量里找。

如果还没有，从这些名字里找

```
static const char * const ts_name_default[] = {
		"/dev/input/ts",
		"/dev/input/touchscreen",
		"/dev/touchscreen/ucb1x00",
		NULL
};
```

对于linux系统，还会扫描/dev/input目录下的内容来尝试。

对于ts_calibrate，会使用fb来显示一些内容，提示用户去点击。



ts_load_module

从ts.conf里看，有module和module_raw这2种模块。

都是调用同一个函数，就是参数不同。

```
int ts_load_module(struct tsdev *ts, const char *module, const char *params)
{
	return __ts_load_module(ts, module, params, 0);
}

int ts_load_module_raw(struct tsdev *ts, const char *module, const char *params)
{
	return __ts_load_module(ts, module, params, 1);
}
```

module结构体：

```
struct tslib_module_info {
	struct tsdev *dev;
	struct tslib_module_info *next;	/* next module in chain	*/
	void *handle;			/* dl handle		*/
	const struct tslib_ops *ops;
};
```

tslib_ops有3个函数指针：

read、read_mt（multi的意思）、fini（去初始化？）

这些module，都在plugins目录下。

以input-raw.c为例，应该是对应配置文件里的module_raw input。



module_raw和module的区别



ENABLE_INPUT_EVDEV_MODULE

我加上

```
checking whether input-evdev module is requested... no
```

input-evdev和input的区别是什么？

```
#include <libevdev/libevdev.h>
```

好像没有本质区别。

就多了一个libevdev的中间层。

不是问题的关键。



怎么只有ts_finddev能工作？

ts_harvest、ts_calibrate这些都不行？



ts_test也不行。

就以这个作为分析对象。代码200行。

那就是ts_read和ts_read_raw的区别。

ts_read_raw有返回。

而ts_read没有。

为什么ts_read没有返回？

怎么配置才能有返回？

**ts_read()读取校正后的相对坐标数据，ts_read_raw()读取校正前的实际坐标。**

正常使用应该是怎样的？



ts_print

这个是打印触摸点的。



我现在把ts.conf里的只保留`module_raw input`。

怎么有的测试程序里，ts_read可以，有的不行？



就看ts_print这个程序的。

ts.conf里只保留一行module_raw input的时候，

ts_print 可以打印。

当ts.conf有这些内容的时候：

```
module_raw input
module pthres pmin=1
module variance delta=30
module dejitter delta=100
module linear
```

ts_print不行，ts_print -r 可以。加-r参数是表示使用ts_read_raw函数。

说明上面的配置有问题。

具体是哪一行有问题呢？

我觉得是linear这一行。去掉这一行看看。

还是不行。

加上module pthres pmin=1就不行了。

那单独去掉这个看看。

就可以。

这个值感觉也没有什么问题。

代码里给的默认值也1啊。

```
	p->pmin = 1;
	p->pmax = INT_MAX;
```



分析配置文件，

然后通过ts_load_module(ts,module_name,param) 或者ts_load_module_raw 来把模块加载到内存，

pthres是压力阈值。



与 ts_print_raw 是一样的分析
只是一个调用ts_read_raw, 一个调用ts_read.
ts_read_raw 只有一层，不会返回给其他module.
ts_read,则是->linear->degitter->variance->pthres->read_raw 这个链来处理数据

是这样遍历module的。

```
info->next->ops->read(info->next, &cur, 1)
```

tslib的代码不复杂。代码量也不大。



触摸屏校正是怎么做的？



ts_harvest还是不行。

通过加打印，read函数还是正常收到数据的。

触摸一下，得到的打印：

```
xhl -- after input read,ret:16
xhl -- ev.type:3, ev.code:57
xhl -- after input read,ret:16
xhl -- ev.type:3, ev.code:53
xhl -- after input read,ret:16
xhl -- ev.type:3, ev.code:54
xhl -- after input read,ret:16
xhl -- ev.type:1, ev.code:330
xhl -- after input read,ret:16
xhl -- ev.type:0, ev.code:0
```

#define EV_ABS			0x03

是坐标事件。code是坐标值。

最后是一个key事件和一个syn事件。

#define BTN_TOUCH		0x14a

330对应的就是touch按钮。

不行的都是因为这个原因，使用的getxy函数里，samp[0].pressure == 0

我估计当前pressure值一直是0 。

```
do {
		if (ts_read_raw(ts, &samp[0], 1) < 0) {
			perror("ts_read_raw");
			close_framebuffer();
			exit(1);
		}
	} while (samp[0].pressure == 0);
```

既然驱动有支持pressure这个特性。为什么值有一直都是0呢？

把check_fd函数看一下。

也不一直都是0 。

我跑dfbtest_input的时候，看到有这个值。

```
TS_READ_RAW----> x = 285, y = 404, pressure = 63
```

但是在ts_calibrate里，pressure一直都是0 。

是因为ts_read_raw和ts_read的区别？

但是现在ts.conf里也只有一行module_raw input了。

这样ts_read和ts_read_raw就是没有区别的吧。



dfbtest_input里使用tslib，跟ts_calibrate使用tslib，有什么不同吗？

也是三步走：
ts_open
ts_config
ts_read
为什么就可以读取到pressure值呢？

pressure值在驱动哪里填充的？

```
__set_bit(EV_KEY, input_dev->evbit);
__set_bit(EV_ABS, input_dev->evbit);
__set_bit(BTN_TOUCH, input_dev->keybit);
__set_bit(INPUT_PROP_DIRECT, input_dev->propbit);

#if FTS_REPORT_PRESSURE_EN//这个宏是使能的。
    input_set_abs_params(input_dev, ABS_MT_PRESSURE, 0, 0xFF, 0, 0);
#endif
```



# focaltech

这个触摸芯片的多点触控。

当前驱动里是默认打开的。

但是dts里，配置最多一个触摸点。

驱动宏配置最多10个点。

驱动的ts_event

```
struct ts_event
{
    u16 au16_x[FTS_MAX_POINTS]; /*x coordinate */
    u16 au16_y[FTS_MAX_POINTS]; /*y coordinate */
    u16 pressure[FTS_MAX_POINTS];
    u8 au8_touch_event[FTS_MAX_POINTS]; /* touch event: 0 -- down; 1-- up; 2 -- contact */
    u8 au8_finger_id[FTS_MAX_POINTS];   /*touch ID */
    u8 area[FTS_MAX_POINTS];
    u8 touch_point;
    u8 point_num;
};
```

从驱动里看pressure怎么得到的。

最好在驱动里进行打印。

触摸事件是靠中断上报的。

```
fts_ts_interrupt
	fts_read_touchdata 读取数据
		fts_i2c_read
	fts_report_value 报告数据
```



驱动这里会把数据buf打印出来。

```
#if (FTS_DEBUG_EN && (FTS_DEBUG_LEVEL == 2))
    fts_show_touch_buffer(buf, event->point_num);
#endif
```

pressure值是这里

```
event->pressure[i] =
            (s16) buf[FTS_TOUCH_PRE_POS + FTS_ONE_TCH_LEN * i];
```

而且这里还对pressure小于等于0的情况进行了处理。

```
#if FTS_REPORT_PRESSURE_EN
            if (event->pressure[i] <= 0)
            {
                FTS_ERROR("[B]Illegal pressure: %d", event->pressure[i]);
                event->pressure[i] = 1;
            }
            input_report_abs(data->input_dev, ABS_MT_PRESSURE, event->pressure[i]);
#endif
```

至少也会是1吧。

那么应用层的pressure为0是怎么回事？

先把驱动里的debug调到最详细的。重新编译烧录kernel看看。

触摸屏幕的kernel打印

```
[  104.077603@2]- [FTS][fts_ts_interrupt]buffer: 00,00,01,01,7B,01,BA,00,00
[  104.078693@2]- [FTS][fts_ts_interrupt]point number: 1, touch point: 1
[  104.085109@2]- [FTS][fts_ts_interrupt][B]P0(379, 442)[p:63,tm:9] DOWN!
[  104.097737@2]- [FTS][fts_ts_interrupt]buffer: 00,00,01,81,7B,01,BA,00,00
[  104.098812@2]- [FTS][fts_ts_interrupt]point number: 1, touch point: 1
[  104.105237@2]- [FTS][fts_ts_interrupt][B]P0(379, 442)[p:63,tm:9] DOWN!
[  104.117796@2]- [FTS][fts_ts_interrupt]buffer: 00,00,00,41,7B,01,BA,00,00
[  104.118862@2]- [FTS][fts_ts_interrupt]point number: 0, touch point: 1
[  104.125281@2]- [FTS][fts_ts_interrupt][B]P0 UP!
[  104.129746@2]- [FTS][fts_ts_interrupt]Points All Up!
```

分析一下buffer的组成

```
00,00,01,01,7B,01,BA,00,00
```

```
0
1
2：点的个数。
3：X值的高位。这个的最高的2bit，还另有用途。是touch事件。0：touch down，1：touch up。2：表示接触（给多点触控用的）
4：X值的低位。
5：Y值的高位。
6：Y值的低位。
7：这个就是pressure值。
8：area。具体代表了什么？
```

那么pressure值的确就一直是0 。

是因为获取不到pressure值吗？

驱动里这样处理了：

```
if (0 == event->area[i])
            event->area[i] = 0x09;

if (0 == event->pressure[i])
event->pressure[i] = 0x3f;
```

那么上面读取的pressure应该是63才对。

这个值怎么上报给应用层的？

这个分支有进

```
FTS_DEBUG("Points All Up!");
input_report_key(data->input_dev, BTN_TOUCH, 0);
```

这个只是上报了一个button值。



使用evtest来测试一下。

从下面打印可以看出：

1、支持3种事件，syn、key、abs。

key事件：就支持一个key，button触摸。

abs事件：有多个。包括了presssure。但是并没有上报。

那么就是驱动写得不够完善？

```
# evtest /dev/input/event1
Input driver version is 1.0.1
Input device ID: bus 0x18 vendor 0x0 product 0x0 version 0x0
Input device name: "fts_ts"
Supported events:
  Event type 0 (EV_SYN)
  Event type 1 (EV_KEY)
    Event code 330 (BTN_TOUCH)
  Event type 3 (EV_ABS)
    Event code 47 (ABS_MT_SLOT)
      Value      0
      Min        0
      Max        0
    Event code 48 (ABS_MT_TOUCH_MAJOR)
      Value      0
      Min        0
      Max      255
    Event code 53 (ABS_MT_POSITION_X)
      Value      0
      Min        0
      Max      720
    Event code 54 (ABS_MT_POSITION_Y)
      Value      0
      Min        0
      Max      720
    Event code 57 (ABS_MT_TRACKING_ID)
      Value      0
      Min        0
      Max    65535
    Event code 58 (ABS_MT_PRESSURE)
      Value      0
      Min        0
      Max      255
Properties:
  Property type 1 (INPUT_PROP_DIRECT)
Testing ... (interrupt to exit)

[ 1961.191409@2]- [FTS][fts_ts_interrupt]buffer: 00,00,01,01,34,01,87,00,00
[ 1961.192485@2]- [FTS][fts_ts_interrupt]point number: 1, touch point: 1
[ 1961.198918@2]- [FTS][fts_ts_interrupt][B]P0(308, 391)[p:63,tm:9] DOWN!
Event: time 1420072365.227099, type 3 (EV_ABS), code 57 (ABS_MT_TRAC[ 1961.211490@2]- [FTS][fts_ts_interrupt]buffer: 00,00,00,41,34,01,87,00,00
[ 1961.217866@2]- [FTS][fts_ts_interrupt]point number: 0, touch point: 1
[ 1961.224251@2]- [FTS][fts_ts_interrupt][B]P0 UP!
[ 1961.228740@2]- [FTS][fts_ts_interrupt]Points All Up!
KING_ID), value 4
Event: time 1420072365.227099, type 3 (EV_ABS), code 53 (ABS_MT_POSITION_X), value 308
Event: time 1420072365.227099, type 3 (EV_ABS), code 54 (ABS_MT_POSITION_Y), value 391
Event: time 1420072365.227099, -------------- SYN_REPORT ------------
Event: time 1420072365.255414, type 3 (EV_ABS), code 57 (ABS_MT_TRACKING_ID), value -1
Event: time 1420072365.255414, type 1 (EV_KEY), code 330 (BTN_TOUCH), value 0
Event: time 1420072365.255414, -------------- SYN_REPORT ------------

```

在fts_input_dev_report_b函数里，有调用上报pressure的，但是有条件。

估计是条件没有满足。

条件满足了的。

每次都有这个打印。

```
[  110.893563@3]- [FTS][fts_ts_interrupt][B]P0(347, 382)[p:63,tm:9] DOWN!
```

有时候，evtest有这个打印：

```
Event: time 1420070514.989533, type 3 (EV_ABS), code 58 (ABS_MT_PRESSURE), value 63
Event: time 1420070514.989533, type 3 (EV_ABS), code 48 (ABS_MT_TOUCH_MAJOR), value 9
```

有的时候没有。

驱动层有发，应用层没有收到。

什么原因？丢掉了？

只有第一次有，后面就都没有了。

是系统层第一次才有。即使把evtest重启。也是仍然没有，除非重启系统。

这是为什么？

看下evtest的代码。应该是很简单的。不应该出错的。

是很简单。不至于出错。

那事件为什么没有上来？



我们知道每次触摸完成后都必须发送一个同步事件（EV_SYN）来表明这次触摸的完成。 

那么对于多点触控的屏幕事件发送分为两种方法，

一是每次事件同步前包括多个点，

一是每次事件同步前仅包含一个点。



现在用hexdump /dev/input/event1的方式来查看。

触摸一下，有这些内容，解析一下。

```
/ # hexdump /dev/input/event1
0000000 8e5e 54a4 f6a2 0007 0003 0039 0001 0000
0000010 8e5e 54a4 f6a2 0007 0003 0035 0139 0000
0000020 8e5e 54a4 f6a2 0007 0003 0036 01a7 0000
0000030 8e5e 54a4 f6a2 0007 0001 014a 0001 0000
0000040 8e5e 54a4 f6a2 0007 0000 0000 0000 0000
0000050 8e5e 54a4 9874 0008 0003 0039 ffff ffff
0000060 8e5e 54a4 9874 0008 0001 014a 0000 0000
0000070 8e5e 54a4 9874 0008 0000 0000 0000 0000
```

每一行对应一个input_event结构体。

```
struct input_event {
	struct timeval time;
	__u16 type;
	__u16 code;
	__s32 value;
};
```

```
8e5e 54a4 f6a2 0007  这个是时间戳
0003 type  表示EV_ABS
0039 code  ABS_MT_TRACKING_ID 
0001 0000  value 
```

所以上面这次触摸的实际依次是：

```
tracking id 为1
X坐标
Y坐标
BTN_TOUCH down
EV_SYN
tracking id为0xffff ffff
BTN_TOUCH up
EV_SYN
```

确实是没有pressure事件。

那就要在内核里继续加打印。看看是哪里抛弃了这个事件。



https://discuss.vlug.narkive.com/gHWmeiHQ/how-to-interpret-dev-input-event0



## A协议和B协议

B协议：

没有SYN_MT_REPORT,

利用ABS_MT_TRACKING_ID来跟踪当前点属于哪一条线。

当前序列中某点的ID值，如果与前一次序列中某点的ID值相等，那么他们就属于同一条线，

应用层就不用再去计算这个点是哪条线上了；

如果按下并一直按同一个点，那么input子系统就会做个处理来屏蔽你上下两次相同点，减少IO负担。

协议B明显优越于协议A，但是协议B需要硬件支持，

ID值并不是随便赋值的，而是硬件上跟踪了点的轨迹，

比如按下一个点硬件就会跟踪这个点的ID，只要不抬起上报的点都会和这个ID相关。



## add_input_randomness

这个函数怎么理解？

看网上的一个注释这么写：

```
        // 对系统随机熵池有贡献，因为这个也是一个随机过程   
        add_input_randomness(type, code, value);
```

函数对事件发送没有一点用处,只是用来对随机数熵池增加一些贡献,因为按键输入是一种随机事件,所以对熵池是有贡献的。 

实现在这里。

```
TRACE_EVENT(add_input_randomness,
	TP_PROTO(int input_bits),

	TP_ARGS(input_bits),

	TP_STRUCT__entry(
		__field(	  int,	input_bits		)
	),

	TP_fast_assign(
		__entry->input_bits	= input_bits;
	),

	TP_printk("input_pool_bits %d", __entry->input_bits)
);
```



https://www.cnblogs.com/sky-heaven/p/5109128.html



input_to_handler

```
handler->filter(handle, v->type, v->code, v->value)
handler->events(handle, vals, count);
```

handler哪里注册进来的？

input_register_handle

input/evdev.c有进行注册。

这个就是对应/dev/input/event0这样的设备吗？

evdev没有实现filter。所以filter不会被调用。

最后events函数是触发了这个

kill_fasync(&client->fasync, SIGIO, POLL_IN);



多触点设备有：

指针类型，例如笔记本的触摸板。

直接类型，例如平板电脑的触摸屏。

```
#define INPUT_MT_POINTER	0x0001	/* pointer device, e.g. trackpad */
#define INPUT_MT_DIRECT		0x0002	/* direct device, e.g. touchscreen */
```



input_get_disposition()获得事件处理者身份。

INPUT_PASS_TO_HANDLERS表示交给input hardler处理，

INPUT_PASS_TO_DEVICE表示交给input device处理，

**INPUT_FLUSH表示需要handler立即处理。**

如果事件正常一般返回的是INPUT_PASS_TO_HANDLERS，

只有code为SYN_REPORT时返回INPUT_PASS_TO_HANDLERS | INPUT_FLUSH。

需要说明的是下面一段：

首先说明的是过滤处理，

如果code不是ABS_MT_FIRST到ABS_MT_LAST之间，那就是单点上报(比如ABS_X)；

否则符合多点上报；

**它们的事件值value存储的位置是不一样的，所以取pold指针的方式是不一样的。**

（这个pold是过滤之后存的*pold = *pval;）。

input_defuzz_abs_event()会对比当前value和上一次的old value；

如果一样就过滤掉；不产生事件，但是只针对type B进行处理；

**type B的framework层sync后是不会清除slot的，所以要确保上报数据的准确；**

**type A的sync后会清除slot。**

我改成协议A的来试一下。

当前我碰到的问题，应该就是pressure值没有变化，所以不会上报。

当前触摸屏到底支不支持获取pressure值？应该是不支持。

而驱动里又使能了。

而且应用层普遍都需要pressure。

改成协议A的。就可以了。





https://www.cnblogs.com/sky-heaven/p/9214329.html

这篇文章非常好，解答了我的疑惑。

https://blog.csdn.net/coldsnow33/article/details/12841077

# 测试工具

现在directfb里获取不到触摸事件。

所以看看怎么进行排查。

在tslib/tests目录下，有几个工具。

```
ts_finddev
	用法：ts_finddev /dev/input/event1 3
	在3秒内，有触摸则返回成功。
	
```



## ts_calibrate

执行完成后，会生成/etc/pointercal文件。

文件内容是：

```
65791 48 -438534 -1442 59395 2416436 65536 720 720 0
```

这些数字表示什么含义？



# 跟qt集成需要设置哪些

我当前的问题是：

1、使用linuxfb，没有配置QT_QPA_FB_TSLIB环境变量。

所以下面这个代码没有执行：

```
#if QT_CONFIG(tslib)
    bool useTslib = qEnvironmentVariableIntValue("QT_QPA_FB_TSLIB");
    if (useTslib)
        new QTsLibMouseHandler(QLatin1String("TsLib"), QString());
#endif
```

在这个前提下，触摸可以生效。那么是怎么生效的？

应该是这个：

```
#if QT_CONFIG(tslib)
    if (!useTslib)
#endif
        new QEvdevTouchManager(QLatin1String("EvdevTouch"), QString() /* spec */, this);
#endif
```

也不一定。这个要依赖这个。当前这个并没有被使能。

```
QT_CONFIG(evdev)
```

没有看到这样的配置项。

还是需要先把buildroot里的配置项看一遍。

没有看到配置evdev的。

那触摸屏是怎么起作用的？

我在pro文件里加message调试。可以看到evdev默认是有使能的。

/usr/lib/qt/plugins/generic input的在这个目录下。

要调试这个，只需要输出一下环境变量：export QT_QPA_EVDEV_DEBUG=1

```
qt.qpa.input: evdevtouch: Using device discovery
qt.qpa.input: evdevtouch: Adding device at "/dev/input/event1"
qt.qpa.input: evdevtouch: Using device /dev/input/event1
qt.qpa.input: evdevtouch: /dev/input/event1: Protocol type A  (multi), filtered=no
qt.qpa.input: evdevtouch: /dev/input/event1: min X: 0 max X: 720
qt.qpa.input: evdevtouch: /dev/input/event1: min Y: 0 max Y: 720
qt.qpa.input: evdevtouch: /dev/input/event1: min pressure: 0 max pressure: 0
qt.qpa.input: evdevtouch: /dev/input/event1: device name: fts_ts
qt.qpa.input: evdevtouch: Updating QInputDeviceManager device count: 1  touch devices, 0 pending handler(s)
```

从打印看，是自动扫描发现的触摸设备。不依赖配置的。

这个可以理解流程了。

不是直接用ts_read，而是read /dev/input/event1。



现在看qdirectfbintegration.cpp里怎么初始化input的。

```
void QDirectFbIntegration::connectToDirectFb()
{
    initializeDirectFB();
    initializeScreen();
    initializeInput();

    m_inputContext = QPlatformInputContextFactory::create();
}
```



```
void QDirectFbIntegration::initializeInput()
{
    m_input.reset(new QDirectFbInput(m_dfb.data(), m_primaryScreen->dfbLayer()));
    m_input->start();
}
```

那就是通过directfb来使用ts_read了。

现在directfb里的事件还是没有上来。

这是为什么？

在tslib.c里加打印，一次触摸打印如下。感觉是合理的。

```
xhl --  x:339, y:407,.presssure:63
xhl -- old x:-1, old y:-1, old pressure:0
xhl -- send x value
xhl -- send y value
xhl -- send press 3
xhl -- after wait event, event.type:5
xhl -- before wait event
xhl -- after wait event, event.type:5
xhl -- before wait event
xhl -- after wait event, event.type:3
xhl -- before wait event
xhl --  x:0, y:0,.presssure:0
xhl -- old x:339, old y:407, old pressure:63
xhl -- send press 4
xhl -- after wait event, event.type:4
xhl -- before wait event
```

dfb_input_dispatch的消息去哪里了？

```
 Fusion/Main/Dispatch:             event_dispatcher_loop() got msg 0x43478 <- arg 0, reaction 1                       
 IDFBEventBuffer:                      IDirectFBEventBuffer_InputReact( 0x434ac, 0x40378 ) <- type 000003             
 -:                                    DirectFB/IDirectFBInputDevice: Unknown event type detected (0x3), skipping!    
 Core/WindowStack:                     _dfb_windowstack_inputdevice_listener( 0x434ac, 0x3d760 )                      
```

IDirectFBInputDevice_React

这个函数，对于这个DFBInputEventType枚举

没有处理button press和button release的情况。

IDirectFBInputDevice_data 里都没有button相关的成员变量。

key的不方便来模拟。

找一个较老的directfb版本看看。

也是没有，应该是一直都没有。

那是怎么处理鼠标事件的？



input事件的传递过程

```
dfb_input_dispatch( data->device, &evt );
输入线程检测到input事件，进行分发。
```

里面调用到这里

```
if (core_local->hub)
          CoreInputHub_DispatchEvent( core_local->hub, device->shared->id, event );

     if (core_input_filter( device, event ))
          D_DEBUG_AT( Core_InputEvt, "  ****>> FILTERED\n" );
     else
          fusion_reactor_dispatch( device->shared->reactor, event, true, dfb_input_globals );
```

core_local->hub 是否有值？

在初始化的时候：

```
if (dfb_config->input_hub_service_qid)
          CoreInputHub_Create( dfb_config->input_hub_service_qid, &core_local->hub );
```

input_hub_service_qid 这个应该没有配置。不存在input hub。

所以还是靠fusion_reactor_dispatch来做。

然后是放入到队列里，然后唤醒等待的线程。

event_dispatcher_loop阻塞在队列上。

取出消息，这样处理：

```
msg->call_handler
也可能是
reaction->func
```

input事件处理的回调，这样注册进来的。

````
dfb_input_attach( device, IDirectFBEventBuffer_InputReact,
                       data, &attached->reaction );
````

这样存放的：

```
reaction->func      = func;
```

然后加入链表里。

IDirectFBEventBuffer_InputReact里做的处理，也只是把事件加入到buffer里。

IDirectFBEventBuffer_WaitForEvent 这个函数里等待buffer里的数据。

应用层调用了WaitForEvent函数指针。

然后就可以取出事件进行自己的处理。

当前的问题，在IDirectFBInputDevice_React这一步，

```
dfb_input_attach( data->device, IDirectFBInputDevice_React,
                       data, &data->reaction );
```

看看KEYPRESS怎么处理的。

DFBInputDeviceKeyIdentifier     key_id;
对应
DFBInputDeviceButtonIdentifier  button; 

按键的数组，是包括了所有的按键的。

data->keystates[index] = DIKS_DOWN;

是IDirectFBInputDevice_data 这个结构体里的。

这个结构体里，没有button的对应成员变量。

还是有一个

```
DFBInputDeviceButtonMask    buttonmask; 
```

有这个mask就够了？不用一个数组？

在IDirectFBInputDevice_React里

```
if (evt->flags & DIEF_BUTTONS)
          data->buttonmask = evt->buttons;
```

IDirectFBInputDevice_React的那个unknown打印，并没有实质影响，只是一行打印而已。

还是返回OK的。

应用层最后还是拿到这个事件了。

那边qt为什么没有拿到这个事件呢？

```
QEvent::Type QDirectFbConvenience::eventType(DFBWindowEventType type)
```



directfb和qt的input是怎么对接起来的？

配置上，只需要配置directfb的就好了吧。

qt的需要对input配置什么？

qt的都不用配置tslib吧。配置了按道理也没有什么关系。因为当前没有调用到。

WaitForEvent，为什么没有拿到数据？

那就要在directfb里加打印。



现在就是这个函数阻塞了。

IDirectFBEventBuffer_WaitForEvent

那就是这个

```
 direct_waitqueue_wait( &data->wait_condition, &data->events_mutex );
```

IDirectFBEventBuffer_AddItem 这个会唤醒线程。

IDirectFBEventBuffer_InputReact 里会调用。

IDirectFBEventBuffer_AttachInputDevice的时候，

```
dfb_input_attach( device, IDirectFBEventBuffer_InputReact,
                       data, &attached->reaction );
```

看这里有没有被执行。

这个函数没有被调用。这个是在扫描到input设备的时候执行。不只，有几处调用了。

IDirectFBEventBuffer_AttachInputDevice



```
IDirectFBInputDevice_AttachEventBuffer
IDirectFBInputDevice_CreateEventBuffer
CreateEventBuffer_Callback
containers_attach_device
```

运行dfbtest_input有调用一次。

```
(*) DFBTest/Input: Testing sensitivity with input device 1...
dispatch reaction 0x3dc48 channel 0 func 0xf615b438
IDirectFBEventBuffer_AttachInputDevice 813,
```

从代码看，执行了：

```
dfb->GetInputDevice
device->CreateEventBuffer
```

这样可以的。

qt可能是没有执行CreateEventBuffer这样的操作。

搜索了一下，在QDirectFbInput构造函数里有调用。

qt调用的是：

```
m_dfbInterface->CreateEventBuffer(m_dfbInterface, m_eventBuffer.outPtr());
```

EventBuffer和InputEventBuffer关系。

而在dfbtest_input里，是调用的这个：

```
device->CreateEventBuffer( device, &buffer );
```

函数指针名字一样，但是主体不一样。



在对于IDirectFB，Event和InputEvent分开了。

```
     thiz->CreateEventBuffer = IDirectFB_CreateEventBuffer;
     thiz->CreateInputEventBuffer = IDirectFB_CreateInputEventBuffer;
```

所以，是需要改qt里的代码。

这样改：

```
// DFBResult ok = m_dfbInterface->CreateEventBuffer(m_dfbInterface, m_eventBuffer.outPtr());
DFBResult ok = m_dfbInterface->CreateInputEventBuffer(m_dfbInterface, 0x7, DFB_TRUE, m_eventBuffer.outPtr());
```

这样改是否妥当，还存疑，应该另外加一个Event的。

现在QDirectFbInput::handleEvents 拿到事件了。

得到的type是4，跟下面这些宏应该是对不上的。中间按道理应该有一次type值的转换的。

```
if (event.clazz == DFEC_WINDOW) {
            switch (event.window.type) {
            case DWET_BUTTONDOWN:
            case DWET_BUTTONUP:
            case DWET_MOTION:
                handleMouseEvents(event);
```

在哪里进行转换的？

```
DWET_BUTTONDOWN     = 0x00010000,  /* mouse button went down in
                                           the window */
     DWET_BUTTONUP       = 0x00020000,  /* mouse button went up in
                                           the window */
```

当前我directfb没有配置wm。

是否有问题？

在directfbrc里加上wm=default。

运行还是一样的。

buttonpress在哪里被转换成DWET_BUTTONDOWN？

当前为什么没有转？

在wm的default里，有这样转：

```
send_button_event
    we.type   = (event->type == DIET_BUTTONPRESS) ? DWET_BUTTONDOWN : DWET_BUTTONUP;
```

wm_process_input 有没有被调用到？

```
.ProcessInput         = wm_process_input,
```

wm_process_input只被dfb_wm_process_input调用

stack_containers_attach_device

但是看代码，这些好像是在多进程的情况才用到。

wm对于单进程有用没？

单进程也可以有多个窗口。

(*) DirectFB/Core/WM: Default 0.3 (directfb.org)

wm是有使用上的。



 IDirectFB_CreateInputEventBuffer这个函数创建一个EventBuffer，通过EventBuffer可以获取输入事件，

**不过通常应该通过Window去创建EventBuffer，**

**那样可以收到更高层的事件。**

InputEventBuffer实际上主要是对InputDevice的包装，

不要小看这个包装，包装后有三个重要变化：

Event被缓冲,不用担心事件丢失或者阻塞驱动程序。

包装前的InputDevice事件是来一个处理一个，

包装后则是先放到缓冲中，然后一个一个的处理。

由被动变为主动，更符合GUI的事件处理的惯例。

包装前是上层设置回调函数，在事件到来时回调函数被下层调用，包装后是上层主动调用GetEvevnt 获取事件。                     

由多线程变为单线程，简化了处理。

包装前是由输入线程回调上层设置的回调函数，每个输入设备都是一个独立的线程，所以回调函数要考虑多线程并发执行的问题，包装后多线程问题由EventBuffer处理掉了，上层通过GetEvent获取事件并处理，处理函数始终是在主线程中执行的，所以不用考虑与输入线程的并发问题了。                    



怎么测试wm的input流程呢？

wm怎么被使用的？

## wm的调用

```
dfb_wm_process_input
被2个函数调用
WindowStack_Input_Flush
_dfb_windowstack_inputdevice_listener

WindowStack_Input_Flush
被下面3处调用：
WindowStack_Input_Add
WindowStack_Input_DispatchCleanup
_dfb_windowstack_inputdevice_listener

WindowStack_Input_Add
被1处调用：
_dfb_windowstack_inputdevice_listener

那么归根结底，是_dfb_windowstack_inputdevice_listener进行了调用。

_dfb_windowstack_inputdevice_listener
被2处调用：
stack_attach_devices
dfb_input_globals里，把_dfb_windowstack_inputdevice_listener作为数组成员。

stack_attach_devices
被2处调用
stack_containers_attach_device
dfb_windowstack_create

stack_containers_attach_device
这个只在多进程的情况下使用。我不考虑这种情况。

dfb_windowstack_create
只被1处调用。
dfb_layer_context_init

dfb_layer_create_context
那就跟踪这个函数的调用情况。
被2出调用：
ILayer_Real::CreateContext
dfb_layer_get_primary_context

ILayer_Real::CreateContext
这个在实际打印中没有看到。

dfb_layer_get_primary_context
这个有看到打印。
(-) [dfbtest_input    12374.173,023] (23139) DirectFB/CoreLayer:                       ILayer_Real::GetPrimaryContext()
(-) [dfbtest_input    12374.173,058] (23139) Fusion/Skirmish:                              fusion_skirmish_prevail( 0x3b5b4, 'Display Layer 0' )
(-) [dfbtest_input    12374.173,083] (23139) Core/Layers:                                  dfb_layer_get_primary_context (FBDev Primary Layer, activate) <- active: -1
(-) [dfbtest_input    12374.173,138] (23139) Fusion/Skirmish:                                  fusion_skirmish_dismiss( 0x3b5b4, 'Display Layer 0' )
(-) [dfbtest_input    12374.173,172] (23139) Core/Layers:                                      dfb_layer_create_context (FBDev Primary Layer)

对wm的初始化
Core/Parts:                                       Going to initialize 'wm_core' core...
Core/WM:                                              dfb_wm_core_initialize( 0x2d838, 0x3b830, 0x3b850 )
```



现在还是要回到Event和InputEvent的关系。

按道理directfb在1.7.7版本上很久了。不应该存在这么明显的问题。



运行dfbtest_window_cursor这个例子。

触摸交互有反应。看看代码是怎么写的。

```
m_dfb->CreateEventBuffer( m_dfb, &m_events );
```

这个测试代码的逻辑是，在（100，100）和（200,400）的位置，有2个正方形的边长为200的window，颜色为白色。当cursor进入对应区域，就是focus变化的时候，进行显示或者隐藏。

我发现现在qt的测试例子也可以了。

通过对directfbrc文件里的修改进行回退。

我就改了2点：

```
去掉no-cursor
增加wm=default
```

发现是no-cursor导致的问题。wm没有影响。因为不写wm默认也是用了的。

cursor为什么会对这个有影响？

现在先把qt的Event的改回去。看看是否正常。

也可以了。

cursor可以从qt这一层来进行隐藏。

qml里试了一下，没有隐藏掉。但是肯定是可以隐藏的。

先不纠结这个。

现在就看no-cursor为什么会影响InputEvent。



这个是一个module_raw galax。

从里面的一段注释，可以看到作用是：tslib依赖pressure值，而有的触摸屏没有pressure值。

这个模块就是用来固定pressure值为255 。

```
	/* Since some touchscreens (eg. infrared) physically can't measure pressure,
	 * the input system doesn't report it on those. Tslib relies on pressure, thus
	 * we set it to constant 255. It's still controlled by BTN_TOUCH - when not
	 * touched, the pressure is forced to 0.
	 */
```

我手动加上这个galax的编译配置。

在ts.conf也加上。

但是运行后，导致ts_read直接返回。一直打印x、y、pressure值都是-1 。

是应该把module_raw input去掉。

去掉还是不行。

应该是ts_read返回了错误导致的。



https://www.raspberrypi.org/forums/viewtopic.php?t=39027



# 环境变量配置

为了实现Tslib的正确运行，需要对如下的Tslib的环境变量进行配置：

TSLIB_TSDEVICE //触摸屏设备文件名。

Default (no inputapi): /dev/touchscreen/ucb1x00

Default (inputapi): /dev/input/event0

TSLIB_CALIBFILE //校准的数据文件，由ts_calibrate校准程序生成。

Default: ${sysconfdir}/pointercal

TSLIB_CONFFILE //配置文件名。

Default: ${sysconfdir}/ts.conf

TSLIB_PLUGINDIR //插件目录

Default: ${datadir}/plugins

TSLIB_CONSOLEDEVICE //控制台设备文件名

Default: /dev/tty

TSLIB_FBDEVICE //设备名

Default: /dev/fb0

以上环境变量在实际开发中的实际配置可以根据实际情况决定。

# ts.conf

在ts.conf 中配置了需要加载的插件、**插件加载顺序**以及插件的一些约束参数，

顺序要注意。是安装写的先后顺序一次加载执行的。

这些配置参数对触摸屏的触摸效果具有十分重要的影响。
其中：

pthres 为Tslib 提供的触摸屏灵敏度门槛插件 默认参数为pmin=1；

variance 为Tslib提供的触摸屏滤波算法插件 默认参数为delta=30；

dejitter 为Tslib 提供的触摸屏去噪算法插件 默认参数为delta=100；

linear为Tslib 提供的触摸屏坐标变换插件。

 由于各种因素的影响，在不同的硬件平台上，相关参数可能需要调整。

以上参数的相互关系为：

采样间隔越大，采样点越少，采样越失真，

但因为信息量少，容易出现丢笔划等丢失信息情况，但表现出来的图形效果将会越好；

去噪算法跟采样间隔应密切互动，采样间隔越大，去噪约束应越小，反之采样间隔越小，去噪约束应越大。去抖算法为相对独立的部分，去抖算法越复杂，带来的计算量将会变大，系统负载将会变重，但良好的去抖算法可以更好的去除抖动，在进行图形绘制时将会得到更好的效果；灵敏度和ts 门槛值为触摸屏的灵敏指标，一般不需要进行变动，参考参考值即



在tslib中为应用层提供了2个主要的接口ts_read()和ts_read_raw()，

其中ts_read()为正常情况下的借口，

ts_read_raw()为校准情况下的接口。

正常情况下，tslib对驱动采样到的设备坐标进行处理的一般过程如下：

raw device --> variance --> dejitter --> linear --> application

module module module

校准情况下，tslib对驱动采样到的数据进行处理的一般过程如下：

raw device--> Calibrate



正常情况下，tslib对驱动采样到的设备坐标进行处理的一般过程如下：

raw device --> variance --> dejitter --> linear --> application

module module module

校准情况下，tslib对驱动采样到的数据进行处理的一般过程如下：

raw device--> Calibrate



# 参考资料

1、

https://blog.csdn.net/orz415678659/article/details/9136575

2、【Device Tree】设备树(一)——GPIO

https://blog.csdn.net/qq_38131812/article/details/88956752

3、

https://doc.qt.io/archives/qt-4.8/qt-embedded-charinput.html

4、

https://www.shangmayuan.com/a/dd0eb857ea284a4d84b13752.html

5、

https://www.fearlazy.com/index.php/post/167.html

6、

https://my.oschina.net/shelllife?q=Qt

7、

https://forum.qt.io/topic/82892/how-to-install-tslib-plugin-for-qt-5-7/4

8、

https://www.cnblogs.com/Rainingday/p/13674210.html

9、【QT学习】QT中使用虚拟键盘

https://blog.csdn.net/ipfpm/article/details/93591905

10、

https://blog.csdn.net/tanhao199406/article/details/45509767

11、Tslib配置文件ts.conf介绍

https://www.cnblogs.com/nanqiang/p/11452408.html

12、

https://www.cnblogs.com/lihaiping/p/tslib.html

13、

https://blog.csdn.net/heanyu/article/details/6715301

14、tslib 代码分析1

https://blog.csdn.net/hejinjing_tom_com/article/details/49252333

15、Linux输入子系统：多点触控协议 -- multi-touch-protocol.txt【转】

https://www.cnblogs.com/sky-heaven/p/5403392.html

16、

https://www.shuzhiduo.com/A/MAzAPVQ1d9/

17、

https://www.codeleading.com/article/67425421626/

18、

https://blog.csdn.net/Lliuzz0827/article/details/73838980/

# 末尾