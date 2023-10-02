---
title: xmake（1）
date: 2023-06-06 10:41:11
tags:
	- 编译
---

--

# xmake发展历史

XMake 的发展历史如下：

1. 2011年：XMake 诞生。最初的 XMake 版本是由 hongliangpan 开发的一个简单的构建工具。它的设计目标是提供一种简单的构建方式，使开发者可以快速地构建 C/C++ 项目。

2. 2013年：引入 Lua 脚本支持。为了提供更灵活和可扩展的构建配置，XMake 引入了 Lua 脚本作为构建配置的脚本语言。开发者可以使用 Lua 脚本编写构建规则和自定义构建过程。

3. 2015年：全面重构。为了改进 XMake 的性能和可扩展性，XMake 在这一年进行了全面的重构。它引入了基于 Lua 的构建脚本和插件系统，使用户能够更好地定制和扩展构建过程。

4. 2016年：支持更多平台。XMake 进一步扩展了其跨平台能力，支持更多的操作系统，包括 Windows、MacOS、Linux 和 FreeBSD。

5. 2017年：增加包管理功能。为了方便项目的依赖管理，XMake 增加了包管理功能，支持下载和安装第三方库和工具。

6. 2018年：支持更多语言。除了 C/C++，XMake 还增加了对其他编程语言的支持，包括 Rust、Golang、Swift 等。

7. 2019年：持续改进和增强。XMake 团队在每个版本中持续改进和增强 XMake 的功能和性能，修复 bug，提供更好的用户体验。

8. 至今：XMake 继续发展。目前，XMake 仍在积极开发和改进中，持续推出新版本，并与社区合作，吸收用户反馈和贡献，以满足开发者在构建方面的需求。

总体而言，XMake 是一个持续发展和不断改进的跨平台构建工具，旨在提供简单、灵活和可扩展的构建解决方案，使开发者能够轻松地构建和管理 C/C++ 项目。



# 安装

这个本质上是编译安装的。

```
wget https://xmake.io/shget.text -O - | bash
```

安装后执行：

```
source ~/.xmake/profile
```

把这个加到.bash_profile里。命令基本语法：

```
xmake [task] [options] [target]
```

任务、选项、目标。

如果没有给定task，那么默认就是执行build任务。

一些任务和缩写：

```
r == run 运行target
i == install 安装target
p == package 打包target
q == require 安装依赖的包
f == config 配置project
b == build 构建target
u == uninstall 卸载
g == global 全局配置
c == clean 清理。
```



## 子命令

输入xmake，然后按tab补全提示的子目录有这些：

```
build
clean
create
format
install
macro
plugin
repo
run
show
update
check
config
doxygen
global
lua
package
project
require
service
uninstall
watch
```

# helloworld

创建 名为hello的控制台工程。

```
xmake create -l c -P ./hello
```

创建过程的打印：

```
create hello ...
  [+]: src/main.c
  [+]: xmake.lua
  [+]: .gitignore
create ok!
```

得到的目录结构：

```
.
└── hello
    ├── src
    │   └── main.c
    └── xmake.lua
```

然后在hello目录下执行：

```
xmake 
```

这样就执行了构建操作。

```
checking for platform ... linux
checking for architecture ... x86_64
[ 25%]: cache compiling.release src/main.c
[ 50%]: linking.release hello
[100%]: build ok, spent 1.357s
```

然后可以调试程序：

需要先调整到debug模式进行编译。

```
xmake config -m debug
xmake
```

然后执行debug：

```
xmake run -d hello 
```

# 目录有多层嵌套，头文件也分散在各处

如果您的工程目录结构是多层嵌套的，并且头文件分散在各个目录中，您可以在xmake.lua文件中使用递归添加目录的方式来处理。

以下是一个示例，假设您的工程目录结构如下：

```
project/
├─ src/
│  ├─ main.c
│  ├─ subdir1/
│  │  ├─ file1.c
│  │  └─ file1.h
│  └─ subdir2/
│     ├─ file2.c
│     └─ subdir3/
│        ├─ file3.c
│        └─ file3.h
└─ include/
   └─ common/
      └─ common.h
```

您可以按照以下方式在xmake.lua文件中配置：

```lua
-- 添加头文件搜索路径
add_includedirs("include")

-- 递归添加源文件
target("demo")
    set_kind("binary")
    add_files("src/*.c") -- 添加根目录下的.c文件

    -- 递归添加子目录下的.c文件
    add_files("src/subdir1/*.c", "src/subdir2/*.c", "src/subdir2/subdir3/*.c")

    -- 添加头文件
    add_includedirs("src/subdir1", "src/subdir2/subdir3", "include/common")

    -- 设置编译选项
    add_cflags("-Wall")
    add_cxxflags("-std=c++11")
```

