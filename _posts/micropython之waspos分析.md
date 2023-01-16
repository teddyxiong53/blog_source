---
title: micropython之waspos分析
date: 2023-01-10 15:14:31
tags:
	- Python

---



# ubuntu下模拟运行

先安装环境：

```
sudo apt install \
  wget git build-essential libsdl2-2.0-0 python3-click python3-gi \
  python3-numpy python3-pexpect python3-pil python3-pip python3-pydbus \
  python3-serial unzip
pip3 install --user cbor pysdl2
sudo apt install sphinx graphviz python3-recommonmark
```

下载代码：

```
git clone https://github.com/daniel-thompson/wasp-os
```

下载submodule：

```
make submodules
```

在gui环境执行下面命令，就可以把模拟环境跑起来。

```
make sim
```

sim是用系统的python来运行的。

构造了一个假的machine.py和micropython.py来兼容。



这个可以跟基于lvgl的x-track来对比着看。

x-track是基于C++的。

waspos是完全python写的。



当前make sim的模拟器是怎么跑起来的？

模拟器是基于sdl2的。

wasp\boards\simulator\watch.py里，

```
from drivers.st7789 import ST7789_SPI
display = ST7789_SPI
```

wasp\drivers\st7789.py

# 代码分析

从make sim开始分析。

```
sim:
	PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=.:wasp/boards/simulator:wasp \
	$(PYTHON) -i wasp/boards/simulator/main.py
```

PYTHONDONTWRITEBYTECODE 这个环境变量怎么使用的？

当前的代码里是没有用到。

难道是python的标准环境变量？

这里是一个知识点，就是设置python不要生成字节码pyc文件。

```
设置不生成字节码文件
方式一：设置环境变量(最常用的)

export PYTHONDONTWRITEBYTECODE=1

方式二：使用 -B参数

$ python -B test.py

方式三：在导入的地方写

import sys
sys.dont_write_bytecode = True
```

PYTHONPATH=.:wasp/boards/simulator:wasp

这个增加了PYTHON的搜索路径。

```
$(PYTHON) -i wasp/boards/simulator/main.py
```



```
# Test app is used a lot on the simulator. Let's make sure it is
# registered by default.
wasp.system.register('apps.testapp.TestApp')
```

wasp对应的是wasp/wasp.py文件。

wasp.system是

```
system = Manager()
```

Manager

```
class Manager():
    """Wasp-os system manager
```

从注释里看，这个Manager是用来处理UI event和分发event给foreground的App的。

是系统的核心类。管理了所有的App。

相当于Android的Launcher的概念？

还给App提供了service。

Manage是单例的，在任意地方都可以通过wasp.system来进行访问。

## wasp/widgets.py

这个是实现各种控件的，例如Button等。给App使用的。

### class

总共13个class。也只有这些class。没有单独的函数。

```
BatteryMeter
	这个对应的就是电池图标，通知栏的右上角的。
	3个函数，构造、draw、update。
	只有一个成员变量：level。表示的是电池的百分比。默认给的-2 。
Clock
	都是3个函数，构造、draw、update。
	一般draw函数就是调用了一下update函数。
NotificationBar
StatusBar
ScrollIndicator
Button
ToggleButton
Checkbox
GfxButton
Slider
Spinner
Stopwatch
ConfirmationView
```

## wasp\boards\simulator\watch.py

这个是对手表硬件的聚合。

包括了这些class

```
Accelerometer
	主要用来计步了。
Backlight
	就一个set函数，里面控制一个gpio。
Battery
RTC
	这个就用time.localtime来模拟。
HRS

```

有一个LauncherApp，所以Manager不是launcher。

## 主循环

```
wasp.system.run()
```

先注册这些App：

```
    def register_defaults(self):
        """Register the default applications."""
        self.register('apps.clock.ClockApp', True, no_except=True)
        self.register('apps.steps.StepCounterApp', True, no_except=True)
        self.register('apps.stopwatch.StopwatchApp', True, no_except=True)
        self.register('apps.heart.HeartApp', True, no_except=True)

        self.register('apps.faces.FacesApp', no_except=True)
        self.register('apps.settings.SettingsApp', no_except=True)
        self.register('apps.software.SoftwareApp', no_except=True)
```

register的逻辑是：

```
if isinstance(app, str):
            modname = app[:app.rindex('.')]
            exec('import ' + modname)

```

这个相当于

```
import apps.clock
```

然后：

```
app = eval(app + '()')
```

这个相当于：

```
app = apps.clock.ClockApp()
```

然后删除掉：应该是为了节省内存。

```\
exec('del ' + modname)
exec('del sys.modules["' + modname + '"]')
```

然后执行这些：

```
# System start up...
            watch.display.poweron()  这个是把屏幕点亮。
            watch.display.mute(True)  display对应的是ST7789_SPI
            watch.backlight.set(self._brightness)
            self.sleep_at = watch.rtc.uptime + 90
            if watch.free:
                gc.collect()
                free = gc.mem_free()
```

ST7789_SPI的属性：

```
宽高240x240
spi总线的。
cs 引脚。片选
dc引脚。data or cmd区分引脚。
res 复位引脚。
```

```
class ST7789_SPI(ST7789):
这个继承关系，应该说明还有非SPI接口的ST7789
```

死循环里调用的是这个：

```
while True:
                self._tick()
                machine.deepsleep()
```

这个tick表示什么？

就是检测时间，主要给闹钟用的。

事件分发是哪里做的呢？

搜索schedule这个函数的调用。没有啥。

这个是切换到某个应用。

```
self.switch(self.quick_ring[0])
```

在LauncherApp里：

```
    def foreground(self):
        """Activate the application."""
        self._page = 0
        self._draw()
        wasp.system.request_event(wasp.EventMask.TOUCH |
                                  wasp.EventMask.SWIPE_UPDOWN)
```





# 参考资料

1、

https://wasp-os.readthedocs.io/en/latest/install.html#install-prerequisites

2、

https://blog.csdn.net/inthat/article/details/116262103