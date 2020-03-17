---
title: windows应用开发（1）
date: 2020-03-17 10:38:11
tags:
	- windows
---

1



windows vs里可以写东西：

调用Windows api的C程序。

调用Windows  api的C++程序。

win32程序。这个有窗口。

MFC程序。这个就是托控件的。



默认是Windows的全局明明控件，所以前面要加2个冒号。

下面那个不带冒号的，是本类继承实现的版本，简化了参数。

还有一个afx开头的版本。





所有的Windows api，都在dll库里。

kernel32.dll 900个左右函数。

user32.dll 700个左右函数。



MessageBoxW，最后这个W，表示是wchar版本。

wchar类型的字符串这样来定义：

```
LPCWSTR msgText = L"hello";
```

MessageBoxW的hWnd给NULL的话，表示属于桌面的。而不是当前窗口。这样是不好的。

我们就把当前窗口的句柄做成全局变量。然后给这个函数用就好了。





参考资料

1、





