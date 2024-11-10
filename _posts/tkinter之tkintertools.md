---
title: tkinter之tkintertools
date: 2024-11-09 16:02:33
tags:
	- tkinter

---

--

# 简介

代码：https://github.com/Xiaokang2022/tkintertools

从介绍看，作者还是一个学生。实力真的强大。

这个写得不错。值得研究一下。

项目主页：https://xiaokang2022.github.io/tkintertools/

安装：

```
pip install tkintertools
```

安装开发版本

```
pip install tkintertools[recommended]==3.0.0rc3
```

demo仓库：

https://github.com/Xiaokang2022/tkintertools-demos

运行测试方法，把demo仓库clone下来。

然后安装依赖：

```
pip install -r requirements.txt
```

然后运行demo：

```
python demos/demo0/main.py
```

这样才能保证正确找到资源文件的位置。

## 限制

需要Python3.10版本以上才行。

主要是因为使用了3.10才引入的match关键字。



# 这个库的主要功能是什么？

`tkintertools` 库主要用于扩展和增强 Python 的 `tkinter` GUI 开发功能。其主要功能包括：

1. **自定义控件**：提供一些额外的控件和小部件，简化界面的设计和开发。
  
2. **布局管理**：改进布局管理，使得在 GUI 中放置和调整控件更加灵活和高效。

3. **样式和主题**：支持主题和样式的定制，帮助开发者创建更美观的界面。

4. **工具集成**：集成一些常用的工具和功能，减少重复代码，提高开发效率。

5. **示例和文档**：提供丰富的示例和文档，帮助用户快速上手和理解库的使用。

# 这个库的原理是什么

`tkintertools` 库的原理主要基于以下几个方面：

1. **封装和扩展**：库通过封装 `tkinter` 的基本控件，提供了更高级别的接口和功能。这使得开发者可以更容易地创建复杂的 GUI，而不需要深入了解 `tkinter` 的底层实现。

2. **继承和组合**：很多自定义控件是通过继承 `tkinter` 的基本控件（如 `Button`、`Label` 等）实现的。开发者可以在这些基础控件上增加新特性或修改行为，以满足特定需求。

3. **布局管理器**：库可能提供了一些自定义的布局管理器，旨在简化控件的排列和调整，使得界面在不同屏幕尺寸上表现良好。

4. **事件驱动模型**：像 `tkinter` 一样，`tkintertools` 也使用事件驱动模型，通过绑定事件和回调函数来处理用户交互，从而实现动态更新和响应。

5. **主题和样式管理**：库可能实现了主题和样式管理的机制，允许开发者轻松应用不同的外观和感觉，这通常是通过 CSS 类似的样式系统实现的。

这些原理结合在一起，使得 `tkintertools` 能够提供更丰富、更灵活的 GUI 开发体验。



导出符号的思路

下面有7个目录：

* animation。里面就2个py文件。
  * animations.py（提供了7个类）和
  * controllers.py（提供了4个工具函数）
* color。3个py文件：
  * colormap.py（一个工具函数，实现颜色rgb值和name的映射）、
  * hsl.py（一种颜色空间）、
  * rgb.py（8个工具函数）。
* core。3个py文件：
  * configs.py（4个类[Env、Font、Theme、Constant]和1个工具函数）、
  * containers.py（这个表示空间顶层容器，4个类，Tk、TopLevel、Canvas、Frame）、
  * virtual.py（6个类，Component、Shape、Text、Feature、Widget，是抽象的widget）。
* standard。这个就是对core的virtual控件的实现。6个py文件。
  * dialogs.py。3个类
    * TkMessage
    * TkColorChooser。
    * TkFontChooser。
  * features.py。12个类，大部分都是XXFeature这种命名。
    * LabelFeature。
    * ButtonFeature。
    * Underline。
    * HighLight。
    * SwitchFeature。
    * ToggleFeature。
    * CheckButtonFeature。
    * RadioButtonFeature。
    * ProgressBarFeature。
    * InputBoxFeature。
    * SliderFeature。
    * SpinBoxFeature。
  * images.py。就一个类。
    * StillImage。
  * shapes.py。9个类。
    * Line。
    * Rectangle。
    * Oval。椭圆。
    * RegularPolygon。常规多边形。
    * RoundedRectangle。圆角矩形。
    * HalfRoundedRectangle。
    * SemicircularRectangle。
    * SharpRectangle。
    * Parallelogram。平行四边形。
  * texts.py。2个类。
    * Information。
    * SingleLineText。
  * widgets.py。17个类。
    * Text。
    * Image。
    * Label。
    * Button。
    * Switch。
    * InputBox。
    * ToggleButton。
    * CheckButton。
    * RadioButton。
    * ProgressBar。
    * UnderlineButton。
    * HighLightButton。
    * IconButton。
    * Slider。
    * SegmentedButton。分段按钮。就网页上经常见到的那种一组按钮的形式。
    * SpinBox。
    * Tooltip。
