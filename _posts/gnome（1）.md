---
title: gnome（1）
date: 2019-07-26 11:49:19
tags:
	- gnome

---

--

# 简介

GNOME 是一个流行的开源桌面环境，旨在提供直观、易于使用的桌面体验。它是一个由社区驱动的项目，拥有全球范围内的贡献者和支持者。

以下是 GNOME 的一些主要特点和亮点：

1. **直观的用户界面**：GNOME 的用户界面设计注重简洁、直观，以提高用户体验和工作效率。它采用了许多现代设计理念，例如平滑的动画效果和自然的工作流程。

2. **可定制性**：尽管 GNOME 提供了一个统一的用户体验，但用户仍然可以根据自己的喜好进行定制。从主题到桌面小部件，用户可以根据自己的偏好和需求调整 GNOME 桌面。

3. **强大的通知系统**：GNOME 的通知系统允许应用程序向用户发送非侵入式的通知，以便及时了解重要信息。

4. **集成的文件管理器**：GNOME 提供了一个称为 Nautilus 的文件管理器，它允许用户轻松地管理文件和文件夹，并支持文件的预览和搜索。

5. **应用程序生态系统**：GNOME 生态系统拥有许多高质量的应用程序，涵盖了各种用途，从办公套件到媒体播放器，再到图形编辑器和开发工具等。

6. **自由和开放源代码**：作为一个开源项目，GNOME 鼓励用户参与到项目的开发和改进中，并保证了用户对其代码的访问和修改权限。

总的来说，GNOME 提供了一个功能丰富、现代化且易于使用的桌面环境，适合各种类型的用户，从初学者到专业人士都能够从中受益。

# 发展历史

GNOME 的发展历史可以追溯到 1997 年，当时由 Miguel de Icaza 和 Federico Mena 等人创建了 GNOME 项目。以下是 GNOME 的一些关键里程碑：

1. **1997 年**：GNOME 项目成立。最初的目标是创建一个免费、开放源代码的桌面环境，提供类似于商业桌面环境的功能和体验。

2. **1999 年**：发布了 GNOME 1.0 版本。这是 GNOME 的首个稳定版本，为用户提供了一个完整的桌面环境，包括文件管理器、面向对象的图形用户界面库等。

3. **2002 年**：发布了 GNOME 2.0 版本。这个版本引入了许多重要的改进，包括改进的用户界面、更好的性能和稳定性，以及许多新的应用程序和工具。

4. **2011 年**：发布了 GNOME 3.0 版本。这是一个里程碑式的版本，引入了名为 GNOME Shell 的全新用户界面，采用了更现代化的设计理念和工作流程。这也标志着 GNOME 项目对桌面环境的重新定义。

5. **2018 年**：发布了 GNOME 3.30 版本，它引入了一些新功能和改进，如更好的平铺窗口管理、通知系统的改进等。

6. **2020 年**：发布了 GNOME 3.38 版本，带来了许多改进和优化，包括对应用程序菜单的重新设计、更好的多显示器支持等。

GNOME 项目一直在不断演进和发展，吸引了全球范围内的开发者和用户参与其中。它秉承着自由和开放的价值观，致力于提供一个现代化、易于使用的桌面环境，以满足用户的需求和期望。

# 主要编程语言

GNOME 项目的主要编程语言是 C。自从 GNOME 项目成立以来，C 一直是其主要的编程语言之一。许多 GNOME 核心组件和库都是用 C 编写的，包括 GTK+（GNU 图形工具包，用于构建 GNOME 应用程序的工具包）、GNOME Shell（GNOME 桌面环境的用户界面）、GLib（一套 C 语言库，提供了许多常用的数据结构和功能）、以及其他许多核心组件。

除了 C 之外，GNOME 项目还广泛使用了其他编程语言，包括：

1. **Python**：Python 在 GNOME 生态系统中得到了广泛应用，特别是在编写应用程序的插件和脚本方面。

2. **Vala**：Vala 是一种为 GNOME 开发而设计的现代编程语言，它的语法类似于 C#，但编译成 C 代码，可以与现有的 GNOME 基础设施无缝集成。

3. **JavaScript**：JavaScript 主要用于编写 GNOME Shell 扩展和主题，以及一些桌面应用程序。

4. **Rust**：Rust 是一种系统级编程语言，它在 GNOME 生态系统中越来越受欢迎，因为它提供了内存安全和并发性，并且易于与现有的 C 代码集成。

