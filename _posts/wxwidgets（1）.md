---
title: wxwidgets（1）
date: 2023-06-27 19:53:43
tags:
	- wxwidgets

---

--

# 资源收集

wxwidgets源代码分析

https://www.cnblogs.com/psbec/tag/wxWidgets/

Windows 应用偶现界面卡死问题的分析

https://blog.csdn.net/luansxx/article/details/123756865



# wxwidgets简介

wxWidgets（前身为 wxWindows）是一个跨平台的C++应用程序框架，用于开发图形用户界面（GUI）应用程序。它提供了一套统一的API，可在不同的操作系统上实现一致的外观和行为。wxWidgets支持多种主流操作系统，包括Windows、macOS、Linux以及其他UNIX系统。

以下是wxWidgets的一些主要特点和功能：

1. 跨平台支持：wxWidgets可以在不同的操作系统上编写一次代码，然后在多个平台上编译和运行。它提供了对各种操作系统的本地控件和功能的封装，使开发人员能够轻松地编写跨平台应用程序。

2. 强大的控件库：wxWidgets提供了丰富的控件库，包括按钮、文本框、列表框、树状结构、菜单、工具栏等。这些控件可以用于构建功能丰富、交互性强的用户界面。

3. 事件驱动架构：wxWidgets使用事件和消息机制来处理用户交互和应用程序逻辑。开发人员可以通过响应各种事件来实现用户界面的交互和处理逻辑。

4. 支持多种编程语言：除了C++，wxWidgets还提供了对其他编程语言的支持，如Python、Perl、Ruby等。这使得开发人员可以使用自己喜欢的编程语言来开发wxWidgets应用程序。

5. 自定义绘图：wxWidgets提供了绘图设备上下文（Device Context）的抽象，允许开发人员进行自定义绘图操作，绘制图形、文本、位图等。

6. 主题和外观样式：wxWidgets支持主题和外观样式的定制，使开发人员能够根据应用程序需求自定义界面的外观和风格。

7. 第三方库整合：wxWidgets可以与其他流行的开源库和工具集成，如数据库访问、图形绘制、网络通信等，扩展应用程序的功能。

wxWidgets是一个开源项目，其源代码可在 wxWidgets 的官方网站上获取。它具有广泛的用户社区和详细的文档，提供了丰富的示例和教程，方便开发人员学习和使用。

# 发展历史

wxWidgets 是一个开源的跨平台图形用户界面(GUI)框架，可以用于构建桌面应用程序。以下是 wxWidgets 的发展历史：

- 1992年，Julian Smart 开始开发一个名为 wxWindows 的 C++ 类库，旨在提供跨平台的 GUI 编程接口。
- 1995年，wxWindows 1.0 版本发布，支持 Windows 和 Unix 平台。该版本的 API 设计与 Motif 类似。
- 1997年，wxWindows 2.0 版本发布，支持 Macintosh 平台。该版本的 API 设计更加面向对象化，并与 Microsoft Foundation Classes (MFC) 相似。
- 2004年，wxWindows 2.5 版本发布，引入了 Unicode 和 STL 支持，并且开始使用 wxWidgets 作为新的名称。
- 2006年，wxWidgets 2.8 版本发布，添加了对 Windows Vista 和 Mac OS X 的支持。
- 2008年，wxWidgets 2.9 版本发布，添加了对 GTK+ 2.0 的支持，并改进了多线程和网络编程 API。
- 2012年，wxWidgets 3.0 版本发布，引入了 C++11 支持，并改进了事件系统、多媒体支持和界面设计工具。
- 2018年，wxWidgets 3.1 版本发布，添加了对 C++17 的支持，并改进了多线程和网络编程 API。

在过去的几十年中，wxWidgets 一直在不断发展和改进，成为了一个成熟、稳定的 GUI 框架。它的跨平台性、面向对象的设计、易用性和扩展性等特点，使得它在许多领域得到了广泛应用，例如科学计算、教育、多媒体、游戏等。

# 基于wxwidgets的开源项目

以下是基于 wxWidgets 的一些开源项目的示例：

