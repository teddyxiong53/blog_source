---
title: Linux之目录层次结构
date: 2023-06-14 13:39:11
tags:
	- Linux
---

--



# XDG 基本目录规范

XDG 目录规范（XDG Base Directory Specification）由 [freedesktop.org](https://www.freedesktop.org/wiki/Specifications/basedir-spec/) 定义，旨在标准化 Linux 系统上用户和应用程序存储文件的位置。这一规范定义了几个环境变量，指示配置文件、数据文件和缓存文件的存储位置。

### 主要目录和环境变量

以下是 XDG 目录规范中定义的主要目录及其相关的环境变量：

（3个HOME结尾，都是user相关的，最后这个也是user相关的）

| 目录类型   | 环境变量          | 默认路径（若环境变量未设置）                  |
| ---------- | ----------------- | --------------------------------------------- |
| 配置文件   | `XDG_CONFIG_HOME` | `$HOME/.config`                               |
| 用户数据   | `XDG_DATA_HOME`   | `$HOME/.local/share`                          |
| 缓存文件   | `XDG_CACHE_HOME`  | `$HOME/.cache`                                |
| 运行时文件 | `XDG_RUNTIME_DIR` | 通常是 `/run/user/$(id -u)`（需要由系统设置） |

### 补充目录和环境变量

除了上述主要目录外，还有一些额外的目录用于特定用途：

| 目录类型         | 环境变量              | 默认路径（若环境变量未设置）          |
| ---------------- | --------------------- | ------------------------------------- |
| 配置文件搜索路径 | `XDG_CONFIG_DIRS`     | `/etc/xdg`                            |
| 数据文件搜索路径 | `XDG_DATA_DIRS`       | `/usr/local/share/:/usr/share/`       |
| 桌面文件目录     | `XDG_DESKTOP_DIR`     | `$HOME/Desktop`（具体取决于桌面环境） |
| 文档目录         | `XDG_DOCUMENTS_DIR`   | `$HOME/Documents`                     |
| 下载目录         | `XDG_DOWNLOAD_DIR`    | `$HOME/Downloads`                     |
| 媒体文件目录     | `XDG_MUSIC_DIR`       | `$HOME/Music`                         |
| 图片目录         | `XDG_PICTURES_DIR`    | `$HOME/Pictures`                      |
| 视频目录         | `XDG_VIDEOS_DIR`      | `$HOME/Videos`                        |
| 公共共享目录     | `XDG_PUBLICSHARE_DIR` | `$HOME/Public`                        |
| 模板目录         | `XDG_TEMPLATES_DIR`   | `$HOME/Templates`                     |

### 使用 XDG 目录规范的示例

#### 1. 设置配置文件存储路径

应用程序应该使用 `XDG_CONFIG_HOME` 来存储配置文件。如果该环境变量未设置，则默认存储在 `$HOME/.config` 下。

示例代码：

```c
#include <stdlib.h>
#include <stdio.h>

int main() {
    const char *config_home = getenv("XDG_CONFIG_HOME");
    if (!config_home) {
        config_home = getenv("HOME");
        if (!config_home) {
            fprintf(stderr, "HOME is not set\n");
            return 1;
        }
        char config_path[256];
        snprintf(config_path, sizeof(config_path), "%s/.config/myapp", config_home);
        printf("Config path: %s\n", config_path);
    } else {
        char config_path[256];
        snprintf(config_path, sizeof(config_path), "%s/myapp", config_home);
        printf("Config path: %s\n", config_path);
    }

    return 0;
}
```

#### 2. 设置数据文件存储路径

应用程序应该使用 `XDG_DATA_HOME` 来存储用户数据文件。如果该环境变量未设置，则默认存储在 `$HOME/.local/share` 下。

示例代码：

```c
#include <stdlib.h>
#include <stdio.h>

int main() {
    const char *data_home = getenv("XDG_DATA_HOME");
    if (!data_home) {
        data_home = getenv("HOME");
        if (!data_home) {
            fprintf(stderr, "HOME is not set\n");
            return 1;
        }
        char data_path[256];
        snprintf(data_path, sizeof(data_path), "%s/.local/share/myapp", data_home);
        printf("Data path: %s\n", data_path);
    } else {
        char data_path[256];
        snprintf(data_path, sizeof(data_path), "%s/myapp", data_home);
        printf("Data path: %s\n", data_path);
    }

    return 0;
}
```

### 目录层级结构

根据 XDG 规范，应用程序应该在各自的环境变量目录下创建一个子目录来存储其相关文件。例如，应用 `myapp` 应该在配置目录下创建 `myapp` 子目录来存储配置文件：

```
~/.config/myapp/
~/.local/share/myapp/
~/.cache/myapp/
```

### 优势

- **标准化文件位置**：==通过使用 XDG 目录规范，应用程序可以标准化用户文件的位置，使得备份和迁移更容易。==
- **环境变量配置**：用户可以通过设置环境变量来自定义配置、数据和缓存文件的位置，以满足不同的需求和偏好。
- **分离文件类型**：通过将配置文件、数据文件和缓存文件分离到不同的目录，简化了系统管理和清理工作。

### 总结

遵循 XDG 目录规范有助于创建一致和用户友好的应用程序，简化了文件管理，并提高了系统的可维护性和灵活性。应用程序开发者应尽量遵循这些规范，以便与其他遵循 XDG 规范的应用程序和工具更好地协作。



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

