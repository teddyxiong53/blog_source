---
title: Linux之ramoops
date: 2021-12-16 14:39:11
tags:
	- Linux

---

--

系统在出现异常时重启，这时候又没有串口log，

那么这时候需要把crash message存储在persistent storage中，

以便在下次重启中获取这些crash信息。

pstore可以让用户空间获取这些last crash message信息，

而平台端实现了具体persistent storage，

并给pstore提供read/write/erase三个接口。

**Ramoops则将RAM划出一块空间作为persistent storage，**

**来保存last crash message。**

```
CONFIG_PSTORE 使能PSTORE功能，用户可以通过文件系统获取last crash message

CONFIG_PSTORE_xx_COMPRESS 选择存储last crash message的压缩算法

CONFIG_PSTORE_CONSOLE PSTORE将会保存所有的kernel message，即使没有发生crash

CONFIG_PSTORE_PMSG PSTORE将会保存用户空间的信息

CONFIG_PSTORE_FTRACE PSTORE将会保存ftrace信息

CONFIG_PSTORE_RAM 将RAM作为persistent storage
```

dts配置

```
ramoops@0x07400000 {
			compatible = "ramoops";
			reg = <0x0 0x07400000 0x0 0x00100000>;
			record-size = <0x20000>;
			console-size = <0x40000>;
			ftrace-size = <0x80000>;
			pmsg-size = <0x20000>;
		};
```

reg表示了预留的内存的起始物理地址和长度。

首先CONFIG_PANIC_TIMEOUT的值大于0，保证在异常时可以重启。

使用下面命令制造一个crash，然后等待Rebooting in 5 seconds..机器自动重启。

```
echo c > /proc/sysrq-trigger
```



```
重启后进入终端输入mount -t pstore -o kmsg_bytes=8000 - /sys/fs/pstore 
```



参考资料

1、