1. CodeLite: 一个跨平台的 C++ 集成开发环境（IDE）。
   GitHub链接：https://github.com/eranif/codelite

2. wxFormBuilder: 一个可视化的 wxWidgets 界面设计器和代码生成器。
   GitHub链接：https://github.com/wxFormBuilder/wxFormBuilder

3. wxMaxima: 一个跨平台的数学软件，用于计算和绘制数学函数和方程。
   GitHub链接：https://github.com/wxMaxima-developers/wxmaxima

4. Code::Blocks: 一个开源的跨平台 C++ 集成开发环境（IDE）。
   GitHub链接：https://github.com/obfuscated/codeblocks

5. Audacity: 一个功能强大的跨平台音频编辑和录音软件。
   官方网站：https://www.audacityteam.org/

6. wxWidgets Samples: 官方提供的 wxWidgets 示例集合，展示了各种使用 wxWidgets 的功能和特性。
   GitHub链接：https://github.com/wxWidgets/wxWidgets/tree/master/samples

7. wxHexEditor: 一个用于查看和编辑二进制文件的免费开源软件。
   GitHub链接：https://github.com/EUA/wxHexEditor

8. wxArt2D: 一个基于 wxWidgets 的 2D 图形引擎和游戏开发框架。
   GitHub链接：https://github.com/klayge/wxArt2D

9. wxAstroCapture: 一个用于天文摄影和天文图像处理的软件。
   GitHub链接：https://github.com/wxAstroCapture/wxAstroCapture

10. wxGIS: 一个用于地理信息系统（GIS）开发的库和工具集合。
    GitHub链接：https://github.com/wxgis/wxgis

以上是一些基于 wxWidgets 的开源项目的示例。它们涵盖了各种应用领域，包括开发工具、图形界面设计、数学计算、音频编辑、游戏开发、二进制编辑等。你可以进一步探索这些项目，了解它们的功能和用途，以及如何使用 wxWidgets 构建各种应用程序。

# 编写wxwidgets应用需要包含的头文件

编写 wxWidgets 应用程序时，需要包含以下常见的头文件：

```cpp
#include <wx/wx.h>                  // 基本 wxWidgets 头文件
#include <wx/app.h>                 // 应用程序类
#include <wx/frame.h>               // 窗口框架类
#include <wx/panel.h>               // 面板类
#include <wx/button.h>              // 按钮类
#include <wx/textctrl.h>            // 文本控件类
#include <wx/sizer.h>               // 布局管理器类
#include <wx/msgdlg.h>              // 消息对话框类
#include <wx/filedlg.h>             // 文件对话框类
#include <wx/dir.h>                 // 目录操作类
#include <wx/image.h>               // 图像处理类
#include <wx/timer.h>               // 定时器类
#include <wx/log.h>                 // 日志记录类
#include <wx/menu.h>                // 菜单类
#include <wx/statusbr.h>            // 状态栏类
#include <wx/toolbar.h>             // 工具栏类
#include <wx/datetime.h>            // 日期和时间类
#include <wx/settings.h>            // 系统设置类
#include <wx/event.h>               // 事件处理类
#include <wx/gdicmn.h>              // 基本图形设备接口类
#include <wx/dcclient.h>            // 设备上下文类
#include <wx/bitmap.h>              // 位图类
#include <wx/font.h>                // 字体类
#include <wx/colour.h>              // 颜色类
#include <wx/utils.h>               // 实用工具类
```

上述头文件包含了 wxWidgets 中常用的类和功能，可以根据具体应用程序的需求进行选择和扩展。另外，还可以根据需要引入其他特定的 wxWidgets 模块的头文件。

需要注意的是，具体的头文件包含可能因不同的 wxWidgets 版本和使用的模块而有所变化。请根据实际情况查阅相应版本的 wxWidgets 文档或参考示例代码来确定需要包含的头文件。

# HelloWorld

以下是一个简单的 wxWidgets HelloWorld 示例：

