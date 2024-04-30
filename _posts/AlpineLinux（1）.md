---
title: AlpineLinux（1）
date: 2024-04-29 10:29:17
tags:
	- Linux

---

--

我觉得还是有必要对alpine linux进行深入研究，所以这篇笔记就是记录相关的知识点。

# 资料收集

不错的笔记

https://wener.me/notes/os/alpine

# 基于alpine的系统

## 手机系统

https://wiki.postmarketos.org/wiki/Main_Page

# 为什么使用alpine

阿里云、腾讯云、物理服务器、虚拟机、容器都是用的 alpinelinux

1. 环境都一样，使用各方面熟悉，熟练
2. 小/快 - 阿里云 ECS 只需要上传一个 几十 MB 的镜像即可，从 0 安装只需要 3 分钟
3. 简单 - ==可以由内而外的了解所有 alpine 细节，对于 debian 和 centos 我都做不到，因为太复杂==
4. 跟上时代 - 内核 一般是最近的 lts，能快速利用上新的内核特性，比如现在 linux 内核支持 io_uring, ntfs
5. 快速更新 - 安全问题响应非常快 - 因为使用面非常广
6. 衍生业务集成系统 - 系统预装一些软件和服务 - 例如: k3sos

**不适用场景**

1. 机器学习 - ubuntu 是最好的 - 最新 Linux 开始要集成 Navdia 驱动，情况会有所好转
2. 商务用桌面系统 - 默认 xface - *生态* 和体验没有 ubuntu 好
3. 定制化嵌入式设备 - alpine 支持的 arch 远没有 debian 的多，如果 arch 支持可以考虑 alpine



## 优点

> Alpine Linux 是一个基于 musl libc 和 busybox, 面向安全, 轻量级的 Linux 发布版.

- 开源
- 轻量级
  - 最小安装 5MB
  - 大部分都是静态链接
  - musl
  - openrc
- 稳定滚动升级
  - 有稳定版和最新版
  - 每半年一个稳定版
  - 稳定版会维护两年
  - 可非常简便的升级
- 简单的包管理
  - Apk
  - 包的构建也很简单
- 现代化
  - 内核版本较新
    - 能够利用上很多新内核的功能
  - 包版本比较新
    - 例如 zfs, docker 等都是对应版本的最新版
- 生态圈丰富
  - 包非常多
- 支持较多平台
  - x86
  - x86_64
  - armhf
  - armv7
  - aarch64
  - ppc64le
  - s390x
- 支持树莓派
- 很多 docker 镜像基于 AlpineLinux
  - Docker For Mac 的基础系统是 AlpineLinux

# 从源代码开始编译alpine

是的，你可以从零开始编译Alpine Linux的镜像。Alpine Linux的源代码托管在GitLab上，你可以获取源代码并按照官方文档的指引进行编译。

以下是从头开始编译Alpine Linux镜像的基本步骤：

1. **获取源代码**：首先，你需要克隆Alpine Linux的源代码仓库。你可以通过GitLab上的官方仓库获取源代码。使用以下命令克隆仓库：

   ```
   git clone https://gitlab.alpinelinux.org/alpine/aports.git
   ```

2. **配置构建环境**：接下来，你需要配置构建Alpine Linux镜像的环境。你可以在克隆的仓库中找到有关构建环境的文档和脚本。通常，你需要一个Linux系统和一些基本的开发工具，如gcc、make等。

3. **选择架构和版本**：Alpine Linux支持多种架构，包括x86、x86_64、ARM等。你需要选择你要构建的目标架构，并决定要构建的Alpine Linux版本（如最新稳定版或开发版）。

4. **配置构建选项**：你可以根据自己的需求配置Alpine Linux的构建选项，比如默认安装哪些软件包、内核配置等。

5. **开始编译**：一切准备就绪后，你可以开始编译Alpine Linux镜像了。通常，你需要运行一些构建脚本或命令来开始构建过程。这个过程可能需要一些时间，具体取决于你的硬件性能和网络速度。

6. **测试和验证**：一旦编译完成，你可以在虚拟机或物理设备上测试和验证你构建的Alpine Linux镜像。确保它可以正常启动并运行你期望的功能。

