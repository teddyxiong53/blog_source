---
title: kindle折腾
date: 2019-01-19 16:19:56
tags:
	- kindle

---



我的kindle买回来之后，就破解了。可以支持阅读epub等格式的。

然后很久没有碰到什么问题了。

今天在清理kindle里的文件的时候，不小心把相关的目录删掉了。导致现在epub打开提示“无法启动选定的应用程序”。

现在只能重新折腾了。

现在重新来认识kindle。把折腾的过程记录下来。

先进设置，查看kindle信息。

我的固件版本是5.9.7的。

我的kindle型号的kindle paper white3 。

之前已经越狱过了。

首先需要安装插件启动器kual和插件安装器MRPI。

我就从这里开始做吧。

kual是Kindle Unified Application Launcher。是插件启动器。

你可以下载或者自己编写插件，并且通过kual启动。

下载地址在这里：

```
https://pan.baidu.com/s/1UqpHNRbevxhoh3GL2MsUqg?errno=0&errmsg=Auth Login Sucess&&bduss=&ssnerror=0&traceid=
```

是一个tgz包。解压好备用。

需要把kindle用数据线连接到电脑上。

把解压得到的Update_KUALBooklet_v2.7.14_install.bin文件，拷贝到kindle的mrpackages目录下。

然后把kindle数据线断开，点击左上角的放大镜，弹出输入框。

输入下面的：

```
; log mrpi
```

点击回车，然后kindle就会重启。

这样就安装了kual了。



kual的插件安装很简单，就下载插件，把目录放到kindle的extension目录下就可以了。



我还是重新从越狱这一步开始操作吧。

所以这就看出记录的重要性了。我之前不记得怎么弄的，反正就弄成功了。

现在要重新弄，反而不支持怎么下手了。

我也不知道为什么我现在的kindle版本这么新了。是5.9.7的。

从这里，可以下载特定版本的固件。

https://bookfere.com/post/409.html



算了，不打算折腾了。把我的epub用calibre转成mobi。

我去，calibre的转换效果并不好。

我还是下定决心重新进行越狱吧。



如何确认自己是否越狱了？

在kindle的根目录下，新建一个RUNME.sh的文件。

内容如下：

```
#!/bin/sh
eips 0 0 'Hello World!'
```



然后还是打开kindle。在搜索框里输入：

```
;log runme
```

如果在屏幕的左上角出现了hello world的打印，就说明当前是处于越狱状态。

我试了一下，我的当前确实还是越狱状态的。

如果要取消越狱，就恢复出厂就可以了。



那我现在需要做的就是，重新下载插件安装就是了。

我之前下载的那些插件都还在的。

我重新放入系统一遍。

上面kual已经弄好了。

现在看mrpi的。

这个也都还在的。所以还是不操作。



然后看koreader的。



我知道是怎么回事了。

我的kindle目前还是正常的。只是epub需要从kual这里面去打开。



不过还是尽量用mobi的。epub的体验还是不太好。



# 参考资料

1、Kindle 越狱插件资源下载及详细安装步骤

https://bookfere.com/post/311.html

2、kindle kual

https://www.wheat.at/others/2014/07/22/kindle-kual.html

3、

https://bookfere.com/post/410.html