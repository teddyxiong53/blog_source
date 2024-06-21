---
title: yodaos之openwrt移植编译
date: 2022-10-17 14:27:33
tags:
	- yodaos

---

--

虽然yodaos就是基于openwrt的，但是我想在amlogic的openwrt里集成一些yodaos的组件进行编译。

先直接把openwrt/package/rokid目录的内容直接拷贝到amlogic的openwrt的package目录下。

```
export ROKID_DIR=$PWD
然后编译
make package/rokid/mutils/compile V=s -j1
```

可以正常编译通过。

但是下面命令不存在，为什么？

```
make package/rokid/mutils/install V=s -j1
```

用打印所有变量的方式查询一下：

```
make printdb |grep "package/rokid/mutils" 
```

有这些：

```
package/rokid/mutils/clean:
package/rokid/mutils/configure
package/rokid/mutils/check
package/rokid/mutils/download
package/rokid/mutils/update
package/rokid/mutils/refresh
package/rokid/mutils/distcheck
```



```
make package/rokid/flora/compile V=s -j1
```



# yodaos的openwrt sdk值得学习的点

整个目录层次结构，还是可以的，跟我们当前的buildroot的一个层次。

```
openwrt
kernel
uboot
vendor
toolchains
hardware
application
frameworks
3rd
```

看起来还支持了配置片段。