aports就是一个类似buildroot的东西。

里面的目录下放了大量的package的配置。不过它是用APKBUILD，而不是makefile的方式。

就以main/7zip这个包的为例，看APKBUILD 的内容：

```
# Maintainer: Alex Xu (Hello71) <alex_y_xu@yahoo.ca>
pkgname=7zip
pkgver=23.01
_pkgver=${pkgver//./}
pkgrel=0
pkgdesc="File archiver with a high compression ratio"
url="https://7-zip.org/"
arch="all"
license="LGPL-2.0-only"
subpackages="$pkgname-doc"
source="https://7-zip.org/a/7z$_pkgver-src.tar.xz
	armv7.patch
	7-zip-flags.patch
	7-zip-musl.patch
	"
builddir="$srcdir"

provides="7zip-virtual p7zip=$pkgver-r$pkgrel"
replaces="p7zip"
provider_priority=100

build() {
	cd CPP/7zip/Bundles/Alone2
	mkdir -p b/g
	# TODO: enable asm (requires jwasm or uasm)
	# DISABLE_RAR: RAR codec is non-free
	# -D_GNU_SOURCE: broken sched.h defines
	make -f ../../cmpl_gcc.mak \
		CC="${CC:-cc} $CFLAGS $LDFLAGS -D_GNU_SOURCE" \
		CXX="${CXX:-c++} $CXXFLAGS $LDFLAGS -D_GNU_SOURCE" \
		DISABLE_RAR=1
}

check() {
	# no proper test suite so just try to compress and decompress some files
	mkdir tmp
	CPP/7zip/Bundles/Alone2/b/g/7zz a tmp/7z$_pkgver-src.7z Asm C CPP DOC
	cd tmp
	../CPP/7zip/Bundles/Alone2/b/g/7zz x 7z$_pkgver-src.7z
	# TODO: check if extracted result is identical
}

package() {
	install -Dm755 CPP/7zip/Bundles/Alone2/b/g/7zz "$pkgdir"/usr/bin/7zz
	ln -s 7zz "$pkgdir"/usr/bin/7z

	install -Dm644 "$builddir"/DOC/* -t "$pkgdir"/usr/share/doc/$pkgname/
}

sha512sums="
e39f660c023aa65e55388be225b5591fe2a5c9138693f3c9107e2eb4ce97fafde118d3375e01ada99d29de9633f56221b5b3d640c982178884670cd84c8aa986  7z2301-src.tar.xz
e52e542709a23ced76b651adf54609efae705801e940e74310ae4e67070bdb3841da5b801362aa0329b77993cdc3f6cd63ac2802240b16cde865f9d01bb1936d  armv7.patch
dfecb69861d00ee47311d83930adf80321b3c95ae01ce325677bde7aee6aa880a1979b0aa2909d9acb7a88ff31f910ac545ac218a0b5fd9e1270df2276b46d44  7-zip-flags.patch
c652a87ad95f61901820adb61f3d1ceacedcb8aeaf9e89b2b728b7372eff67d9669eb363d5b2d2fb848ff2d8c5a727134fe13cc77d1215df7b2d32fe87711ebf  7-zip-musl.patch
"
```

## 在ubuntu下编译alpine

在Ubuntu下编译Alpine Linux可能有些挑战，因为Alpine Linux和Ubuntu有不同的软件包管理系统和依赖项。不过，你可以尝试使用Docker容器来模拟Alpine Linux的环境，并在其中进行编译。以下是大致的步骤：

1. **安装Docker**：如果你的Ubuntu系统上还没有安装Docker，你需要先安装Docker。你可以按照官方文档或使用apt安装Docker。

   ```
   sudo apt update
   sudo apt install docker.io
   ```

2. **创建并运行Alpine Linux容器**：你可以使用Docker来创建一个Alpine Linux的容器，并在其中进行编译。

   ```
   docker run -it alpine /bin/sh
   ```

   这将启动一个新的Alpine Linux容器，并进入其shell。

