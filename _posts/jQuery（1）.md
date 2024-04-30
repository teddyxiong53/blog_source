---
title: jQuery（一）
date: 2018-05-24 22:27:05
tags:
	- js

---



工作中涉及到一点jQuery，所以现在学习一下。

jQuery是一个js库。用来简化js编程的。

jQuery很容易学习的。



jQuery可以做什么？

1、html元素选取和操作。

2、css操作。

3、html事件函数。

4、js特效和动画。

5、html dom遍历和修改。

6、ajax。

7、utilities。



jQuery的意义是什么？为什么需要jQuery？

现在又为什么不再需要了？



jQuery的设计宗旨是：用更少的代码做更多的事情。

jQuery封装了常用的功能代码，优化了html文档参照，事件处理，动画设计和ajax交互。



jQuery的核心特性可以总结为：

1、具有独特的链式语法。

2、短小清晰的多功能接口。

3、具有高效的css选择器。

4、拥有便捷的插件机制和丰富的插件。

5、兼容主流浏览器。



jQuery的具体作用：

1、取得页面里的元素。不用js库，自己写代码遍历dom，需要写很多行的代码。

2、修改界面的外观。浏览器支持的css标准不同的时候，写css代码就很烦人。jQuery帮我们解决了这种问题。

3、改变页面的内容。

4、响应用户的界面操作。

5、为页面添加动态效果。

6、ajax。



jQuery的发展历史：

1、2005年8月，John Resig提议改进Prototype里的Behavior库。于是他在博客上发表了自己的想法，并用3个简单的例子做了流程说明。

（Prototype这个库，已经退出历史舞台了。被jQuery完全取代了。）

这篇博客在业内引起了广泛关注。

2、2006年1月14日，John以jQuery发布了自己的程序库。

3、8月份，jQuery有了第一个稳定版本。已经开始支持css选择符、事件处理和ajax提交。

4、微软、诺基亚等大公司也参与了进来。



工作原理

jQuery的模块分为3部分：

1、入口模块。

2、底层支持模块。

3、功能模块。

# 简介

jQuery 是一个快速、简洁的 JavaScript 库，专注于简化 HTML 文档的遍历、事件处理、动画和 Ajax 操作。它提供了易于使用的 API，使得在 web 开发中操作 DOM 和处理事件变得更加便捷和高效。

jQuery 的主要特点包括：

1. **简化DOM操作**：通过 jQuery，您可以轻松地选取、操作、创建和删除 HTML 元素，而不需要繁琐的 DOM 操作。

2. **事件处理**：jQuery 提供了简单而强大的事件处理功能，使得对于用户交互的响应变得更加简单和直观。

3. **动画效果**：jQuery 提供了丰富的动画效果，使得在网页中添加动态效果变得更加容易。

4. **Ajax支持**：通过 jQuery，您可以轻松地执行 Ajax 请求，与服务器进行数据交换，实现页面的局部更新。

5. **跨浏览器兼容性**：jQuery 在不同浏览器中表现一致，并且解决了很多浏览器兼容性的问题，使得开发者不需要为不同浏览器写不同的代码。

总的来说，jQuery 的出现极大地简化了前端开发的工作，使得开发者能够更加专注于实现功能而不是解决浏览器兼容性和复杂的 DOM 操作。

# 现在浏览器标准逐渐规范，所以不需要jquery了吗？

尽管现代浏览器的标准逐渐规范，并且原生 JavaScript API 的功能也在不断增强，但是 jQuery 仍然有其存在的价值和优势。以下是一些关于是否需要 jQuery 的考虑因素：

1. **项目需求**：如果您的项目需要兼容旧版浏览器或者需要大量的 DOM 操作、事件处理和动画效果，那么使用 jQuery 仍然是一个不错的选择。jQuery 简化了这些操作，使得开发更加高效。

2. **开发速度**：使用 jQuery 可以加速开发速度，因为它提供了简洁的 API 和丰富的功能，可以让开发者更快地实现想要的效果。