总的来说，GNOME 项目使用多种编程语言来开发其组件和应用程序，以满足不同开发者的需求和偏好，并且在保持高效性和现代性的同时，为用户提供强大的功能和体验。

## 当前gnome的桌面程序主要什么语言开发

当前 GNOME 桌面环境中的桌面程序主要是使用 C、Vala 和 JavaScript 开发的。

1. **C**：C 语言是 GNOME 项目的传统编程语言之一，许多核心组件和库都是用 C 编写的，如 GTK+、GLib 等。C 语言在 GNOME 中仍然扮演着重要的角色，特别是在编写高性能、系统级别的组件时。

2. **Vala**：Vala 是为 GNOME 开发而设计的一种现代编程语言，它的语法类似于 C#，但编译成 C 代码，可以与现有的 GNOME 基础设施无缝集成。许多 GNOME 应用程序使用 Vala 进行开发，以获得更高的开发效率和代码可维护性。

3. **JavaScript**：JavaScript 主要用于编写 GNOME Shell 扩展、主题和一些桌面应用程序。GNOME Shell 是 GNOME 桌面环境的核心组件之一，它的扩展和定制通常使用 JavaScript 进行编写。

除了这些主要的编程语言之外，还有其他语言在 GNOME 生态系统中得到了一定的应用，例如 Python、Rust 等。总的来说，GNOME 项目鼓励多样化的编程语言使用，以便开发者可以根据自己的偏好和需求选择适合的工具进行开发。

## vala这个语言有前途吗

Vala 是一种为 GNOME 开发而设计的现代编程语言，它具有许多吸引人的特性，比如语法类似于 C#、自动内存管理、强类型系统等。虽然 Vala 在 GNOME 生态系统中有一定的影响力，但是评判一种编程语言的前途并不仅仅取决于它的设计和特性，还受到许多其他因素的影响。

以下是 Vala 的一些优势和挑战，以及对其前景的一些考虑：

优势：
1. **与 GNOME 集成**：Vala 是为 GNOME 开发而设计的，可以与 GNOME 基础设施无缝集成，使得开发 GNOME 应用程序更加高效。
2. **现代特性**：Vala 借鉴了现代编程语言的许多特性，如类、接口、泛型等，使得开发者可以编写更加简洁、易于理解和维护的代码。
3. **自动内存管理**：Vala 使用 GObject 系统提供的引用计数内存管理，避免了手动内存管理带来的麻烦，提高了开发效率和代码安全性。

挑战：
1. **生态系统支持**：虽然 Vala 在 GNOME 生态系统中得到了广泛应用，但它的生态系统相对较小，与其他主流编程语言相比，社区和第三方库的支持相对有限。
2. **学习曲线**：尽管 Vala 的语法类似于 C#，但对于新手来说，仍然需要一定的学习曲线，特别是对于那些没有 C# 或类似语言经验的开发者来说。

考虑到这些因素，Vala 在 GNOME 生态系统中仍然具有一定的前景，特别是对于那些希望开发 GNOME 应用程序的开发者来说。然而，要想在更广泛的范围内取得成功，可能需要解决生态系统支持和学习曲线等方面的挑战。

# 使用python开发gnome gui程序举例

当使用 Python 开发 GNOME GUI 程序时，常用的工具是 GTK+（Python 绑定为 `Gtk`），它是 GNOME 应用程序开发的主要工具包。以下是一个简单的示例，演示如何使用 Python 和 GTK+ 创建一个简单的 GNOME GUI 程序：

```python
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class MyWindow(Gtk.Window):

    def __init__(self):
        Gtk.Window.__init__(self, title="Hello GNOME")

        self.box = Gtk.Box(spacing=6)
        self.add(self.box)

        self.button = Gtk.Button(label="Click Me!")
        self.button.connect("clicked", self.on_button_clicked)
        self.box.pack_start(self.button, True, True, 0)

    def on_button_clicked(self, widget):
        print("Hello GNOME!")

win = MyWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
```

这个示例创建了一个简单的窗口，其中包含一个按钮。当点击按钮时，会在控制台打印出 "Hello GNOME!"。这个程序使用了 GTK+ 的 Python 绑定来创建 GUI 元素，并使用 Python 的事件机制来处理按钮点击事件。