3. **在容器中编译Alpine Linux**：在Alpine Linux容器中，你可以按照Alpine Linux的官方文档指引，克隆Alpine Linux的源代码仓库，并使用提供的脚本进行编译。

   ```
   git clone https://gitlab.alpinelinux.org/alpine/aports.git
   cd aports
   ./scripts/mkimage.sh
   ```

4. **等待编译完成**：编译过程可能需要一些时间，具体取决于你的系统性能和网络速度。等待编译完成后，你将在容器中得到Alpine Linux的镜像文件。

5. **将镜像从容器中导出**：一旦编译完成，你可以将Alpine Linux的镜像文件从容器中导出到宿主机上。

   ```
   docker cp CONTAINER_ID:/path/to/alpine_image.tar.gz /local/path
   ```

   其中，`CONTAINER_ID`是你运行的Alpine Linux容器的ID，`/path/to/alpine_image.tar.gz`是Alpine Linux镜像文件在容器中的路径，`/local/path`是你想要将镜像文件导出到的本地路径。

通过这种方式，你可以在Ubuntu系统上使用Docker容器来编译Alpine Linux，并在其中获得Alpine Linux的镜像文件。

所以这个意思还是要在alpine进行alpine的编译。

## 在alpine下编译alpine

需要安装这个包：

```
 apk add \
	abuild apk-tools alpine-conf busybox fakeroot syslinux xorriso cmd:mksquashfs
	mtools grub-efi
```

# apkbuild

`apkbuild` 是 Alpine Linux 中用于构建软件包（package）的工具。使用 `apkbuild` 可以简化构建过程，并将软件包打包成 `.apk` 格式，以便在 Alpine Linux 上安装和管理。

以下是使用 `apkbuild` 的基本步骤：

1. **创建软件包目录**：首先，你需要在 Alpine Linux 的 `aports` 仓库中创建一个新的软件包目录。通常，每个软件包都有一个单独的目录，其中包含构建该软件包所需的所有文件。

2. **编写构建脚本**：在软件包目录中，你需要编写一个构建脚本（通常命名为 `APKBUILD`），其中包含构建软件包的步骤和相关信息，如软件包的名称、版本、依赖项等。

3. **运行 `apkbuild`**：一旦编写了构建脚本，你可以使用 `apkbuild` 工具来构建软件包。运行 `apkbuild` 时，它会读取 `APKBUILD` 文件，并执行其中定义的构建步骤。

4. **生成 `.apk` 文件**：`apkbuild` 工具会根据构建脚本的指示，将软件包构建成一个 `.apk` 文件。这个文件包含了软件包的二进制文件、元数据和其他必要的信息。

5. **安装软件包**：最后，你可以使用 `apk` 命令在 Alpine Linux 上安装构建的软件包。只需将 `.apk` 文件复制到目标系统，并运行 `apk add` 命令即可。

总的来说，`apkbuild` 是一个用于构建 Alpine Linux 软件包的工具，它通过简化构建过程和自动化打包步骤，使得构建和管理软件包变得更加简单和可靠。

# 怎样自己打包一个新的alpine package

要自己打包一个新的 Alpine 软件包，你需要执行以下步骤：

1. **准备工作环境**：
   - 确保你的系统中安装了 Alpine Linux 的 `abuild` 工具。如果没有安装，可以通过 `apk add abuild` 命令来安装。
   - 创建一个工作目录，用于存放你的软件包构建文件。

2. **创建构建文件**：
   - 在工作目录中创建一个新的目录，用于存放你的软件包构建文件。命名这个目录为你要打包的软件包的名称。
   - 在该目录中创建一个名为 `APKBUILD` 的文件，这是软件包构建的主要文件。`APKBUILD` 文件包含了构建软件包的所有信息和指令。
   - 编辑 `APKBUILD` 文件，填写必要的信息，比如软件包的名称、版本、描述、依赖项等。同时，在文件中定义构建过程，包括下载源代码、配置、编译和安装。

3. **构建软件包**：
   - 执行 `abuild -r` 命令来构建软件包。`-r` 选项表示构建为 root 权限。
   - `abuild` 工具会读取 `APKBUILD` 文件，并执行其中定义的构建步骤。它会下载源代码，编译软件包，并生成 `.apk` 文件。