在上面的示例中，通过使用通配符`*`来匹配不同层级的目录和文件，递归地添加了源文件和头文件的路径。您可以根据实际情况进行相应的调整。

请注意，如果您的工程目录结构非常复杂，可能需要更多的配置和匹配规则来确保正确地包含所有的源文件和头文件。

# xmake f == xmake config

这2个是等价的。

# xmake.lua写法

# 基本命令

假设我的项目名字叫lacpp：

```
# 创建项目
xmake create -l c++ -t console lacpp
# 配置项目
xmake config -p linux -a x86_64 -m debug
# 编译项目
xmake build lacpp
# 运行项目
xmake run lacpp
```

## 调试

```
xmake config -m debug
# 这个就启动了gdb来运行了，你可以指定调试器：xmake config --debugger=lldb
xmake run -d lacpp
```

# 工程例子

https://github.com/xmake-io/xmake/tree/master/tests/projects

## 编译动态库

```
add_rules("mode.debug", "mode.release")

target("foo")
    set_kind("shared")
    add_files("src/foo.cpp")

target("demo")
    set_kind("binary")
    add_deps("foo")
    add_files("src/main.cpp")

```

# 多层目录结构

对于一些轻量型的小工程，通常只需要单个xmake.lua文件就能搞定，大体结构如下：

```
projectdir
  - xmake.lua
  - src
    - test
      - *.c
    - demo
      - *.c
```

xmake.lua：

```
-- 在根域设置通用配置，当前所有targets都会生效
add_defines("COMMON")

target("test")
    set_kind("static")
    add_files("src/test/*.c")
    add_defines("TEST")

target("demo")
    set_kind("static")
    add_files("src/demo/*.c")
    add_defines("DEMO")
```

但是对于一些大型项目，通常的组织结构层次很多也很深，需要编译的target目标也可能有十几甚至上百个，这个时候如果还是都在根xmake.lua文件中维护，就有点吃不消了。

这个时候，我们就需要通过在每个子工程模块里面，单独创建xmake.lua来维护他们，然后使用xmake提供的includes接口，将他们按层级关系包含进来，最终变成一个树状结构：

```
projectdir
  - xmake.lua
  - src
    - test
      - xmake.lua
      - test1
        - xmake.lua
      - test2
        - xmake.lua
      - test3
        - xmake.lua
    - demo
      - xmake.lua
      - demo1
        - xmake.lua
      - demo2
        - xmake.lua
    ...
```

然后，根xmake.lua会将所有子工程的xmake.lua通过层级includes全部引用进来，那么所有定义在子工程的target配置也会完全引用进来，我们在编译的时候永远不需要单独去切到某个子工程目录下操作，只需要：

```
$ xmake build test1
$ xmake run test3
$ xmake install demo1
```

就可以编译，运行，打包以及安装指定的子工程target，所以除非特殊情况，平常不推荐来回切换目录到子工程下单独编译，非常的繁琐。

通常推荐的做法就是在根xmake.lua中仅仅配置一些对所有target都通用的设置，以及includes对子工程的引用，不放置对targets的定义，例如：

```
-- define project
set_project("tbox")
set_xmakever("2.3.2")
set_version("1.6.5", {build = "%Y%m%d%H%M"})

-- set common flags
set_warnings("all", "error")
set_languages("c99")
add_cxflags("-Wno-error=deprecated-declarations", "-fno-strict-aliasing", "-Wno-error=expansion-to-defined")
add_mxflags("-Wno-error=deprecated-declarations", "-fno-strict-aliasing", "-Wno-error=expansion-to-defined")

-- add build modes
add_rules("mode.release", "mode.debug")

-- includes sub-projects
includes("test", "demo")
```



https://tboox.org/cn/2020/04/11/quickstart-11-subprojects/

https://blog.csdn.net/hx1113/article/details/127331035

# 添加头文件搜索路径

