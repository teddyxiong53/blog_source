---
title: wxpython重新梳理（1）
date: 2022-12-30 10:54:30
tags:
	- python
---

--



https://zhuanlan.zhihu.com/p/525972401

wxWidgets和MFC的确太相似了，连命名习惯和架构都高度相似。

事实上，wxWidgets就是跨平台的MFC，

对各个平台的差异做了抽象，后端还是用各平台原生的API实现。

这正是wxWidgets的优点：编译出来的程序发行包比较小，性能也相当优异。

缺少或拒绝商业化运作的支持，wxWidgets的悲情结局早已是命中注定。

如果不是因为Python的兴盛和wxPython的复兴，wxWidgets也许早已经和MFC一样被遗忘在了角落里。

不无夸张地说，wxPython是以MFC为代表的一个时代的挽歌，更是一曲理想主义的绝唱。

# 资源收集

这个简单实用的小手册

https://wiki.wxpython.org/wxClassesCheatSheet

# 基于wxpython的应用

https://wiki.wxpython.org/wxPythonPit%20Apps



https://sourceforge.net/projects/boa-constructor/



# 看core.pyi文件

D:\python36-32\Lib\site-packages\wx\core.pyi

这个相当于wx这个namespace下面的主要符号。

有5万行。

# 基本教程

尽管wxPython也与时俱进地增加了一些诸如wx.xml、wx.svg之类地外围模块，

但除了wx这个核心模块之外，我个人觉得只有wx.aui和wx.grid模块算是必要的扩展。

如果想让界面更花哨点，那就要了解以下wx.adv、wx.ribbon这两个模块，

纯python构建的控件库wx.lib也绝对值得一试。

总之，站在我的应用领域看，wxPython的组织架构如下图所示。

根据使用频率的高低，我给各个模块标注了红黄绿蓝四种颜色。



用wxPython写一个桌面应用程序，通常分为6个步骤：

- 第1步：导入模块
- 第2步：创建一个应用程序
- 第3步：创建主窗口
- 第4步：在主窗口上实现业务逻辑
- 第5步：显示窗主口
- 第6步：应用程序进入事件处理主循环



wxPython的控件在使用风格上保持着高度的一致性，

一方面因为它们从一个共同的基类派生而来，

更重要的一点，wxPython不像PyQt那样充斥着随处可见的重载函数。

比如，PyQt的菜单栏QMenuBar增加菜单，

就有addMenu(QMenu)、addMenu(str)和addMenu(QIcon, str)等三种不同的重载形式。

方法重载固然带来了很多便利，但也会增加使用难度，让用户无所适从。



除了用户自定义事件，在wxPython中我习惯把事件分为4类：

- 鼠标事件：鼠标左右中键和滚轮动作，以及鼠标移动等事件
- 键盘事件：用户敲击键盘产生的事件
- 控件事件：发生在控件上的事件，比如按钮被按下、输入框内容改变等
- 系统事件：关闭窗口、改变窗口大小、重绘、定时器等事件



常用的鼠标事件包括：

- wx.EVT_LEFT_DOWN - 左键按下
- wx.EVT_LEFT_UP - 左键弹起
- wx.EVT_LEFT_DCLICK - 左键双击
- wx.EVT_RIGHT_DOWN - 右键按下
- wx.EVT_RIGHT_UP - 右键弹起
- wx.EVT_RIGHT_DCLICK - 右键双击
- wx.EVT_MOTION - 鼠标移动
- wx.EVT_MOUSEWHEEL - 滚轮滚动
- wx.EVT_MOUSE_EVENTS - 所有的鼠标事件

常用的键盘事件有：

- wx.EVT_KEY_DOWN - 按键按下
- wx.EVT_KEY_UP - 按键弹起

常用的系统事件包括：

- wx.EVT_CLOSE - 关闭
- wx.EVT_SIZE - 改变大小
- wx.EVT_TIMER - 定时器事件
- wx.EVT_PAINT - 重绘
- wx.EVT_ERASE_BACKGROUND -背景擦除

常用的控件事件包括：

