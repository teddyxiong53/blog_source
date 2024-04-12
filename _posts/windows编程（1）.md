---
title: windows编程（1）
date: 2024-04-07 15:37:17
tags:
	- Linux

---

--

# win32 api简介

Win32 API（Windows API）是微软Windows操作系统的应用程序编程接口（API）。它提供了一组功能丰富的函数、结构和常量，用于开发Windows平台上的应用程序。Win32 API允许开发者与操作系统进行交互，控制窗口、处理消息、管理文件、调用系统服务等。

以下是Win32 API的一些主要特点和组成部分：

1. **窗口和消息处理**：Win32 API提供了创建和管理窗口的功能，开发者可以使用这些功能创建用户界面，处理鼠标和键盘输入，并响应系统消息。

2. **图形设备接口（GDI）**：GDI提供了绘制图形和处理图形设备的功能。开发者可以使用GDI来绘制图形、文本和图像，并控制打印和显示设备。

3. **文件和I/O操作**：Win32 API包含了文件和I/O操作的功能，开发者可以使用这些功能来读取和写入文件、管理文件和目录，并进行串行和并行通信。

4. **线程和进程管理**：Win32 API提供了创建和管理线程和进程的功能。开发者可以使用这些功能来实现多线程应用程序，控制进程的执行和资源分配。

5. **系统服务和注册表操作**：Win32 API包含了许多系统服务和注册表操作的功能，开发者可以使用这些功能来管理系统设置、访问硬件设备，并与系统进行通信。

Win32 API是使用C语言编写的，因此可以与几乎所有支持C语言的编程语言进行集成，如C++、C#、VB.NET等。虽然Win32 API是功能强大的，但也较为底层，因此在使用时需要处理更多的细节和复杂性。近年来，随着.NET框架和其他高级开发工具的发展，使用Win32 API的情况已经减少，但它仍然是理解Windows系统内部工作原理和进行系统级编程的重要基础。

## win32 api的基本数据类型

Win32 API中有一些基本的数据类型，这些类型在使用API函数时经常会遇到。以下是一些常见的基本数据类型：

1. **BOOL**: 代表布尔值，可以是TRUE或FALSE。

2. **BYTE**: 一个字节（8位），范围为0到255。

3. **CHAR**: 一个字符，通常是ASCII编码的字符，范围为-128到127。

4. **WORD**: 一个字（16位），范围为0到65535。

5. **DWORD**: 双字（32位），范围为0到4294967295。

6. **HANDLE**: 句柄，用于引用资源，如文件、窗口等。

7. **HWND**: 窗口句柄，用于引用窗口。

8. **HINSTANCE**: 实例句柄，用于引用应用程序的实例。

9. **HMODULE**: 模块句柄，用于引用动态链接库（DLL）或可执行文件。

10. **LPSTR**: 指向字符（字符串）的指针。

11. **LPCSTR**: 指向常量字符（字符串）的指针。

12. **LPWSTR**: 指向宽字符（Unicode字符串）的指针。

13. **LPCWSTR**: 指向常量宽字符（Unicode字符串）的指针。

14. **LPARAM**: 参数，通常用于传递额外的数据给窗口过程函数。

这些基本数据类型在Win32 API中被广泛使用，开发者在编写Windows应用程序时会频繁地与它们打交道。

## win32 api的命名规范

Win32 API的命名规范遵循一定的规则，这些规则旨在提高代码的可读性和一致性。以下是一些常见的Win32 API命名规范：

1. **函数名**：
   - 函数名通常使用小写字母，并以驼峰式命名法命名，例如：`CreateWindow`, `MessageBox`.
   - 一般情况下，函数名以操作的动词开头，例如：`Create`, `Destroy`, `Get`, `Set`等。

2. **数据类型名**：
   - 数据类型名通常使用大写字母开头的驼峰式命名法，例如：`HWND`, `DWORD`, `LPCSTR`.
   - 有时数据类型名可能包含前缀，以便指示类型的用途，例如：`LP`表示长指针（long pointer）。

3. **宏定义和常量名**：
   - 宏定义和常量名通常使用大写字母，并用下划线分隔单词，例如：`WM_CLOSE`, `SW_HIDE`.
   - 宏定义的命名通常采用全大写，以区分于变量名。

