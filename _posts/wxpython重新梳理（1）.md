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

# 实现国际化和本地化

# wxpython里的颜色表示

在 wxPython 中，可以使用不同的方式来表示颜色。下面是几种常用的方式：

1. RGB 值表示：使用 0-255 之间的整数表示红、绿、蓝三原色的强度，例如：

   ````python
   red = wx.Colour(255, 0, 0)  # 红色
   green = wx.Colour(0, 255, 0)  # 绿色
   blue = wx.Colour(0, 0, 255)  # 蓝色
   ```

2. 十六进制表示：使用六位十六进制数表示红、绿、蓝三原色的强度，例如：

   ````python
   red = wx.Colour(0xFF, 0, 0)  # 红色
   green = wx.Colour(0, 0xFF, 0)  # 绿色
   blue = wx.Colour(0, 0, 0xFF)  # 蓝色
   ```

3. 预定义颜色名称：wxPython 中提供了一些常用颜色的预定义名称，例如：

   ````python
   red = wx.RED  # 红色
   green = wx.GREEN  # 绿色
   blue = wx.BLUE  # 蓝色
   ```

4. HTML 颜色表示：使用 HTML 颜色代码表示颜色，例如：

   ````python
   red = wx.Colour('#FF0000')  # 红色
   green = wx.Colour('#00FF00')  # 绿色
   blue = wx.Colour('#0000FF')  # 蓝色
   ```

在 wxPython 中，可以将颜色应用于各种控件和绘图操作中。例如，可以将颜色应用于按钮、文本、背景等控件，或者将颜色用于绘制图形、线条等。

需要注意的是，wxPython 中的颜色表示可能因不同平台而有所不同，例如在 Windows 上使用的 RGB 值与在 Linux 上使用的 RGB 值可能不同。因此，建议使用 wxPython 中提供的预定义颜色名称，以确保在不同平台上都能获得一致的效果。

## 预定义颜色梳理

在 wxPython 中，可以使用预定义的颜色名称来表示常见的颜色。以下是 wxPython 中预定义的一些常用颜色及其说明：

- `wx.BLACK`：黑色
- `wx.WHITE`：白色
- `wx.RED`：红色
- `wx.GREEN`：绿色
- `wx.BLUE`：蓝色
- `wx.CYAN`：青色
- `wx.MAGENTA`：洋红色
- `wx.YELLOW`：黄色
- `wx.LIGHT_GREY`：浅灰色
- `wx.MEDIUM_GREY`：中灰色
- `wx.DARK_GREY`：深灰色
- `wx.TRANSPARENT`：透明色

除了上述预定义颜色之外，wxPython 还提供了一些较少使用的预定义颜色，例如：

- `wx.Colour(0, 128, 0)`：深绿色
- `wx.Colour(128, 0, 128)`：紫色
- `wx.Colour(255, 140, 0)`：橙色
- `wx.Colour(210, 105, 30)`：棕色

如果需要使用其他颜色，可以使用 `wx.Colour()` 类来创建自定义颜色。其构造函数可以接受红、绿、蓝三原色的值，例如：

```python
my_color = wx.Colour(255, 255, 0)  # 创建一个黄色
```

需要注意的是，wxPython 中预定义的颜色名称可能因不同平台而有所不同，例如在 Windows 上使用的颜色名称可能与在 Linux 上使用的颜色名称不同。因此，建议在使用预定义颜色名称时进行测试，以确保在不同平台上都能获得一致的效果。

# wxpython的类构造参数

一般是这6个：

```
parent
id
name
上面3个一般都要。
pos
size
空间信息。
style：风格。
```

# wx.Window分析

在 wxPython 中，`wx.Window` 是所有可显示窗口的基类，它提供了一些基本的窗口功能。`wx.Window` 类是许多其他 wxPython 控件的直接或间接父类，包括 `wx.Frame`、`wx.Panel`、`wx.Dialog` 等。

`wx.Window` 类提供了许多常用的方法和事件，可以用于处理鼠标、键盘、绘图和尺寸变化等事件。以下是一些常用的方法和事件：