3. **团队技能**：如果您的团队成员熟悉 jQuery，并且项目中已经使用了大量的 jQuery 代码，那么继续使用 jQuery 可能会更加合适，因为他们已经对其熟悉并且能够快速地开发和维护代码。

4. **性能考虑**：==原生 JavaScript 的性能通常比 jQuery 更好，因为 jQuery 本身需要一定的初始化和运行开销。在对性能有严格要求的项目中，可能会选择避免使用 jQuery。==

5. **学习成本**：现代前端开发者通常会学习原生 JavaScript API，因为它们是标准的一部分，并且在很多情况下已经足够满足需求。对于一些新手开发者来说，学习 jQuery 可能会增加额外的学习成本。

综上所述，尽管原生 JavaScript 的功能越来越强大，但 jQuery 仍然是一个有价值的工具，特别是在需要快速开发和兼容性考虑的情况下。选择是否使用 jQuery 取决于项目的具体需求、团队技能和性能考虑。

# jquery发展历史

jQuery 的发展历史可以追溯到2006年，当时由约翰·雷西格（John Resig）创建并首次发布。以下是 jQuery 的主要发展里程碑：

1. **2006年：诞生**：jQuery 由约翰·雷西格创建，并在2006年8月首次发布。最初的版本是 jQuery 1.0。

2. **版本更新**：随着时间的推移，jQuery 不断更新和改进，添加了新的功能、修复了 bug，并且逐渐成为最受欢迎的 JavaScript 库之一。

3. **2009年：发布jQuery 1.3**：jQuery 1.3 发布，引入了新的选择器引擎 Sizzle，并且带来了性能改进和新的 API。

4. **2010年：发布jQuery 1.4**：jQuery 1.4 发布，引入了链式操作的改进、事件模型的重构以及性能优化。

5. **2013年：发布jQuery 2.0**：jQuery 2.0 主要针对现代浏览器进行了优化，放弃了对 IE6/7/8 的支持，从而减小了文件大小，并提升了性能。

6. **2013年：发布jQuery 2.1和1.11**：jQuery 2.1 和 1.11 发布，主要是对 1.x 分支的维护版本，修复了一些 bug，并提供了更好的兼容性。

7. **2015年：发布jQuery 3.0**：jQuery 3.0 发布，带来了一些重大的改进，包括对 IE6/7/8 的彻底放弃支持、对 ES6 的部分支持以及更多的性能优化。

8. **版本迭代**：自发布以来，jQuery 持续进行版本迭代，不断更新以适应现代 web 开发的需求，并且保持对老版本的兼容性。

9. **社区支持**：jQuery 拥有一个庞大的社区，提供了大量的插件、扩展和教程，使得开发者能够更加便捷地使用和扩展 jQuery。

尽管现在有更多选择，而且原生 JavaScript 的功能也在不断增强，但 jQuery 仍然是许多开发者和项目的首选，特别是在需要兼容旧版浏览器、快速开发以及简化 DOM 操作的情况下。

# jquery原理

jQuery 的原理主要是基于对原生 JavaScript API 的封装和扩展，以及对跨浏览器兼容性的处理。以下是 jQuery 的一些主要原理：

1. **封装DOM操作**：jQuery 封装了常见的 DOM 操作，例如选取元素、修改元素属性和样式、插入和删除元素等，使得这些操作更加简单和便捷。例如，使用 jQuery，可以通过 `$(selector)` 来选取元素，然后通过链式操作调用各种方法进行操作。

2. **事件处理**：jQuery 封装了事件处理机制，使得添加、移除和触发事件更加简单。它提供了一系列事件方法，例如 `click()`、`hover()`、`on()` 等，可以方便地绑定和处理事件。

3. **动画效果**：jQuery 提供了丰富的动画效果，例如淡入淡出、滑动、缩放等，这些效果通过修改元素的 CSS 属性来实现，并且封装了复杂的动画过渡和回调函数，使得添加动画效果变得更加容易。

