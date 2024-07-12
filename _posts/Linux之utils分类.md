---
title: Linux之utils分类
date: 2017-10-02 11:21:16
tags:
	- Linux

---



Linux下有很多的命令行工具，这些工具应该怎样分类呢？

我根据busybox的readme里提到的信息，和这个地址的信息，进行简单的梳理。

https://www.google.com.hk/url?sa=t&rct=j&q=&esrc=s&source=web&cd=7&cad=rja&uact=8&ved=0ahUKEwiNhNv7_NDWAhVhyVQKHWNDCVgQFghDMAY&url=http%3A%2F%2Fwww.iitk.ac.in%2FLDP%2FLDP%2Flfs%2F5.0%2Fhtml%2Fappendixb%2Fappendixb.html&usg=AOvVaw2u_2pvanL_vUqQKOpkk89F

为了抓住重点，只看最常用的。

http://www.tldp.org/LDP/lfs/5.0/html/ 

这个网站很有用。

# binutils

1、binutils是用于软件开发的。

2、包括一个linker、一个assembler和其他的用于处理obj文件的archive文件的。

程序有：

addr2line

ar：

as：

c++flit：

gprof：

ld：

nm：

objcopy：

objdump：

ranlib：

readelf：

size：

strings：

strip：

库有：

libiberty.a

libbfd.[a,so]

libopcodes.[a, so]



# coreutils

这个就是最基础的组件。

basename：

cat：

chgrp：

chmod：

chown：

chroot：

cksum：

comm：

cp：

csplit：

cut：

date：

dd：

df：

dir：

dircolors：

dirname：

du：

echo：

env：

expand：

expr：

factor：

false：

fmt：

fold：

groups：

head：

hostid：

hostname：

id：

install：

join：

kill：

link：

ln：

logname：

ls：

md5sum：

mkdir：

mkfifo：

mknod：

mv：

nice：

nl：

nohup：

od：

paste：

pathchk：

pinky：

pr：

printenv：

printf：

ptx：

pwd：

readlink：

rm：

rmdir：

seq：

sha1sum：

shred：

sleep：

sort：

split：

stat：

stty：

su：

sum：

sync：

tac：

tail：

tee：

test：

touch：

tr：

true：

tsort：

tty：

uname：

unexpand：

uniq：

unlink：

uptime：

users：

vdir：

wc：

who：

whoami：

yes：一直输出y。

总计89个工具。



# file

这个组很简单。一个程序一个库。

程序有：

file。

库有：

libmagic.[a, so]



# findutils

bigram：

code：

find：

frcode：

locate：

updatedb：

xargs：



# inetutils

ftp：

ping：

rcp：

rlogin：

rsh；

talk：

telnet：

tftp：



#modutils：

这个是给module用的。

depmod：

genksyms：

insmod：

insmod_ksymoops_clean：

kallsyms：

kernelversion：

kyms：

lsmod：

modinfo：

modprobe：

rmmod：

# net-tools

arp：

dnsdomainname：

domainname：

hostname：

ifconfig：

nameif：

netstat：

nisdomainname：

plipconfig：

rarp：

route：

slattach：

ypdomainname：



# sysvinit

halt：

init：

killall5：

last：

lastb：

mesg：

pidof：

poweroff：

reboot：

runlevel：

shutdown：

sulogin：

telinit：

utmpdump：

wall：



# util-linux

`util-linux` 的发展历史可以追溯到 Unix 操作系统的早期。以下是 `util-linux` 的主要里程碑和发展阶段：

1. 初始阶段：`util-linux` 最早是作为 Unix 系统的一部分开发的，旨在提供一些基本的系统工具和实用程序。这些工具包括 `mount`、`umount`、`login`、`su` 等。

2. GNU 项目：在 1980 年代，GNU 项目开始为 Unix 系统开发自由和开源软件。GNU 工具集中的一部分是 `coreutils`，它包括了一些与 `util-linux` 重叠的功能。随着时间的推移，一些工具从 `coreutils` 中移动到了 `util-linux` 中，以便更好地组织和管理。

3. 发展和增加功能：随着时间的推移，`util-linux` 增加了许多新的工具和功能，以适应不断发展的 Linux 操作系统和用户需求。这些包括磁盘分区工具如 `fdisk`、`parted`，进程管理工具如 `kill`、`killall`，文件系统工具如 `fsck`、`mkfs`，以及其他实用程序如 `dmesg`、`hwclock` 等。每个新版本都带来了更多功能和改进。

4. 技术更新和改进：随着技术的进步和新的需求的出现，`util-linux` 不断进行更新和改进。这些改进可能包括性能优化、安全增强、新的功能支持以及与新硬件和软件标准的兼容性。

总体而言，`util-linux` 经历了多个版本和演进，以适应不断变化的 Linux 环境和用户需求。它成为了一个重要的工具集，用于管理和操作 Linux 系统的各个方面，并在各个 Linux 发行版中被广泛使用。



`util-linux` 是一个常见的 Linux 系统工具集合，它提供了许多标准的系统工具和实用程序，用于管理和操作 Linux 操作系统的各个方面。这个工具集通常被包含在大多数 Linux 发行版中。

以下是 `util-linux` 提供的一些主要工具和功能：

1. `mount` 和 `umount`：用于挂载和卸载文件系统。

