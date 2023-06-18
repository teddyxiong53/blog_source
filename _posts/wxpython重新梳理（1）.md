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



# 一些链接



https://blog.csdn.net/seniorwizard/article/details/130894657

https://blog.csdn.net/jdzhangxin/article/details/78377619

# 参考资料

https://blog.csdn.net/qq_37534835/article/details/90715871