通过这个示例，你可以看到使用 Python 和 GTK+ 来开发 GNOME GUI 程序是相当简单直观的。你可以根据自己的需求和兴趣进一步扩展这个程序，添加更多的 GUI 元素和功能。

# gnome包含了哪些组件？

GNOME 是一个庞大的桌面环境项目，包含了许多组件和子项目，涵盖了各种不同的功能和用途。以下是 GNOME 项目中一些主要的组件和子项目：

1. **GNOME Shell**：GNOME 桌面环境的核心组件，提供了桌面的用户界面和交互方式。

2. **GTK+**：GNU 图形工具包，是 GNOME 应用程序开发的主要工具包，提供了丰富的 GUI 组件和功能。

3. **GLib**：一套 C 语言库，提供了许多常用的数据结构和功能，是 GNOME 应用程序开发的基础库之一。

4. **Nautilus**：GNOME 默认的文件管理器，用于管理文件和文件夹，并提供了预览、搜索等功能。

5. **GNOME Settings Daemon**：负责管理 GNOME 桌面环境的各种设置和配置。

6. **GNOME Control Center**：提供了一个集中管理系统设置和配置的界面。

7. **GNOME Terminal**：GNOME 默认的终端仿真器，提供了命令行界面。

8. **GNOME Calculator**：GNOME 默认的计算器应用程序。

9. **GNOME Software**：提供了一个图形化的软件包管理工具，用于安装、卸载和更新软件包。

10. **GNOME Calendar**：一个简单的日历应用程序，用于管理日程和提醒。

11. **GNOME Weather**：一个简单的天气应用程序，用于查看天气预报。

12. **GNOME Maps**：一个简单的地图应用程序，用于查看地图和获取导航信息。

除了上述列举的组件之外，还有许多其他的 GNOME 子项目和应用程序，涵盖了各种不同的领域，如办公套件、媒体播放器、图形编辑器、开发工具等。总的来说，GNOME 项目提供了一个完整的桌面环境，包含了几乎所有用户日常所需的功能和工具。

## 哪个组件是python写的

在 GNOME 项目中，有几个组件是使用 Python 编写的，尤其是一些辅助性的工具、应用程序和插件。以下是一些主要的 GNOME 组件和项目，其中一部分是使用 Python 编写的：

1. **GNOME Software**：这是一个图形化的软件包管理工具，用于安装、卸载和更新软件包。它的一部分功能是使用 Python 编写的。

2. **GNOME Weather**：这是一个简单的天气应用程序，用于查看天气预报。它的一部分功能是使用 Python 编写的。

3. **GNOME Calendar**：这是一个简单的日历应用程序，用于管理日程和提醒。其中一些功能是使用 Python 编写的。

4. **GNOME Maps**：这是一个简单的地图应用程序，用于查看地图和获取导航信息。一部分功能也是使用 Python 编写的。

5. **GNOME Control Center**：GNOME 控制中心提供了一个集中管理系统设置和配置的界面。虽然它的主要部分是使用 C 编写的，但是其中一些模块和插件可能是使用 Python 编写的。

除了上述列举的一些组件之外，还有其他一些辅助性的工具和插件，它们可能也是使用 Python 编写的。Python 在 GNOME 生态系统中得到了广泛的应用，尤其是在开发辅助工具和应用程序时，因为 Python 具有简洁、易读易写的语法，以及丰富的标准库和第三方库支持。

# gnome的主要版本

GNOME 项目的主要版本通常指的是 GNOME 桌面环境的稳定发布版本。这些版本通常以主要版本号命名，比如 GNOME 3、GNOME 4 等。以下是一些主要的 GNOME 版本：

1. **GNOME 1.x**：GNOME 项目的最初版本，于 1999 年发布。它引入了一些基本的桌面环境功能和应用程序。

2. **GNOME 2.x**：于 2002 年发布，是 GNOME 项目的第二个主要版本。GNOME 2.x 版本引入了许多重要的改进，包括改进的用户界面、更好的性能和稳定性等。

3. **GNOME 3.x**：于 2011 年发布，是 GNOME 项目的第三个主要版本。GNOME 3.x 版本引入了名为 GNOME Shell 的全新用户界面，采用了更现代化的设计理念和工作流程。

4. **GNOME 40.x**：GNOME 40 是 GNOME 项目的最新主要版本，于 2021 年发布。GNOME 40 版本引入了一些重大变化，包括重新设计的工作区布局、改进的多显示器支持、新的应用网格布局等。

