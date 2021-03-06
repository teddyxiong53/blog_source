---
title: 渗透之exe捆绑
date: 2020-09-22 09:36:30
tags:
	- 渗透

---

1

一直都对EXE捆绑机很感兴趣,想知道那种运行一个EXE文件就相当于运行多个EXE文件的软件是什么原理.

其实捆绑机在不懂之前感觉很神秘,弄懂它的原理后就很简单了,下面就开始解说捆绑机的制作原理.

 想实现运行一个EXE文件同时运行其它多个EXE文件,**必须要把多个EXE文件"组合"成一个EXE文件,**

**而这一个EXE文件还必须有"分解"的能力,**

这样才能把捆绑起来的EXE分离出来,使之正常运行.

而"组合"也可以有多种形式,比如把**EXE文件一个一个的加到文件末尾,**

或者**以资源形式组合到一个EXE文件**中,

还有复杂一点的利用专用的安装打包工具组合(例如安装时捆绑的流氓软件).

下面主要介绍最简单的**第一种组合方式,也称为传统式捆绑机**,其他方式可以触类旁通,举一反三.

  我把捆绑之前的文件叫宿主文件,

其他EXE文件依次捆绑在宿主文件尾部.

宿主文件运行的时候检查自身文件大小,

如果发现比"纯洁"的宿主文件大就说明有别的EXE文件捆绑在宿主文件后,

那么就把那个文件从自身读出来创建成一个新文件,否则就什么都不做退出(具体请参加源码).

  捆绑就更简单了,一般需要另写一个专门用来捆绑的程序,

我管它叫主程序.

主程序要和宿主文件协调工作,以规范的方式捆绑文件这样宿主文件才能读出捆绑的文件.

比如在轩辕EXE捆绑机中就是简单的在宿主文件后先写入捆绑文件的大小,然后就是整个EXE文件.

这样宿主文件先读出一个大小,再按大小读取相应个字节就能分解出EXE文件.

  运行方式:

一般都是创建成一个新的EXE文件,并运行.

不知道能不能直接读入内存运行,我功力太差就只能写文件了.

功能强大一些的捆绑机还可以加入对运行程序的控制,比如隐藏运行,定时运行,关闭后自动删除等.

  轩辕EXE捆绑机制作初衷就是为了技术研究,根本没打算做成一个黑客工具,

对捆绑的文件没有进行特殊处理(比如对文件每一个字节和文件大小进行异或运算,这里仅提供个思路),捆绑的文件运行后会在c:\windows\temp下创建捆绑的EXE文件,并运行.

  好了捆绑机的原理就介绍到这,是不是非常简单?



捆绑器病毒是一个很新的概念，

人们编写这些程序的最初目的是希望通过**一次点击可以同时运行多个程序，**

然而这一工具却成了病毒的新帮凶。

比如说，用户可以将一个小游戏与病毒通过捆绑器程序捆绑，

当用户运行游戏时，病毒也会同时悄悄地运行，给用户计算机造成危害。



## 传统捆绑器

这种原理很简单，也是用的最多的一种。

就是将B.exe附加到A.exe的末尾。这样当A.exe被执行的时候，B.exe也跟着执行了。

这种捆绑器的代码是满网都是。我最早是从jingtao的一篇关于流的文章中得知的。已经没什么技术含量了。

检测方法：稍微懂一点PE知识的人都应该知道。一个完整有效的PE/EXE文件，他的里面都包含了几个绝对固定的特点[不管是否加壳]。

一是文件以MZ开头，跟着DOS头后面的PE头以PE\0\0开头。

有了这两个特点，检测就变得很简单了。

**只需利用UltraEdit一类工具打开目标文件搜索关键字MZ或者PE。**

**如果找到两个或者两个以上。则说明这个文件一定是被捆绑了。**

不过值得注意的是，一些生成器也是利用了这个原理，将木马附加到生成器末尾，用户选择生成的时候读出来。

另外网上流行的多款“捆绑文件检测工具”都是文件读出来，然后检索关键字MZ或者PE。

说到这里，相信大家有了一个大概的了解。那就是所谓的“捆绑文件检测工具”是完全靠不住的一样东西。

## 包源捆绑器

就这原理也很简单。

大部分检测器是检测不出来的，但[灰鸽子木马](https://baike.baidu.com/item/灰鸽子木马)辅助查找可以检测出捆绑后未经加壳处理的EXE文件。

但一般人都会加壳，所以也十分不可靠。

这个学过编程或者了解PE结构的人都应该知道。资源是EXE中的一个特殊的区段。

可以用来包含EXE需要/不需要用到的任何一切东西。

利用这个原理进行100%[免杀](https://baike.baidu.com/item/免杀)捆绑已经让人做成了动画。

大家可以去下载看看。那捆绑器是如何利用这一点的呢？

这只需要用到[BeginUpdateResource](https://baike.baidu.com/item/BeginUpdateResource)、[UpdateResource](https://baike.baidu.com/item/UpdateResource)和[EndUpdateResource](https://baike.baidu.com/item/EndUpdateResource)这三个API函数就可以搞定。

这三个API函数是用来做资源更新/替换用的。

作者只需先写一个包裹捆绑文件的头文件Header.exe.头文件中只需一段释放资源的代码。

而捆绑器用的时候先将头文件释放出来，然后用上面说的三个API函数将待捆绑的文件更新到这个头文件中即完成了捆绑。

类似原理被广泛运用到[木马生成器](https://baike.baidu.com/item/木马生成器)上。

检测方法：一般这种很难检测。如果你不怕麻烦，可以先将[目标文件](https://baike.baidu.com/item/目标文件)进行脱壳。

然后用“[灰鸽子木马](https://baike.baidu.com/item/灰鸽子木马)辅助查找”或“ResTorator”一类工具将资源读出来进行分析。但这种方法毕竟不通用。

所以还是推荐有条件的朋友使用[虚拟机](https://baike.baidu.com/item/虚拟机)。



参考资料

1、EXE捆绑机制作原理

https://www.cnblogs.com/qintangtao/archive/2013/02/21/2919994.html

2、捆绑器

https://baike.baidu.com/item/%E6%8D%86%E7%BB%91%E5%99%A8/10844115

3、捆绑后门的艺术–CobaltStrike backdoor分析

https://www.secpulse.com/archives/110317.html