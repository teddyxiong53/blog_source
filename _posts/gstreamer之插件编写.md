---
title: gstreamer之插件编写
date: 2019-07-19 15:53:19
tags:
	- gstreamer

---



插件是用一段代码来封装元件得到的东西。

一个插件里，可以包含多个元件。

我们先从只包含一个元件的插件看起。

gstreamer的主要功能都是通过插件来实现的。

一个xml文件被用来保存所有注册的插件的信息。



gstreamer里的所有数据流都被分割成一块块的。

数据包结构体就是用来描述这一块块的数据的。

数据包结构体包括：

1、类型。是控制包还是数据包。

2、引用计数。

控制包包括了2个相连的pad之间的流的状态信息。



从这里下载

```
git clone git://anongit.freedesktop.org/gstreamer/gst-template.git
```

然后得到一个gst-template的目录。

下面有2个子目录。

一个是gst-app。是一个应用的例子。没什么。

一个是gst-plugin目录。

```
cd gst-plugin/src
../tools/make_element MyFilter 
```

make_element是一个脚本，可以接收2个参数：

```
参数1：
	插件的名字。注意大小写。
参数2：
	这个是指定模板。
	可以省略。省略就是用gstplugin.c这个文件作为模板。
	也可以用gsttransform.c来做模板。
```

脚本的作用，就是批量替换字符串。

然后在gst-plugin目录下，执行autogen.sh脚本。然后执行make。

可以看到会提示GST_LICENSE等3个宏没有定义。

这个就是在gstplugin.c里最后部分，自己写一下对应的宏定义就好了。



https://gstreamer.mazdermind.de/

这个网站也可以帮助我们生成代码。这个生成的不太好。



怎样测试我们写的插件呢？

用gst-launch-1.0就可以。

用法是这样：

```
gst-launch-1.0 --gst-plugin-path=$HOME/gst-template/gst-plugin/src/.libs TESTPIPELINE
```

# 插件没有加载的原因

一般是因为插件加载有出错。

```
gst-inspect-1.0 |grep xx
```

这样查看真正出错的原因：

```
rm ~/.cache/gstreamer-1.0/ -rf
gst-inspect-1.0  | grep xx
```

然后解决问题再看看。

查看黑名单

```
gst-inspect-1.0 -b
```



# 参考资料

1、gstreamer插件指南

https://blog.csdn.net/sinat_28502203/article/details/46010485

2、gstreamer插件开发手册

https://wenku.baidu.com/view/775e189a10a6f524cdbf8533.html

3、gstreamer---Gobject类对象

https://www.jianshu.com/p/5acdb9ea7a08

4、GStreamer Plugin Writer’s Guide

https://gstreamer.freedesktop.org/data/doc/gstreamer/head/pwg/pwg.pdf

5、writing sample plugin

https://lists.freedesktop.org/archives/gstreamer-devel/2007-October/016184.html

6、Creating object files  

这个关于libtool object file的。

https://www.gnu.org/software/libtool/manual/html_node/Creating-object-files.html

7、

https://zhuanlan.zhihu.com/p/557704790