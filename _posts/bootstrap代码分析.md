---
title: bootstrap代码分析
date: 2021-01-28 09:19:11
tags:
	- bootstrap

---

--

https://github.com/twbs/bootstrap/tree/v3.4.1

我就看3.4.1版本的。

先看看怎么编译。

下面有一个package.json，那么就可以用npm来做。

```
"release": "grunt prep-release && npm run sri && npm run release-zip",
```

编译得到release包，是上面的命令。

grunt是什么？是一个前端的编译工具。依赖一个Gruntfile.js。类似make和Makefile。这个单独用一篇文章来描述。

这个版本的css是用less写的。

gulp的子任务有：

```
clean
jslint
jscs
concat
uglify
less
postcss
stylelint
cssmin
copy
connect
jekyll
pug
htmllint
watch
exec
```

目录主要关注js和less这2个目录。

我先看js的。

我关注的是tab的切换。data-toggle='tab' 这个具体是怎样实现tab切换的效果的。

用上面这个场景作为切入点。

对应的是js/tab.js。

这个相当于构造函数。参数是一个dom元素。转成jquery对象。保存起来。

```
var Tab = function (element) {
    this.element = $(element)
  }
```

这个是tab切换的时间。

```
Tab.TRANSITION_DURATION = 150
```

Tab.prototype.show

```javascript
var hideEvent = $.Event('hide.bs.tab', {
    relatedTarget: $this[0]
})
var showEvent = $.Event('show.bs.tab', {
    relatedTarget: $previous[0]
})
$previous.trigger(hideEvent)
$this.trigger(showEvent)

```

Tab.prototype.activate

```

```



通过结合一下data属性，你可以轻松创建一个tab界面。

通过这个插件，你可以把内容放在tab页，或者pill页，甚至dropdown页里。

你可以通过下面两种方式来使用tab

1、通过data属性。

```
给外层的ul添加nav和nav-tab这2个css类。
给<a>标签添加data-toggle="tab"或"pill"属性。
```

例子

```
<ul class="nav nav-tab" id="myTab">
	<li><a href="#home" data-toggle="tab">home</a></li>
</ul>
```

2、通过js代码。

```
$('#myTab a').click(function(e) {
	e.preventDefault()
	$(this).tab('show')
})
```

tab页，需要用一个div括起来。div的css类是tab-content。

里面的对应不同的tab页面的，css类是tab-pane。

添加淡入淡出效果。这个是给每个tab-pane添加fade这css类。



# less文件

看一下less文件。

bootstrap.less这个是总的文件，把其他的文件都import进来的。

就按照这个文件里import的顺序看。

## 核心变量和mixins

### variables.less

```
定义了颜色
字体
iconfont
padding
table
btn
form
dropdown
zindex
screen
grid系统
container
navbar
navbar-inverse
navbar-link
navbar-tabs
pagination
pager
jumbotron
state
tooltip
popover
label
modal
alert
progress bar
list-group
panel
thumbnail
well
badge
breadcrumb
carousel
close
code

```

### mixins.less

```
这个是有一个mixins目录。下面有十几个文件。
```

## reset和依赖

有3个文件。

normalize、print、glyphicons。

### normalize

```
这个是清除默认的样式。
设置基本的样式。
```

### print

```
这个是设置@media print的。我不管。
```

### glyphicons

```
这个就是设置iconfont的。
```

## 核心css

### scaffolding

```
这个单词的意思是脚手架。
内容不多。
就是设置基本元素的margin、padding这些。border。
```

### type

定义h1、address、ul等有语义的标签的

### code

code、kbd、pre等几个代码相关的标签。

### grid

定义了container、row、

### tables

## 组件

组件包括：

dropdown、button-groups、input-group、

navs、navbar、等等。

## 其他



参考资料

1、Bootstrap 标签页（Tab）插件

https://www.runoob.com/bootstrap/bootstrap-tab-plugin.html