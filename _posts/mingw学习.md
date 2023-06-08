---
title: mingw学习
date: 2018-09-01 11:36:31
tags:
	- Windows

---



mingw是Min Gnu for Windows 的缩写，是在Windows搭建一个最小的gnu环境。



和cygwin比较，更小，也方便很多。



https://osdn.net/projects/mingw/downloads/68260/mingw-get-setup.exe/

这里下载安装器。

下载的内容放在这里。

C:\MinGW\var\cache\mingw-get\packages



下载完成后。然后设置环境变量。

1、新建MINGW_HOME。

2、在path里加上：

```
%MINGW_HOME%\bin;%MINGW_HOME%\libexec\gcc\mingw32\6.3.0;
```

还有添加环境变量。

```
LIBRARY_PATH = %MINGW_HOME%/lib
C_INCLUDE_PATH = %MINGW_HOME%/include
```



然后基本环境就好了。



eclipse下载安装c++版本的。

然后新建一个工程，选择c++ manage project，这个才可以选择工具链的。



然后点击锤子按钮，进行编译，然后就可以运行了。



现在点击调试是不行的，因为默认没有安装gdb。

解决方法是继续打开mingw安装器，勾选gdb的。安装。



然后就可以调试了。

我写了c++11的代码，发现shared_ptr这种不能补全。

给eclipse 添加c++11的支持。





```
error: 'shared_ptr' in namespace 'std' does not name a template type
```



试用一下codeblock这个ide看看。



# 发展历史

MinGW（Minimalist GNU for Windows）是一套用于Windows平台的开发工具集，它提供了一组基于GNU工具的开发环境，包括编译器、调试器、链接器等。MinGW的目标是为Windows提供一个轻量级的开发环境，使开发者能够在Windows平台上使用GNU工具链进行开发。

以下是MinGW的发展历史的一些重要里程碑：

1. 初始版本（1998年）：MinGW最初由Colin Peters于1998年创建，他将GNU工具链移植到Windows平台上，以便在Windows上进行C和C++开发。

2. MinGW-w64项目（2005年）：2005年，MinGW-w64项目启动，旨在提供对64位Windows平台的支持。该项目继承了原始的MinGW，并扩展了对64位架构的支持，使开发者能够在64位Windows系统上进行开发。

3. MSYS（Minimal System）项目（2001年）：为了提供更完整的开发环境，MinGW项目还开发了MSYS项目，它是一个基于GNU工具的轻量级Unix风格环境，可以在Windows上模拟类Unix环境。

4. MinGW-w64更新和发展：随着时间的推移，MinGW-w64项目不断更新和发展，增加了对新的Windows版本、新的CPU架构和新的功能的支持。它逐渐成为Windows上广泛使用的开发工具之一。

5. MSYS2项目（2013年）：为了取代原始的MSYS项目，MSYS2项目于2013年启动。MSYS2是一个重新设计和改进的基于MSYS的环境，它提供了更好的软件包管理和更新机制，以及更好的兼容性和性能。

MinGW的发展历史中，MinGW-w64和MSYS2项目的推出对于提供更强大和灵活的开发环境起到了重要作用。它们使得在Windows平台上进行跨平台开发和使用GNU工具链变得更加方便和便捷。

# msys2和mingw的区别

MSYS2（Minimal SYStem 2）和MinGW（Minimalist GNU for Windows）是两个在Windows平台上用于开发的工具集，它们有一些区别和不同的用途。

1. MSYS2：
   - MSYS2是一个重新设计和改进的基于MSYS的环境，它提供了类Unix的环境，可以在Windows上模拟类Unix操作系统。
   - MSYS2提供了一套用于开发的核心工具，例如shell（bash）、GNU工具链（gcc、make等）和基本的Unix命令（ls、grep等）。
   - MSYS2还提供了强大的包管理器（pacman），可以方便地安装、更新和管理各种开发工具和库。
   - MSYS2主要用于在Windows平台上进行跨平台开发和构建软件，它提供了一个轻量级的开发环境。

2. MinGW：
   - MinGW是一套用于Windows平台的开发工具集，它提供了一组基于GNU工具的开发环境，包括编译器、调试器、链接器等。
   - MinGW旨在为Windows提供一个轻量级的开发环境，使开发者能够在Windows平台上使用GNU工具链进行C和C++开发。
   - MinGW的目标是生成原生的Windows可执行文件，而不需要依赖于额外的运行时库或类Unix环境。

主要区别：
- MSYS2提供了完整的类Unix环境，包括shell和常用的Unix工具，用于在Windows上模拟类Unix操作系统。它更适用于跨平台开发和使用类Unix工具的场景。
- MinGW提供了基于GNU工具的开发环境，专注于在Windows上进行C和C++开发，生成原生的Windows可执行文件。它更适用于纯粹的Windows开发场景。

需要注意的是，MSYS2和MinGW是可以共存的，并且在MSYS2环境中可以使用MinGW来编译和构建Windows应用程序。在某些情况下，可能会同时使用它们来满足不同的开发需求。

## 简单说，msys2包含了mingw

# msys2由哪些部分组成

MSYS2（Minimal SYStem 2）由以下几个主要部分组成：

1. MSYS2 Runtime：MSYS2 Runtime是MSYS2的核心部分，它提供了一套基于MSYS的类Unix环境，包括shell（bash）、常用的Unix工具和命令（ls、grep、sed等）以及基本的文件系统操作等。MSYS2 Runtime通过模拟Unix环境，在Windows上提供了一个类Unix的开发环境。

