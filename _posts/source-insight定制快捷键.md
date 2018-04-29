---
title: source insight定制快捷键
date: 2016-11-03 22:43:08
tags:
	- source insight
typora-root-url: ..\
---
source insight是大名鼎鼎的代码阅读工具，因为非常轻巧，所以我把它也作为一个写代码的工具，下面总结我的一些实用经验。
# 自定义快捷键
快捷键就是生产力。source insight其实有不少的功能还没有，用起来不太顺手，不过还好有自定义快捷键的方法来解决这种问题。下面就列出我定义的一些快捷键。尽量定义地合理好用好记。
我尽量自定义的快捷键用Alt+Shift来做开头。后面就用命令的首字母来做。
* 打开文件所在目录。
  菜单里options--custom commands，点击Add，添加一条叫open folder的命令。在run里面输入`explorer /select, %f`。然后点击keys按钮，定义一个快捷键。我们就把快捷键定为Alt+Shift+o。o表示open。
  ![](/images/si-custom-commands.jpg)

* 弹出window list，以便选择需要的文件。
  这个命令source insight里有了，只是差一个快捷键而已。
  在菜单里options--Key Assignments。找到`Windows: Window List...`，点击`Assign New Key`。把快捷键定为`Alt+Shift+L`。L表示list。

# 解决阅读linux源代码的解析问题
linux里定义了大量的宏，用法非常复杂，source insight无法正常解析。所以需要改一改c语言的解析规则，来保证linux源代码可以支持进行解析。
在`C:\Program Files (x86)\Source Insight 3`安装目录下，找到c.tom文件。
tom文件是Token Macro File的意思。
```
Language                  File Name
 
C and C++          C.tom – a default copy ships with Source Insight.
 
HTML               Html.tom
 
Java               Java.tom

```
我们摘取c.tom文件的一部分看看。基本是就是把宏的定义填到这个文件里就好了，这样source insight就会忽略这些宏，从而正常识别函数和变量。
```
BEGIN_PROPERTY_MAP(theClass)
BEGIN_PROP_MAP(theClass)
PROP_ENTRY(szDesc, dispid, clsid)
```

# c.tom修改后重新载入

修改了c.tom文件，如果要马上触发生效，有个简单的方式，就是拖一个c文件到source insight里。就可以马上触发。