除了这些主要版本之外，每个主要版本通常都有一系列的次要版本和补丁版本，用于修复错误、改进性能和添加新功能。例如，GNOME 3 系列包括 GNOME 3.2、GNOME 3.4、GNOME 3.6 等版本。每个次要版本都会引入一些新的功能和改进，但整体上保持了主要版本的稳定性和一致性。

## 版本号为什么从3一下子跳到40

GNOME 桌面环境的版本号从 3.x 跳到 40.x 的变化反映了 GNOME 项目在版本号方面的一次重大调整。这个调整主要是出于两个方面的考虑：

1. **语义化版本号**：GNOME 项目决定采用更符合语义化版本规范的版本号方案。根据语义化版本规范，当进行破坏性改动时（意味着向后不兼容的改动），主版本号应该增加。在这种情况下，从 3.x 直接跳到 40.x 可以清晰地表明这是一次重大的版本升级，可能包含了向后不兼容的改动。

2. **用户界面和用户体验的重大变化**：GNOME 40 版本引入了一些重大的用户界面和用户体验方面的改进，包括重新设计的工作区布局、改进的多显示器支持、新的应用网格布局等。这些变化被认为足够重大，以至于将主版本号从 3.x 提升到 40.x，以突出这一重要的里程碑。

总的来说，版本号从 3.x 跳到 40.x 主要是为了反映 GNOME 项目的重大进步和变化，同时也更好地遵循语义化版本规范。

## gnome40的主要特点

GNOME 40 是 GNOME 桌面环境的一个重要版本，引入了许多新特性和改进。以下是 GNOME 40 的一些主要特点：

1. **新的工作区布局**：GNOME 40 引入了重新设计的工作区布局，将活动视图从水平布局更改为垂直布局。这个改变使得在不同窗口和工作区之间进行导航更加直观和流畅。

2. **改进的多显示器支持**：GNOME 40 改进了对多显示器的支持，引入了新的显示器布局模式，使得在多个显示器之间进行切换和管理更加方便。

3. **新的应用网格布局**：GNOME 40 引入了新的应用网格布局，使得在应用启动器中更容易地浏览和管理应用程序。这个新布局将应用程序按照网格方式排列，提供了更直观的视图。

4. **改进的通知系统**：GNOME 40 改进了通知系统，引入了一些新的动画效果和交互方式，使得通知更加易于识别和处理。

5. **新的默认字体**：GNOME 40 使用了新的默认字体，称为 Cantarell。这个字体具有更好的可读性和美观性，提高了整体用户体验。

6. **GNOME 软件中心的改进**：GNOME 40 对 GNOME 软件中心进行了一些改进，包括性能优化、界面改进和更好的软件包管理功能。

总的来说，GNOME 40 带来了一系列重大的改进和新特性，旨在提高 GNOME 桌面环境的用户体验、性能和功能性。

# gnome未来的发展规划

GNOME 项目的未来发展规划通常由 GNOME 社区和开发者共同讨论和制定。虽然我无法直接提供 GNOME 未来发展的详细计划，但可以分享一些可能影响 GNOME 未来发展的一般趋势和方向：

1. **持续改进用户体验**：GNOME 项目将继续致力于改进用户体验，包括优化用户界面设计、提高系统稳定性、改进性能等方面。这可能包括引入新的动画效果、改进通知系统、优化资源管理等。

2. **更好的多任务处理和多显示器支持**：随着用户对多任务处理和多显示器工作环境的需求不断增加，GNOME 项目可能会继续改进多任务处理和多显示器支持功能，以提供更流畅和高效的工作体验。

3. **更紧密的应用程序集成**：GNOME 项目可能会继续促进 GNOME 应用程序之间的集成，以提供更一体化的用户体验。这可能包括更深入的应用程序间通信、共享设置和数据、统一的外观和行为等。

4. **支持新硬件和技术**：随着新硬件和技术的不断出现，GNOME 项目可能会持续改进对新硬件的支持，并考虑如何利用新技术提供更先进的功能和体验，比如增强现实、虚拟现实等。

5. **社区参与和开放合作**：GNOME 项目将继续鼓励全球范围内的开发者和用户参与其中，共同推动项目的发展。这可能包括更多的社区活动、开发者会议、教育计划等，以及与其他开源项目和社区的合作。