4. **Ajax操作**：jQuery 封装了原生 JavaScript 的 Ajax 功能，使得与服务器进行数据交换更加简单。通过 `$.ajax()` 方法或者简化的 `$.get()`、`$.post()` 方法，可以方便地发送 Ajax 请求，并且处理返回的数据。

5. **链式操作**：jQuery 支持链式操作，允许在同一个选择器或对象上连续调用多个方法。这种设计使得代码更加简洁和易读，同时减少了对 DOM 的多次遍历，提升了性能。

6. **跨浏览器兼容性**：jQuery 处理了不同浏览器之间的兼容性问题，使得开发者不需要为不同的浏览器编写不同的代码。jQuery 封装了对浏览器特性和bug的检测和处理，从而保证了在各种浏览器下的一致性和稳定性。

综上所述，jQuery 的原理主要是通过封装和扩展原生 JavaScript API，提供了一套简洁而强大的操作 DOM、处理事件、实现动画效果和执行 Ajax 请求的工具集，同时处理了跨浏览器兼容性问题，使得前端开发变得更加高效和便捷。

# 自己实现一个最小的jquery

要实现一个最小的 jQuery，您可以创建一个简单的 JavaScript 函数，该函数接受一个选择器作为参数，并返回匹配该选择器的元素列表。然后，您可以添加一些方法来操作这些元素，例如修改它们的样式、绑定事件等。以下是一个示例：

```javascript
// 最小的 jQuery 实现
function $(selector) {
    // 选取匹配选择器的元素
    var elements = document.querySelectorAll(selector);

    // 返回一个对象，包含了一些操作方法
    var obj = {
        // 添加一个方法用于修改元素的样式
        css: function(property, value) {
            for (var i = 0; i < elements.length; i++) {
                elements[i].style[property] = value;
            }
            return this; // 支持链式操作
        },

        // 添加一个方法用于绑定事件
        on: function(eventType, handler) {
            for (var i = 0; i < elements.length; i++) {
                elements[i].addEventListener(eventType, handler);
            }
            return this; // 支持链式操作
        }
    };

    return obj;
}
```

使用这个最小的 jQuery 实现，您可以按照以下方式操作元素：

```javascript
// 选取所有的 <button> 元素，并将它们的背景色设置为红色
$("button").css("background-color", "red");

// 给所有的 <a> 元素绑定点击事件
$("a").on("click", function() {
    alert("Clicked!");
});
```

请注意，这只是一个非常简单的 jQuery 实现，仅支持选取元素、修改样式和绑定事件等基本功能。实际上，jQuery 还有很多其他功能和方法，例如动画效果、Ajax 请求等，这些功能可以通过在这个最小实现的基础上进行扩展来实现。

# 怎样安装

要在你的网页里加入jQuery，有两种方式：

1、在你的网站里放一份jQuery代码。

2、引用公共网址上的jQuery。

jQuery分为两种版本：

1、生产环境版本。被压缩过，体积小。不适合阅读。

2、测试环境版本。格式比较好，方便阅读和调试。



下载网站在这里。

https://code.jquery.com/jquery-3.3.1.js

我们把这个文件保存到本地就好了。

代码有1万行。



# 基本测试代码

下面的测试都在这个基础上改。

```
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>test</title>
    <script src="./jquery-3.3.1.js">

    </script>
    <script>
        $(document).ready(function() {
            //add your code here
            alert("hello jquery")
        })
    </script>

</head>
<body>

</body>
</html>
```

目录结构：

```
D:\work\test\jquery
λ  tree
.
├── jquery-3.3.1.js
└── test.html
```



# jQuery语法

本来$美元符在js语法里是没有特别意义的。

但是jQuery大量使用了，而且赋予了特别含义。

$代表了jQuery。



# jQuery选择器

所有的选择器都以美元符开头。

