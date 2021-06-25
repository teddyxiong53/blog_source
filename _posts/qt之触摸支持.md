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