- `wx.Window.SetBackgroundColour(colour)`：设置窗口的背景颜色。
- `wx.Window.SetForegroundColour(colour)`：设置窗口的前景颜色。
- `wx.Window.SetSizer(sizer)`：将指定的 Sizer 应用到窗口上。
- `wx.Window.GetSize()`：获取窗口的大小。
- `wx.Window.GetPosition()`：获取窗口的位置。
- `wx.Window.SetSize(size)`：设置窗口的大小。
- `wx.Window.SetPosition(pos)`：设置窗口的位置。
- `wx.Window.Refresh()`：刷新窗口。
- `wx.Window.Show(show=True)`：显示或隐藏窗口。

`wx.Window` 类还提供了许多事件，可以用于处理鼠标、键盘、绘图和尺寸变化等事件。以下是一些常用的事件：

- `wx.EVT_LEFT_DOWN`：鼠标左键按下事件。
- `wx.EVT_LEFT_UP`：鼠标左键释放事件。
- `wx.EVT_RIGHT_DOWN`：鼠标右键按下事件。
- `wx.EVT_RIGHT_UP`：鼠标右键释放事件。
- `wx.EVT_MOUSEWHEEL`：鼠标滚轮滚动事件。
- `wx.EVT_KEY_DOWN`：键盘按键按下事件。
- `wx.EVT_KEY_UP`：键盘按键释放事件。
- `wx.EVT_PAINT`：绘图事件。
- `wx.EVT_SIZE`：窗口大小变化事件。

在使用 `wx.Window` 类时，可以通过继承该类来创建自定义窗口，也可以直接使用该类来创建基本窗口。例如，以下是一个使用 `wx.Window` 类创建一个基本窗口的示例代码：

```python
import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        self.panel = wx.Window(self, size=(200, 200))
        self.panel.SetBackgroundColour(wx.RED)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
```

在这个例子中，我们使用 `wx.Window` 类创建了一个大小为 (200, 200) 的红色窗口，并将其添加到了 `wx.Frame` 中。我们还可以使用其他方法和事件来处理这个窗口的鼠标、键盘、绘图和尺寸变化等事件。

# 前景色和背景色

在 GUI 编程中，前景色和背景色通常用于定义窗口和控件的颜色。

前景色指的是控件上的文本、边框和图标等元素的颜色，而背景色则指的是控件本身的颜色。

# wx.Control分析

在 wxPython 中，`wx.Control` 是所有具有用户交互能力的控件的基类，包括按钮、文本框、复选框、单选框等等。

`wx.Control` 类提供了许多常用的方法和事件，可以用于处理鼠标、键盘、尺寸变化等事件。以下是一些常用的方法和事件：

- `wx.Control.GetLabelText()`：获取控件中显示的文本。
- `wx.Control.SetLabelText(label)`：设置控件中显示的文本。
- `wx.Control.Enable(enable=True)`：启用或禁用控件。
- `wx.Control.IsEnabled()`：检查控件是否启用。
- `wx.Control.SetFocus()`：将键盘焦点设置到控件上。
- `wx.Control.GetSize()`：获取控件的大小。
- `wx.Control.GetPosition()`：获取控件的位置。
- `wx.Control.SetSize(size)`：设置控件的大小。
- `wx.Control.SetPosition(pos)`：设置控件的位置。
- `wx.Control.Refresh()`：刷新控件。
- `wx.Control.Show(show=True)`：显示或隐藏控件。

`wx.Control` 类还提供了许多事件，可以用于处理鼠标、键盘和尺寸变化等事件。以下是一些常用的事件：

- `wx.EVT_LEFT_DOWN`：鼠标左键按下事件。
- `wx.EVT_LEFT_UP`：鼠标左键释放事件。
- `wx.EVT_RIGHT_DOWN`：鼠标右键按下事件。
- `wx.EVT_RIGHT_UP`：鼠标右键释放事件。
- `wx.EVT_MOUSEWHEEL`：鼠标滚轮滚动事件。
- `wx.EVT_KEY_DOWN`：键盘按键按下事件。
- `wx.EVT_KEY_UP`：键盘按键释放事件。
- `wx.EVT_SIZE`：控件大小变化事件。

在使用 `wx.Control` 类时，可以通过继承该类来创建自定义控件，也可以直接使用该类来创建基本控件。例如，以下是一个使用 `wx.Control` 类创建一个基本按钮的示例代码：

```python
import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        self.button = wx.Button(self, label='Click Me', pos=(50, 50))

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()
```