4. **安装软件包**：
   - 构建完成后，在 `~/packages/<arch>` 目录中会生成一个 `.apk` 文件，其中 `<arch>` 是你的系统架构（如 x86、x86_64、armhf 等）。
   - 将生成的 `.apk` 文件复制到你的 Alpine Linux 系统中。
   - 使用 `apk add <package>.apk` 命令来安装软件包，其中 `<package>.apk` 是你复制的软件包文件名。

5. **测试和验证**：
   - 安装软件包后，确保它能够正常工作并符合你的预期。

通过以上步骤，你就可以自己打包一个新的 Alpine 软件包了。记得在构建过程中保持注意力，确保所有依赖项都正确安装，并且软件包构建过程中没有错误。

# alpine安装vscode

这个看起来还比较麻烦。

# alpine的代码仓库分析

https://gitlab.alpinelinux.org/

# alpine的初始化系统

在 Alpine Linux 中，`init` 系统通常由 `runit` 或 `OpenRC` 管理。这些初始化系统负责在系统引导时启动和管理各种服务，并确保系统处于正确的状态。

1. **runit**：
   - `runit` 是 Alpine Linux 默认的初始化系统之一。它使用简单的目录结构和脚本来管理服务。每个服务都由一个目录表示，其中包含了启动、停止和其他相关操作所需的脚本和配置文件。
   - 在 Alpine Linux 中，`/sbin/init` 实际上是一个符号链接，指向 `runit` 的执行文件。
   - 使用 `rc-update` 命令来管理 `runit` 的服务。例如，使用 `rc-update add <service_name>` 命令添加一个新的服务到系统启动中。

2. **OpenRC**：
   - OpenRC 是另一个常见的初始化系统，在一些 Alpine Linux 的发行版中也可用。它提供了更传统的 SysV init 风格的脚本管理方式。
   - OpenRC 的配置文件通常位于 `/etc/init.d/` 目录中，每个服务都有一个对应的脚本文件。你可以编辑这些脚本文件来管理服务的启动和停止行为。
   - 使用 `rc-update` 命令来管理 OpenRC 的服务。例如，使用 `rc-update add <service_name>` 命令添加一个新的服务到系统启动中。

在 Alpine Linux 中，你可以选择使用 `runit` 或 `OpenRC` 中的任何一个来管理系统的初始化和服务。默认情况下，Alpine Linux 使用 `runit` 作为其初始化系统，但你也可以选择安装和配置 `OpenRC` 来代替。

## openrc

rc-service  rc-sstat    rc-status   rc-update  



# s6 overlay

`s6 overlay` 是一个基于 `s6` 和 `s6-rc` 的轻量级进程管理工具，

==用于在容器化环境中管理多个服务。==

它允许你在单个容器中运行多个进程，并提供了一种简单而强大的方法来管理这些进程的生命周期和依赖关系。

以下是一些关于 `s6 overlay` 的关键特点和用法：

1. **轻量级和高效**：`s6 overlay` 采用了 `s6` 和 `s6-rc` 这两个轻量级的进程管理工具，因此具有很小的内存占用和启动时间。

2. **容器友好**：`s6 overlay` 设计用于容器化环境，提供了一种方便的方式来管理容器中的多个服务和进程。

3. **进程管理**：`s6 overlay` 允许你定义和管理多个服务，并指定它们的启动顺序和依赖关系。它还提供了一套灵活的工具和脚本，用于控制服务的生命周期。

4. **易于使用**：`s6 overlay` 提供了一些方便的命令和脚本，使得在容器中添加、启动、停止和重启服务变得简单而直观。

5. **可与其他工具集成**：`s6 overlay` 可以与其他容器化工具和技术（如 Docker、Podman 等）无缝集成，使得在容器中运行多个服务变得更加方便和灵活。

要使用 `s6 overlay`，通常你需要将其添加到你的容器中，并通过一些简单的配置文件来定义和管理你的服务。然后，你可以使用提供的命令和工具来启动、停止和管理这些服务。在 Alpine Linux 中，`s6 overlay` 可以通过 `apk` 包管理器安装，并且具有相应的文档和示例，帮助你开始使用它。