6. **可持续性和开放性**：GNOME 项目将继续坚持开源和可持续性的价值观，保持项目的开放性和透明度，并致力于维护一个健康、包容和繁荣的社区。

总的来说，GNOME 项目的未来发展规划将会受到多种因素的影响，包括技术趋势、用户需求、社区参与等。通过持续的讨论和合作，GNOME 社区将努力确保 GNOME 桌面环境保持在创新的前沿，为用户提供优秀的桌面体验。

# gnome使用x11还是wayland

GNOME 可以在两种显示服务器中运行：X11 和 Wayland。X11 是传统的显示服务器协议，而 Wayland 则是一个现代的显示服务器协议，旨在提供更好的性能、更好的安全性和更现代化的特性。

从 GNOME 3 开始，GNOME 提供了对 Wayland 的原生支持，并且在很多发行版中已经成为默认选项。然而，X11 仍然是 GNOME 的另一个选择，特别是在某些情况下，比如兼容性问题或者特定的硬件驱动问题。

总的来说，大多数现代的 GNOME 发行版都默认使用 Wayland 作为显示服务器，因为它提供了更好的性能和安全性，并且支持更多的现代特性，如高 DPI 显示、全局触摸手势等。不过，用户仍然可以根据自己的需求选择使用 X11 或 Wayland。



| 特性         | X11                                        | Wayland                                                      |
| ------------ | ------------------------------------------ | ------------------------------------------------------------ |
| 性能         | 相对较低，因为它是一个较旧的显示服务器协议 | 更好的性能，可以实现更流畅的桌面体验                         |
| 安全性       | 安全性较差，由于设计上的限制               | 更好的安全性，使用更严格的安全模型                           |
| 特性支持     | 对于现代特性的支持有限                     | 对于现代特性的支持更加全面                                   |
| 兼容性       | 兼容性较好，许多应用程序和驱动程序都支持   | 在某些情况下兼容性较差，可能需要修改或更新应用程序和驱动程序 |
| 开发和维护   | 开发和维护较困难，因为它是一个较老的协议   | 开发和维护相对容易，因为它是一个现代的协议                   |
| 应用程序集成 | 应用程序集成相对简单                       | 应用程序集成需要更多的工作                                   |

# api分类

```
核心库
	核心
		glib
		gio
			提供了对文件系统的访问。
		GObject
	用户界面
	多媒体
		gstreamer
```



为了方便开发，官方提供了一个模板。

https://wiki.gnome.org/AppsTemplate

但是下载不了。

github上有。从这里下载。

https://github.com/ikeydoherty/gnome-app-templates

在我的笔记本上，执行autogen.sh脚本。出错。

```
src/Makefile.am:34: error: HAVE_INTROSPECTION does not appear in AM_CONDITIONAL
```

执行下面的命令，安装这个就可以。

```
sudo apt-get install gobject-introspection
```

编译处理，只有一个动态库。怎么使用呢？



编译gedit的代码。

https://github.com/GNOME/gedit

必须用git clone的方式来做。下载压缩包不行，因为还依赖了其他的工程。

gnome的音乐应用，是用python写的。这个会是gnome上的主流吗？可能会，至少说明目前用C语言来开发，确实比较费力。而python比较省力。gnome目前还是缺失应用，而不是应用的效率。所以当务之急是先产生足够多的应用。

https://github.com/GNOME/gnome-music

计算器应用，是用vala语言写的。

vala是gnome社区开发的编程语言。



# gnome music

从github下载代码，

```
mkdir _build
meson.py _build
```

然后需要安装这个。

```
sudo apt-get install  libgirepository1.0-dev
```

但是还是出错，提示gtk版本太低了。

写在我升级一下gtk版本。

```
sudo add-apt-repository ppa:gnome3-team/gnome3-staging
sudo add-apt-repository ppa:gnome3-team/gnome3
sudo apt update
sudo apt dist-upgrade
```

这个需要下载400M左右的东西。

还是不行，版本要求太严格了。

不继续编译了。

# gnome Bluetooth



参考资料

1、官网

https://developer.gnome.org/references

2、

https://access.redhat.com/documentation/zh-cn/red_hat_enterprise_linux/7/html/desktop_migration_and_administration_guide/what-is-gnome-classic

3、官方应用

https://wiki.gnome.org/Apps

4、升级Ubuntu16.04的gtk版本

https://www.omgubuntu.co.uk/2016/05/install-gnome-3-20-ubuntu-16-04-lts