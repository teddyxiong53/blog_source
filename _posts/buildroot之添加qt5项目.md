---
title: buildroot之添加qt5项目
date: 2021-06-22 15:08:33
tags:
	- buildroot

---

--

要基于buildroot+qt来开发一个带界面的产品。

为了方便维护，肯定是把qt的项目代码放到buildroot里一起编译了。

应该怎么来加这个工程呢？

其实很简单，主要是要理解qmake的用法。

基本思路是：先执行qmake得到Makefile，再执行make操作。

这个就是一个例子

```
build:
	mkdir -p build
	qmake src/slide.pro -o build/Makefile
	make -C build
```

而集成到buildroot里的写法

```
./qt5/qt5tools/qt5tools.mk:54:  (cd $(@D); $(TARGET_MAKE_ENV) $(HOST_DIR)/bin/qmake)
```

以qt5/qt5script/qt5script.mk 这个作为参考更好些，因为更简单。

在package目录下，新建一个demo_qt的目录。

demo_qt.mk

```
DEMO_QT_VERSION = 1.0.0
DEMO_QT_SITE_METHOD = local
DEMO_QT_SITE = $(TOPDIR)/package/demo_qt/src

DEMO_QT_DEPENDENCIES = qt5base
DEMO_QT_INSTALL_STAGING = YES

OUT_BIN := demo_qt

define DEMO_QT_CONFIGURE_CMDS
	(cd $(@D); $(TARGET_MAKE_ENV) $(HOST_DIR)/bin/qmake)
endef

define DEMO_QT_BUILD_CMDS
	$(TARGET_MAKE_ENV) $(MAKE) -C $(@D)
endef

define DEMO_QT_INSTALL_STAGING_CMDS
	$(TARGET_MAKE_ENV) $(MAKE) -C $(@D) install
endef


define DEMO_QT_INSTALL_TARGET_CMDS
	$(INSTALL) -m 0755 -D $(@D)/$(OUT_BIN)  $(TARGET_DIR)/usr/bin
endef

$(eval $(generic-package))
```

Config.in

```
config BR2_PACKAGE_DEMO_QT
	bool "demo_qt"
	help
	  demo qt
```

src/main.cpp

```
#include <QCoreApplication>

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    
    return a.exec();
}
```

src/demo_qt.pro

```
QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

TARGET = demo_qt
TEMPLATE = app

DEFINES += QT_DEPRECATED_WARNINGS


SOURCES += \
        main.cpp

HEADERS +=


target.path = /usr/bin/

INSTALLS += target
```

make demo_qt-rebuild 

可以正常编译得到文件，并可以正常运行。



参考资料

1、在Linux下搭建嵌入式Qt交叉编译环境

https://yuanze.wang/posts/build-qt-embedded-linux/

2、Embedded Qt with Buildroot

https://github.com/pbouda/buildroot-qt-dev

3、Add a Qmake package to buildroot

https://stackoverflow.com/questions/26999299/add-a-qmake-package-to-buildroot