- wx.EVT_BUTTON - 点击按钮
- wx.EVT_CHOICE - 下拉框改变选择
- wx.EVT_TEXT - 输入框内容改变
- wx.EVT_TEXT_ENTER - 输入框回车
- wx.EVT_RADIOBOX - 单选框改变选择
- wx.EVT_CHECKBOX - 点击复选框



事件驱动机制有三个要素：事件、事件函数和事件绑定。

比如，当一个按钮被点击时，就会触发按钮点击事件，该事件如果绑定了事件函数，事件函数就会被调用。

所有的事件函数都以事件对象为参数，事件对象提供了事件的详细信息，比如键盘按下事件的事件对象就包含了被按下的键的信息。



# aui

Advanced User Interface，简称AUI，是wxPython的子模块，使用AUI可以方便地开发出美观、易用的用户界面。

从2.8.9.2版本之后，wxPython增加了一个高级通用部件库Advanced Generic Widgets，简称AGW库， AGW库也提供了AUI模块 wx.lib.agw.aui，而 wx.aui也依然保留着。

相比较而言，我更喜欢使用wx.lib.agw的AUI框架。

使用AUI框架可以概括为以下四步：

1. 创建一个布局管理器：mgr = aui.AuiManager()
2. 告诉主窗口由mgr来管理界面：mgr.SetManagedWindow()
3. 添加界面上的各个区域：mgr.AddPane()
4. 更新界面显示：mgr.Update()



# 嵌入base64编码的图片

在使用wxpython进行可视化界面编程时，可能遇到的一些需要插入图片的地方有：

窗口图标、工具栏图标、按钮图标等，且这些地方使用的图片格式可能不一样。