4. **结构体和枚举类型名**：
   - 结构体和枚举类型名通常使用大写字母开头的驼峰式命名法，例如：`RECT`, `POINT`, `COLORREF`.

5. **参数名**：
   - 参数名通常使用小写字母，并以驼峰式命名法命名，例如：`lpClassName`, `dwStyle`.
   - 参数名应具有描述性，以便于理解该参数的含义。

6. **回调函数名**：
   - 回调函数名通常以回调的用途或操作开头，后跟"Proc"或"Callback"，例如：`WndProc`, `EnumWindowsProc`.

这些命名规范有助于使Win32 API的代码具有一致性和可读性，并且可以更轻松地理解和维护。在编写Win32 API的应用程序时，遵循这些命名规范是一个良好的实践。

## win32 api常用函数

Win32 API拥有大量的函数，涵盖了操作系统的各个方面，从创建窗口到文件操作、内存管理等等。以下列举了一些常用的Win32 API函数，它们在Windows应用程序的开发中经常被使用：

1. **创建和管理窗口**：
   - CreateWindowEx: 创建带有扩展风格的窗口。
   - ShowWindow: 显示或隐藏窗口。
   - UpdateWindow: 更新指定窗口的客户区。
   - DestroyWindow: 销毁指定的窗口。

2. **消息处理**：
   - GetMessage: 从消息队列中获取消息。
   - TranslateMessage: 翻译消息。
   - DispatchMessage: 分发消息给窗口过程函数。
   - PostQuitMessage: 向消息队列插入退出消息，以退出消息循环。

3. **图形设备接口（GDI）**：
   - CreateDC: 创建设备上下文。
   - SelectObject: 选择对象到设备上下文。
   - BitBlt: 在设备上下文之间执行位块传输操作。
   - StretchBlt: 在设备上下文之间执行拉伸位块传输操作。

4. **文件和I/O操作**：
   - CreateFile: 创建或打开文件。
   - ReadFile: 从文件中读取数据。
   - WriteFile: 向文件中写入数据。
   - CloseHandle: 关闭文件句柄或其他内核对象的句柄。

5. **进程和线程管理**：
   - CreateProcess: 创建一个新的进程和其主线程。
   - CreateThread: 创建一个新的线程。
   - TerminateProcess: 终止指定的进程。
   - WaitForSingleObject: 等待线程或进程的内核对象变为有信号状态。

6. **系统信息和设置**：
   - GetSystemMetrics: 获取系统度量信息，如屏幕尺寸、字体大小等。
   - GetSystemTime: 获取系统时间。
   - SetSystemTime: 设置系统时间。
   - GetVersion: 获取操作系统的版本信息。

7. **其他常用函数**：
   - MessageBox: 显示一个消息框。
   - Sleep: 使当前线程挂起指定的时间。
   - GetModuleHandle: 获取当前进程中已加载模块的句柄。
   - LoadLibrary: 加载一个动态链接库（DLL）。

这只是Win32 API中的一小部分常用函数，它们涵盖了Windows应用程序开发中的一些关键方面。在实际开发中，您可能会遇到更多的函数，具体取决于您的应用程序的需求和功能。

## win32 api helloworld

以下是一个简单的Win32 API HelloWorld 程序示例，它创建一个窗口并显示 "Hello, World!" 文本：

```c
#include <windows.h>

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    // 定义窗口类
    WNDCLASS wc = {0};
    wc.lpfnWndProc = WindowProc; // 指定窗口过程函数
    wc.hInstance = hInstance;
    wc.lpszClassName = L"HelloWindowClass";

    // 注册窗口类
    RegisterClass(&wc);

    // 创建窗口
    HWND hwnd = CreateWindowEx(0, L"HelloWindowClass", L"Hello, World!", WS_OVERLAPPEDWINDOW, 
        CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, NULL, NULL, hInstance, NULL);

    // 显示窗口
    ShowWindow(hwnd, nCmdShow);

    // 消息循环
    MSG msg = {0};
    while(GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    return 0;
}

LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch(uMsg) {
        case WM_DESTROY:
            PostQuitMessage(0);
            return 0;
        case WM_PAINT: {
            PAINTSTRUCT ps;
            HDC hdc = BeginPaint(hwnd, &ps);
            TextOut(hdc, 10, 10, L"Hello, World!", 13);
            EndPaint(hwnd, &ps);
            return 0;
        }
    }
    return DefWindowProc(hwnd, uMsg, wParam, lParam);
}
```