```
 -- 设置使用的交叉编译工具链
set_toolchains("arm-linux-gnueabihf")  

-- -- 设置平台
set_plat("cross")
-- 设置架构
set_arch("arm")

set_languages("c99", "c++11")

-- 设置链接库搜索路径
add_linkdirs("/opt/tslib-1.21/lib")  
add_linkdirs("/home/ares/work/tmp_lib/ffmpeg/lib")   
add_linkdirs("/home/ares/work/tmp_lib/x264/lib")   
--add_linkdirs("/usr/local/arm_gcc/gcc-linaro-4.9.4-2017.01-i686_arm-linux-gnueabihf/arm-linux-gnueabihf/libc/usr/lib")
-- 设置链接的库
add_links("m", "pthread", "ts")
add_deps("lvglv8")
add_links("x264")
add_links("avformat", "avcodec", "avutil", "swscale", "swresample", "m", "pthread")

--  add_cflags(
--     "-O3"
--  )

local lvgl_src_path = {
--    "lvgl/src/",
    "lvgl/demos/",
    "lv_drivers/"
}

for _, index in ipairs(lvgl_src_path) do
    for _, dir in ipairs(os.dirs(index.."/**")) do
        add_files(dir.."/*.c") 
        add_includedirs(dir)
    end
end

add_includedirs("lvgl")
add_files("lvgl/examples/libs/ffmpeg/*.c") 
add_includedirs("lvgl/examples/libs/ffmpeg")

local usr_src_path = {
    ".",
    "multimedia",
    "multimedia/font",
    "multimedia/img/camera",
    "multimedia/img/desktop",
    "multimedia/img/light",
    "multimedia/img/music",
    "multimedia/img/time", 
    "multimedia/img/video",
    "multimedia/img/weather",
}

for _, dir in ipairs(usr_src_path) do
    add_files(dir.."/*.c");  
end

remove_files("multimedia/font/myFontDailyWeather.c")
remove_files("multimedia/font/myFont_Foshan.c")
remove_files("multimedia/font/myFontNumber.c")

add_includedirs(".")   
add_includedirs("/opt/tslib-1.21/include")
add_includedirs("/home/ares/work/tmp_lib/x264/include")

-- add_includedirs("th3lib/include/libavcodec") 
-- add_includedirs("th3lib/include/libavfilter") 
-- add_includedirs("th3lib/include/libavutil") 
-- add_includedirs("th3lib/include/libswresample") 
-- add_includedirs("th3lib/include/libavdevice") 
-- add_includedirs("th3lib/include/libavformat") 
-- add_includedirs("th3lib/include/libpostproc") 
-- add_includedirs("th3lib/include/libswscale") 
-- add_includedirs("/home/ares/work/tmp_lib/ffmpeg/include/")

-- add_includedirs("th3lib/include/")
add_includedirs("/home/ares/work/tmp_lib/ffmpeg/include/")

-- local ffmpeg_inc = { 
--     "/home/ares/work/tmp_lib/ffmpeg/include/libavcodec",
--     "/home/ares/work/tmp_lib/ffmpeg/include/libavfilter",
--     "/home/ares/work/tmp_lib/ffmpeg/include/libavutil",
--     "/home/ares/work/tmp_lib/ffmpeg/include/libswresample",
--     "/home/ares/work/tmp_lib/ffmpeg/include/libavdevice",
--     "/home/ares/work/tmp_lib/ffmpeg/include/libavformat",
--     "/home/ares/work/tmp_lib/ffmpeg/include/libpostproc",
--     "/home/ares/work/tmp_lib/ffmpeg/include/libswscale",
-- }
-- for _, ffmpeg in ipairs(ffmpeg_inc) do  
--     add_includedirs(ffmpeg)
-- end

-- -- 递归遍历获取所有子目录
-- for _, dir in ipairs(os.dirs("lvgl/src/**")) do
--     add_files(dir.."/*.c");    
--     add_includedirs(dir);
-- end

-- -- 递归遍历获取所有子目录
-- for _, dir in ipairs(os.dirs("lvgl/demos/**")) do
--     add_files(dir.."/*.c");   -- 添加目录下所有C文件
--     add_includedirs(dir);  -- 添加目录作为头文件搜索路径
-- end

-- for _, v in ipairs(os.dirs("lv_drivers/**")) do
--     add_files(v.."/*.c");
--     add_includedirs(v);
-- end

after_build(
    function(target)
    cprint("Compile finished!!!")

    print(" ")
    os.exec("sudo cp build/cross/arm/release/mutlimedia /mnt/nfs/")  
end)`
```



https://github.com/xmake-io/xmake/issues/2794

# xmake api梳理

## [命名规范](https://xmake.io/#/zh-cn/manual/specification?id=命名规范)

接口的命名，是有按照预定义的一些规范来命名的，这样更加方便理解和易于使用，目前命名按照如下一些规则：

| 接口规则                | 描述                                                         |
| ----------------------- | ------------------------------------------------------------ |
| `is_`, `has_`前缀的接口 | 表示为条件判断                                               |
| `set_`前缀的接口        | 表示为覆盖设置                                               |
| `add_`前缀的接口        | 表示为追加设置                                               |
| `s`后缀的接口           | 表示支持多值传入，例如：`add_files("*.c", "test.cpp")`       |
| `on_`前缀的接口         | 表示为覆盖内置脚本                                           |
| `before_`前缀的接口     | 表示为在内置脚本运行前，执行此脚本                           |
| `after_`前缀的接口      | 表示为在内置脚本运行后，执行此脚本                           |
| `scope("name")`的接口   | 表示为定义一个描述域，例如：`target("xxx")`, `option("xxx")` |
| 描述域/描述设置         | 建议缩进表示                                                 |



# 常用的函数

# 自定义toolchain

另外，我们也可以在xmake.lua中自定义toolchain，然后通过`set_toolchains`指定进去，例如：

```lua
toolchain("myclang")
    set_kind("standalone")
    set_toolset("cc", "clang")
    set_toolset("cxx", "clang", "clang++")
    set_toolset("ld", "clang++", "clang")
    set_toolset("sh", "clang++", "clang")
    set_toolset("ar", "ar")
    set_toolset("ex", "ar")
    set_toolset("strip", "strip")
    set_toolset("mm", "clang")
    set_toolset("mxx", "clang", "clang++")
    set_toolset("as", "clang")

    -- ...
