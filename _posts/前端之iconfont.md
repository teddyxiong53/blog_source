---
title: 前端之iconfont
date: 2020-09-03 10:01:59
tags:
	- 前端
---

1

**icon font** ，图标字体，也叫字体图标，顾名思义，就是字体做的图标。受到近些年 **扁平化设计** 的影响，越来越多的图标都开始使用 **icon font**

**优点：**

1. 自由的变化大小，且不会模糊
2. 比图片小，加载快
3. 可以任意改变颜色

**缺点：**

1. 只能被渲染成单色或者CSS3的渐变色
2. 创作自已的字体图标很费时间，重构人员后期维护的成本偏高。



我们都知道，在网页制作中，会经常用到不同的字体，常用的有 **微软雅黑**、**宋体**、**Aria** 等等。在我们写css的样式的时候，通过 **font-family** 可以指定元素的字体名称。

如果是 **特殊字体** ，因为我们的电脑没有安装那个字体，所以在网页中显示不出来，所以我们通过 **@font-face** 来引入特殊字体。

**WebFont** 技术可以让网页使用在线字体，在国外，**WebFont** 已经非常流行了，

大量的网站使用了 **WebFont** 技术，

而业界大佬 Google 也顺势推出的免费 **WebFont** 云托管服务，

这一切均带动了国外字体制作行业的高速发展。

为什么是国外呢，那是因为中文字体比较尴尬，

英文字体只有26个字母，一套字体不过几十 **KB** ，

而汉字却有数万个，导致字体文件通常有好几 **MB** 大小，

再加上国内的网络环境，显然不现实。

所以中文的 **特殊字体** 必须经过压缩才能使用，怎么压缩呢，请看 **腾讯ISUX** 开发的 [中文字体压缩器--字蛛（FontSpider）](http://font-spider.org/) 。



# 原理

每种字体在相同的字都是不一样的，比如 **宋体** 跟 **微软雅黑** ，相同的字 ，由于调用的不同的字体，浏览器显示明显是有区别的。

在我们还不识字的时候，每个字都是一个图案，

所以老师会告诉你哪个图案念什么 ，是什么字，

**iconfont** 同理，我认为 **三角形** 是 **a**，那对于我来说，只要是 **a** ，就应该是个 **三角形**。

在电脑上，我给电脑规定 **a** 的样子是个 **三角形**，那么当显示 **a** 的时候，他就显示个三角形。

当我把网页上的所有图标都对应一个字符的时候，你在代码里输入某个字符，那这个字符就显示你规定的形状，这就是 **iconfont** 图标。

**把所有的图标都放在一个字体里面，就是一个字体库了**，然后按照正常字体库（本来就是正常的字体库）调用就行了。



可以用typetool来打开字体文件，查看里面的内容。

但是这个工具是收费的。

这个是在线工具。

http://fontstore.baidu.com/static/editor/index.html



# 使用入门

https://www.iconfont.cn

打开这个网站，使用github账号进行登陆。

在搜索框搜索“美女”。

点击上面的购物车样式的图标，则是表示添加到库。

![image-20210105141227765](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210105141227765.png)

现在可以看到我们添加了3个图标到库了。

![image-20210105141338445](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210105141338445.png)



![image-20210105141414180](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210105141414180.png)

下载到本地，解压开是这样。

![image-20210105141448074](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210105141448074.png)

打开demo_index.html文件。

![image-20210105141706590](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210105141706590.png)

可以看到，是有3种方式来引用这些图标的。

方法1：直接使用unicode。

优点是兼容性好，就跟文字是等价的，缺点是只能单色。

而且Unicode很不直观，是一串十六进制的数字。

```
<span class="iconfont">&#x33;</span>
```



方法2：使用font class

这个是Unicode的改进，就是要解决Unicode不直观的问题。

```
<link rel="stylesheet" href="./iconfont.css">
<span class="iconfont icon-xxx"></span>
```

![image-20210105142541038](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210105142541038.png)

方法3：使用symbol

这是一种全新的方式，应该说这个才是未来的主流。

也是推荐的用法。

这种用法实际上是做了一个svg的集合。

相比于前面两种方式，有如下特点：

1、支持多色图标。

2、通过一些技巧，支持像字体那样，通过font-size、color来调整样式。

3、兼容性较差

4、浏览器渲染svg的性能一般，还不如png。

使用方法：

```
引入iconfont.js文件。
<script src="./iconfont.js"></script>
加入通用css代码，引入一次就可以了。
<style>
.icon {
  width: 1em;
  height: 1em;
  vertical-align: -0.15em;
  fill: currentColor;
  overflow: hidden;
}
</style>

挑选对应的图标，并获取类名。
<svg class="icon" aria-hidden="true">
  <use xlink:href="#icon-xxx"></use>
</svg>
```



参考资料

1、css3中，`&#xe66c;`这样的代码为什么会显示成图片？

https://segmentfault.com/q/1010000008327512

2、iconfont字体图标的使用方法--超简单!

https://www.cnblogs.com/hjvsdr/p/6639649.html

3、Ionic使用Iconfont-阿里巴巴矢量图标库

https://jingyan.baidu.com/article/14bd256e4bd36bbb6c26126e.html#5827690-tsina-1-80491-fe183374908e783f9dbfe7dcb7ed2bb5