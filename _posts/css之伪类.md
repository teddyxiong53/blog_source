---
title: css之伪类
date: 2019-03-04 11:14:03
tags:
	- css
---



1

什么是伪类？

```
伪类就是一个：
1、以冒号为前缀。
2、被添加到一个选择器末尾的关键字。
```

所有的伪类有：

```
:active
:any
:checked
:default
:dir()
:disabled
:empty
:enabled
:first
:first-child
:first-of-type
:fullscreen
:focus
:hover
:indeterminate
:in-range
:invalid
:lang()
:last-child
:last-of-type
:left
:link
:not()
:nth-child()
:nth-last-child()
:nth-last-of-type()
:nth-of-type()
:only-child
:only-of-type
:optional
:out-of-range
:read-only
:read-write
:required
:right
:root
:scope
:target
:valid
:visited
```



伪类的语法：

```
a: link {
    color: red;
}
```

`:link`这个就是一个伪类。

伪类名称对大小写不敏感。



看一个实际一点的例子。

```
a {
    color: blue;
    font-weight: bold;
}
a:visited {
    color: blue;
}
a:hover,
a:active,
a:focus {
    color: darked;
    text-decoration: none;
}
```



伪元素

什么是伪元素？

```
伪元素的前缀是2个冒号。
```

伪元素有这些：

```
::after
::before
::first-letter
::first-line
::selection
::backdrop
```

例子：

```
[href^=http]::after {
    content: '==';
}
```

这个是在http开头的超链接的后面加2个等号。



参考资料

1、css伪类

http://www.w3school.com.cn/css/css_pseudo_classes.asp

2、伪类和伪元素

https://developer.mozilla.org/zh-CN/docs/Learn/CSS/Introduction_to_CSS/Pseudo-classes_and_pseudo-elements