```

https://github.com/xmake-io/xmake-repo/blob/dev/packages/l/luajit/port/xmake.lua

# xmake config --menu配置

# xrepo的用法

https://github.com/xmake-io/xmake-repo

xrepo是xmake构建工具的扩展包管理器，可以用于管理和安装第三方包和依赖项。以下是xrepo的一些常用用法：

1. 初始化仓库：使用`xrepo init`命令初始化仓库，该命令会在当前目录下创建一个`.xrepo`文件夹用于存储仓库信息和缓存。

2. 添加仓库：使用`xrepo add <name> <url>`命令添加仓库，该命令会添加一个新的仓库到仓库列表中。其中，`<name>`是仓库名称，`<url>`是仓库地址。

3. 安装包：使用`xrepo install <name>`命令安装包，该命令会从仓库中下载并安装指定的包及其依赖项。其中，`<name>`是要安装的包名称，可以是完整的包名称或包名称的一部分。

4. 卸载包：使用`xrepo remove <name>`命令卸载包，该命令会卸载指定的包及其依赖项。其中，`<name>`是要卸载的包名称。

5. 搜索包：使用`xrepo search <name>`命令搜索包，该命令会从仓库中搜索指定名称的包。其中，`<name>`是要搜索的包名称，可以是完整的包名称或包名称的一部分。

6. 更新仓库：使用`xrepo update`命令更新仓库，该命令会从仓库中更新包的信息和版本信息。

7. 清理缓存：使用`xrepo clear`命令清理缓存，该命令会清理仓库中的缓存和临时文件。

8. 列出已安装的包：使用`xrepo list`命令列出已安装的包，该命令会显示当前仓库中已安装的所有包及其版本信息。

9. 列出可用的包：使用`xrepo list <name>`命令列出可用的包，该命令会显示当前仓库中与指定名称匹配的所有包及其版本信息。其中，`<name>`是要列出的包名称，可以是完整的包名称或包名称的一部分。

以上是xrepo的一些常用用法，使用xrepo可以方便地管理和安装第三方包和依赖项，提高开发效率。



它基于 xmake 提供的运行时，但却是一个完整独立的包管理程序，相比 vcpkg/homebrew 此类包管理器，xrepo 能够同时提供更多平台和架构的 C/C++ 包。

并且还支持多版本语义选择，另外它还是一个去中心化的分布式仓库，不仅仅提供了官方的 [xmake-repo](https://github.com/xmake-io/xmake-repo) 仓库，还支持用户自建多个私有仓库。

package的仓库在这里：

https://github.com/xmake-io/xmake-repo/tree/master/packages

以cjson的为例：

https://github.com/xmake-io/xmake-repo/blob/master/packages/c/cjson/xmake.lua

```
package("cjson")

    set_homepage("https://github.com/DaveGamble/cJSON")
    set_description("Ultralightweight JSON parser in ANSI C.")
    set_license("MIT")

    set_urls("https://github.com/DaveGamble/cJSON/archive/v$(version).zip",
             "https://github.com/DaveGamble/cJSON.git")
    add_versions("1.7.10", "80a0584410656c8d8da2ba703744f44d7535fc4f0778d8bf4f980ce77c6a9f65")
    add_versions("1.7.14", "d797b4440c91a19fa9c721d1f8bab21078624aa9555fc64c5c82e24aa2a08221")
    add_versions("1.7.15", "c55519316d940757ef93a779f1db1ca809dbf979c551861f339d35aaea1c907c")

    add_deps("cmake")

    on_install("windows", "macosx", "linux", "iphoneos", "android", function (package)
        local configs = {"-DENABLE_CJSON_TEST=OFF"}
        table.insert(configs, "-DCMAKE_BUILD_TYPE=" .. (package:debug() and "Debug" or "Release"))
        table.insert(configs, "-DBUILD_SHARED_LIBS=" .. (package:config("shared") and "ON" or "OFF"))
        import("package.tools.cmake").install(package, configs)
    end)

    on_test(function (package)
        assert(package:has_cfuncs("cJSON_malloc", {includes = "cjson/cJSON.h"}))
    end)