分为两种：

1、元素选择器。

2、`#id`选择器。

3、`.class`选择器。

元素选择器的。

```
$("p")
```

这个表示选取所有的`<p>`元素。

下面这段代码表示，点击按钮后，所有的`<p>`元素都被隐藏。

```
$(document).ready(function(){
  $("button).click(function() {
    $("p").hide();
  });
});
```

`#id`选择器的。

```
$("#test")
```

`.class`选择器。

```
$(".test")
```



# jQuery事件

jQuery的设计主要就是为了做事件处理的。

什么叫事件？

页面对不同访问者的响应就叫事件。

例如：

在元素上移动鼠标。

选取单选按钮。

点击元素。

常见的事件有：

1、鼠标事件。

```
click
dblclick
mouseenter
mouseleave
```

2、键盘事件。

```
keypress
keydown
keyup
```

3、表单事件。

```
submit
change
focus
blur 失去焦点的时候。
```

4、文档和窗口事件

```
load
resize
scroll
unload
```

## 常见的jQuery事件方法

1、`$(document).ready()`

这个是表示文档加载完成后执行的函数。

2、click。



# 和普通js代码对比

jQuery能做的。普通js代码也可以做到。只是麻烦一点。

怎么个麻烦法呢？

我们看看对比。

加载dom

```
//普通js
function my_onload() {
	console.log("xx");
}
window.onload = my_onload;
```

```
//jquery
$(document).ready() {
    
}
```

获取id

```
//普通js
document.getElementByID("xx");
```

```
//jquery
$("#xx")
```

获取class

```
//普通js
无法获取
```

```
//jQuery
$(".xx")
```

取得tagName

```
//普通js
document.getElementByTagName("xx");
//jquery
$("xx")
```

创建对象并加入到文档里。

```
//普通js
var para = document.createElement("p");
document.body.appendElement(para);
```

```
//jquery
$("p").append('<p>xxx</>');
```



# 常用方法

## 事件方法

### bind

格式：

```
$(sel).bind(event[, data], function[,map])
```

举例

```
$('p').bind('click', {x:1}, function(e) {
	alert('click now:' + e.data.x)
})
```



拿到input的值。

```
$('input').css('background-color', 'green')
            .change(function() {
                alert('改变了，改变后：' + $(this).val())
            })
```

## 效果方法

```
toggle：在show和hidden之间切换。
```

## html和css方法

这部分比较重要。

```
addClass
	这个是给元素添加一个css的class。
after
	在选中元素的后面插入内容。
append
	也是在后面插入，但是不会换行。会紧跟着前面的元素。
appendTo
	这个跟append的区别是，插入的必须的html标签内容。
attr
	set或者get选中元素的属性值。
before
	在前面插入内容。
css
	set或者get css样式。
	$('p').css('color', 'red')
empty
	清空选中元素。
hasClass
	判断选中元素是否有某个css class
height
	得到元素的高度。
html
	获取元素的html内容。
insertAfter
insertBefore
prop
	跟attr类似。但是不同。
remove
removeAttr
removeClass
removeProp
text
toggleClass

```

## 遍历方法

```
add	
	这个是相当于把多个元素都进行选中。
	$('h1').add('p').add('span').css('color', 'green')
	这个就相当于把h1和p和span，都进行颜色设置。
children
	返回选中元素的所有子元素。
each
	为每次选中的元素执行函数。
	
```

## ajax方法

## 杂项方法



# 参考资料

1、菜鸟教程

https://www.runoob.com/jquery/jquery-selectors.html

2、jQuery UI。

http://www.runoob.com/jqueryui/api-easings.html

3、jQuery的具体作用

https://blog.csdn.net/qq_15016387/article/details/82378054

4、Prototype这个JS库的现状如何？

https://www.zhihu.com/question/21165560

5、jquery和javascript的区别(常用方法比较)

https://blog.csdn.net/yyy183833/article/details/52413357