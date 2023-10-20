---
title: js引擎之quickjs分析
date: 2023-04-27 10:31:11
tags:
	- quickjs
---

--

本来不打算看这个的，但是看了jerryscript，那个代码也看起来非常繁琐。

而这个看起来就干净整洁很多。所以还是研究一下。

# 资料收集

知乎topic

https://www.zhihu.com/topic/21191363/hot

这篇文章非常好。QuickJS 引擎一年见闻录

https://ewind.us/2020/quickjs-one-year-brief/



https://zhuanlan.zhihu.com/p/456759292

# js发展历史

第一个图文浏览器是1993年的 Mosaic，由 Marc Andreessen 开发。

后替代 Mosaic 的是 Netscape 的 Netscape Navigator 浏览器。

Brendan Eich 给 Netscape 开发 Java 辅助语言 Mocha（后更名为 JavaScript），耗时10天出原型（包含了eval 函数），集成到 Netscape 2预览版里，

Mocha 基于对象而非 Java 那样基于类。

Mocha 采用源码解析生成字节码解释执行方式而非直接使用字节码的原因是 Netscape 公司希望 Mocha 代码简单易用，能够直接在网页代码中编写。

直到现在各 js 引擎都还不直接使用字节码，

**这是由于不同的 js 引擎都有自己的字节码规范，**

不像 js 代码规范有统一一套，

而且字节码会有捆绑版本和验证难的问题。

 TC39 有份中间代码的提案，叫做 Binary AST，

