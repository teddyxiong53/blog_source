---
title: qt之Ubuntu下开发环境搭建
date: 2021-06-08 15:59:11
tags:
	- qt

---

--

先从这里下载

http://download.qt.io/archive/qt/

我选择5.15.2版本。

算了。还是选择这个版本。因为这个有打包好的版本。

https://download.qt.io/archive/qt/5.12/5.12.11/

 qt-opensource-linux-x64-5.12.11.run

选择这个进行下载。

有1.3G。挂着梯子下载。选择美国节点速度会比较快。

下载完之后，执行这个文件进行安装就好了。

是图形界面的安装。

需要用sudo权限来执行，不然是提示网络不通（真是令人迷惑）

需要登陆，我就用1073167306@qq.com这个账号来登陆，密码是要复杂的那种。

把所有的组件都勾选上。默认就带了QtCreator了。

默认是安装到/opt/Qt5.12.11目录下。



Qt编译出现 :-1 error: cannot find -lGL 问题，未安装 opengl 依赖库：

```shell
sudo apt-get install libgl1-mesa-dev
```



把这个项目自己写一遍。来掌握基本的开发过程。

https://github.com/NautiluX/slide

使用QtCreator来开发。

有疑问的一个点：怎么实现播放时全屏的？

SizePolicy：

前面提到过，表示窗口的行为方式

用于描述一个窗口（Widget）被调整大小（resizing）时，采用的策略。

在QSizePolicy类中定义了七种策略：

Fixed:使用sizeHint,不能更大，不能更小

Minimum:不能小于sizeHint，可以更大，但不需要更大

Maximum:不得大于sizeHint,可以更小

Preferred:优先使用sizeHint，可大可小

Expanding:使用sizeHint，越大越好

MinimumExpanding:不得小于sizeHint，越大越好

Ignored:忽略sizeHint，越大越好

当前slide是这样配置的。

```
<property name="sizePolicy">
   <sizepolicy hsizetype="Maximum" vsizetype="Maximum">
    <horstretch>0</horstretch>
    <verstretch>0</verstretch>
   </sizepolicy>
  </property>
```



参考资料

1、

https://segmentfault.com/a/1190000037588941