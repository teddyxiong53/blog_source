---
title: alpine（七）apkbuild使用
date: 2018-01-28 21:13:46
tags:
	- alpine

---



#基本环境搭建

1、先要安装alpine-sdk。

```
apk add alpine-sdk
```

2、建议作为一个普通用户来做这个事情。

```
adduser teddy
```

然后把teddy加入到sudo用户组。

```
1、visudo
2、然后编辑，保存。
3、作为teddy登陆。su - teddy
```

3、下面的操作都是以teddy的身份进行的。配置git信息。

```
git config --global user.name "teddyxiong53"
git config --global user.email "1073167306@qq.com"
```

4、开始clone aports的代码。

```
git clone git://git.alpinelinux.org/aports
```

要花一点时间才能下载完成。但是这一步有用吗？好像没用。

5、添加一个组abuild，把teddy加到这个组里。这个是必须的，因为下面的很多工具，只有abuild这个组的用户才能用。

```
sudo addgroup teddy abuild
```

6、确保/var/cache/distfiles目录存在，而且有写入的权限。

可以把目录给abuild这个组。

```
sudo chgrp abuild /var/cache/distfiles/
```

7、用abuild-keygen脚本来生成一个key。

```
abuild-keygen -a -i
```

这样基本的环境就搭建好了。



# 创建一个APKBUILD文件

用newabuild创建一个项目helloapk。生成目录如下。

```
vm-alpine-0:~/work/aports$ newapkbuild  helloapk
vm-alpine-0:~/work/aports$ tree
.
└── helloapk
    ├── APKBUILD
    └── src

2 directories, 1 file
```

APKBUILD文件内容是：

```
# Contributor:
# Maintainer:
pkgname=helloapk
pkgver=
pkgrel=0
pkgdesc=""
url=""
arch="all"
license=""
depends=""
makedepends=""
install=""
subpackages="$pkgname-dev $pkgname-doc"
source=""
builddir="$srcdir/"

build() {
        cd "$builddir"

}

package() {
        cd "$builddir"

}
```





#其他

包的命名规则：

1、全部用小写字母。

2、dev文件另外放一个包，用-dev做后缀。xxx-dev这样。

3、帮助文档另外放一个包，用-doc做后缀。xxx-doc这样。

4、lua模块用lua-做前缀。lua-xxx。

5、perl的。perl-xxx。

6、Python2的。py2-xxx。

7、Python3的。py3-xxx。

包版本编号类似于gentoo。



newapkbuild helloapk

编辑你的APKBUILD文件，包名，版本、描述信息、url、license、依赖、源代码。



abuild checksum

在APKBUILD文件后面加上校验和。有修改时，要重新生成。



alpine的一个基本原则就是尺寸要小。



APKBUILD示例：

```
# Contributor: teddyxiong53 <1073167306@qq.com>
# Maintainer: 
pkgname=helloapk
pkgver=0.0.1
pkgrel=0
pkgdesc="this is a demo for apkbuild"
url=""
arch="all"
license="GPL"
depends=""
depends_dev=""
makedepends="$depends_dev"
install=""
subpackages="$pkgname-doc"
source=""
builddir="$srcdir/$pkgname-$pkgver"

prepare() {
  default_prepare
}
build() {
  cd "$builddir"
  make
}
check() {
  cd "$builddir"
  make check
}
package() {
  cd "$builddir"
  make DESTDIR="$pkgdir" install
}
```

