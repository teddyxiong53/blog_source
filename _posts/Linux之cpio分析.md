---
title: Linux之cpio分析
date: 2020-04-16 15:35:01
tags:

	- Linux

---

--

# cpio命令

cpio是Linux下的一个命令。

用来把文件打包进行archive，或者从archive里解包。

cpio跟tar这些打包文件的不同在于，**它甚至可以把/dev下的东西都打包进archive。**

不过cpio有个问题，就是它不会自己家去找文件来备份。

怎么办？用find来配合它工作。

在/boot下的initrd就是一个用cpio打包起来的文件。

```
file /boot/initrd.img-4.13.0-43-generic 
/boot/initrd.img-4.13.0-43-generic: ASCII cpio archive (SVR4 with no CRC)
```

我们可以用cpio把这个文件解包开来，看看有什么内容。

```
hlxiong@hlxiong-VirtualBox:~/work/test/cpio$ cpio -idmv < /boot/initrd.img-4.13.0-43-generic 
.
kernel
kernel/x86
kernel/x86/microcode
kernel/x86/microcode/AuthenticAMD.bin
```

解开来，得到的实际上就是一个AuthenticAMD.bin文件。

打包命令：

```
find ./* | cpio -H newc -o > test.cpio
```



# cpio格式

cpio（Copy In, Copy Out）是一种归档（archive）文件格式和相应的命令行工具，通常用于在类Unix系统中创建、读取和提取文件归档。cpio 文件格式有多种变种，包括早期的二进制格式和更常见的ASCII格式。以下是对cpio文件格式的简要介绍：

1. **cpio 归档格式：**
   cpio 归档文件通常==包含一组文件和目录的备份或归档==。这些文件可以在一个单独的文件中打包，并且可以使用 cpio 命令来创建、提取和查看这些归档。

2. **cpio 文件类型：**
   cpio 归档中的每个文件都有一个文件类型，用于指示它是普通文件、目录、符号链接等等。这些文件类型包括 "regular"（普通文件）、 "directory"（目录）、 "symlink"（符号链接） 等。

3. **cpio 头部：**
   cpio 归档的每个文件都具有一个头部，包括文件名、权限、拥有者、修改时间等信息。这些头部用于描述文件和目录。

4. **cpio 命令行工具：**
   cpio 命令行工具用于创建 cpio 归档、提取归档内容或列出归档中的文件。常见的 cpio 命令行选项包括 `-i`（提取文件）、`-o`（创建归档） 和 `-t`（列出归档内容）。

5. **cpio 归档格式的变种：**
   - **Binary cpio（早期的二进制格式）**：早期版本的 cpio 使用二进制格式存储文件。
   - **New ASCII cpio（ASCII格式）**：现代 cpio 使用ASCII格式，更易于理解和编辑。ASCII cpio 归档可以直接查看和编辑。

6. **用途：**
   cpio 常常用于系统备份、软件分发和软件打包等任务。它还与其他工具结合使用，如 `tar`（tape archive）来创建和处理文件归档。

总之，cpio 是一种常见的文件归档格式，它具有多个变种和用途，可以在Unix和类Unix系统中执行文件备份和操作任务。这个格式的特点在于其头部信息，文件类型和可读性。

# cpio头部介绍

cpio 归档文件的头部是一个包含有关归档中文件和目录的元信息的数据结构。它位于每个文件或目录的前面，用于描述文件的属性和相关信息。以下是 cpio 头部中可能包含的一些常见字段和信息：

1. **文件名（Filename）：**
   - 文件名字段指定了文件或目录的名称。它是一个字符串，可以是相对路径或绝对路径。

2. **权限和模式（Mode）：**
   - 权限和模式字段指定了文件或目录的权限和属性。这包括文件的所有者、所属组、文件类型（如普通文件、目录、符号链接等）以及权限位（如读、写、执行权限）。