提案在这 [Binary AST Proposal Overview](https://link.zhihu.com/?target=https%3A//github.com/tc39/proposal-binary-ast)。

Binary AST 这份提案还会去设计解决变量的绑定机制对解析性能影响，

还有延缓 Early Error 语义到最近的 enclosing 函数或全局执行脚本的时候来提升解析性能，

解决区分列表表达式和箭头函数参数列表的区别需要做回溯等可能会存在字符层面歧义，还有单字节和双字节编码检查的问题，字符串和标识符使用 UTF-8，不用转义码。

Binary AST 借鉴 WebAssembly 对解析后得到的 AST 使用基本 primitives（字符串、数字、元组）来进行简单二进制编码，再压缩，每个文件都会有个 header 来保证向前和向后的兼容，节点种类通过 header 的索引来引用，避免使用名称可能带来的版本问题，为减少大小会支持 presets。



下面回到90年代，接着说代号是 Mocha 的 JavaScript 发展历程。

Mocha 的动态的对象模型，

使用原型链的机制能够更好实现，

对象有属性键和对应的值，

属性的值可以是多种类型包括函数、对象和基本数据类型等，

找不到属性和未初始化的变量都会返回 undefined，

对象本身找不到时返回 null，null 本身也是对象，表示没有对象的对象，

因此 typeof null 会返回 object。

基础类型中字符串还没支持 Unicode，有8位字符编码不可变序列组成，数字类型由 IEEE 754 双精度二进制64位浮点值组成。

新的属性也可以动态的创建，使用键值赋值方式。



Brendan Eich 喜欢 Lisp，来 Netscape 本打算是将 lisp 引入浏览器的。

因此 Mocha 里有着很多的 lisp 影子，比如函数一等公民和 lambda，

函数是一等公民的具体表现就是，函数可以作为函数的参数，函数返回值可以是函数，也可将函数赋值给变量。

Brendan Eich 的自己关于当时开发的回顾文章可以看他博客[这篇](https://link.zhihu.com/?target=https%3A//brendaneich.com/2008/04/)，还有这篇《[New JavaScript Engine Module Owner](https://link.zhihu.com/?target=https%3A//web.archive.org/web/20190320112431/https%3A//brendaneich.com/2011/06/)》，访谈稿《[Bending over backward to make JavaScript work on 14 platforms](https://link.zhihu.com/?target=https%3A//www.infoworld.com/article/2077132/bending-over-backward-to-make-javascript-work-on-14-platforms.html)》。



Netscape 2 正式版将 Mocha 更名为 JavaScript，后简称 js。

1.0 版本 js 语法大量借鉴 C 语言。

行末可不加分号，一开始 js 就是支持的。

1.1版 js 支持隐式类型转换，可以把任意对象转成数字和字符串。

1.0版 js 对象不能继承，

1.1 加入对象的 prototype 属性，prototype 的属性和实例的对象共享。

为了加到 ISO 标准中，Netscape 找到了 Ecma，因为 ISO 对 Ecma 这个组织是认可的。

接着 Ecma 组建了 TC39 技术委员会负责创建和维护 js 的规范。

期间，微软为了能够兼容 js，组建了团队开发 JScript，过程比较痛苦，

因为 js 的规范当时还没有，微软只能自己摸索，

并写了份规范 [The JScript Language Specification, version 0.1](https://link.zhihu.com/?target=http%3A//archives.ecma-international.org/1996/TC39/96-005.pdf) 提交给 TC39，

微软还将 VBScript 引入 IE。

96年 Netscape 为 JavaScript 1.1 写了规范 [Javascript 1.1 Specification in Winword format](https://link.zhihu.com/?target=http%3A//archives.ecma-international.org/1996/TC39/96-002.pdf) 作为 TC39 标准化 js 的基础。

97年 TC39 发布了 [ECMA-262 第一版规范](https://link.zhihu.com/?target=https%3A//www.ecma-international.org/wp-content/uploads/ECMA-262_1st_edition_june_1997.pdf)。



Netscape 3 发布后，Brendan Eich 重构了 js 引擎核心，加了嵌套函数、lambda、正则表达式、伪属性（动态访问修改对象）、对象和数组的字面量、基于标记和清除的 GC。



lambda 的函数名为可选，运行时会创建闭包，闭包可递归引用自己作为参数。

新 js 引擎叫 SpiderMonkey。

js 语言增加新特性，从更多语言那做了借鉴，

比如 Python 和 Perl 的数组相关方法，Perl 对于字符串和正则的处理，Java 的 break / continue 标签语句以及 switch。

语言升级为 JavaScript 1.2（[特性详细介绍](https://link.zhihu.com/?target=https%3A//web.archive.org/web/19970630092641/http%3A//developer.netscape.com/library/documentation/communicator/jsguide/intro.htm)），和 SpiderMonkey 一起集成到 Netscape 4.0。

[ES3](https://link.zhihu.com/?target=https%3A//www.ecma-international.org/wp-content/uploads/ECMA-262_3rd_edition_december_1999.pdf) 结合了 js 1.2 和 JScript 3.0，I18N 小组为 ES3 加入了可选 Unicode 库支持。

开始兼容 ES3的浏览器是运行微软 JScript 5.5的 IE 5.5，运行 js 1.5 的 Netscape 6。



ES3 标准坚持了10年。

这10年对 js 设计的抱怨，也可以说 js 不让人满意的地方，

在这个地方 [wtfjs - a little code blog about that language we love despite giving us so much to hat](https://link.zhihu.com/?target=https%3A//wtfjs.com/) 有汇总。

当然也有人会站出来为 js 正名，比如 Douglas Crockford，可以看看他的这篇文章 [JavaScript:The World's Most Misunderstood Programming Language](https://link.zhihu.com/?target=http%3A//www.crockford.com/javascript/javascript.html)，

里面提到很多书都很差，比如用法和特性的遗漏等，只认可了 JavaScript: The Definitive Guide 这本书。

并且 Douglas Crockford 自己还写了本书 JavaScript: The Good Parts，中文版叫《JavaScript语言精粹》。

另外 Douglas Crockford 做出的最大贡献是利用 js 对象和数组字面量形式实现了独立于语言的数据格式 JavaScript Object Notation，并加入 TC39 的标准中，JavaScript Object Notation 也就是我们如今应用最多的数据交换格式 JSON 的全称。



ES4 初期目标是希望能够支持类、模块、库、package、Decimal、线程安全等。

2000年微软 Andrew Clinick 主导的.NET Framework 开始支持 JScript。

微软希望通过 ES4 标准能够将 JScript 应用到服务端，并和以往标准不兼容。

浏览器大战以 Netscape 失败结束后，微软取得了浏览器统治地位，对 TC39 标准失去了兴趣，希望用自家标准取而代之，以至 TC39 之后几年没有任何实质进展。



这个期间流行起来的 Flash 使用的脚本语言 ActionScript 也只是基于 ES3 的，

2003年 ActionScript 2.0 开始支持 ES4 的提案语法以简化语义，

为了提升性能 Flash 花了3年，在2007年开发出 AVM2虚机支持静态类型的 ActionScript 3.0。

那时我所在的创业公司使用的就是 flash 开发的图形社交网站 xcity，网站现在已经不在了，只能在 [xcity贴吧](https://link.zhihu.com/?target=https%3A//tieba.baidu.com/f%3Fie%3Dutf-8%26kw%3Dxcity)找到当年用户写的故事截的图。



Brendan Eich 代表 Mozilla 在2004年开始参与 ES4 的规划，

2006年 Opera 的 Lars Thomas Hansen 也加入进来。

Flash 将 AVM2 给了 Mozilla，命名为 Tamarin。

起初微软没怎么参与 ES4 的工作，后来有20多年 Smalltalk 经验的 Allen Wirfs-Brock 加入微软后，

发现 TC39正在设计中 ES4 是基于静态类型的 ActionScript 3.0，

于是提出动态语言加静态类型不容易成，而且会有很大的兼容问题，

还有个因素是担心 Flash 会影响到微软的产品，

希望能够夺回标准主动权。

Allen Wirfs-Brock 的想法得到在雅虎的 Douglas Crockford 的支持，他们一起提出新的标准提案，提案偏保守，只是对 ES3 做补丁。



AJAX，以及支持 AJAX 和解决浏览器兼容性问题的库 jQuery 库（同期还有 Dojo 和 Prototype 这样 polyfill 的库）带来了 Web2.0时代。

polyfill 这类库一般使用命名空间对象和 IIFE 方式解决库之间的命名冲突问题。

我就是这个时期开始使用 js 来开发自己的网站 [www.starming.com](https://link.zhihu.com/?target=http%3A//www.starming.com/)，

当时给网站做了很多小的应用比如图片收藏、GTD、博客系统、记单词、RSS订阅，

还有一个三国演义小说游戏，

记得那会通过犀牛书（也就是 Douglas Crockford 推荐的 JavaScript: The Definitive Guide ，中文版叫《JavaScript 权威指南》）学了 js 后，

就弄了个兼容多浏览器的 js 库，然后用这个库做了个可拖拽生成网站的系统。

2013年之后 starming 已经做成了一个个人博客，现在基于 hexo 的静态博客网站。

2013年之前的 starming 网站内容依然可以通过 [https://web.archive.org/](https://link.zhihu.com/?target=https%3A//web.archive.org/) 网站查看到，点击这个[地址](https://link.zhihu.com/?target=https%3A//web.archive.org/web/20130124221354/http%3A//www.starming.com/)。

2006年 Google 的 Lars Bak 开始了 V8 引擎的开发，2008 基于 V8 的 Chrome 浏览器发布，性能比 SpiderMonkey 快了10倍。

V8 出来后，各大浏览器公司开始专门组建团队投入 js 引擎的性能角逐中。

当时 js 引擎有苹果公司的 SquirrelFish Extreme、微软 IE9 的 Chakra 和 Mozilla 的 TraceMonkey（解释器用的是 SpiderMonkey）。



随着 IBM、苹果和 Google 开始介入标准委员会，

更多的声音带来了更真实的诉求，

TC39 确定出 ES4 要和 ES3 兼容，

同时加入大应用所需的语言特性，比如类、接口、命名空间、package，还有可选静态类型检查等等。

部分特性被建议往后延，比如尾调用、迭代器生成器、类型自省等。

现在看起来 ES4 10年设计非常波折，激进的加入静态类型，不兼容老标准，把标准当研究而忽略了标准实际上是需要形成共识的，而不是要有风险的。

在 TC39 成员达成共识后，ES4 还剔除了 package 和命名空间等特性，由于 Decimal 的设计还不成熟也没能加入。

由于 ES4 很多特性无法通过，而没法通过标准，因此同步设计了10年多的 ES 3.1 最终改名为 ES5，也就是 ECMA-262 第 5 版。

ES5 主要特性包括严格模式，对象元操作，比如setter、getter、create等，另外添加了些实用的内置函数，比如 JSON 相关解析和字符串互转函数，数组增加了高阶函数等等。

ES5 的测试套件有微软 Pratap Lakshman 的，[这里](https://link.zhihu.com/?target=https%3A//www.ecma-international.org/archive/ecmascript/2009/TC39/tc39-2009-030.zip)可以下载看到，谷歌有 [Sputnik](https://link.zhihu.com/?target=https%3A//blog.chromium.org/2009/06/launching-sputnik-into-orbit.html)，有5000多个测试，基于他们，TC39 最后统一维护著名的 Test262 测试套件。



ES5 之后 TC39 开始了 Harmony 项目，

Harmony 开始的提案包括类、const、lambda、词法作用域、类型等。

从 Brenda Eich 的 《[Harmony Of My Dreams](https://link.zhihu.com/?target=https%3A//brendaneich.com/2011/01/harmony-of-my-dreams/)》这篇文章可以 js 之父对于 Harmony 的期望，例如文章中提到的 # 语法，用来隐藏 return 和 this 词法作用域绑定，最终被 ES2015 的箭头函数替代，但 # 用来表示不可变数据结构没有被支持，模块和迭代器均获得了支持。



Harmony 设计了 Promise 的基础 Realm 规范抽象、内部方法规范 MOP、Proxy 对象、WeakMap、箭头函数、完整的 Unicode 支持、属性 Symbol 值、尾调用、类型数组等特性。

对于类的设计，TC39 将使用 lambda 函数、类似 Scheme 的词法捕获技术、构造函数、原型继承对象、实例对象、扩展对象字面量语法来满足类所需要的多次实例化特性。

模块的设计思路是通过 module 和 import 两种方式导入模块，

import 可以用模块声明和字符串字面量的方式导入模块。

模块导入背后是模块加载器的设计，

设计的加载流程是，

先处理加载标识的规范，再处理预处理，处理模块间的依赖，关联上导入和导出，最后再进行依赖模块的初始化工作。

整个加载过程可以看这个 js 实现的[原型](https://link.zhihu.com/?target=https%3A//github.com/jorendorff/js-loaders)，

后来这个加载器没有被加入规范，而由浏览器去实现。

CommonJS 作者 Kevin Dangoor 的文章《[CommonJS: the First Year](https://link.zhihu.com/?target=https%3A//www.blueskyonmars.com/2010/01/29/commonjs-the-first-year/)》写下做 CommonJS 的初衷和目标，标志着 js 开始在服务端领域活跃起来。

CommonJS 的思路就是将函数当作模块，和其他模块交互是通过导出局部变量作为属性提供值，

但是属性能被动态改变和生成，所以对于模块使用者，这是不稳定的。

Ryan Dahl 2009 开发的 Node.js （介绍参看作者[jsconf演讲](https://link.zhihu.com/?target=https%3A//www.youtube.com/watch%3Fv%3DztspvPYybIY%26feature%3Dyoutu.be%26ab_channel%3Dstri8ted)）就是用 CommonJS 的模块加载器。

Node.js 链接了 POSIX API，网络和文件操作，

有个自己的 Event Loop，有些基础的 C 模块，还包含了 V8 引擎。



2010 年开始出现其他语言源码转 js 源码这种转译器的风潮，

最有代表的是 CoffeeScript，

CoffeeScript 某种程度上是对 js 开发提供了更优雅更先进的开发语言辅助。

从 CoffeeScript 一些特性在开发者的反馈，

能够更好的帮助 TC39 对 js 特性是否进入标准提供参考。

后来还有以优化性能为目的的 Emscripten 和 asm.js 翻译成高效 js 代码的转译器。

转义器对于 Harmony 甚至是后面的 ES2015 来说有着更重要的意义。

当时的用户没有主动进行软件升级的习惯，特别是由系统绑定的浏览器。

适配 IE6的痛苦，相信老一辈的前端开发者会有很深的体会。

大量浏览器低版本的存在对于新的标准推广造成了很大的阻碍，

因此使用新标准编写代码转移成可兼容低版本浏览器的代码能够解决兼容问题。

在 Harmony 项目开发过程中除了 Mozilla 使用 SpiderMonkey 引擎开发的 [Narcissus](https://link.zhihu.com/?target=https%3A//github.com/mozilla/narcissus/) 转译器外，

还有直到目前还在使用的 [Babel](https://link.zhihu.com/?target=https%3A//babeljs.io/) 和 [TypeScript 语言](https://link.zhihu.com/?target=https%3A//www.typescriptlang.org/)的转译器。

另外还有使用 rust 写的 js 编译器 [swc](https://link.zhihu.com/?target=https%3A//github.com/swc-project/swc)，主打速度，打算来替代 babel。

2015年，[ECMAScript 2015](https://link.zhihu.com/?target=https%3A//www.ecma-international.org/wp-content/uploads/ECMA-262_6th_edition_june_2015.pdf)发布。

ECMAScript 2015 之后，由于各个浏览器都开始更快的迭代更新， TC39 开始配合更新的节奏，开始每年更新标准，以年作为标准的版本号。

ES2016 增加了 async/await 异步语法特性，

纵观 js 的异步历程，

从最开始的 Callback方式到 Promise/then，js 解决了回调地狱的问题，

但缺少能够暂停函数和恢复执行的方法，

因此在 ES2015 加入了生成器，

其实现核心思想就是协程，

协程可以看作是运行中线程上的可暂停和恢复执行的任务，这些任务都是可通过程序控制的。

在 ES2016 加入简洁的 async/await 语法来更好的使用协程。

js 异步编程历程如下图：



ECMAScript 2016 开始 js 进入了框架百家争鸣的时代。

js 框架方面，早期 js 的框架是以兼容和接口优雅为基准比较胜出的 PrototypeJS 和 jQuery。

MVC 流行起来的框架是 Backbone，

MVVM 时代是 AngularJS 为代表的数据双向绑定只用关注 Model 框架新星崛起。

Vue 在 MVVM 基础上增加了用来替代 Options API 的 Composition API 比拟 React 的 Hooks。

React（React 的创作者是 [Jord Walke](https://link.zhihu.com/?target=https%3A//twitter.com/jordwalke)，在 facebook，不过现在已经离开了 facebook，创立了自己的公司）后来居上，

以函数式编程概念拿下头牌，这也是因为 React 核心团队成员喜欢 OCaml 这样的函数式编程语言的原因。。

React 的组件有阿里的 [Ant Design](https://link.zhihu.com/?target=https%3A//ant.design/index-cn) 和 [Fusion Design](https://link.zhihu.com/?target=https%3A//fusion.design/) 可用。

React 对于逻辑复用使用的是更优雅的 Hooks，接口少，以声明式方式供使用，

很多开发者会将自己开发的逻辑抽出来做成 hooks，

出现了很多基于 hooks 状态管理公用代码。

对于状态的缓存维护由 React 的内核来维护，

这能够解决一个组件树渲染没完成又开始另一个组件树并发渲染状态值管理问题，开发者能够专注写函数组件，和传统 class 组件的区别可以看 Dan Abramov 的这篇文章《[How Are Function Components Different from Classes?](https://link.zhihu.com/?target=https%3A//overreacted.io/how-are-function-components-different-from-classes/)》。





为了使 js 能够应用于更大的工程化中，出现了静态类型 js 框架。

静态类型的 js 框架有微软的 TypeScript 和 Facebook 的 [Flow](https://link.zhihu.com/?target=https%3A//flow.org/)。

TypeScript 的作者是当年我大学时做项目使用的 IDE Delphi 的作者 Anders Hejlsberg，当时的 Delphi 开发体验非常棒，我用它做过不少项目，改善了大学生活品质。



对于 React 的开发，现需要了解脚手架 [create-react-app](https://link.zhihu.com/?target=https%3A//github.com/facebook/create-react-app)，

一行命令能够在 macOS 和 Windows 上不用配置直接创建 React 应用。

然后是使用 JSX 模版语法创建组件，组件是独立可重用的代码，组件一般只需要处理单一事情，数据通过参数和上下文共享，上下文共享数据适用场景类似于 UI 主题所需的数据共享。

为了确保属性可用，可以使用 defaultProps 来定义默认值，使用 propTypes 在测试时进行属性类型设置和检查。在组件里使用状态用的是 Hooks，最常见的 Hooks 是 setState 和 useEffect，项目复杂后，需要维护的状态就会很复杂，React 本身有个简单使用的状态管理库 React Query 数据请求的库，作用类似 Redux，但没有模版代码，更轻量和易用，还可用 Hooks。React Router 是声明式路由，通过 URL 可以渲染出不同的组件。

react 跑在 QuickJS 上的方法可以参看 QuickJS 邮件列表里[这封邮件](https://link.zhihu.com/?target=https%3A//www.freelists.org/post/quickjs-devel/Running-React-on-QuickJS)。



React 框架对应移动端开发的是 React Native。

React Native 使用了类似客户端和服务器之间通讯的模式，通过 JSON 格式进行桥接数据传递。

React Native 中有大量 js 不适合编写的功能和业务逻辑，比如线程性能相应方面要求高的媒体、IO、渲染、动画、大量计算等，还有系统平台相关功能特性的功能业务代码。



这样的代码以前都是使用的原生代码和 C++ 代码编写，

C++ 代码通过静态编译方式集成到工程中，也能实现部分平台通用，

但是 C++ 编写代码在并发情况下非常容易产生难查的内存安全和并发问题，

对于一些比较大的工程，开启 Monkey 测试由于插桩导致内存会增大好几倍，从而无法正常启动，查问题更加困难。

当然 Rust 也许是另一种选择，rust 语言层面对 FFI 有支持，使用 extern 就可以实现 rust 与其他编程语言的交互。

rust 对内存安全和并发的问题都能够在编译时发现，而不用担心会在运行时发现，这样开发体验和效率都会提高很多，

特别是在重构时不会担心引入未知内存和并发问题。

使用 rust 编译 iOS 架构的产物也很简单，先安装 Rustup，然后在 rustup 里添加 iOS 相关架构，rust 的包管理工具是 cargo，类似于 cocoapods，cargo 的子命令 cargo-lipo 可以生成 iOS 库，创建一个 C 的桥接文件，再集成到工程中。对于 Android 平台，rust 有专门的 android-ndk-rs 库。rust 的 ffi 在多语言处理中需要一个中间的通信层处理数据，性能和安全性都不高，可以使用 flatbuffers 。关于序列化方案性能比较可以参看 [JSON vs Protocol Buffers vs FlatBuffers](https://link.zhihu.com/?target=https%3A//codeburst.io/json-vs-protocol-buffers-vs-flatbuffers-a4247f8bda6f) 这篇文章。



React Native 本身也在往前走。

以前 React Native 有三个线程，

分别是执行 js 代码的 JS Thread，

负责原生渲染和调用原生能力的 UI Thread，

模拟虚拟 DOM 将 Flexbox 布局转原生布局的 Shadow Thread。



三个线程工作方式是 JS Thread 会先对 React 代码进行序列化，

通过 Bridge 发给 Shadow Thread，

Shadow Thread 会进行反序列化，

形成虚拟 DOM 交由 Yogo 转成原生布局，

Shadow Thread 再通过 Bridge 传给 UI Thread，

UI Thread 获取消息先反序列化，再按布局信息进行绘制，

可以看出三个线程交互复杂，而且消息队列都是异步，

使得事件难保处理，

序列化都是用的 JSON 性能和 Protocol Buffers 还有 FlatBuffers 相比差很多。



新架构会从线程模型做改进，高优先级线程会直接同步调用 js，低优先级更新 UI 的任务不在主线程工作。

同时新架构的核心 JSI 方案简化 js 和原生调用，

改造成更轻量更高效的调用方式，用来替换 Bridge。

JSI 使得以前的三个线程通信不用都通过 Bridge 这种依赖消息序列化异步通信方式，而是直接同步通信，消除异步通信会出现的拥塞问题，

具体使用例子可以看这篇文章《[React Native JSI Challenge](https://link.zhihu.com/?target=https%3A//medium.com/%40christian.falch/https-medium-com-christian-falch-react-native-jsi-challenge-1201a69c8fbf)》。

另外 React Native 新架构的 JSI 是一个轻量的 C++桥接框架，通信对接的 js 引擎比如 JSC、Hermes、V8、QuickJS、JerryScript 可以很方便的替换。关于 JSI 的详情和进展可以参考其[提案地址](https://link.zhihu.com/?target=https%3A//github.com/react-native-community/discussions-and-proposals/issues/91)。



2019 年出现的 Svelte。

Svelte 的特点是构建出的代码小，使用时可以直接使用构建出带有少量仅会用到逻辑的运行时的组件，不需要专门的框架代码作为运行时使用，不会浪费。

Svelte 没有 diff 和 patch 操作，也能够减少代码，减少内存占用，性能会有提升。

当然 Svelte 的优点在项目大了后可能不会像小项目那么明显。



CSS 框架有 Bootstrap、Bulma、Tailwind CSS，

其中认可度最高的是 Tailwind CSS，

近年来 Bootstrap 持续降低，Tailwind CSS 和 Bootstrap 最大的不同就是 Tailwind CSS 没有必要的内置组件，因此非常轻量，还提供了 utility class 集合和等价于 Less、Sass 样式声明的 DSL。

浏览器对 CSS 样式和 DOM 结合进行渲染的原理可以参看我以前《[深入剖析 WebKit](https://link.zhihu.com/?target=https%3A//ming1016.github.io/2017/10/11/deeply-analyse-webkit/)》这篇文章。





在浏览器之外领域最成功的框架要数 Node.js 了。

Node.js 作者 Ryan Dahl 后来弄了 Deno，

针对 Node.js 做了改进。

基于 Node.js 开发应用服务的框架还有 Next.js，

Next.js 是一个 React 框架，

包括了各种服务应用的功能，比如 SSR、路由和打包构建，

Netflix 也在用 Next.js。

最近前端流行全栈无服务器 Web 应用框架，

包含 React、GraphQL、Prisma、Babel、Webpack 的 Redwood 框架表现特别突出，能够给开发的人提供开发 Web 应用程序的完整体验。



Node.js 后的热点就是开发工具，工程构建，最近就是 FaaS 开发。

工程开发工具有依赖包管理的 npm 和 yarn，webpack、Snowpack、Vite、[esbuild](https://link.zhihu.com/?target=https%3A//github.com/evanw/esbuild) 和 rollup 用来打包。

其中 esbuild 的构建速度最快。



测试框架有 Karma、Mocha、Jest，React 测试库 Enzyme。

其中 Jest 非常简单易用，可进行快照测试，可用于 React、Typescript 和 Babel 里，Jest 目前无疑是测试框架中最火的。

另外还有个 Testing Library 可用来进行 DOM 元素级别测试框架，接口易用，值得关注。



最近比较热门的是低代码，低代码做的比较好的有 [iMove](https://link.zhihu.com/?target=https%3A//github.com/imgcook/imove) 等，他们通过拖拽可视化操作方式编辑业务事件逻辑。

这里有份[低代码的 awesome](https://link.zhihu.com/?target=https%3A//github.com/taowen/awesome-lowcode)，收录了各厂和一些开源的低代码资源

2020 年 Stack Overflow 开发者调查显示超过半数的开发者会使用 js，这得益于多年来不断更新累积的实用框架和库，还有生态社区的繁荣，还有由各大知名公司大量语言大师专门为 js 组成的技术委员会 TC39，不断打磨 js。

js 背景说完了，接下来咱们来聊聊 QuickJS 的作者吧。







https://zhuanlan.zhihu.com/p/456759292

# 编码风格推测

有这样3种函数命名：

```
JS_GetPropertyUint32
	大小JS前缀，后面大驼峰的。这种是对外的函数接口。
find_hashed_shape_prop
	这种全部小写的。是内部工具函数。
js_loadScript
js_std_loadFile
	这种分别对了global和std模块的函数。
	
js_Date_now
	这种是类方法，Date是大写的。
js_date_getTime
	这种是对象方法，date是小写的。
```

数据类型：

```
所有结构体都typedef，
枚举都是
```



# 重要概念

如上图所示，其中最上层是 qjs 和 qjsc，qjs 包含了命令行参数处理，引擎环境创建，加载模块和 js 文件读取解释执行。

**qjsc 可以编译 js 文件成字节码文件，生成的字节码可以直接被解释执行，性能上看是省掉了 js 文件解析的消耗。**

中间层是核心，JSRuntime 是 js 运行时，可以看做是 js 虚拟机环境，多个 JSRuntime 之间是隔离的，

他们之间不能相互调用和通信。

JSContext 是虚机里的上下文环境，

一个 JSRuntime 里可以有多个 JSContext，

每个上下文有自己的全局和系统对象，

不同 JSContext 之间可以相互访问和共享对象。

JS_Eval 和 JS_Parse 会把 js 文件编译为字节码。

JS_Call 是用来解释执行字节码的。

JS_OPCode 是用来标识执行指令对应的操作符。

JSClass 包含标准的 js 的对象，

是运行时创建的类，

对象类型使用 JSClassID 来标记，

使用 JS_NewClassID 和 JS_NewClass 函数注册，

使用 JS_NewObjectClass 来创建对象。

JSOpCode 是字节码的结构体，

通过 quickjs-opcode.h 里的字节码的定义可以看到，

QuickJS 对于每个字节码的大小都会精确控制，

目的是不浪费内存使用，

比如8位以下用不到1个字节和其他信息一起放在那1个字节里，

8位用2个字节，整数在第2个字节里，16位用后2个字节。

Unicode 是 QuickJS 自己做的库 libunicode.c，

libunicode 有 Unicode 规范化和脚本通用类别查询，

包含所有 Unicode 二进制属性，

libunicode 还可以单独出来用在其他工程中。

中间层还包含支持科学计算 BigInt 和 BigFloat 的 libbf 库，

正则表达式引擎 libregexp。

扩展模块 Std Module 和 OS Module，提供标准能力和系统能力，比如文件操作和时间操作等。



底层是基础，JS_RunGC 使用引用计数来管理对象的释放。

JS_Exception 是会把 JSValue 返回的异常对象存在 JSContext 里，

通过 JS_GetException 函数取出异常对象。

内存管理控制 js 运行时全局内存分配上限使用的是 JS_SetMemoryLimit 函数，

自定义分配内存用的是 JS_NewRuntime2 函数，

堆栈的大小使用的是 JS_SetMaxStackSize 函数来设置。



## JSRuntime和JSContext关系

在QuickJS中，`JSRuntime`和`JSContext`是两个核心概念，用于管理JavaScript运行时的不同层面。它们之间的关系如下：

1. **JSRuntime**：
   - `JSRuntime`是QuickJS中的最高级别概念，代表一个JavaScript运行时环境。
   - ==一个`JSRuntime`可以包含多个`JSContext`，并且它们之间共享一些全局资源，如原型对象和标准库函数。==
   - `JSRuntime`通常在应用程序初始化时创建，然后在整个应用程序的生命周期内保持不变。这允许多个`JSContext`在同一个运行时环境内执行JavaScript代码，共享运行时环境的资源。

2. **JSContext**：
   - `JSContext`代表一个JavaScript执行上下文，其中可以执行JavaScript代码。
   - ==每个`JSContext`都是相对独立的，拥有自己的JavaScript对象、变量、堆栈等==。这意味着在一个`JSContext`中定义的变量和函数不会自动在其他`JSContext`中可见。
   - `JSContext`通常用于隔离不同部分的JavaScript代码，以确保它们不会相互干扰。例如，你可以在一个`JSContext`中执行一个脚本，然后在另一个`JSContext`中执行另一个脚本，它们之间不会相互影响。

总结来说，`JSRuntime`表示JavaScript的运行时环境，可以包含多个`JSContext`，而每个`JSContext`代表一个独立的JavaScript执行上下文。`JSRuntime`通常在应用程序级别创建和管理，而`JSContext`则用于在不同的上下文中执行JavaScript代码，以实现隔离和分离不同部分的代码逻辑。这种分层的结构有助于确保代码的隔离性和可维护性。



新建：

```
    rt = JS_NewRuntime();
    ctx = JS_NewContext(rt);
```

## JSShape

QuickJS中的`JSShape`是JavaScript对象的内部表示之一，

==用于跟踪对象的属性和属性的特征，==

这包括属性的名称、值、标志等。

`JSShape` 是 QuickJS 引擎用于实现对象属性存储和访问的关键数据结构之一。



具体来说，`JSShape` 存储了以下信息：

1. **属性列表**：包含对象的所有属性。这些属性通常是对象的成员变量，可以包括实例属性和原型属性。属性按名称排序，这有助于提高属性查找的效率。

2. **属性特征**：每个属性都有与之关联的特征，包括属性的标志（例如，是否可写、是否可枚举、是否可配置等）和属性的值。

`JSShape` 的存在使 QuickJS 引擎能够高效地执行属性查找和访问操作。这对于 JavaScript 对象的内部实现非常重要，因为它们可以包含大量属性，且访问属性是 JavaScript 中的常见操作。

需要注意的是，`JSShape` 是 QuickJS 引擎内部使用的数据结构，通常不会直接由 JavaScript 代码访问。开发者主要与 JavaScript 对象和属性交互，而引擎会负责管理底层的 `JSShape` 数据结构以支持这些操作。



## JSModuleDef

在 QuickJS 中，`JSModuleDef` 是一个数据结构，用于表示 JavaScript 模块（ES6 模块）的定义。

它包含了模块的各种属性和信息，

以便在 QuickJS 引擎中加载、解析和执行模块。

`JSModuleDef` 具有以下属性和功能：

1. **`name`（模块名称）**：表示模块的名称，通常对应于模块的文件路径或标识符。

2. **`func`（模块函数）**：一个指向模块执行函数的指针。模块执行函数是 JavaScript 模块的入口点，用于初始化模块的导出对象。

3. **`native_module`（原生模块标志）**：一个标志，指示模块是否为原生模块。原生模块通常是由 C/C++ 编写的模块，通过 QuickJS 的 C API 注册并加载。

4. **`import_list`（导入列表）**：一个列表，包含了模块导入的信息。这些信息通常包括导入的模块名称和导入的变量或名称空间。

5. **`export_list`（导出列表）**：一个列表，包含了模块导出的信息。这些信息指定了哪些变量或值将在模块外部可见。

6. **`import_meta`（导入元数据）**：一个指向包含有关模块导入的元数据的 `JSObject` 的指针。这可以包含有关模块的额外信息，如其来源等。

`JSModuleDef` 数据结构允许 QuickJS 引擎加载和执行模块，并管理模块之间的依赖关系。在应用程序或库中使用 QuickJS 时，你可以创建和注册自定义模块定义，以便在 JavaScript 代码中导入和使用它们。这对于将外部功能模块化并在 JavaScript 中使用非常有用。

通常，模块定义是通过 QuickJS 的 C API 创建并注册的，然后可以在 JavaScript 代码中通过 `import` 语句导入。这种模块系统的支持使 QuickJS 成为一个强大的嵌入式 JavaScript 引擎，可以与应用程序和库集成以支持模块化开发。

# 命令用法

直接运行：

```
./qjs examples/hello.js
```

编译为二进制运行：

```
./qjsc -o hello examples/hello.js
./hello
```

还有一个qjscalc命令，这个是简单的计算器命令。

# 标准库

标准库默认包含在命令行解释器中。它包含两个模块std和os以及一些全局对象。

## 全局对象

```
scriptArgs
print(...args)
console.log(...args)
```

## std

std模块为libc stdlib.h和stdio.h以及其他一些实用程序提供了包装程序。

```
exit(n)
evalScript(str, options=undefined)

loadScript(fn) 这个是直接执行了。
loadFile(fn) 这个是读取文件内容，返回字符串。

open(fn, flags, errObj=undefined)
popen(cmd, flags, errorObj=undefined)
fdopen(fd, flags, errorObj=undefined)
tmpfile(errorObj=unedefined)

puts(str)
printf(fmt, ...args)
sprintf(fmt, ...args)

in
out
err

SEEK_SET
SEEK_CUR
SEEK_END

Error 错误枚举。
strerror(errno)

gc()

getenv(name)
setenv(name, value)
unsetenv(name)
getenviron()

urlGet(url, options=undefined)

parseExtJSON(str)


FILE的prototype
close()
puts(str)
printf(fmt, ...args)
flush()
seek(offset, whence)
tell()
tello()
eof()
fileno()
error()
clearerr()
read(buffer, pos, len)
write(buffer, pos, len)
getline()
readAsString(max_size=undefined)
getByte()
putByte(c)

```

## os

The os module provides Operating System specific functions:

*•* low level file access

*•* signals

*•* timers

*•* asynchronous I/O

*•* workers (threads)

```
open(fn, flags, mode=0o666)
close(fd)
seek(fd, offset, whence)
read(fd, buffer, off, len)
write(fd, buffer, off, len)
isatty(fd)
ttyGetWinSize(fd)
ttySetRaw(fd)
remove(fn)
rename(oldname, newname)

```



# bignum

这个是quickjs的一个大的特色。

Bignum 扩展向 Javascript 语言添加了以下功能，

同时 100% 向后兼容：

运算符重载的调度逻辑灵感来自 https://github.com/tc39/proposal-operator-overloading/ 上的提案。

使用 IEEE 754 语义的以 2 为基数的任意大浮点数 (BigFloat)。
基于 https://github.com/littledan/proposal-bigdecimal 上的提案，以 10 为基数的任意大浮点数 (BigDecimal)。

数学模式：

默认可以使用任意大的整数和浮点数。

整数除法和幂可以重载，例如返回分数。模运算符 (%) 定义为欧几里得余数。
是幂运算符 (**) 的别名。

用作异或运算符。

除了数学模式依赖于 BigFloat 和运算符重载之外，这些扩展彼此独立。



参考资料

1、

https://bellard.org/quickjs/jsbignum.html

# qjsc

`qjsc` 是 QuickJS 提供的一个命令行工具，

==用于将 JavaScript 代码编译成 QuickJS 字节码，==

以便稍后执行。

它的基本用法如下：

```
qjsc [选项] [-o 输出文件] 输入文件
```

其中，`[选项]` 包括各种编译选项，`-o` 用于指定输出文件，而 `输入文件` 是要编译的 JavaScript 源文件。

以下是一些常见的 `qjsc` 选项和用法示例：

- `-o 输出文件`：指定输出文件的名称。
- `-c`：生成 C 代码，使你可以将 QuickJS 字节码嵌入到 C/C++ 应用程序中。
- `-M`：将多个 JavaScript 模块编译成一个字节码文件。
- `-m`：指定生成的字节码文件的模块名称。
- `-e`：指定要编译的 JavaScript 文件。
- `-t`：在生成的 C 代码中包括标准输入/输出处理。
- `-x`：生成源映射文件，用于调试。
- `-v`：增加编译的详细度，输出更多信息。

示例用法：

1. 编译单个 JavaScript 文件为 QuickJS 字节码文件：

   ```bash
   qjsc -o output.qjsc input.js
   ```

2. 生成 C 代码，以便将 QuickJS 字节码嵌入到 C/C++ 应用程序中：

   ```bash
   qjsc -o output.c -c input.js
   ```

3. 将多个 JavaScript 模块编译成一个字节码文件：

   ```bash
   qjsc -o output.qjsc -M -m main_module input.js
   ```

4. 生成源映射文件以进行调试：

   ```bash
   qjsc -o output.qjsc -x input.js
   ```

这些示例涵盖了一些常见的 `qjsc` 用法，但你可以根据你的项目需求使用其他选项。

`qjsc` 是 QuickJS 引擎的一个有用工具，允许你将 JavaScript 代码编译成字节码，以提高执行效率或在嵌入式系统中使用。

可以输出这些类型：

```
typedef enum {
    OUTPUT_C,
    OUTPUT_C_MAIN,
    OUTPUT_EXECUTABLE,
} OutputTypeEnum;

```

输出的名字：

```
    if (!out_filename) {
        if (output_type == OUTPUT_EXECUTABLE) {
            out_filename = "a.out";
        } else {
            out_filename = "out.c";
        }
    }
```

默认就是OUTPUT_EXECUTABLE。

# quickjs自定义一个C语言module

要在 QuickJS 中自定义一个 C 语言模块，你需要完成以下步骤：

1. **编写 C 代码**：首先，你需要编写包含模块功能的 C 代码。这可以是你的模块的实际实现，可以包括函数、变量和其他功能。例如，假设你要创建一个简单的模块，用于计算两个数字的和，你的 C 代码可能如下所示：

   ```c
   #include "quickjs.h"
   
   static JSValue my_add_func(JSContext *ctx, JSValueConst this_val, int argc, JSValueConst *argv) {
       if (argc != 2) {
           return JS_ThrowTypeError(ctx, "Two arguments are required");
       }
       int a, b;
       JS_ToInt32(ctx, &a, argv[0]);
       JS_ToInt32(ctx, &b, argv[1]);
       return JS_NewInt32(ctx, a + b);
   }
   
   static const JSCFunctionListEntry my_module_funcs[] = {
       JS_CFUNC_DEF("add", 2, my_add_func),
       JS_PROP_END
   };
   
   int js_init_module_my_module(JSContext *ctx, JSModuleDef *m) {
       JS_SetModuleExportList(ctx, m, my_module_funcs);
       return 0;
   }
   ```

   这个示例代码定义了一个名为 "my_module" 的模块，包含一个名为 "add" 的函数，用于将两个数字相加。在模块初始化函数 `js_init_module_my_module` 中，使用 `JS_SetModuleExportList` 来导出模块的函数。

2. **注册模块**：在 QuickJS 中注册你的模块，以便在 JavaScript 代码中导入和使用。你可以在 QuickJS 初始化时注册模块。示例如下：

   ```c
   JSModuleDef *m;
   JSContext *ctx;
   
   // 创建模块定义
   m = JS_NewCModule(ctx, "my_module", js_init_module_my_module);
   
   // 注册模块
   JS_AddModuleExportList(ctx, m);
   ```

   在上述示例中，首先使用 `JS_NewCModule` 创建一个模块定义，然后使用 `JS_AddModuleExportList` 注册模块，以便它在 JavaScript 代码中可用。

3. **使用 JavaScript 导入模块**：在你的 JavaScript 代码中，你可以使用 `import` 语句来导入你的自定义模块。例如：

   ```javascript
   import { add } from 'my_module';
   const result = add(5, 3);
   console.log(result); // 输出 8
   ```

这样，你的自定义 C 模块就可以在 QuickJS 中使用了。你可以根据你的需求扩展和自定义模块，以添加更多功能。当你的 C 模块在 QuickJS 中注册并导入后，你可以像使用任何其他 JavaScript 模块一样使用它。

## 官方的fib例子分析

examples\fib.c

## 模块的导入过程分析

```
js_module_loader
	js_module_loader_so
		dlsym(hd, "js_init_module");
			然后这个js_init_module在每个模块定义里有实现。
```

## 接口分析

可以看到接口非常简单清晰。

JS_NewCModule

## 参考资料

1、Writing native modules in C for QuickJS engine

https://calbertts.medium.com/writing-native-modules-in-c-for-quickjs-engine-49043587f2e2

# QuickJS中的atom设计

QuickJS源码中的atom（32位无符号整数）可以认为是字符串（覆盖的范围包括JS中的关键字、标识符、Symbol等）的别名。

其中最高位为1的atom代表的是整数，为0代表字符串，

所以atom可以表示的整数和字符串个数都是(2^31)-1个。

==引入atom的目的是为了减少内存使用（重复的字符串只存储一次）和提高字符串比较速度（在转换成atom之后，只需要比较两个atom的数值是否一致）。==

其中内置了大概200多个常驻的atom（包括关键字、JS中常见的标识符、JS中内置的Symbol），

在创建runtime的时候就被添加进去了，这些atom不会被清除。

之后在解析JS代码过程中添加的atom，会根据引用计数进行清除。



字符串转换为atom的步骤如下（如果是Symbol，转化为atom就比较简单，只需要往`atom_array`添加并使用其index作为Symbol的atom值即可，并不涉及到`atom_hash`的添加）：

1. 根据字符串的ascii码和atom类型，按照一定规则计算出一个hash值`hash_index`（32位无符号整数）
2. 获取`atom_array`空闲位置`free_atom_index`，然后将字符串的指针添加进去（`atom_array[free_atom_index]=s`。如果`atom_array`空间不足，则还会涉及到`atom_array`的扩充，以3/2的倍数扩充，注意扩充前后已经存储的atom对应的`atom_index`保持不变）
3. 将原来`atom_hash`的`hash_index`位置对应的`atom_index`存放到`s.hash_next`中，再将其修改为`free_atom_index`（这一步如果atom的个数大于`atom_hash`可以存放的数量的两倍，则将`atom_hash`扩充到原来的2倍容量）
4. 将第二步添加到`atom_array`中的位置（`atom_index`）作为该字符串的atom值，在后续的程序中使用



https://zhuanlan.zhihu.com/p/320599997

# 以quickjs分析setTimeout

只要搞明白这个问题，你就已经能自己实现 Event Loop 和 JS 运行时了。

我比较熟悉 QuickJS 引擎，写过两篇相关的教学文章，

下面复读下其中关于 setTimeout 的部分吧。



实际上由于一些历史原因[[1\]](#ref_1)，[ECMA-262](https://www.zhihu.com/search?q=ECMA-262&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540}) 规范里只定义了 Run to Completion 的部分，

并未包含任何对平台 API 的约定。

我们可以认为，狭义的 JS 引擎就是对这部分规范的实现。

==每次[解释执行](https://www.zhihu.com/search?q=解释执行&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540}) JS 脚本，==

==就相当于在 C 语言里调用一个名为 `JS_Eval` 然后同步完成的[函数](https://www.zhihu.com/search?q=函数&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})。==

而 setTimeout 需要的显然不只是单纯进行 `JS_Eval` 的能力，

**它的调用形式是反转过来的，要求在未来自动触发一次对 JS 函数的解释执行，亦即所谓的 callback（回调）**。

从 JS 运行时开发者的视角看来，

==只要走通了 setTimeout 这个最经典的回调例子，==

==就能够支撑起整个事件驱动应用的 Event Loop 架构了。==

因为 UI 应用中对按钮 onclick 等事件的支持，

其实也不外乎是在相应原生事件到来时，去执行相应的[回调函数](https://www.zhihu.com/search?q=回调函数&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})，

其原理是完全一致的。

==这方面 QuickJS 自带的 [libc](https://www.zhihu.com/search?q=libc&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540}) 运行时里有个非常简单优雅的实现案例，==

不妨直接看看 [Fabrice Bellard](https://www.zhihu.com/question/28388113) 大神代码的「实现机理」吧。

QuickJS 引擎编译时默认会内置 `std` 和 `os` 两个原生模块，能这样用 setTimeout 来支持异步：

```js
import { setTimeout } from "os";

setTimeout(() => { /* ... */ }, 0);
```



这个 `"os"` 模块就来自上面说的 libc 运行时，

==具体代码不属于引擎本体，==

==而是位于 `quickjs-libc.c` 文件里，==

也是通过标准化的 QuickJS API 挂载上去的原生模块。

这个原生的 setTimeout 函数是怎么实现的呢？

它的源码其实很少，像这样：

```c
static JSValue js_os_setTimeout(JSContext *ctx, JSValueConst this_val,
                                int argc, JSValueConst *argv)
{
    int64_t delay;
    JSValueConst func;
    JSOSTimer *th;
    JSValue obj;

    func = argv[0];
    if (!JS_IsFunction(ctx, func))
        return JS_ThrowTypeError(ctx, "not a function");
    if (JS_ToInt64(ctx, &delay, argv[1]))
        return JS_EXCEPTION;
    obj = JS_NewObjectClass(ctx, js_os_timer_class_id);
    if (JS_IsException(obj))
        return obj;
    th = js_mallocz(ctx, sizeof(*th));
    if (!th) {
        JS_FreeValue(ctx, obj);
        return JS_EXCEPTION;
    }
    th->has_object = TRUE;
    th->timeout = get_time_ms() + delay;
    th->func = JS_DupValue(ctx, func);
    list_add_tail(&th->link, &os_timers);
    JS_SetOpaque(obj, th);
    return obj;
}
```

可以看出，这个 setTimeout 的实现中，并没有任何[多线程](https://www.zhihu.com/search?q=多线程&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})或 poll 的操作，

只是把一个存储 timer 信息的结构体通过 `JS_SetOpaque` 的方式，

挂到了最后返回的 JS 对象上而已，

是个非常简单的同步操作。

因此，就和调用原生 fib 函数一样地，**在 eval 执行 JS 代码时，遇到 setTimeout 后也是同步地执行一点 C 代码后就立刻返回，没有什么特别之处**。



但为什么 setTimeout 能实现异步呢？

关键在于 eval 之后，我们就要启动 Event Loop 了。

熟悉 QuickJS 的朋友知道，QuickJS 支持直接把 JS 编译成[可执行文件](https://www.zhihu.com/search?q=可执行文件&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})，

这时候它会生成并编译一份标准的 C 代码，

在里面的 `main` 函数里调用 QuickJS 的 API 来启动 Event Loop。

我们可以通过 `qjs -c hello.js` 这行命令 dump 出相应的 C 文件，

直接看到启动 Event Loop 时的相关[逻辑](https://www.zhihu.com/search?q=逻辑&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})：

```
// ...
int main(int argc, char **argv)
{
  // ...
  // eval JS 字节码
  js_std_eval_binary(ctx, qjsc_hello, qjsc_hello_size, 0);
  // 启动 Event Loop
  js_std_loop(ctx);
  // ...
}
```

因此，eval 后的这个 `js_std_loop` 就是真正的 Event Loop，而它的源码则更是简单得像是[伪代码](https://www.zhihu.com/search?q=伪代码&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})一样：

```
/* main loop which calls the user JS callbacks */
void js_std_loop(JSContext *ctx)
{
    JSContext *ctx1;
    int err;

    for(;;) {
        /* execute the pending jobs */
        for(;;) {
            err = JS_ExecutePendingJob(JS_GetRuntime(ctx), &ctx1);
            if (err <= 0) {
                if (err < 0) {
                    js_std_dump_error(ctx1);
                }
                break;
            }
        }

        if (!os_poll_func || os_poll_func(ctx))
            break;
    }
}
```

这不就是在双重的死循环里先执行掉所有的 Job（也就是 Promise 带来的[微任务](https://www.zhihu.com/search?q=微任务&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})），

然后调 `os_poll_func` 吗？

可是，[for 循环](https://www.zhihu.com/search?q=for 循环&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})不会吃满 CPU 吗？

这是个[前端](https://www.zhihu.com/search?q=前端&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})同学们容易误解的地方：

**在原生开发中，进程里即便写着个死循环，也未必始终在前台运行，可以通过[系统调用](https://www.zhihu.com/search?q=系统调用&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})将自己挂起**。



例如，一个在死循环里通过 sleep 系统调用不停休眠一秒的进程，

就只会每秒被系统执行一个 tick，其它时间里都不占资源。

而这里的 `os_poll_func` 封装的，

就是原理类似的 poll 系统调用（准确地说，用的其实是 [select](https://link.zhihu.com/?target=https%3A//man7.org/linux/man-pages/man2/select.2.html)），

从而可以借助[操作系统](https://www.zhihu.com/search?q=操作系统&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})的能力，

使得只在【[定时器](https://www.zhihu.com/search?q=定时器&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})触发、[文件描述符](https://www.zhihu.com/search?q=文件描述符&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})读写】等事件发生时，

让进程回到前台执行一个 tick，把此时应该运行的 JS 回调跑一遍，而其余时间都在后台挂起。

在这条路上继续走下去，就能以经典的[异步非阻塞方式](https://www.zhihu.com/search?q=异步非阻塞方式&search_source=Entity&hybrid_search_source=Entity&hybrid_search_extra={"sourceType"%3A"answer"%2C"sourceId"%3A1927497540})来实现整个运行时了。



鉴于 `os_poll_func` 的代码较长，这里只概括下它与 timer 相关的工作：

- 如果上下文中存在 timer，将到期 timer 对应的回调都执行掉。
- 找到所有 timer 中最小的时延，用 select 系统调用将自己挂起这段时间。



这样，setTimeout 的「底层原理」就非常容易说清楚了：

**先在 eval 阶段简单设置一个 timer 结构，然后在 Event Loop 里用这个 timer 的参数去调用操作系统的 poll，从而在被唤醒的下一个 tick 里把到期 timer 对应的 JS 回调执行掉就行**。





参考资料

1、

https://www.zhihu.com/question/463446982/answer/1927497540

# 把quickjs改造为一个运行时

我们对事件循环有所了解，在 NodeJS 的情况下，异步 I/O 由 libuv 提供支持，但对于 QuickJS 来说并不相同。

**由于QuickJS是为了嵌入到其他系统中而创建的，试图最大限度地减少外部依赖，因此它使用了select系统调用。**

这种方法有几个重要的缺点，但我认为，其背后的目的是使其尽可能简单。

我不会深入研究 select/poll 的内部结构，相反，我将展示如何在考虑到这种异步模型的情况下开发 C 模块。



https://zhuanlan.zhihu.com/p/104333176

# quickjs剖析系列文章



https://www.zhihu.com/column/c_1337176691518140416

# quickjs的官方文档

## 生成

make build_doc，会生成html和pdf的文档。



QuickJS是一个小型的和可嵌入的Javascript引擎。

它支持ES2020规范1，包括模块、异步生成器、代理和BigInt。

它支持数学扩展，如大十进制浮数浮点数（大十进制数）、大二进制浮点数（BigFloat）和运算符重载。





# 使用了quickjs的项目

在github搜索包含了quickjs.c这个c文件的项目。

https://github.com/guillaumechereau/goxel

https://github.com/ekibun/flutter_qjs



https://github.com/phynos/qt-litesolar

https://github.com/ZhUyU1997/MEUI

frida的版本，自己更新了不少。

https://github.com/frida/quickjs



https://github.com/suchipi/quickjs

# txiki分析

## 作者的一些介绍

txiki.js 是一个小而强大的 JavaScript 运行时。

它建立在巨人的肩膀上：

它使用 QuickJS 作为 JavaScript 引擎，

libuv 作为平台层，

wasm3 作为 WebAssembly 引擎，

curl 作为 HTTP / WebSocket 客户端。



我早在 2019 年就开始从事 txiki.js 的工作，当时 QuickJS 刚刚发布。

我很快就迷上了，并想再次尝试构建一个小型 JavaScript 运行时。

再次？是的，早在 2016 年，我就尝试过同样的事情，但使用 Duktape 作为我的引擎，那就是 SkookumJS。

这次尝试并没有完全成功，主要是由于我的经验不足，以及我为自己设定的限制（请参阅公告帖子），所以我最终搁置了该项目。



我的主要收获：

如果运行时不与 Node 兼容，则它必须与浏览器兼容（API 方面）
依靠外部工具（如 Node）来准备核心 JS 包可以大大简化事情，因为您可以将代码转换为 JS 引擎支持的任何内容
对于 ES6 并承诺一个不包含事件循环概念的运行时似乎是遥不可及的
C 和 CMake 仍然是可靠的选择，我们可以包装任何东西！



txiki.js 诞生
可以公平地说，如果没有 QuickJS，txiki.js 就不会实现。它支持 ES2020、ES 模块，附带示例标准库，C API 非常易于使用，并且非常容易嵌入到其他项目中，只是几个 C 文件。它拥有一切。

所以我开始工作了。我选择 libuv 作为事件循环，并移植了 QuickJS 附带的小标准库。这让我确信自己走在正确的道路上。



这时deno已经出现在场景中。

它的一些主张听起来确实对我很有吸引力，

特别是它针对浏览器 API 并且没有任何要求，

只有 ESM 模块这一事实。 

Deno 背后的人肯定知道他们在做什么，这进一步巩固了一些我不确定的想法。



我一直在缓慢但坚定地开发 txiki.js。

一些重要的里程碑是集成 wasm3 以提供 WebAssembly 和 WASI 功能，以及用于 XHR / fetch 的curl。

它现在已经非常实用了，我意识到我忘了在这里发布它，所以我想是时候“宣布”它了。



几周前，FOSDEM 以虚拟方式举行。

这是我最喜欢的会议之一，

当论文征集开始时，我心想“让我们以此为契机，让 txiki.js 变得更好并告诉世界”。

值得庆幸的是，我的演讲提案被接受了，我谈到了我从 SkookumJS 到 txiki.js 的旅程。您可以在这里查看。



https://code.saghul.net/2022/02/introducing-txiki-js-a-tiny-javascript-runtime/

## 作者简介

https://code.saghul.net/about-me/

是一个西班牙程序员，主要在通信领域工作。



## 下载代码并运行

```
git clone --recursive https://github.com/saghul/txiki.js --shallow-submodules && cd txiki.js
```

直接make就行了。

执行repl：

```
./build/tjs
```

执行脚本：

```
./build/tjs run examples/hello_world.js
```

## 依赖的库

### wasm3

https://github.com/wasm3/wasm3

为什么使用“慢速解释器”而不是“快速 JIT”？

在许多情况下，速度并不是主要考虑的问题。

运行时可执行文件的大小、内存使用情况、启动延迟可以通过解释器方法得到改善。

可移植性和安全性更容易实现和维护。

此外，开发阻抗要低得多。

像 Wasm3 这样的简单库很容易编译并集成到现有项目中。 （Wasm3 只需几秒钟即可构建）。

最后，在某些平台（即 iOS 和 WebAssembly 本身）上，您无法在运行时生成可执行代码页，因此 JIT 不可用。

为什么要在嵌入式设备上运行 WASM？

Wasm3 最初是一个研究项目，并且在很多方面仍然如此。

在不同环境下评估发动机是研究的一部分。

鉴于我们有 Lua、JS、Python、Lisp...在 MCU 上运行，WebAssembly 实际上是一个有前途的替代方案。

它提供工具链解耦以及完全沙盒化、定义明确、可预测的环境。

在实际用例中，我们可以列出边缘计算、脚本、插件系统、运行物联网规则、智能合约等。



## 启动参数

https://zhuanlan.zhihu.com/p/343562220

## 代码分析

这个是主要的结构体。

```
struct TJSRuntime {
    TJSRunOptions options;
    JSRuntime *rt;
    JSContext *ctx;
    uv_loop_t loop;
    struct {
        uv_check_t check;
        uv_idle_t idle;
        uv_prepare_t prepare;
    } jobs;
    uv_async_t stop;
    bool is_worker;
    struct {
        CURLM *curlm_h;
        uv_timer_t timer;
    } curl_ctx;
    struct {
        IM3Environment env;
    } wasm_ctx;
    struct {
        JSValue date_ctor;
        JSValue u8array_ctor;
    } builtins;
};
```

以TJS开头。

最重要的一点，搞清楚，uv怎么替换默认的loop的。

默认的std和os不注册，自己注册一些东西就可以替换了。



## src\vm.c

这个是主要的运行函数。

才400行。不多。

```
TJS_NewRuntime
```

```
    tjs__bootstrap_core(qrt->ctx, bootstrap_ns);

    CHECK_EQ(tjs__eval_bytecode(qrt->ctx, tjs__polyfills, tjs__polyfills_size), 0);
    CHECK_EQ(tjs__eval_bytecode(qrt->ctx, tjs__core, tjs__core_size), 0);
```

`tjs__bootstrap_core`内容：

```c
static void tjs__bootstrap_core(JSContext *ctx, JSValue ns) {
    tjs__mod_dns_init(ctx, ns);
    tjs__mod_error_init(ctx, ns);
    tjs__mod_ffi_init(ctx, ns);
    tjs__mod_fs_init(ctx, ns);
    tjs__mod_fswatch_init(ctx, ns);
    tjs__mod_os_init(ctx, ns);
    tjs__mod_process_init(ctx, ns);
    tjs__mod_signals_init(ctx, ns);
    tjs__mod_sqlite3_init(ctx, ns);
    tjs__mod_streams_init(ctx, ns);
    tjs__mod_sys_init(ctx, ns);
    tjs__mod_timers_init(ctx, ns);
    tjs__mod_udp_init(ctx, ns);
    tjs__mod_wasm_init(ctx, ns);
    tjs__mod_worker_init(ctx, ns);
    tjs__mod_ws_init(ctx, ns);
    tjs__mod_xhr_init(ctx, ns);
#ifndef _WIN32
    tjs__mod_posix_socket_init(ctx, ns);
#endif
}
```

各个模块内部，看起来就像lua注册模块类似。

tjs_module_loader，自定义了module_loader函数。

```
    JS_SetModuleLoaderFunc(qrt->rt, tjs_module_normalizer, tjs_module_loader, qrt);

```



## src\cli.c

这个是入口。

main函数就调用了4个函数：

```
TJS_SetupArgs
TJS_NewRuntime
TJS_Run
TJS_FreeRuntime
```

## repl测试

```
teddy@teddy-pc:~/work/txiki.js$ ./build/tjs
Welcome to txiki.js — The tiny JavaScript runtime
Type "\h" for help
> tjs.args
[ "./build/tjs" ]
> t
tjs             toLocaleString  toString        
> tjs.version
"23.1.0"
> 
```

支持tab补全。怎么做到的？



## 写代码测试

在example/test1.js里写入下面的内容：

```
console.log('11');
var res = await tjs.confirm('hello');
console.log('aa');
console.log(res);
```

运行：

```
./build/tjs run ./example/test1.js
```

tjs是一个全局对象。

有哪些常用的属性？

## d.ts分析

txikijs

```
namespace tjs {
	Reader
	Writer
	alert
	confirm
	prompt
	args
	Signal
	SignalHandler
	signal
	kill
	gc
	version 字符串
	versions 一个dict，包括qjs、tjs、uv、curl的版本。
	exepath
	environ
	gethostname
	getenv
	putenv
	unsetenv
	platform
	exit
	chdir
	cwd
	一些inet的红对应SOCKET_STREAM这些。
	Hints
	AddrInfo
	IErrors
	Error
	errors
	realpath
	unlink
	rename
	mkdtemp
	mkstemp
	FileHandle
	StatResult
	mkdir等等
	
}
```



# qjs-ffi

https://github.com/ratboy666/qjs-ffi

可以写出比较复杂的代码。

https://github.com/ratboy666/qjs-ffi/blob/master/examples/telnet.js

# awtk-quickjs

https://github.com/zlgopen/awtk-quickjs

原理：

https://github.com/zlgopen/awtk-binding/blob/master/docs/binding_js.md

# 运行时

https://github.com/doodlewind/minimal-js-runtime



# Reflect

这个是ES6里引入进来的概念。

但是我之前一直没有注意过。

现在看手动抄写quickjs的test_builtin.js时，发现有这个东西。

看看具体是怎么回事。

```text
反射机制指的是程序在运行时能够获取自身的信息
```

```text
Reflect是一个内建的对象，用来提供方法去拦截JavaScript的操作。Reflect不是一个函数对象，所以它是不可构造的，也就是说它不是一个构造器，你不能通过`new`操作符去新建或者将其作为一个函数去调用Reflect对象。Reflect的所有属性和方法都是静态的。
```

因为我们刚才说过了，利用JS的for..in可以实现，还有比如`Array.isArray`/`Object.getOwnPropertyDescriptor`，或者甚至`Object.keys`都是可以归类到反射这一类中。

那么ECMA为什么还要这个呢？

当然是为了让JS更加强大了，

**相当于说提供Reflect对象将这些能够实现反射机制的方法都归结于一个地方并且做了简化，**

保持JS的简单。

于是我们再也不需要调用`Object`对象，然后写上很多的代码。

比如：

```js
var myObject = Object.create(null) // 此时myObject并没有继承Object这个原型的任何方法,因此有：

myObject.hasOwnProperty === undefined // 此时myObject是没有hasOwnProperty这个方法，那么我们要如何使用呢？如下：

Object.prototype.hasOwnProperty.call(myObject, 'foo') // 是不是很恐怖，写这么一大串的代码！！！！
```

而如果使用Reflect对象呢？

```text
var myObject = Object.create(null)
Reflect.ownKeys(myObject)
```

再比如当你对象里有Symbol的时候，如何遍历对象的keys？

```js
var s = Symbol('foo');
var k = 'bar';
var o = { [s]: 1, [k]: 1 };
// getOwnPropertyNames获取到String类型的key，getOwnPropertySymbols获取到Symbol类型的key
var keys = Object.getOwnPropertyNames(o).concat(Object.getOwnPropertySymbols(o));
```

而使用Reflect的话：

```js
var s = Symbol('foo');
var k = 'bar';
var o = { [s]: 1, [k]: 1 };
Reflect.ownKeys(o)
```

相比较之下，Reflect对象的作用凸显出来了吧？

另外Reflect还提供了一些Object对象没有的方法，比如`Reflect.apply`。



参考资料

1、

https://zhuanlan.zhihu.com/p/92700557

# Worker



# 参考资料

1、

https://blog.csdn.net/Innost/article/details/98491709

2、

https://blog.csdn.net/wsyzxxn9/article/details/114116614

3、

https://blog.csdn.net/HaaSTech/article/details/120948020