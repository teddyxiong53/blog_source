---
title: Linux之gettext
date: 2020-05-05 11:13:16
tags:
	- Linux

---



gettex是一种本地化和国际化的系统。

在类unix系统里编写多语言程序的时候，经常要用到。

gettext的一个实现版本为gun gettext。这个在1995年发布。

使用方法是，在代码里，所有需要多语言支持的字符串，都用gettext函数包裹起来。

一般会给gettext命名一个别名为`_`。这样写起来方便一些。

如下：

```
printf(gettext("my name is %s\n"), myname);
```

或者：

```
printf(_("my name is %s\n"), myname);
```

gettext函数会使用当前提供的字符串作为key去找当前设置语言的对应的翻译版本。

如果没有找到，那么就使用当前的字符串。

那么怎么制作各种语言的翻译版本呢？

xgettext这个程序，会从源代码里识别到gettext。生成对应的pot文件（Portable Object Template）。

例如，上面的例子得到的pot文件内容是这样的：

```
msgid "my name is %s\n"
msgstr ""
```

使用msginit程序，可以从pot文件得到一个po文件。

```
msginit --local=zh_CN --input=name.pot
```

然后我们就手动修改po文件。填入翻译的内容：

```
msgid "my name is %s\n"
msgstr "我的名字是%s\n"
```

然后msgfmt程序，将po文件编译为二进制的mo文件。

gnu gettext使用gmo扩展名。就可以使用了。





参考资料

1、

<https://blog.csdn.net/yjwx0018/article/details/52312437>