这个程序首先定义了一个窗口类 `WNDCLASS`，然后注册这个窗口类并创建一个窗口。在窗口过程函数 `WindowProc` 中，处理了窗口的消息，包括绘制窗口内容和处理窗口关闭消息。最后，在 `WinMain` 函数中，进入消息循环处理消息，直到程序退出。

# 现在windows上界面编程的主要语言和方案是什么

在Windows上进行界面编程的主要语言和方案取决于开发者的需求和偏好。以下是几种常见的主要语言和方案：

1. **C++和Win32 API**：
   - C++结合Win32 API是传统的Windows应用程序开发方式。使用C++和Win32 API可以获得对操作系统底层功能的直接控制，适用于对性能和灵活性要求较高的应用程序。

2. **C#和Windows Forms**：
   - C#是一种现代的、面向对象的编程语言，Windows Forms是一种基于.NET框架的图形用户界面（GUI）工具包。使用C#和Windows Forms可以快速构建功能丰富、易于维护的Windows桌面应用程序，它提供了丰富的控件和事件处理机制。

3. **C#和WPF（Windows Presentation Foundation）**：
   - WPF是.NET框架中的一个GUI框架，提供了一种声明式的方式来构建现代化的Windows应用程序界面。使用C#和WPF可以创建具有高度定制化和富交互性的用户界面，支持数据绑定、样式模板、动画效果等功能。

4. **C#和Universal Windows Platform（UWP）**：
   - UWP是一种用于构建跨设备的现代化应用程序的平台，支持Windows桌面、移动设备和IoT设备。使用C#和UWP可以创建适用于各种Windows设备的统一的用户界面和功能，具有自适应布局、本地化、通知等特性。

5. **其他跨平台解决方案**：
   - 除了上述方案外，还有一些跨平台的GUI框架可以用于Windows应用程序开发，如Electron（使用HTML、CSS和JavaScript）、Qt（C++或Python）、Avalonia（C#）、Gtk#（C#）等。

总的来说，C#和.NET框架在Windows上的应用非常广泛，特别是Windows Forms和WPF提供了强大的工具和库，使得开发Windows应用程序变得简单、高效。

## Windows Forms和WPF比较

Windows Forms和WPF是两种不同的GUI（图形用户界面）框架，均用于在Windows操作系统上开发桌面应用程序。它们在设计理念、技术实现和使用方式上有一些明显的区别，下面我会对它们进行简要的比较：

1. **设计理念**：
   - Windows Forms：Windows Forms是一种传统的GUI框架，采用的是面向过程的设计模式。它的设计目标是简单易用，提供了一组可视化的控件，开发者可以通过拖放控件并设置属性来构建用户界面。
   - WPF：Windows Presentation Foundation是一种现代化的GUI框架，采用的是基于XAML的声明式编程模式。它的设计目标是可扩展性和灵活性，通过数据绑定、样式模板、动画效果等特性实现高度定制化的用户界面。

2. **技术实现**：
   - Windows Forms：Windows Forms是建立在Win32 API之上的封装，使用的是GDI+（图形设备接口）进行绘制。它是直接使用底层Windows API来创建和管理窗口和控件的。
   - WPF：WPF使用DirectX技术作为其底层渲染引擎，通过Direct3D来进行图形渲染。它采用了分离了界面和逻辑的架构，使用XAML来定义界面，通过CLR（Common Language Runtime）来执行代码逻辑。

3. **功能和扩展性**：
   - Windows Forms：Windows Forms提供了一组基本的控件和功能，包括按钮、文本框、列表框等。虽然它相对简单，但也可以通过自定义控件和绘制来实现更复杂的界面。
   - WPF：WPF提供了更丰富和强大的功能，包括数据绑定、样式模板、命令绑定、路由事件、动画效果等。它还支持矢量图形、3D图形、高分辨率屏幕适配等特性。

4. **学习曲线**：
   - Windows Forms：由于其简单易用的设计，Windows Forms相对于WPF来说学习曲线较低，尤其适合初学者或需要快速开发简单应用的场景。
   - WPF：WPF的学习曲线较陡，需要掌握XAML语言、数据绑定、样式模板等概念和技术。但一旦掌握了这些，就可以实现更加复杂和灵活的用户界面。

