---
title: 分区表之GPT
date: 2020-04-08 14:01:51
tags:
	- Linux

---

--

看rk3308的分区表，是使用GPT的方式。了解一下这个。

# 简介

GPT（GUID Partition Table，全局唯一标识分区表）是一种磁盘分区方案，用于在计算机存储设备上管理分区和数据。

相比于传统的 MBR（Master Boot Record，主引导记录）方式，==GPT 提供了更先进的功能和更强大的特性。==

以下是 GPT 分区的一些重要特点和优势：

1. **容量支持**：GPT 支持更大容量的磁盘。MBR 分区表最大支持2TB的磁盘，而 GPT 则能够处理更大容量的磁盘，这对于现代大容量存储设备尤为重要。

2. **备份和恢复**：GPT 存储了主分区表和备份分区表，有助于数据恢复。==如果主分区表损坏，系统可以从备份分区表还原数据。==

3. **标识符**：==每个 GPT 分区都有一个唯一的标识符（GUID），这有助于区分不同的分区并避免冲突==。

4. **灵活性**：GPT 支持更多的分区，最多支持128个分区，相比之下，MBR 仅支持4个主分区。

5. **安全性**：GPT 使用CRC32校验和来检测分区表的完整性，可以更好地防止数据损坏和错误。



在使用 GPT 时，操作系统和硬件必须支持它。

大多数现代操作系统，如 Windows（Vista 及更新版本）、Linux 和 macOS 都能够与 GPT 磁盘进行兼容。

但是，一些旧的操作系统和旧的 BIOS 系统可能不支持 GPT。

UEFI（统一扩展固件接口）是支持 GPT 分区表的一种固件接口，与传统的 BIOS 不同。

总的来说，GPT 分区表是一个更现代、更强大且更灵活的磁盘分区方案，适用于支持大容量磁盘和需要更多分区的情况。



GPT被存放在介质的LBA0到LBA64。

LBA是Logic Block Address的意思。逻辑块地址。



# uboot如何支持gpt分区

uboot支持标准的GPT格式。

GPT是EFI标准的一部分。特点是使用UUID作为磁盘分区的代号。

==GPT的第一个扇区，还是放MBR信息，这样来保持对MBR 的兼容。==



U-Boot 是一个常用的嵌入式系统引导加载程序，在其版本更新中，已经添加了对 GPT 分区表的支持。使用 U-Boot 支持 GPT 分区，需要考虑以下几点：

1. **编译选项**：确保 U-Boot 版本是支持 GPT 分区表的。通常，较新版本的 U-Boot 已经包含了对 GPT 的支持。在编译 U-Boot 时，==需要启用相关的配置选项，比如 `CONFIG_EFI_PARTITION` 或者 `CONFIG_PARTITION_UUIDS`。==

2. **存储介质支持**：确保存储设备的引导分区和其他分区是基于 GPT 分区表创建的。使用适当的磁盘分区工具（如 `gdisk`、`parted` 等）创建 GPT 分区表，并在其中创建所需的分区。

3. **文件系统**：确保 U-Boot 可以识别并加载 GPT 分区中的文件系统。U-Boot 需要支持要使用的文件系统类型，比如 ext4、FAT32 等。通常情况下，U-Boot 需要包含相关的文件系统模块以支持识别和加载文件系统。

4. **引导参数设置**：在 U-Boot 中设置引导参数时，可能需要指定 GPT 分区中的引导位置或者其他分区信息。这些参数可能会根据您的系统配置和分区布局而有所不同。



# 参考资料

1、

https://thestarman.pcministry.com/asm/mbr/PartTables.htm

2、

http://rockchip.wikidot.com/partitions

3、GPT在uboot里的文档

https://github.com/rockchip-linux/u-boot/blob/android/doc/README.gpt

4、

https://blog.csdn.net/haiross/article/details/38659825

5、逻辑区块地址

https://baike.baidu.com/item/%E9%80%BB%E8%BE%91%E5%8C%BA%E5%9D%97%E5%9C%B0%E5%9D%80/22660818?fromtitle=LBA&fromid=2025827

6、MBR 与 GPT，关于分区表你应该知道的一些知识 - 硬盘使用知识大全（8）

https://www.eassos.cn/jiao-cheng/ying-pan/mbr-vs-gpt.php