3. **用户标识（UID）和组标识（GID）：**
   - UID 和 GID 字段分别指定了文件或目录的用户标识和组标识。这些标识用于确定文件的所有者和所属组。

4. **最后修改时间（Modification Time）：**
   - 最后修改时间字段包含了文件或目录的最后修改时间戳，通常以秒数表示。

5. **文件大小（File Size）：**
   - 文件大小字段表示文件的大小，以字节为单位。

6. **连接目标（Symlink Target）：**
   - 如果归档条目是一个符号链接，则此字段包含了符号链接的目标路径。

7. **校验和（Checksum）：**
   - 校验和字段用于校验文件内容的完整性。它通常用于检测文件是否损坏。

8. **设备号（Device Number）：**
   - 如果归档条目是一个设备文件（块设备或字符设备），则此字段包含了设备号。

9. **inode 号（Inode Number）：**
   - Inode 号字段包含了文件或目录的唯一标识符。

10. **设备号（Device Number）：**
    - 如果文件或目录属于特殊设备文件，设备号字段包含了主设备号和次设备号。

这些头部字段中的信息有助于 cpio 工具在提取归档内容时恢复文件和目录的属性。不同的 cpio 归档格式可能会使用稍有不同的头部结构，但通常包括上述信息以及其他必要的元数据。头部通常以二进制或ASCII格式存储，具体取决于 cpio 归档的类型。



```
struct new_ascii_header
{
  char c_magic[6];
  char c_ino[8];
  char c_mode[8];
  char c_uid[8];
  char c_gid[8];
  char c_nlink[8];
  char c_mtime[8];
  char c_filesize[8];
  char c_dev_maj[8];
  char c_dev_min[8];
  char c_rdev_maj[8];
  char c_rdev_min[8];
  char c_namesize[8];
  char c_chksum[8];
};
```



# cpio常用命令

cpio 是一个用于创建、提取和操作归档文件的命令行工具，通常在 Unix 和类 Unix 系统中使用。以下是 cpio 命令的一些常用选项和示例：

1. **创建 cpio 归档文件：**
   - 创建一个新的 cpio 归档文件，将指定的文件和目录添加到归档中。
   ```bash
   find /path/to/files -print | cpio -o > archive.cpio
   ```

2. **从 cpio 归档文件提取文件：**
   
   - 从 cpio 归档文件中提取文件和目录。
   ```bash
   cpio -i < archive.cpio
```
   
3. **列出 cpio 归档文件的内容：**
   - 列出 cpio 归档文件中包含的文件和目录。
   ```bash
   cpio -t < archive.cpio
   ```

4. **以不覆盖方式提取文件：**
   - 以不覆盖方式提取文件，避免覆盖已存在的文件。
   ```bash
   cpio -idmu < archive.cpio
   ```

5. **指定归档文件格式：**
   
   - 使用 `-H` 选项来指定归档文件的格式。例如，对于旧格式二进制 cpio 归档，可以使用：
   ```bash
   cpio -o -H bin > archive.cpio
```
   
6. **将归档文件的内容写入目录：**
   - 将 cpio 归档文件的内容写入指定目录。
   ```bash
   cpio -idmu -D /destination/directory < archive.cpio
   ```

7. **通过管道处理文件列表：**
   - 通过管道将文件列表传递给 cpio 命令。例如，将 `find` 命令的输出传递给 cpio。
   ```bash
   find /path/to/files -print | cpio -o > archive.cpio
   ```

8. **从标准输入读取归档文件内容：**
   - 从标准输入读取 cpio 归档文件内容。
   ```bash
   cat archive.cpio | cpio -i
   ```

这些是 cpio 命令的一些常见用法。cpio 支持多种选项，可以根据具体需求进行配置，以便执行不同的归档操作。它通常与其他命令和管道一起使用，以创建、提取和处理文件归档。

# 参考资料

1、linux 下cpio使用

https://blog.csdn.net/lhl_blog/article/details/7910145

2、

https://www.cnblogs.com/f-ck-need-u/p/7008380.html