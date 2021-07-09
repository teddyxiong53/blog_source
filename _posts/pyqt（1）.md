---
title: pyqt（1）
date: 2021-07-08 17:36:33
tags:
	- qt

---

--

现在要较多地使用qt。为了让自己对qt有更多直观的认识。

我决定把自己写小工具的工具从wxpython改成pyqt。

# pyqt和wxpython对比

PyQt也是使用C++编写的，它基于著名的Qt工具包。

与wxPython不同的是，它不使用native widget，

而是根据它检测到操作系统创建小部件的近似值。

但是它的近似可以说是做到了极致，就连艺术生基本都分辨不出其与原生有何不同。

如果您使用KDE，可以使用其他PyKDE库来弥补原始PyQt与Linux和BSD之间Plasma desktop外观之间的差距，但这增加了新的依赖关系。

PyQt正在努力的消除跨平台差异，允许Python本身需要的常见调整。

PyQt可以避免大多数跨平台问题，所以在不同的操作系统中，GUI代码基本都可以保持不变。

在wxPython中，用户可能就需要根据编程内容对不同平台中的GUI代码做一些调整。

例如，为了防止Microsoft Windows上的某些元素闪烁，USE_BUFFERED_DC属性必须设置为True才能对图形进行双缓冲。

这不是默认的，即使可以无条件地对所有平台进行操作，因此在某些用例中可能存在缺陷。



WxPython具有很多很好的功能，但它在灵活性和用户控制方面不能和PyQt相提并论，

PyQt更易于开发人员设计和布局，

在开发Qt之前，要先花费一些时间从用户获取跟踪自定义布局的方法，

或者如何找到意外关闭的丢失面板等等。

而对于wxPython来说，想要重新打开因意外关闭的面板则是件困难的事情。



# 安装

```
sudo apt install python3-pip 
sudo python3 -m pip install --upgrade pip
sudo pip3 install pyqt5==5.12.0

sudo apt install pyqt5* #安装pyqt5的依赖项
sudo apt install qt5-default qttools5-dev-tools # 安装qtdesigner
```

我的基本环境是：

windows上安装vscode。

ubuntu下安装qt的环境。

vscode ssh方式连接到ubuntu来进行代码编写。

vscode remote安装pyqt的插件。



# HelloWorld

1、ubuntu下命令行输入：designer。这个是打开qt-designer工具。然后创建一个mainwindow，拖一个按钮进去。然后保存成test.ui。

2、vscode里，在test.ui上右键，选择compile，这样就把test.ui编译，生成了Ui_test.py文件。这个就是界面文件。

3、新建一个test.py文件。内容如下：

```
import sys
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from Ui_test import Ui_MainWindow
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(mw)
    mw.show()
    sys.exit(app.exec_())
```

然后运行：python3 test.py，就可以看到运行效果了。



# 参考资料

1、

https://iowiki.com/pyqt/pyqt_quick_guide.html

2、多角度对比PythonGUI库:wxPython和PyQt

http://tech.it168.com/a2017/0407/3114/000003114629.shtml?2

3、Ubuntu18.04安装pyQt5

https://zhuanlan.zhihu.com/p/137571552