```



## 参考资料

1、

https://xrepo.xmake.io/#/zh-cn/

# xmake的描述域和脚本域

xmake是一个基于Lua语言的跨平台构建工具，**它的配置文件分为描述域和脚本域两个部分，分别用于描述项目和编写构建脚本。**

**描述域是xmake配置文件的静态部分**，用于描述项目的基本信息、编译选项、依赖项等。在描述域中，可以使用一些预定义的关键字和函数来定义项目的属性，例如：

- `set_project()`：设置项目的名称、版本号和描述信息。
- `add_rules()`：添加构建规则，例如C/C++编译器规则、静态库规则等。
- `add_requires()`：添加依赖项，例如第三方库、工具链等。
- `add_files()`：添加源代码文件和头文件。
- `add_defines()`：添加编译时宏定义。
- `add_linkdirs()`：添加链接库的搜索路径。
- `add_links()`：添加链接的库。

**脚本域是xmake配置文件的动态部分，**用于编写构建脚本和自定义构建过程。在脚本域中，可以使用Lua语言编写构建脚本，例如定义自定义任务、编写构建脚本、设置环境变量等。脚本域中可以使用描述域中定义的变量和函数，以及一些预定义的变量和函数，例如：

- `_G`：全局变量表，可以用于定义全局变量和函数。
- `_ARGV`：命令行参数列表。
- `_HOST`：当前主机系统的信息。
- `_ARCH`：当前编译架构的信息。
- `_OPTIONS`：当前选项的信息。
- `_ACTION`：当前执行的动作（例如build、clean、install等）。

通过描述域和脚本域的结合，可以方便地定义项目的属性和自定义构建过程，实现灵活、高效的构建流程。

# 循环遍历添加同一类型的target

我的需求来源是，我的本地有一堆的test-xx.c的文件。要一个个编译成对应的可执行文件。

https://github.com/xmake-io/xmake/issues/1938

# xmake环境变量

```
$ xmake show -l envs
XMAKE_RAMDIR            Set the ramdisk directory.
                        
XMAKE_GLOBALDIR         Set the global config directory of xmake.
                        /Users/ruki/.xmake
XMAKE_ROOT              Allow xmake to run under root.
                        
XMAKE_COLORTERM         Set the color terminal environment.
                        
XMAKE_PKG_INSTALLDIR    Set the install directory of packages.
                        
XMAKE_TMPDIR            Set the temporary directory.
                        /var/folders/vn/ppcrrcm911v8b4510klg9xw80000gn/T/.xmake501/211104
XMAKE_PKG_CACHEDIR      Set the cache directory of packages.
                        
XMAKE_PROGRAM_DIR       Set the program scripts directory of xmake.
                        /Users/ruki/.local/share/xmake
XMAKE_PROFILE           Start profiler, e.g. perf, trace.
                        
XMAKE_RCFILES           Set the runtime configuration files.

XMAKE_CONFIGDIR         Set the local config directory of project.
                        /Users/ruki/projects/personal/xmake-docs/.xmake/macosx/x86_64
XMAKE_LOGFILE           Set the log output file path.
```



# XMAKE_RCFILES

看rt-smart的userapps里，有这样使用：

XMAKE_RCFILES           Set the runtime configuration files.

# 使用xmake开发Android程序

# windows安装xmake

在

```
Invoke-Expression (Invoke-Webrequest 'https://raw.githubusercontent.com/tboox/xmake/master/scripts/get.ps1' -UseBasicParsing).Content
```