* style。2个py文件。用来管理theme文件夹。
  * manager.py。
  * parser.py。
* theme。2个文件。
  * dark.py。
  * light.py。
* toolbox。2个py文件。
  * enhanced.py。里面就一个类。
    * PhotoImage。
  * tools.py。里面是工具函数。

对外只从animation、core、toolbox.enhanced这3个包导出符号。

其余的包，会被其他的包通过`..color`这样的相对引入方式进行内部导入使用。

# windows的high DPI检测

```
if sys.platform == "win32":
    import ctypes
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Set Windows DPI awareness
```

设置 DPI 感知对于在高分辨率显示器上运行的应用程序至关重要。

没有正确设置，应用程序可能会显示模糊或界面元素的尺寸不合适，影响用户体验。

通过启用 DPI 感知，应用程序可以根据屏幕的 DPI 动态调整其布局和控件大小，从而提供更好的视觉效果。

# 缩写

tkintertools，缩写为tkt。

# 优点

类型注解写得非常完整。代码读起来很方便。

就像在看强类型语言的感觉。



# 重要代码分析

## **Tk**(**tkinter**.**Tk**)

这个是顶层窗口的相关配置。

默认窗口大小是1280x720的。

默认位置是随机的。

持有一个`list[Canvas]`

## Canvas(tkinter.Canvas)

所有tkt控件的parent都是Canvas。



# 风格名词说明

这些都是windows上的风格描述。

```
"mica", "acrylic", "aero", "transparent",
"optimised", "win7", "inverse", "native",
"popup", "dark", “normal" 
```

这些风格名词通常与用户界面的视觉效果和主题相关，尤其是在 Windows 操作系统或某些 GUI 库中。以下是对每个风格名词的简要说明：

1. **Mica**：
   - 一种半透明的效果，常用于 Windows 11 中，提供了一种模糊背景的外观，使得窗口与桌面背景融合，增加视觉层次感。

2. **Acrylic**：
   - 这种效果让窗口背景模糊并带有轻微的颜色，常用于现代 Windows 应用程序。它提供了半透明的外观，使得内容与背景相互渗透。

3. **Aero**：
   - Windows Vista 和 Windows 7 中的视觉风格，提供透明和模糊效果，使窗口看起来更现代。Aero 设计强调了光影效果，给用户更流畅的体验。

4. **Transparent**：
   - 窗口或控件完全透明，允许底层内容可见。通常用于特殊效果或自定义界面。

5. **Optimised**：
   - 可能指的是经过优化的界面风格，旨在提高性能或用户体验。具体含义可能依赖于上下文。

6. **Win7**：
   - 指 Windows 7 操作系统的视觉风格，通常与 Aero 相关，强调透明效果和光滑的界面设计。

7. **Inverse**：
   - 这种风格可能指与常规色彩反转的视觉效果。例如，白色文字在黑色背景上显示，通常用于暗模式或高对比度主题。

8. **Native**：
   - 指应用程序遵循操作系统的原生视觉风格，使得应用与系统界面无缝集成，保持一致性。

9. **Popup**：
   - 通常指弹出窗口或对话框的样式，强调临时显示的界面元素，可能具有不同的视觉效果以引起用户注意。

10. **Dark**：
    - 指暗色主题，通常使用深色背景和浅色文字，以减轻眼睛疲劳并在低光环境中提高可读性。

11. **Normal**：
    - 可能指标准的或默认的视觉风格，没有特殊效果或自定义设置，通常是应用程序的基本外观。

### 总结

这些风格名词涉及用户界面的设计和视觉效果，通常用于描述应用程序的外观和感觉，尤其是在 Windows 系统中。选择合适的风格可以显著增强用户体验。如果有任何具体风格的实现或使用问题，欢迎继续询问！

# 魔方项目

https://github.com/Xiaokang2022/Intelligent-Magic-Cube