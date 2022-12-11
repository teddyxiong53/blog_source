---
title: lua为什么在游戏领域广泛应用
date: 2022-12-10 20:13:19
tags:
	- lua

---

--

大部分语言的虚拟机设计的目的是为了直接解决实际问题的，

所以希望虚拟机能够独立运行，

这就与线程、进程等等操作系统功能发生了直接联系。

比如Python环境就直接是全局变量，

导致你无法在C里面优雅地使用一个沙盒式的Python环境，

也就是说Python环境和C代码的部分理论上来讲是毫无分隔的。



Lua所有API的设计，都带有上面的lua_State* L参数，

这就用无副作用的方式让Lua成为了一种非常非常非常适合嵌入的语言。

无论你的框架是如何复杂，你总能找到一种简单的嵌入Lua的方式而且对框架没什么影响。



lua适合业务频繁变更的场景。



比如说 Adobe Photoshop Lightroom 的 40% - 60% 由 Lua 写成。版本 3.0 之后几乎没有新的 non-Lua 代码加入。但是大多数非专业人士连 Lightroom 这个名字都没有听到过。所以说，Lua 在游戏领域被广泛运用只是 Lua 被所有领域广泛应用的显现。



有人给Lua 克服的问题起了一个名字：集成污染。



《大话西游》用的脚本语言是微软的JScript（JavaScript的一种方言），维护不便bug多，

受系统IE版本的影响兼容性差。

所以2002年网易开发《大话西游II》时，决定在客户端内嵌别的脚本语言。

当时该项目技术负责人云风认为**要挑不出名的语言，让做外挂的人搞不懂**（《大话西游》一代被外挂《[月光宝盒](https://www.zhihu.com/search?q=月光宝盒&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A19099371})》搞死了），于是就选择了Lua 4.0。

云风在游戏开发领域声望高。网易《大话西游II》是首个在市场上取得成功的国产网络游戏。所以后来国内游戏开发行业纷纷受此影响采用Lua.



云风为了防外挂，后来修改了《大话西游II》的Lua字节码格式，让官方的Lua虚拟机无法兼容《大话西游II》的Lua字节码。如果采用不开源的JScript，就不可能自己修改虚拟机和编译器了。



但游戏App的主要逻辑并不是命令式的，而是涉及大量的数据结构处理。

例如相机渲染要分层，对象刷新使用链表，处理碰撞使用[八叉树](https://www.zhihu.com/search?q=八叉树&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A843708301})等，一个游戏对象的不同组件有各自的数据结构，远比应用型App中以[控件树](https://www.zhihu.com/search?q=控件树&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A843708301})为主的数据结构要复杂。



**脚本语言对非程序专业的同学更友好**

开发一款游戏并不单单是程序员的事。例如策划，他们需要定制游戏中用的的各种数值（资源转化、升级进度这些），甚至编写NPC的[行为树](https://www.zhihu.com/search?q=行为树&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A843708301})。

脚本语言运行环境简单，学习曲线平滑，能够构建DSL（领域特定语言），更为非程序专业的同学接受。



参考资料

1、lua为什么在游戏领域广泛应用

https://www.zhihu.com/question/21717567