在这个例子中，我们使用 `wx.Control` 类创建了一个名为 `button` 的按钮，并将其添加到了 `wx.Frame` 中。我们还可以使用其他方法和事件来处理这个按钮的鼠标、键盘和尺寸变化等事件。

# wxpython自带参数读取和保存

在 wxPython 中，常用的参数读取和保存方式包括使用 `wx.Config` 类和 `wx.FileConfig` 类。

`wx.Config` 类是一个基类，用于实现应用程序的配置信息的读取和保存。它提供了一组简单的接口，可以读取和保存应用程序的配置信息，包括字符串、整数、浮点数、布尔值等数据类型。`wx.Config` 类提供了多种实现方式，包括注册表、INI 文件、XML 文件等，可以根据具体情况选择不同的实现方式。

默认是保存到注册表的。

```
import wx

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        self.config = wx.FileConfig('MyApp', style=wx.CONFIG_USE_LOCAL_FILE)

        self.text_ctrl = wx.TextCtrl(self)
        self.load_button = wx.Button(self, label='Load')
        self.save_button = wx.Button(self, label='Save')

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND|wx.ALL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.load_button, flag=wx.RIGHT, border=10)
        hbox.Add(self.save_button)
        vbox.Add(hbox, flag=wx.ALIGN_RIGHT|wx.ALL, border=10)

        self.SetSizer(vbox)

        self.load_button.Bind(wx.EVT_BUTTON, self.OnLoad)
        self.save_button.Bind(wx.EVT_BUTTON, self.OnSave)

    def OnLoad(self, event):
        text = self.config.Read('text', 'Hello, world!')
        self.text_ctrl.SetValue(text)

    def OnSave(self, event):
        text = self.text_ctrl.GetValue()
        self.config.Write('text', text)
        self.config.Flush()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()

```

上面代码是保存到文件里的。

默认是ini的。路径在：C:\Users\teddy\AppData\Roaming\MyApp.ini

怎么指定为其他类型的文件呢？

我测试了，路径和xml都不能成功指定。

这个用起来还是挺麻烦的。

## 自己用json做参数配置

```
import wx
import json

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')
        self.config_file = 'config.json'

        self.text_ctrl = wx.TextCtrl(self)
        self.load_button = wx.Button(self, label='Load')
        self.save_button = wx.Button(self, label='Save')

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND|wx.ALL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.load_button, flag=wx.RIGHT, border=10)
        hbox.Add(self.save_button)
        vbox.Add(hbox, flag=wx.ALIGN_RIGHT|wx.ALL, border=10)

        self.SetSizer(vbox)

        self.load_button.Bind(wx.EVT_BUTTON, self.OnLoad)
        self.save_button.Bind(wx.EVT_BUTTON, self.OnSave)

    def OnLoad(self, event):
        try:
            with open(self.config_file, 'r') as f:
                config = json.load(f)
        except FileNotFoundError:
            config = {}
        text = config.get('text', 'Hello, world!')
        self.text_ctrl.SetValue(text)

    def OnSave(self, event):
        text = self.text_ctrl.GetValue()
        config = {'text': text}
        with open(self.config_file, 'w') as f:
            json.dump(config, f)

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()

```

# wxpython日志输出到控件

## 方式1

```
import wx
import logging

class LogPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        self.clear_button = wx.Button(self, label='Clear')

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        vbox.Add(self.clear_button, flag=wx.ALIGN_RIGHT|wx.ALL, border=10)

        self.SetSizer(vbox)

        self.clear_button.Bind(wx.EVT_BUTTON, self.OnClear)

        # 创建日志处理器
        self.handler = LogHandler(self.text_ctrl)

        # 创建日志器
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(self.handler)

    def OnClear(self, event):
        self.text_ctrl.Clear()

class LogHandler(logging.Handler):
    def __init__(self, text_ctrl):
        super().__init__()
        self.text_ctrl = text_ctrl

    def emit(self, record):
        msg = self.format(record) + '\n'
        wx.CallAfter(self.text_ctrl.WriteText, msg)

class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title='My Frame')

        self.log_panel = LogPanel(self)
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_PROCESS_ENTER)

        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.log_panel, proportion=1, flag=wx.EXPAND)
        vbox.Add(self.text_ctrl, flag=wx.EXPAND|wx.ALL, border=10)

        self.SetSizer(vbox)

        self.logger = logging.getLogger()
        self.logger.addHandler(self.log_panel.handler)

        self.text_ctrl.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)

    def OnEnter(self, event):
        text = self.text_ctrl.GetValue()
        self.logger.debug(text)
        self.text_ctrl.SetValue('')

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
    app.MainLoop()

```



