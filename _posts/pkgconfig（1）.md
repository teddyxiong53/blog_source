---
title: pkgconfig（1）
date: 2024-04-15 13:34:17
tags:
	- Linux

---

--

# pkgconfig简介

pkg-config 是一个用于检索已安装软件包的元数据的工具，

==主要用于编译和链接时的依赖管理。==

它通常用于 Unix-like 系统中的软件开发。

pkg-config ==允许开发者查询已安装软件包的元数据，==

如编译选项、链接标志、版本信息等，以便在编译和链接软件时正确地指定依赖关系。

使用 pkg-config，开发者可以避免手动编写复杂的编译和链接命令，

而是使用 pkg-config 提供的信息来自动生成这些命令。

这样可以使软件包的构建更加简洁、可维护性更高，并且可以更轻松地管理软件包之间的依赖关系。

通常，软件包的开发者会提供一个以 `.pc` 为后缀的 pkg-config 描述文件，其中包含了该软件包的元数据信息。

然后，开发者可以使用 `pkg-config` 命令来查询这些信息，例如：

```
pkg-config --cflags <package>     # 获取编译选项
pkg-config --libs <package>       # 获取链接标志
pkg-config --modversion <package> # 获取软件包版本信息
```

pkg-config 在许多开源项目中被广泛使用，是构建和管理软件包依赖关系的重要工具之一。

# buildroot里新增的package怎么添加pkgconfig信息

要在 Buildroot 中为新增的 package 添加 pkg-config 信息，你需要：

1. 在 package 的目录下创建一个 `.pc` 文件，命名为 `<package_name>.pc`，内容包括该 package 的 pkg-config 信息。
2. 在 package 的 `.mk` 文件中添加适当的安装命令，以将 `.pc` 文件复制到正确的位置。
3. 确保 Buildroot 的配置中启用了 pkg-config 工具链。

以下是一个示例，假设你的 package 名称为 `example`：

1. 在 `package/example/` 目录下创建一个名为 `example.pc` 的文件，内容类似于以下内容：

   ```
   prefix=/usr
   exec_prefix=${prefix}
   libdir=${exec_prefix}/lib
   includedir=${prefix}/include

   Name: Example
   Description: Example package description
   Version: 1.0.0
   Libs: -L${libdir} -lexample
   Cflags: -I${includedir}
   ```

   这是一个示例的 `.pc` 文件，你需要根据你的 package 的实际情况来编写。

2. 在 `package/example/example.mk` 文件中添加以下内容，以将 `.pc` 文件安装到正确的位置：

   ```makefile
   define EXAMPLE_INSTALL_TARGET_CMDS
       $(INSTALL) -D -m 644 $(@D)/example.pc $(TARGET_DIR)/usr/lib/pkgconfig/example.pc
   endef
   ```

   这个命令会将 `example.pc` 文件安装到目标系统的 `/usr/lib/pkgconfig/` 目录下。

3. 确保 Buildroot 的配置中启用了 pkg-config 工具链。你可以在 `make menuconfig` 的 `Toolchain` 菜单中检查并确保启用了 `Enable pkg-config` 选项。

添加完 pkg-config 信息后，重新构建 Buildroot 并编译你的 package，pkg-config 将会识别到你的 package 并在编译其他软件时使用它。

## 假如我有一个名字为foo的包，依赖了上面的example包，怎么通过pkgconfig去搜索和使用上面的example包

要在你的包 `foo` 中使用 pkg-config 来搜索和使用依赖的 `example` 包，你需要：

1. 在 `foo` 包的 `.mk` 文件中，指定 `example` 包的 pkg-config 名称，并添加对应的编译选项和链接选项。

2. 在 `foo` 包的 `.mk` 文件中，确保指定正确的头文件和库文件路径，以便编译器和链接器能够找到 `example` 包提供的头文件和库文件。

下面是一个示例，在 `foo` 包的 `.mk` 文件中，如何使用 pkg-config 来搜索和使用 `example` 包：

```makefile
FOO_DEPENDENCIES += example

FOO_CONF_OPTS += $(shell PKG_CONFIG_PATH=$(STAGING_DIR)/usr/lib/pkgconfig pkg-config --cflags example)
FOO_LDFLAGS += $(shell PKG_CONFIG_PATH=$(STAGING_DIR)/usr/lib/pkgconfig pkg-config --libs example)
```

上面的示例中，`FOO_DEPENDENCIES` 变量用于指定 `foo` 包的依赖关系，确保在编译 `foo` 包之前先编译 `example` 包。然后，`FOO_CONF_OPTS` 和 `FOO_LDFLAGS` 变量使用 `pkg-config` 命令来获取 `example` 包的编译选项和链接选项，并将其传递给编译器和链接器。

确保在 `foo` 包的 `.mk` 文件中添加这些内容，并根据需要调整路径和其他选项，以适应你的实际情况。然后重新构建 Buildroot，并编译你的包 `foo`，它将会使用 pkg-config 来正确地搜索和使用依赖的 `example` 包。





https://jasonblog.github.io/note/linux_system/1513.html