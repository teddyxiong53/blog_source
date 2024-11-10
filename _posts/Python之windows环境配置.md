---
title: Python之windows环境配置
date: 2018-06-28 19:16:34
tags:
	- Python

---



为了逼迫自己向Python3转，我现在在windows上安装了Python3的版本。

把默认的Python配置配置为Python3的。

修改PATH的路径就好了。

这样验证就好了。

```
C:\Users\Administrator
λ python
Python 3.7.0 (v3.7.0:1bf9cc5093, Jun 27 2018, 04:06:47) [MSC v.1914 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

我现在学习爬虫的。

```
pip install beautifulsoup4
```

这个安装没有问题。因为按照Python3.7的，默认就勾选了pip工具了。



# windows下多个Python环境共存配置

1、在环境变量里加入2个的。

```
C:\python27;C:\Python27\Scripts;C:\python37;C:\Python37\Scripts;
```

2、当前之所以不能共存，是因为有同名的可执行文件。

主要是pip和Python这2个exe文件。

我都拷贝一个为pip2和python2这样的名字文件。



用脚本来做。思路就是改文件名。

# windll用法

`ctypes.windll` 是 Python 的 `ctypes` 库的一部分，专门用于加载和调用 Windows 动态链接库（DLL）。具体来说，`windll` 允许你使用 Windows API 和其他本地 DLL 函数。以下是一些关键点和常用的 DLL 及其功能：

### 1. **基本概念**

- **动态链接库（DLL）**：是一种包含可被多个程序共享的代码和数据的文件。Windows 提供了许多系统 DLL，用于实现各种功能。
- **`ctypes` 库**：是 Python 的一个标准库，允许你调用 C 语言编写的函数和使用 C 结构体等。

### 2. **常用的 `windll` DLL**

以下是一些常用的 DLL 和它们的功能：

#### 1. **`user32.dll`**
   - 提供与用户界面相关的功能，如窗口管理、消息处理、用户输入等。
   - 常用函数：
     - `MessageBox`: 显示一个消息框。
     - `GetSystemMetrics`: 获取系统的度量信息（如屏幕尺寸）。
     - `SystemParametersInfo`: 获取或设置系统参数（如桌面壁纸）。

#### 2. **`kernel32.dll`**
   - 提供操作系统核心功能，包括文件管理、内存管理和进程控制。
   - 常用函数：
     - `GetLastError`: 获取最后一个错误代码。
     - `CreateFile`: 创建或打开文件。
     - `CloseHandle`: 关闭一个打开的句柄。

#### 3. **`gdi32.dll`**
   - 提供图形设备接口（GDI）功能，用于绘制图形和处理图形输出。
   - 常用函数：
     - `CreatePen`: 创建一个画笔。
     - `BitBlt`: 从一个设备上下文（DC）复制位图到另一个 DC。

#### 4. **`advapi32.dll`**
   - 提供高级 Windows API 功能，包括安全性和注册表访问。
   - 常用函数：
     - `RegOpenKeyEx`: 打开注册表项。
     - `OpenEventLog`: 打开事件日志。

#### 5. **`shell32.dll`**
   - 提供与Windows Shell相关的功能，如文件管理和用户界面操作。
   - 常用函数：
     - `ShellExecute`: 执行一个程序或打开一个文件。

### 3. **如何使用 `windll`**

使用 `windll` 加载 DLL 和调用其中的函数非常简单。以下是一个示例：

```python
import ctypes

# 加载 user32.dll
user32 = ctypes.windll.user32

# 调用 MessageBox 函数
user32.MessageBoxW(0, "Hello, World!", "Test", 1)
```

### 4. **注意事项**

- **调用约定**：大多数 Windows API 使用 `stdcall` 调用约定，因此使用 `windll` 是合适的。如果使用 `cdecl`，则应使用 `ctypes.cdll`。
- **参数类型**：在调用 DLL 函数时，确保正确设置参数类型和返回值类型，以避免错误。

### 总结

`ctypes.windll` 提供了一种强大的方式，使 Python 可以直接调用 Windows API 和其他 DLL 函数。通过使用这些函数，开发者可以实现许多与操作系统交互的功能。如果你对某个特定 DLL 或函数有更多问题，欢迎继续询问！

# windll对象

https://www.cnblogs.com/zhchoutai/p/7403151.html

[`ctypes`](https://docs.python.org/zh-cn/3/library/ctypes.html#module-ctypes) 导出了 *cdll* 对象，在 Windows 系统中还导出了 *windll* 和 *oledll* 对象用于载入动态连接库。



# 参考资料

1、windows下通过cmd切换python2和python3版本

https://blog.csdn.net/fxjzzyo/article/details/77070868