2. Pacman：Pacman是MSYS2的包管理器，它用于安装、更新和管理软件包。通过Pacman，用户可以方便地获取和安装各种开发工具、库和依赖项，包括GNU工具链（gcc、make等）、编程语言解释器（Python、Ruby等）、版本控制系统（Git、Mercurial等）以及其他常用的开发工具和库。

3. MSYS2 Shell：MSYS2提供了一个基于MSYS2 Runtime的交互式shell环境，通常是bash。这个shell环境允许用户在Windows上使用类Unix的命令行界面，并执行类Unix的命令和脚本。

4. MinGW-w64：MinGW-w64是MSYS2提供的一个重要组成部分，它是一个基于MinGW的工具集，用于在Windows上进行C和C++开发。MinGW-w64提供了一组基于GNU工具的开发环境，包括编译器、调试器、链接器等，用于生成原生的Windows可执行文件。

这些组件一起构成了MSYS2的完整环境，使用户能够在Windows平台上获得一个强大的开发工具集和类Unix环境，方便进行跨平台开发和使用各种开发工具和库。

# git bash和msys的关系

Git Bash是基于MSYS（Minimal SYStem）的一个工具，用于在Windows上运行Git命令和使用类Unix的Shell环境。MSYS是为了在Windows上提供一个类Unix环境而创建的，它提供了一套Unix工具和命令行界面，可以在Windows上执行类Unix的命令和脚本。

Git Bash是在MSYS的基础上进行了定制和扩展，主要用于支持Git版本控制系统。它集成了Git命令行工具，并提供了一个类Unix的Shell环境，使用户可以在Windows上使用Git命令，并执行类Unix的操作和脚本。

因此，Git Bash是基于MSYS的，它继承了MSYS的功能和特性，并加入了Git相关的功能。通过Git Bash，用户可以在Windows上使用Git命令和操作，以及执行类Unix的命令和脚本，提供了方便的版本控制和开发环境。

# msys 和msys2区别

MSYS（Minimal SYStem）和MSYS2是两个不同的项目，它们有一些区别。

1. 发展历史：MSYS是早期的项目，而MSYS2是MSYS的后续版本和改进版本。

2. 软件包管理器：MSYS使用了旧的软件包管理器，称为"mingw-get"，而MSYS2引入了一个新的软件包管理器，称为"Pacman"，它是Arch Linux发行版所使用的包管理器。

3. 软件包更新：MSYS的软件包更新相对较少，而MSYS2的软件包更新更频繁，并且可以提供较新的软件包版本。

4. 软件包数量：MSYS的软件包数量较少，而MSYS2的软件包数量更丰富，包括了更多的开发工具、库和应用程序。

5. Windows版本支持：MSYS只支持32位Windows操作系统，而MSYS2可以同时支持32位和64位的Windows操作系统。

综上所述，MSYS2是对MSYS的改进和升级版本，它引入了新的软件包管理器和更新的软件包版本，提供更好的软件包支持和更广泛的Windows版本支持。因此，在选择使用MSYS还是MSYS2时，通常推荐使用MSYS2来获得更好的体验和更丰富的功能。

# msys2和cygwin区别

MSYS2和Cygwin是两种在Windows操作系统上提供类Unix环境的工具集，它们有一些区别。

1. 发展历史：MSYS2是相对较新的项目，而Cygwin则更早被开发和使用。

2. 软件包管理器：MSYS2使用"Pacman"作为软件包管理器，而Cygwin使用自己的"setup.exe"作为软件包管理器。Pacman是Arch Linux发行版所使用的包管理器，更加现代化和高效。

3. 软件包数量：MSYS2的软件包数量相对较多，包括了更多的开发工具、库和应用程序。Cygwin的软件包数量也很丰富，但可能不如MSYS2那么全面。

4. 性能：由于MSYS2是基于MinGW（Minimalist GNU for Windows）构建的，它更接近原生Windows环境，因此在性能方面可能更好一些。Cygwin则提供了更完整的POSIX兼容性，但可能会对性能产生一些影响。

5. Windows API 支持：Cygwin提供了对Windows API的较好支持，可以使用Cygwin开发应用程序并直接访问Windows系统功能。MSYS2主要关注提供GNU开发工具链和类Unix环境，对于Windows API的支持相对较少。

综上所述，MSYS2更注重提供类Unix环境下的开发工具和环境，软件包管理更现代化和高效。Cygwin则提供了更完整的POSIX兼容性和对Windows API的支持。选择使用哪个工具取决于具体需求，如果需要更接近原生Windows环境的开发工具和性能，可以选择MSYS2；如果需要更完整的Unix环境和对Windows API的支持，可以选择Cygwin。



# 参考资料

1、Cygwin、Msys、MinGW、Msys2的区别与联系(转)

https://www.cnblogs.com/tshua/p/5932501.html

2、用MinGW和MSYS搭建windows下的linux环境仿真器

https://blog.csdn.net/haifeng_gu/article/details/52652808

3、Windows下为 Eclipse 配置 C/C++ 编译环境（转）

https://www.cnblogs.com/hezhiyao/p/8533808.html

4、C++ 11开发环境搭建（Windows Platform）

https://blog.csdn.net/chuchus/article/details/37774027

5、在Eclipse中实现C++ 11的完整支持

https://blog.csdn.net/lx_ros/article/details/72354211

6、Eclipse使用之C++11语法提示功能配置

https://blog.csdn.net/zhanghm1995/article/details/80879245