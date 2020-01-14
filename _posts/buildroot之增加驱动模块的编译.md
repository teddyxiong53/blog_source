---
title: buildroot之增加驱动模块的编译
date: 2020-01-14 10:55:08
tags:
	- buildroot

---

1

在package目录下，新建一个test_driver目录。

在package/Config.in里的hardware handling层次下面增加一行：

```
source "package/test_driver/Config.in"
```

在test_driver目录下增加一个Config.in文件。

```
config BR2_PACKAGE_test_driver
bool "test_driver"
depends on BR2_LINUX_KERNEL
help
  Test for adding driver in buildroot
comment "hello-world driver needs a Linux kernel to be built"
depends on !BR2_LINUX_KERNEL
```

在test_driver目录下，新建一个test_driver.mk文件，内容如下：

```
TOP_DIR:=$(CURDIR)

TEST_DRIVER_VERSION:=1.0.0
TEST_DRIVER_SITE=$(TOP_DIR)/package/test_driver/src
TEST_DRIVER_SITE_METHOD=local

# 这个不需要在这里定义BUILD_CMD这些。
$(eval $(kernel-module))
$(eval $(generic-package))
```



参考emlog的写法。

https://github.com/nicupavel/emlog

这个也编译不过。

ktap这个也编译不过。

参考v4l2loop的来改。这个可以的。

在src下面，放Makefile和test_dt.c这2个文件。

```
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

static int __init hello_init(void){
    printk(KERN_ALERT "hello driver init!\n");
    return 0;
}

static void __exit hello_exit(void){
    printk(KERN_ALERT "hello driver exit\n");
}

module_init(hello_init);
module_exit(hello_exit);
```

Makefile这样写：

```
KERNELRELEASE	?= `uname -r`
KERNEL_DIR	?= /lib/modules/$(KERNELRELEASE)/build
PWD		:= $(shell pwd)
obj-m		:= test_dt.o

PREFIX ?= /usr/local
BINDIR  = $(PREFIX)/bin
MANDIR  = $(PREFIX)/share/man
MAN1DIR = $(MANDIR)/man1
INSTALL = install
INSTALL_PROGRAM = $(INSTALL) -p -m 755
INSTALL_DIR     = $(INSTALL) -p -m 755 -d
INSTALL_DATA    = $(INSTALL) -m 644


TARGET_NAME := test_dt


.PHONY: all install clean distclean
.PHONY: install-all install-utils install-man
.PHONY: modprobe

# we don't control the .ko file dependencies, as it is done by kernel
# makefiles. therefore $(TARGET_NAME).ko is a phony target actually
.PHONY: $(TARGET_NAME).ko

all: $(TARGET_NAME).ko

$(TARGET_NAME).ko:
	@echo "Building test_dt"
	$(MAKE) -C $(KERNEL_DIR) M=$(PWD) modules

install-all: install
install:
	$(MAKE) -C $(KERNEL_DIR) M=$(PWD) modules_install
	depmod -a  $(KERNELRELEASE)



clean:
	rm -f *~
	rm -f Module.symvers Module.markers modules.order
	$(MAKE) -C $(KERNEL_DIR) M=$(PWD) clean

distclean: clean
```

在顶层make test_driver就可以编译，然后自动拷贝到rootfs的/lib/modules/4.11.3/extra目录下。



参考资料

1、在buildroot中添加驱动

https://bbs.csdn.net/topics/395088534

https://buildroot.org/downloads/manual/manual.html#_infrastructure_for_packages_building_kernel_modules