```cpp
#include <wx/wx.h>

class MyFrame : public wxFrame
{
public:
    MyFrame(const wxString& title)
        : wxFrame(NULL, wxID_ANY, title, wxDefaultPosition, wxSize(250, 150))
    {
        // 创建一个面板
        wxPanel* panel = new wxPanel(this, wxID_ANY);

        // 创建一个静态文本控件
        wxStaticText* label = new wxStaticText(panel, wxID_ANY, "Hello, wxWidgets!",
                                               wxPoint(50, 50));

        // 设置字体和颜色
        wxFont font(14, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD);
        label->SetFont(font);
        label->SetForegroundColour(wxColour(255, 0, 0)); // 设置为红色

        // 设置面板的布局管理器
        wxBoxSizer* sizer = new wxBoxSizer(wxVERTICAL);
        sizer->Add(label, 0, wxALIGN_CENTER | wxALL, 10);
        panel->SetSizer(sizer);
    }
};

class MyApp : public wxApp
{
public:
    virtual bool OnInit()
    {
        MyFrame* frame = new MyFrame("Hello World");
        frame->Show(true);
        return true;
    }
};

wxIMPLEMENT_APP(MyApp);
```

在上述示例中，我们创建了一个继承自 `wxFrame` 的自定义窗口类 `MyFrame`，并在其中创建了一个面板和一个静态文本控件。然后，我们创建了一个继承自 `wxApp` 的应用程序类 `MyApp`，并重写了它的 `OnInit` 方法，在该方法中创建了一个 `MyFrame` 对象，并显示出来。

最后，我们使用 `wxIMPLEMENT_APP` 宏来实例化 `MyApp` 类，并启动应用程序。

当我们运行该应用程序时，将显示一个带有 "Hello, wxWidgets!" 文本的窗口。

请注意，编译和运行 wxWidgets 应用程序需要正确配置和链接 wxWidgets 库，并在相应的编译环境中设置正确的编译选项。详细的编译和链接指南可以在 wxWidgets 的官方网站上找到。

# windows codeblocks搭建wxwidgets开发环境

以下是在 Windows 上使用 Code::Blocks 搭建 wxWidgets 开发环境的步骤：

1. 下载 wxWidgets：访问 wxWidgets 的官方网站（https://www.wxwidgets.org/downloads/），下载适用于 Windows 的 wxWidgets 发行版。选择稳定版本或开发版本根据需要。

2. 安装 wxWidgets：解压下载的 wxWidgets 压缩包到合适的位置，例如 `C:\wxWidgets`。

3. 打开 Code::Blocks：启动 Code::Blocks 集成开发环境。

4. 创建新的 wxWidgets 项目：点击菜单栏的 "File"，然后选择 "New" -> "Project"，选择 "wxWidgets project"，点击 "Go"。

5. 配置项目属性：在项目向导中，选择 "Console application" 或 "GUI application"，然后点击 "Next"。在 "wxWidgets build options" 页面，点击 "Yes"，然后浏览并选择 wxWidgets 的安装路径（步骤2中的路径）。选择正确的编译器（例如 GCC）和目标架构（例如 x86），然后点击 "Finish"。

6. 配置编译器：在 Code::Blocks 中，点击菜单栏的 "Settings" -> "Compiler"，选择你正在使用的编译器。在 "Selected compiler" 页面，选择 "Other options" 选项卡，将 `-std=c++11` 添加到 "Compiler flags"。

7. 编写和构建应用程序：在 Code::Blocks 的项目窗口中，展开 "Sources" 目录，双击 "main.cpp" 文件以打开编辑器。在这里编写你的 wxWidgets 应用程序代码。然后点击 "Build" 工具栏按钮或使用快捷键 F9 来构建应用程序。

8. 运行应用程序：在构建成功后，你可以点击 "Run" 工具栏按钮或使用快捷键 F10 来运行应用程序。

以上是使用 Code::Blocks 搭建 wxWidgets 开发环境的基本步骤。请注意，根据你的操作系统和开发环境的不同，某些步骤可能会有所差异。建议参考 wxWidgets 的官方文档和 Code::Blocks 的使用手册来获取更详细和具体的指导。

