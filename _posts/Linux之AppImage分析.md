---
title: Linux之AppImage分析
date: 2020-12-09 10:48:30
tags:
	- Linux
---



1

安装Etcher这个工具的时候，发现Linux版本是AppImage格式的。

这个格式之前倒没留意过。

使用的效果，就相当于windows下的绿色版软件，直接双击运行就可以了。

这样倒是非常方便的。

这个是怎样实现的呢？



 Applmage某种程度上你可以理解为windows某些软件的“便携版”。

它的做法有点类似于docker镜像，把软件运行的所有依赖环境都打包在一起，包装成一个Applmage，

**运行的时候会将打包到一起的内容释放到/tmp/下运行，运行完毕之后通常会自动清理。**



AppImage文件虽然可以直接运行，但是不像其他的deb  apt 等获得的软件一样，在系统菜单中显示图标，

因为它就像windows中免安装所谓绿色版的exe一样，有的不添加到注册表之类的（个人理解），

所以，只在运行的时候才会和操作系统有关系，这就很麻烦；

而且，我把 AppImage放到 /usr/local 文件夹下面，那么每次都要打开这个文件夹，双击它才可运行，

这样很不好使，**我希望能够像普通的软件一样，有系统图标，可以固定在收藏夹栏中**。

1.想要让AppImage有图标

2.想固定在收藏栏上

**这就需要 AppImageLauncher了**



该程序可让你轻松运行 AppImage 文件，而无需使其可执行。

但它最有趣的特点是可以轻松地将 AppImage 与你的系统进行整合：

AppImageLauncher 可以自动将 AppImage 程序快捷方式添加到桌面环境的程序启动器/菜单



参考资料

1、超级方便的AppImage 和管理器AppImageLauncher（安装）

https://blog.csdn.net/u012057432/article/details/103097632