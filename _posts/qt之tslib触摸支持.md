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
export TSLIB_TSDEVICE=/dev/input/input1
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



# 测试工具

现在directfb里获取不到触摸事件。

所以看看怎么进行排查。

在tslib/tests目录下，有几个工具。

```
ts_finddev
	用法：ts_finddev /dev/input/event1 3
	在3秒内，有触摸则返回成功。
	
```

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

# 末尾