总的来说，Windows Forms适合快速开发简单的Windows应用程序，而WPF则更适合构建复杂、现代化的用户界面，并且具有更好的可扩展性和灵活性。选择哪种框架取决于项目的需求、开发团队的技术栈和开发周期等因素。

# 有哪些简单典型的windows应用适合用来做入门学习

对于入门学习Windows应用程序开发，以下是一些简单典型的项目建议，它们涵盖了基本的GUI开发、文件操作、数据展示等方面，适合初学者掌握基本的编程概念和技能：

1. **简单文本编辑器**：
   - 创建一个基本的文本编辑器应用程序，允许用户打开、编辑和保存文本文件。可以添加一些基本的编辑功能，如复制、粘贴、撤销等。

2. **TODO List 应用程序**：
   - 制作一个简单的TODO List应用程序，允许用户添加、编辑和删除待办事项。可以使用列表框或数据网格来显示待办事项。

3. **简单的绘图应用程序**：
   - 创建一个简单的绘图应用程序，允许用户绘制基本的图形（如线条、矩形、圆形）。可以使用GDI+或WPF中的画布控件来实现。

4. **简单的计算器**：
   - 制作一个简单的计算器应用程序，允许用户进行基本的数学计算，如加、减、乘、除等。可以使用按钮控件和文本框来实现。

5. **简单的日历应用程序**：
   - 创建一个简单的日历应用程序，显示当前月份的日历，并允许用户查看不同的月份和年份。可以添加提醒功能，显示重要日期。

6. **简单的图像查看器**：
   - 制作一个简单的图像查看器应用程序，允许用户打开和查看图像文件。可以添加缩放、旋转、裁剪等基本功能。

以上这些项目都是基于Windows桌面应用程序开发的，可以使用Windows Forms或WPF等技术来实现。它们涵盖了一些常见的GUI控件和操作，对于入门学习Windows应用程序开发非常有帮助。您可以根据自己的兴趣和技能选择其中一个项目作为入门学习的起点。

# windows下轻量级的gui开发环境

对于希望在Windows平台上进行轻量级GUI开发的开发者，有几个简单而易于上手的工具和框架可供选择：

1. **Visual Studio Code + WinForms 或 WPF**：
   - 使用Visual Studio Code作为代码编辑器，结合WinForms或WPF来进行GUI开发。Visual Studio Code是一款轻量级的、跨平台的代码编辑器，具有丰富的扩展生态系统和强大的代码编辑功能。您可以使用C#扩展来编写WinForms或WPF应用程序，并在Visual Studio Code中进行代码编辑和调试。

2. **SharpDevelop**：
   - SharpDevelop是一款开源的.NET集成开发环境（IDE），支持C#和VB.NET等语言。它提供了可视化的设计工具和代码编辑器，适用于WinForms和WPF应用程序的开发。SharpDevelop界面简洁清晰，对于入门学习Windows应用程序开发非常友好。

3. **JetBrains Rider**：
   - JetBrains Rider是一款强大的跨平台.NET开发工具，支持C#、VB.NET和F#等语言。它提供了集成的GUI设计器和代码编辑器，适用于WinForms和WPF应用程序的开发。虽然不如Visual Studio或SharpDevelop那么轻量级，但是它的功能和性能表现非常出色。

这些工具和框架都能够满足轻量级GUI开发的需求，您可以根据自己的喜好和需求选择合适的工具。无论您选择哪种工具，都可以使用C#语言来编写WinForms或WPF应用程序，并在Windows平台上进行GUI开发。

# vscode搭建wpf开发环境

在Visual Studio Code中搭建WPF开发环境相对于使用Visual Studio来说，可能需要一些额外的配置和扩展。以下是一些步骤，可以帮助您在Visual Studio Code中搭建WPF开发环境：

1. **安装Visual Studio Code**：
   
- 首先，您需要下载并安装Visual Studio Code编辑器。您可以从Visual Studio Code官方网站（https://code.visualstudio.com/）下载适用于Windows平台的安装程序，并按照安装向导的步骤进行安装。
   
2. **安装C#扩展**：
   
- 打开Visual Studio Code，转到扩展视图（Extensions view），搜索并安装C#扩展。C#扩展为Visual Studio Code添加了对C#语言的支持，包括语法高亮、智能代码补全、调试支持等功能。
   
