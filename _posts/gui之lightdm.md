---
title: gui之lightdm
date: 2021-05-28 14:30:11
tags:
	- gui

---

--

LightDM，即：Light Display Manager，

是一个全新的、轻量的Linux桌面的**桌面显示管理器**，

而传统的Ubuntu用的是GNOME桌面标准的GDM 。

 LightDM是一个跨桌面显示管理器，

其目的是成为 X org X 服务器的标准显示管理器。

我们之所以编写一个新的显示管理器，

是因为从XDM以来 （通常基于 XDM 源代码） 出现了很多新的显示管理器。

这些项目之间的主要区别是在GUI（比如说不同的开发工具包） 和性能上面— — 这些可以更好地用一个通用的显示管理器实现，并允许这些差异。

**主要特点包括：**

- **轻量**：LightDM是2010年开始的新项目，一开始就设计为轻量、小巧，没有GDM那样的历史代码负担，因此不仅完整支持标准，而且轻量、快速。
- **支持各种界面**：相较于[GDM](https://baike.baidu.com/item/GDM/4597441)－GTK，[KDM](https://baike.baidu.com/item/KDM)－Qt，LightDM实际上是界面无关性的，因为它设计上就是支持本地图形界面以获得最好的兼容性。因此LightDM已经具备了[GTK](https://baike.baidu.com/item/GTK/3138659)、[Qt](https://baike.baidu.com/item/Qt/451743)甚至[WebKit](https://baike.baidu.com/item/WebKit/1467841)的界面，也就是用[HTML](https://baike.baidu.com/item/HTML/97049)来做登陆界面。
- **可配置性**：[Linux](https://baike.baidu.com/item/Linux/27050)最大的优势就是定制性强了，LightDM也继承了这一优点，除了可以定制上面提到的界面以外，LightDM还可以定制其他丰富的选项，如自动登录、禁止特定用户登录等等 [1] 
- **一个支持多个[图形用户界面](https://baike.baidu.com/item/图形用户界面/3352324)的良好的 API**
- **通过合适的插件支持所有显示管理器**
- **代码复杂度低**
- **高速性能**



显示管理器或登录管理器

是一个在启动最后显示的图形界面,即登录界面(显示管理器),是进到桌面环境之前的用户登录界面。





参考资料

1、lightdm

https://baike.baidu.com/item/LightDM/9557430?fr=aladdin