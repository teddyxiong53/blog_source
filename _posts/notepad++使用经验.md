---
title: notepad++使用经验
date: 2017-05-14 17:26:35
tags:
	- notepad++

---

notepad++是常用的编辑器，下面把一些使用经验记录下来，以备后面查阅。以下简称为npp。



# 配对括号高亮

npp自动的括号补全，有些不好用，例如在生成括号后，你再马上敲一个括号，它只给你生成半边。这么写着写着括号，就不配对了。有时候就需要查看一下括号配对是否是自己想要的。默认的模式设置，这种配对关系不容易看出来。不过可以自己配置颜色，让这个配对提示变得很明显。

操作方法如下：

```
设置--语言格式设置--Global Styles--Brace highlight style--然后把前景色和背景色改一下就好了。
```

# 实用快捷键

通过菜单设置，管理快捷键这里来查看。把常用的记下来。在平时多用，提高效率。



Ctrl + L：删除当前行。

Ctrl + T：上下行交换。

Ctrl + D：复制当前行。

Ctrl + Shift + Q：注释选中部分。用多行注释。

Ctrl + Q：用单行注释。

Ctrl + Delete或者Backspace，可以一次删除一个单词。

Ctrl + B ：转到匹配的括号。

Ctrl + Alt + B：选中括号内的内容。

Ctrl + U：转小写。

Ctrl + Shift + U：转大写。





版本

有ansi版本和unicode 2个版本。

可以在“关于”菜单里看到。如果是Unicode版本，会特意标注的。

尽量使用Unicode的版本。

安装64位的版本。

保证可以方便安装插件。



# 正则表达式使用经验

替换的时候，使用正则表达式，还是非常方便的。

所以要多用。

C语言结构体，把内容拷贝出来，改造为json文件内容。

1、去掉//注释内容。

```
匹配：用贪婪模式。
//.*
替换：
（空的）
```

2、去掉数据类型。

```
这个按单词匹配就好了。
```

3、给每一行的单词加上前后引号。

```
匹配：
[\w]{2,}
替换：
"$0"
```

4、然后给引号的第二部分，替换为

```
匹配：这样才是匹配第二部分的引号。
"$
替换
":"",
```





# 参考资料

1、在Linux系统上安装NotePad++的三种方法介绍

https://ywnz.com/linuxjc/5382.html

2、

https://www.crifan.com/files/doc/docbook/rec_soft_npp/release/htmls/npp_func_regex_replace.html

3、3.4. Notepad++的正则表达式替换和替换

这篇文章写得非常好。是crifan写的。

http://shouce.jb51.net/notepad_book/npp_func_regex_replace.html