2. `fdisk` 和 `parted`：用于磁盘分区和管理。

3. `blkid`：用于查找块设备的文件系统类型和属性。

4. `fsck`：用于文件系统检查和修复。

5. `mkfs`：用于创建文件系统。

6. `login` 和 `su`：用于用户登录和切换。

7. `kill` 和 `killall`：用于终止进程。

8. `hwclock`：用于管理硬件时钟。

9. `dmesg`：用于显示内核日志消息。

10. `more` 和 `less`：用于分页显示文本文件。

11. `uptime`：显示系统的运行时间和负载。

12. `chroot`：用于改变根文件系统。

这只是 `util-linux` 工具集中的一小部分。它提供了许多其他实用程序，用于诸如系统管理、磁盘操作、进程管理、时间管理等任务。

请注意，`util-linux` 的具体版本和可用工具可能会因 Linux 发行版和版本而异。这些工具通常是在命令行界面上使用的，您可以通过在终端中键入命令来调用它们。

以下是 `util-linux` 工具集中列出的一些工具，并使用 Markdown 表格形式进行说明：

| 工具         | 说明                                                         |
| ------------ | ------------------------------------------------------------ |
| blkdiscard   | 用于舍弃（丢弃）块设备的内容。                               |
| blkid        | 用于查找块设备的文件系统类型和属性。                         |
| blockdev     | 用于查询或设置块设备的属性。                                 |
| chcpu        | 用于在线更改 CPU 的状态和属性。                              |
| choom        | 用于设置进程的 OOM （内存不足）行为。                        |
| col          | 用于将文本文件中的空格转换为制表符。                         |
| colcrt       | 用于将文本文件适应终端宽度并分页显示。                       |
| colrm        | 用于删除文本文件中的指定列。                                 |
| column       | 用于将文本数据按列格式化并输出。                             |
| ctrlaltdel   | 用于控制是否允许通过按下 Ctrl+Alt+Del 组合键来重启系统。     |
| dmesg        | 用于显示和控制内核的环形缓冲区消息。                         |
| fdisk        | 用于磁盘分区和管理。                                         |
| fincore      | 用于统计文件在缓存中的页帧和状态。                           |
| findfs       | 用于根据文件系统的标签或UUID查找设备。                       |
| findmnt      | 用于查找已挂载的文件系统。                                   |
| flock        | 用于在 shell 脚本中提供文件锁定机制。                        |
| fsfreeze     | 用于冻结或解冻文件系统，以便进行一致的磁盘快照。             |
| fstrim       | 用于从文件系统中释放未使用的块并回收存储空间。               |
| getopt       | 用于解析命令行选项参数。                                     |
| hexdump      | 用于以十六进制或其他格式显示文件的内容。                     |
| ipcmk        | 用于在 System V IPC（进程间通信）资源中创建新的 IPC 对象。   |
| isosize      | 用于获取 ISO 9660 文件系统映像的大小。                       |
| ldattach     | 用于将 Linux 终端连接到串口设备上。                          |
| look         | 用于按字典顺序搜索文件中的单词。                             |
| lsblk        | 用于列出块设备的信息，如磁盘、分区和挂载点。                 |
| lscpu        | 用于显示 CPU 和系统架构的详细信息。                          |
| lsipc        | 用于显示 System V IPC（进程间通信）对象的信息。              |
| lslocks      | 用于显示被进程锁定的文件。                                   |
| lsns         | 用于显示 Linux 命名空间的信息。                              |
| mcookie      | 用于生成随机的机器码（cookie）。                             |
| mkfs         | 用于创建文件系统。                                           |
| mkswap       | 用于创建交换分区。                                           |
| namei        | 用于显示文件或目录的路径名解析。                             |
| prlimit      | 用于显示或修改进程的资源限制。                               |
| readprofile  | 用于从 Linux 内核中读取性能分析数据。                        |
| renice       | 用于修改正在运行进程的优先级。                               |
| rev          | 用于反转文本文件中每一行的字符顺序。                         |
| rtcwake      | 用于设置系统在指定时间唤醒或进入睡眠状态。                   |
| script       | 用于记录和回放终端会话。                                     |
| scriptlive   | 用于实时记录和回放终端会话。                                 |
| scriptreplay | 用于回放通过 `script` 记录的终端会话。                       |
| ------------ | -------------------------------------------------------------- |
| setarch      | 用于设置进程执行的架构（如 x86、x86_64）。                   |
| setsid       | 用于启动一个新的会话并执行命令。                             |
| sfdisk       | 用于分析和操作磁盘分区表。                                   |
| swaplabel    | 用于设置或查看交换分区的标签。                               |
| swapoff      | 用于关闭交换分区。                                           |
| swapon       | 用于启用交换分区。                                           |
| uuidgen      | 用于生成 UUID（通用唯一标识符）。                            |
| uuidparse    | 用于解析和验证 UUID。                                        |
| whereis      | 用于查找二进制可执行文件的位置。                             |
| wipefs       | 用于从块设备上删除文件系统或签名。                           |

这些工具在 `util-linux` 中提供了各种功能，从处理块设备、文件系统和磁盘分区，到系统管理和性能分析，以及其他实用程序。请注意，每个工具的具体用法和参数可能会有所不同，您可以在命令行中使用工具的 `--help` 选项或查阅相关文档以获取更多详细信息。