# 一些链接



https://blog.csdn.net/seniorwizard/article/details/130894657

https://blog.csdn.net/jdzhangxin/article/details/78377619

# 带欢迎界面的应用

下面是一个简单的 wxPython 应用程序示例，带有一个欢迎界面：

```python
import wx

class WelcomeFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Welcome", size=(400, 300))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        welcome_text = wx.StaticText(panel, label="Welcome to My App!", style=wx.ALIGN_CENTER)
        vbox.Add(welcome_text, 1, wx.EXPAND|wx.ALL, 20)
        
        start_button = wx.Button(panel, label="Start")
        start_button.Bind(wx.EVT_BUTTON, self.on_start)
        vbox.Add(start_button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        panel.SetSizer(vbox)
        self.Show(True)
        
    def on_start(self, event):
        # 打开主应用程序窗口
        self.Close()  # 关闭欢迎界面
        main_frame = MainFrame()
        main_frame.Show()

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="My App", size=(400, 300))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        welcome_text = wx.StaticText(panel, label="Welcome to My App!", style=wx.ALIGN_CENTER)
        vbox.Add(welcome_text, 1, wx.EXPAND|wx.ALL, 20)
        
        panel.SetSizer(vbox)
        self.Show(True)

if __name__ == "__main__":
    app = wx.App()
    welcome_frame = WelcomeFrame()
    app.MainLoop()
```

这个示例包含两个窗口，一个欢迎界面窗口 `WelcomeFrame`，和一个主应用程序窗口 `MainFrame`。当用户点击欢迎界面上的 "Start" 按钮时，会关闭欢迎界面窗口并打开主应用程序窗口。

## 在欢迎界面上带一个下拉列表，把下拉列表选择的值传递给MainFrame 

好的，我稍微修改一下代码，在欢迎界面上添加一个下拉列表，并将用户选择的值传递给主应用程序窗口：

```python
import wx

class WelcomeFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Welcome", size=(400, 300))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        welcome_text = wx.StaticText(panel, label="Welcome to My App!", style=wx.ALIGN_CENTER)
        vbox.Add(welcome_text, 1, wx.EXPAND|wx.ALL, 20)
        
        # 添加下拉列表
        choices = ['Option 1', 'Option 2', 'Option 3']
        self.choice = wx.Choice(panel, choices=choices)
        vbox.Add(self.choice, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        start_button = wx.Button(panel, label="Start")
        start_button.Bind(wx.EVT_BUTTON, self.on_start)
        vbox.Add(start_button, 0, wx.ALIGN_CENTER|wx.ALL, 5)
        
        panel.SetSizer(vbox)
        self.Show(True)
        
    def on_start(self, event):
        selected_value = self.choice.GetStringSelection()  # 获取用户选择的值
        self.Close()  # 关闭欢迎界面
        main_frame = MainFrame(selected_value)  # 将选择的值传递给主应用程序窗口
        main_frame.Show()

class MainFrame(wx.Frame):
    def __init__(self, selected_value):
        super().__init__(None, title="My App", size=(400, 300))
        
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        welcome_text = wx.StaticText(panel, label=f"Welcome to My App! You selected: {selected_value}", style=wx.ALIGN_CENTER)
        vbox.Add(welcome_text, 1, wx.EXPAND|wx.ALL, 20)
        
        panel.SetSizer(vbox)
        self.Show(True)

if __name__ == "__main__":
    app = wx.App()
    welcome_frame = WelcomeFrame()
    app.MainLoop()
```

在这个修改后的示例中，我添加了一个名为 `choice` 的下拉列表控件，并在欢迎界面窗口的 `on_start` 方法中获取用户选择的值，并将其作为参数传递给主应用程序窗口 `MainFrame` 的初始化方法。然后，在主应用程序窗口中显示欢迎文本时，将用户选择的值显示出来。

# 参考资料

https://blog.csdn.net/qq_37534835/article/details/90715871