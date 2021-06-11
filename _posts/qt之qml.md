---
title: qt之qml
date: 2021-06-08 15:36:11
tags:
	- qt

---

--

QML是一种描述性的脚本语言，文件格式以.qml结尾。

语法格式非常像CSS（参考后文具体例子），

但又支持javascript形式的编程控制。

QtDesigner可以设计出·ui界面文件，

但是不支持和Qt原生C++代码的交互。

QtScript可以和Qt原生代码进行交互，

但是有一个缺点，

如果要在脚本中创建一个继承于QObject的图形对象非常不方便，

只能在Qt代码中创建图形对象，然后从QtScript中进行访问。



**而QML可以在脚本里创建图形对象，并且支持各种图形特效，以及状态机等，**

**同时又能跟Qt写的C++代码进行方便的交互，使用起来非常方便。**



QML是Qt推出的Qt Quick技术的一部分，是一种新增的简便易学的语言。

QML是一种陈述性语言，用来描述一个程序的用户界面：

无论是什么样子，以及它如何表现。

**在QML，一个用户界面被指定为具有属性的对象树。**

 这使得Qt更加便于很少或没有编程经验的人使用。



QML实际上是Qt Quick （Qt4.7.0中的新特性）核心组件之一：

Qt Quick是一组旨在帮助开发者创建在移动电话，媒体播放器，机顶盒和其他便携设备上使用越来越多的直观、现代、流畅UI的工具集合。



为了适应手机移动应用开发， Qt5 将 QML 脚本编程提到与传统 C++ 部件编程相同的高度，

力推 QML 界面编程，

当然 QML 主要用于手机移动应用程序。 

QML 包含大量使用手机移动设备的功能模块，

比如基本部件（QtQuick 模块）、GPS 定位、渲染特效、蓝牙、NFC、WebkKit 等等。



在Ubuntu下搭建好开发环境。开始看看怎么用qml来做一个demo程序。

是新建工程的时候，选择Qt quick Application。

创建可部署的 Qt Quick 2 应用程序。

Qt Quick 是 Qt 支持的一套 GUI 开发架构，其界面设计采用 QML 语言，程序架构采用 C++ 语言。

利用 Qt Quick 可以设计非常炫的用户界面，一般用于移动设备或嵌入式设备上**无边框的应用程序的设计。**

Qt Quick Controls 2 Application，创建基于 Qt Quick Controls 2 组件的可部署的 Qt Quick 2 应用程序。Qt Quick Controls 2 组件只有 Qt 5.7 及以后版本才有。



QML 是一种多范式语言，

使对象   能够根据其属性  以及  如何关联和响应其他对象的更改  来   定义对象。

与纯粹的命令式代码相反，

属性和行为的变化通过一系列逐步处理的语句表达。

QML 的声明性语法将属性和行为更改直接集成到单个对象的定义中，

这些属性定义可以包含必要的代码，在情况复杂的自定义应用程序行为是必要的。



QML 源代码通常由引擎通过 QML 文档加载，

QML 文档是 QML 代码的独立文档。

**这些可以用于定义 QML 对象类型，然后可以在整个应用程序中重复使用。**

QML 文档可以在文件的顶部包含一个或多个 import 语句。一个 import 可以是以下任何一种：

- 一个已经注册了类型的版本化命名空间（例如：通过插件）
- 一个包含 QML 文档类型定义的相对目录
- 一个 JavaScript 文件

```
各种 import 的通用形式如下：

import Namespace VersionMajor.VersionMinor
import Namespace VersionMajor.VersionMinor as SingletonTypeIdentifier
import "directory"
import "file.js" as ScriptIdentifier
例如：

import QtQuick 2.0
import QtQuick.LocalStorage 2.0 as Database
import "../privateComponents"
import "somefile.js" as Script

```



对象声明
在语法上，一个 QML **代码块**定义了一个要被创建的 QML **对象树**。

使用对象声明来定义对象，

对象声明描述了要创建对象的**类型**以及要给予对象的**属性**。

每个对象也可以使用**嵌套**对象声明来声明**子对象**。

一个对象声明包含：

对象类型的名称（例如：Rectangle ）
一组花括号{ }： 紧随其（对象类型的名称）后
属性（例如：width）和子对象（例如：Text）：在花括号中声明
来看一个简单的对象声明：

Rectangle {
    width: 300
    height: 200
    color: "green"
}
这声明了一个类型为 Rectangle 的对象（**Rectangle 类型由 QtQuick 模块提供**），

后跟一组包含为该对象定义属性的花括号，定义的属性是矩形的 width （宽度）、height（高度）和 color（颜色）。



使用qml要加上这2个模块。

```
QT += qml quick
```



首先，分清QML与qtquick， 

QML是一种格式类似css、混杂javaScript的“语言”，是一种工具，它属于qtquick。

qtquick是一些“工具集”。



这段代码开头引入了模块QtQuick 2.0 (模块名与版本号)，这个模块主要用于描述界面（使用元素组合成可视界面）

使用了Rectangle与Image两个QtQuick 模块中的元素，Image内嵌在Rectangle中，Rectangle是最顶层的，所以这个程序运行后，长与宽与这个Rectangle的长宽相同，都是200px。

qml语言也有继承关系，但关系都不复杂，以上两个元素都继承自Item元素。



QML的Window与ApplicationWindow

ApplicationWindow需要导入QtQuick.Controls 

Window需要导入QtQuick.Window 。 

默认不可见，需要设置visible:true才可见。 

主要区别就是ApplicationWindow提供了简单的方式创建程序窗口，因为其有属性menuBar、toolBar、Tabview等属性，可以方便快速创建一个丰富的窗口。



参考资料

1、QML

https://baike.baidu.com/item/QML/153014

2、学习QML还是C++？

http://c.biancheng.net/view/3877.html

3、QML 语法基础

https://blog.csdn.net/liang19890820/article/details/54376860

4、qt quick文档

https://doc.qt.io/qt-5/qtquick-index.html

5、Qt模块化笔记之Qt_Quick——引入

https://blog.csdn.net/iloveqt5/article/details/17150637

6、QML的Window与ApplicationWindow

https://www.cnblogs.com/judes/p/9438084.html