这里介绍一种处理图片的方法，以二进制形式打开图片文件，并将其以[base64](https://so.csdn.net/so/search?q=base64&spm=1001.2101.3001.7020)编码，再解码为字符串形式。

这里的picture可以是各种格式的图片（png、jpg、ico、bmp等）

```
with open(picture 'rb') as f:
    base64_data = base64.b64encode(f.read())
    pic_data = base64_data.decode()
```

这里得到的字符串pic_data就可以直接存放入代码中，替代放在目录中的图片

之后再通过类**wx.lib.embeddedimage.PyEmbeddedImage**来获取图片对象



然而使用wxPython开发windows程序时，却没有类似资源文件的概念，我们不得不将图片等一些媒体文件一个一个的保存到程序的某个目录下面，待需要时从磁盘读取。如：

```python
icon = wx.Bitmap('icons/chat.ico', wx.BITMAP_TYPE_ICO)
icon = wx.IconFromLocation(wx.IconLocation(r'icons/chat.ico', 0))
icon = wx.Icon(r'icons/chat.ico', wx.BITMAP_TYPE_ICO)
```

以上几种方式都可以取到chat.ico图标文件，

当然还有其他方法。

为避免在程序的目录下出现太多的这样的媒体文件，

可以将这些文件进行序列化成base64编码的字符串，并在py文件中存在，

当程序加载时，这些字符串则直接存在于内存，当需要这些媒体文件时，就可以直接从内存解码出文件流。



wxPython在wx.lib.embeddedimage模块下有PyEmbeddedImage类，专门用于将经过base64编码过的图片的字符串解码成文件流，并提供了接口，将文件流转化成相应的图片格式。



然而在开发过程中可能会有很多这样的图片，并且这样的图片还有可能在开发过程中发生变化，

如果要一个一个的手动把图片都进行base64编码，那将是一个非常麻烦的事情。

因此这里提供一个简单的脚本，帮助快速生成“资源”文件。

# seniorwizard csdn博客梳理

这个系列博客非常好。值得通读一遍。

# wx.lib 下面的类主要的作用

wxPython 中的 `wx.lib` 模块是 wxPython 库的扩展模块，提供了一些额外的功能和控件，用于增强和扩展 wxPython 的能力。

下面是 `wx.lib` 模块中一些常用类的主要作用：

1. `wx.lib.mixins`：提供了一些混合类（Mixin Class），用于在用户定义的类中添加特定功能，如事件处理、状态管理等。

2. `wx.lib.agw`：包含了许多高级控件和自定义控件，如 `FlatNotebook`、`AuiManager` 等，用于创建复杂的用户界面和定制化的控件。

3. `wx.lib.buttons`：提供了一些自定义按钮控件，如带图标的按钮、切换按钮、复选框按钮等，扩展了 wxPython 默认提供的按钮控件的功能和样式。

4. `wx.lib.colourdb`：提供了一些颜色相关的函数和常量，用于操作和管理颜色。

5. `wx.lib.floatcanvas`：提供了一个基于浮点数的画布类，用于创建和操作可缩放的矢量图形。

6. `wx.lib.masked`：提供了一个掩码文本框类，用于限制和格式化用户输入的文本。

7. `wx.lib.plot`：提供了一个简单的绘图库，用于绘制二维数据图表，如折线图、散点图等。

8. `wx.lib.rcsizer`：提供了一个可重用的布局管理器类，用于自动调整和调整大小的布局。

这些类扩展了 wxPython 库的功能和控件，提供了更多的选项和功能，可以帮助开发者更方便地创建复杂的用户界面和实现特定的需求。可以根据具体的项目需求，选择合适的类进行使用和定制。

# wxpython的类怎么划分进行理解记忆

理解和记忆 wxPython 中的类可以通过以下方法进行划分和组织：

1. 根据类的作用和功能：将类按照其在用户界面开发中的作用和功能进行划分。例如，将控件类（如按钮、文本框、列表框等）归为一组，将布局管理器类（如 BoxSizer、GridSizer、FlexGridSizer 等）归为一组，将事件处理类（如 EVT_BUTTON、EVT_TEXT 等）归为一组。这样可以根据开发的需要选择和记忆相关的类。

2. 根据类的继承关系和层级：wxPython 中的类存在继承关系，可以根据类之间的继承关系进行组织和理解。例如，wx.Window 是所有窗口类的基类，它派生出了 wx.Frame、wx.Dialog、wx.Panel 等具体的窗口类。了解这种继承关系可以帮助理解类的层级结构和类之间的关联。

3. 根据类的模块或命名空间：wxPython 的类根据所属的模块或命名空间进行组织。例如，wx 模块下的类是核心类，提供了基本的窗口和控件功能；wx.lib 模块下的类是扩展类，提供了额外的功能和控件；wx.adv 模块下的类是高级类，提供了一些高级的控件和功能。了解类所属的模块或命名空间可以帮助定位和记忆相关的类。

4. 根据类的常用性和普遍性：wxPython 中有一些常用且普遍适用的类，例如 wx.Frame、wx.Panel、wx.Button 等，它们在几乎所有的 wxPython 项目中都会使用到。对这些常用的类进行重点学习和记忆，可以建立起一个基础的类库，并随着项目的进展逐渐添加和学习其他类。

5. 根据实际项目需求：根据具体的项目需求和功能要求，选择性地学习和记忆相关的类。如果项目需要使用特定的控件或实现特定的功能，可以重点学习与之相关的类，并逐步扩展和掌握其他相关的类。

无论选择哪种方法，都建议结合实践和实际项目进行学习和记忆。通过实际的编码和项目实践，将类的概念与实际应用相结合，加深对类的理解和记忆。同时，使用官方文档、教程和示例代码等资源，以及参与社区和开发者的讨论和交流，可以进一步加深对 wxPython 类的理解和

# 通过wxpython的源代码目录下的demo运行来学习

下面的run.py文件。可以帮助运行其他的文件。效果不错。

# wxpython源代码的samples目录

这个是c++和wxpython混合编程。

D:\download\Phoenix-master\samples\embedded

这个是ribbon的界面。做得很好。

D:\download\Phoenix-master\samples\ribbon\ribbonbar_demo.py

# wxpython etgtools介绍

`etgtools`是wxPython中的一个工具集，它用于生成与C++库的绑定代码。这些绑定代码使得开发者可以使用Python编程语言来访问和操作底层的wxWidgets C++库。

`etgtools`是由`wxPython/tools`目录中的一组Python脚本组成。这些脚本被用于解析wxWidgets的头文件，并生成对应的Python绑定代码。

使用`etgtools`生成的绑定代码提供了与底层C++库进行交互的接口，使得开发者可以使用Python编写wxPython应用程序，享受Python的简洁性和易用性。

具体来说，`etgtools`的主要功能包括：

1. 解析C++头文件：`etgtools`通过解析wxWidgets的C++头文件，分析类、方法、属性和事件等元素的定义和结构。

2. 自动生成绑定代码：根据解析的结果，`etgtools`自动生成与C++类、方法和属性对应的Python绑定代码。

3. 处理包装器特性：`etgtools`还能够处理包装器特性，如自动类型转换、异常处理和内存管理等。

通过使用`etgtools`，wxPython能够提供完整而强大的Python绑定，使得开发者能够方便地使用Python编写GUI应用程序。

值得注意的是，一般情况下，作为wxPython用户，您不需要直接使用或了解`etgtools`。您只需要安装和导入wxPython库，即可使用它提供的功能和控件来构建应用程序界面。`etgtools`主要是用于开发者维护和扩展wxPython的底层绑定代码。

# xrc用法

```
<?xml version="1.0" encoding="utf-8"?>
<!-- design layout in a separate XML file -->
<resource>
  <object class="wxFrame" name="mainFrame">
    <title>My Frame</title>
    <object class="wxPanel" name="panel">
      <object class="wxFlexGridSizer">
        <cols>2</cols>
        <rows>3</rows>
        <vgap>5</vgap>
        <hgap>5</hgap>
        <object class="sizeritem">
          <object class="wxStaticText" name="label1">
            <label>First name:</label>
          </object>
        </object>
        <object class="sizeritem">
          <object class="wxTextCtrl" name="text1"/>
        </object>
        <object class="sizeritem">
          <object class="wxStaticText" name="label2">
            <label>Last name:</label>
          </object>
        </object>
        <object class="sizeritem">
          <object class="wxTextCtrl" name="text2"/>
        </object>
        <object class="spacer">
          <size>0,0</size>
        </object>
        <object class="sizeritem">
          <object class="wxButton" name="button">
            <label>Submit</label>
          </object>
        </object>
      </object>
    </object>
  </object>
</resource>

```

```

import wx
from wx import xrc


class MyApp(wx.App):

    def OnInit(self):
        self.res = xrc.XmlResource('gui.xrc')
        self.init_frame()
        return True

    def init_frame(self):
        self.frame = self.res.LoadFrame(None, 'mainFrame')
        self.panel = xrc.XRCCTRL(self.frame, 'panel')
        self.text1 = xrc.XRCCTRL(self.panel, 'text1')
        self.text2 = xrc.XRCCTRL(self.panel, 'text2')
        self.frame.Bind(wx.EVT_BUTTON, self.OnSubmit, id=xrc.XRCID('button'))
        self.frame.Show()

    def OnSubmit(self, evt):
        wx.MessageBox('Your name is %s %s!' %
            (self.text1.GetValue(), self.text2.GetValue()), 'Feedback')


if __name__ == '__main__':
    app = MyApp(False)
    app.MainLoop()

```

感觉写起来也没有很好用。

还不如直接写界面。

# *encode_bitmaps.py*生成PyEmbeddedImage

看到wxpython的sample里有这样的数据：

```
Mondrian = PyEmbeddedImage(
    b"iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAHFJ"
    b"REFUWIXt1jsKgDAQRdF7xY25cpcWC60kioI6Fm/ahHBCMh+BRmGMnAgEWnvPpzK8dvrFCCCA"
    b"coD8og4c5Lr6WB3Q3l1TBwLYPuF3YS1gn1HphgEEEABcKERrGy0E3B0HFJg7C1N/f/kTBBBA"
    b"+Vi+AMkgFEvBPD17AAAAAElFTkSuQmCC")

```

这个是怎么生成的？

看注释里写了

```
# This file was generated by encode_bitmaps.py
```

encode_bitmaps.py这个是wxpython的demo里的一个工具。

具体使用方法是：

```

```



# 一些链接



https://blog.csdn.net/seniorwizard/article/details/130894657

https://blog.csdn.net/jdzhangxin/article/details/78377619

# 参考资料

https://blog.csdn.net/qq_37534835/article/details/90715871