3. **安装.NET Core SDK**：
   
- WPF应用程序通常使用.NET框架来进行开发。您需要下载并安装.NET Core SDK，以便在Visual Studio Code中编译和运行WPF应用程序。您可以从Microsoft官方网站（https://dotnet.microsoft.com/download/dotnet）下载最新的.NET Core SDK安装程序，并按照安装向导的步骤进行安装。
   
4. **创建WPF项目**：
   - 打开Visual Studio Code，通过命令行工具（如PowerShell）或集成的终端窗口，使用dotnet命令创建一个新的WPF项目。例如，您可以运行以下命令来创建一个名为"MyWpfApp"的新WPF项目：
     ```
     dotnet new wpf -n MyWpfApp
     ```
   - 进入新创建的项目目录：
     ```
     cd MyWpfApp
     ```

5. **编辑和运行项目**：
   - 在Visual Studio Code中打开刚刚创建的WPF项目。您可以在Visual Studio Code中编辑XAML文件和C#代码，并使用终端窗口执行以下命令来编译和运行项目：
     ```
     dotnet build     // 编译项目
     dotnet run       // 运行项目
     ```

通过以上步骤，您就可以在Visual Studio Code中搭建WPF开发环境，并开始编写和调试WPF应用程序了。虽然Visual Studio Code没有Visual Studio那么完整的集成开发环境，但是它提供了丰富的扩展和功能，足以满足您进行WPF开发的需求。

# wpf helloworld

以下是一个简单的WPF HelloWorld 程序示例：

```xaml
<!-- MainWindow.xaml -->
<Window x:Class="HelloWorld.MainWindow"
        xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
        xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
        Title="Hello, World!" Height="200" Width="300">
    <Grid>
        <TextBlock HorizontalAlignment="Center" VerticalAlignment="Center" FontSize="20" FontWeight="Bold">
            Hello, World!
        </TextBlock>
    </Grid>
</Window>
```

```csharp
// MainWindow.xaml.cs
using System.Windows;

namespace HelloWorld
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
        }
    }
}
```

这个程序创建了一个简单的窗口，其中包含一个居中显示的文本块，文本内容为 "Hello, World!"。

在XAML中，使用`<Window>`元素定义了窗口，并在其中添加了一个`<TextBlock>`元素，用于显示 "Hello, World!" 文本。在C#代码中，`MainWindow`类继承自`Window`类，它的构造函数调用了`InitializeComponent`方法，该方法用于加载XAML文件中定义的界面。

您可以创建一个新的WPF项目，在其中添加MainWindow.xaml和MainWindow.xaml.cs文件，并将以上代码复制到对应的文件中。然后编译和运行项目，就可以看到一个简单的WPF窗口显示 "Hello, World!"。

## 为什么界面描述都偏爱使用xml，而不是其他的配置文件格式，例如json

使用XML作为界面描述语言的主要原因之一是XML具有丰富的结构化表示能力，以及在各种系统和平台之间广泛的互操作性。下面是一些导致XML在界面描述中流行的原因：

1. **结构化表示能力**：XML具有树形结构，能够很好地表示复杂的层次结构和关系。这对于描述GUI界面中的控件、布局、样式等元素非常有用，使得XML能够清晰地表达界面的层次结构和组织关系。

2. **标准化和可扩展性**：XML是一种标准的、通用的标记语言，有着丰富的工具和库支持。它可以被各种程序和系统解析和处理，使得界面描述可以被多种工具和框架使用。此外，XML还具有良好的可扩展性，可以定义自定义的元素和属性来满足特定需求。

3. **兼容性和互操作性**：XML格式是一种通用的数据交换格式，在不同平台和系统之间具有良好的兼容性和互操作性。这意味着您可以将界面描述导出为XML文件，并在不同的开发工具、框架和平台之间共享和重用。

尽管XML在界面描述中具有许多优点，但也有一些缺点，例如XML的语法相对复杂，文件体积较大，可读性较差等。因此，有些开发者更喜欢使用其他格式如JSON来描述界面。JSON具有简洁的语法和良好的可读性，适合于描述简单的数据结构和配置信息。在某些情况下，使用JSON作为界面描述也是完全可行的选择，特别是对于Web应用程序或跨平台开发来说。

