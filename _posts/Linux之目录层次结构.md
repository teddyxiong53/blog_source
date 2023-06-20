---
title: Linux之目录层次结构
date: 2023-06-14 13:39:11
tags:
	- Linux
---

--



# XDG 基本目录规范

XDG 基本目录规范是一个用于定义用户数据、配置和缓存文件存放位置的规范，旨在提供跨平台和统一的文件组织结构。XDG 是 X Desktop Group 的缩写，该规范最初由 FreeDesktop.org 提出。

根据 XDG 基本目录规范，以下是常见的 XDG 目录及其用途：

1. `XDG_DATA_HOME`：默认为 `$HOME/.local/share/`，用于存放用户特定的数据文件，如应用程序的数据文件、图标、桌面背景等。

2. `XDG_CONFIG_HOME`：默认为 `$HOME/.config/`，用于存放用户特定的配置文件，如应用程序的配置文件、主题设置等。

3. `XDG_CACHE_HOME`：默认为 `$HOME/.cache/`，用于存放用户特定的缓存文件，如应用程序的缓存数据、临时文件等。这些文件可以在不影响应用程序功能的情况下被清理。

4. `XDG_RUNTIME_DIR`：默认为 `/run/user/$UID/`，用于存放用户运行时的非持久化数据，如应用程序的 IPC 文件、套接字等。这个目录是临时性的，会在用户注销时被清理。

5. `XDG_CONFIG_DIRS`：默认为 `/etc/xdg/`，用于存放全局的配置文件，可以被多个用户共享。这个目录下的配置文件会覆盖用户目录下的相同文件。

6. `XDG_DATA_DIRS`：默认为 `/usr/local/share/:/usr/share/`，用于存放全局的数据文件，如共享的图标、桌面背景等。这个目录下的数据文件可以被多个用户共享。

通过遵循 XDG 基本目录规范，应用程序可以在不同的操作系统和桌面环境下提供一致的文件组织结构，便于用户管理和维护。

需要注意的是，XDG 基本目录规范提供了默认值，但实际路径可能因操作系统和用户配置而有所不同。此外，还可以通过环境变量覆盖默认路径或通过配置文件进行自定义。



```
GENERAL STRUCTURE
RUNTIME DATA
/run/
/run/log/
/run/user/
VENDOR-SUPPLIED OPERATING SYSTEM RESOURCES
/usr/
/usr/bin/
/usr/include/
/usr/lib/
/lib/arch-id/
/usr/share/
/usr/share/doc/
/usr/share/factory/etc/
/usr/share/factory/var/


PERSISTENT VARIABLE SYSTEM DATA
/var/
/var/cache/
/var/lib/
/var/log/
/var/spool/
/var/tmp/

VIRTUAL KERNEL AND API FILE SYSTEMS	
/dev/
/dev/shm/
/proc/
/proc/sys/
/sys/

COMPATIBILITY SYMLINKS
/bin/, /sbin/, /usr/sbin/
/lib/
/lib64/
/var/run/

HOME DIRECTORY
~/.cache/
~/.config/
~/.local/bin/
~/.local/lib/
~/.local/lib/arch-id/
~/.local/share/

UNPRIVILEGED WRITE ACCESS
/tmp/, /var/tmp/, /dev/shm/

SYSTEM PACKAGES



```

# file-hierarchy 介绍

`file-hierarchy` 是一个术语，用于描述操作系统中文件和目录的层次结构或文件系统的组织方式。它定义了文件和目录在系统中的布局和归类方式，使得文件的存储和查找更加有序和一致。

常见的 file hierarchy 包括：

1. Unix 文件层次结构：Unix 系统采用一种标准的文件层次结构，常见的是 Filesystem Hierarchy Standard (FHS)。该层次结构定义了根目录、用户目录、系统目录、配置文件目录、可执行文件目录等的位置和用途，以提供统一的文件组织方式。

2. Windows 文件层次结构：Windows 操作系统也有一种文件层次结构，其中包括系统根目录、用户个人文件夹、系统目录、程序文件夹等。Windows 的文件层次结构在不同版本中可能有所差异。

3. 跨平台文件层次结构：一些跨平台的开发框架和应用程序提供自己的文件层次结构，旨在在不同的操作系统上提供一致的文件组织方式。例如，Java 的文件层次结构遵循 Java Naming and Directory Interface (JNDI) 规范。

文件层次结构的设计旨在提供一种有序的方式来组织文件和目录，使得用户和应用程序可以方便地访问和管理文件。它还有助于确保文件的存储位置一致性，使得不同的应用程序和系统组件可以共享和访问相关的文件。

需要注意的是，不同的操作系统和软件可能有不同的文件层次结构，具体的层次结构和命名约定可能因操作系统或标准的不同而有所差异。因此，在开发和管理文件系统时，需要了解和遵循相应的文件层次结构规范。

# 参考资料

1、man 7 file-hierarchy  命令查看到的内容

