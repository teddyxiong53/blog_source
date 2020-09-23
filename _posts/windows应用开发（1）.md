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

# 常见数据类型

WORD：                16位无符号整形数据
　　DWORD：             32位无符号整型数据（DWORD32）
　　DWORD64：         64位无符号整型数据
　　INT：                       32位有符号整型数据类型
　　INT_PTR：             指向INT数据类型的指针类型
　　INT32：                  32位符号整型
　　INT64：                  64位符号整型
　　UINT：                    无符号INT
　　LONG：                 32位符号整型（LONG32）
　　ULONG：              无符号LONG
　　LONGLONG：      64位符号整型（LONG64）
　　SHORT：              无符号短整型（16位）
　　LPARAM：           消息的L参数
　　WPARAM：         消息的W参数
　　**HANDLE：**           **对象的句柄，最基本的句柄类型**　　HICON：               图标的句柄
　　HINSTANCE：    程序实例的句柄
　　HKEY：                注册表键的句柄
　　HMODULE：       模块的句柄
　　**HWND：              窗口的句柄**
　　LPSTR：              字符指针，也就是字符串变量
　　LPCSTR：           字符串常量
　　LPCTSTR：         根据环境配置，如果定义了UNICODE宏，则是LPC**W**STR类型，否则则为LPCSTR类型
　　LPCWSTR：       UNICODE字符串常量
　　LPDWORD：      指向DWORD类型数据的指针
　　CHAR：               8比特字节
　　TCHAR：             如果定义了UNICODE，则为WCHAR，否则为CHAR
　　UCHAR：            无符号CHAR
　　WCHAR：           16位Unicode字符
　　BOOL：                布尔型变量
　　BYTE：                 字节类型（8位）
　　CONST：             常量
　　FLOAT：              浮点数据类型
　　SIZE_T：              表示内存大小，以字节为单位，其最大值是CPU最大寻址范围
　　VOID：                 无类型，相当于标准C语言中的void
　　WINAPI：             Windows API的函数调用方式，常见于SDK头文件中对API函数的声明中，相当于_stdcall（更严格地说，这不是数据类型，而是一种函数调用约定



# Windows参数简写

 

1、  b 布尔

2、 by BYTE

3、 c chr 或WCHAR TCHAR

4、 n short

5、 i int

6、 x、y 分别表示x 坐标，y 坐标

7、 cx、cy 分别表示x 方向长度和y 方向长度

8、 b 或f BOOL(int),f 代表“flag”

9、 w WORD(无符号short)

10、l LONG 长整数

11、dw DWORD 无符号长整数

12、fn function 函数

13、s string 字符串

14、sz 以0 字节结尾的字符串

15、h 句柄

16、p 指针

17、lpfn 指向函数的长指针

18、cb 字节数

19、lpsz 指向以0 结尾的字符串的长指针

**20、g_ 全局变量**

**21、c_ 常量**

**22、m_ 类数据成员**

**23、s_ 静态变量**

24、CS_ 类风格选项

25、CW_ 创建窗口选项

26、DT_ 绘制文本选项

27、IDI_ 图标ID 号 
28、IDC_ 光标ID 号

29、MB_ 消息框选项

30、SND_ 声音选项

31、WM_ 窗口消息

32、WS_ 窗口风格

33、rc 矩形





参考资料

1、【Windows核心编程】Windows常见数据类型

https://blog.csdn.net/tianshuai1111/article/details/8163115

2、



