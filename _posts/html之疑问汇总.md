---
title: html之疑问汇总
date: 2018-08-22 22:43:37
tags:
	- html

---

## div和span关系

div是块级元素。

span是内联元素。可以做文本的容器。



div的常见用途是文档布局。



## ie版本判断

```
<!--[if lt IE 9]>
  <script src="//cdnjs.cloudflare.com/ajax/libs/html5shiv/r29/html5.min.js">
  </script>
<![endif]-->
```

这些写法为什么可以被识别？

因为`<!--[if lt IE 9]>`这个对应IE来说，是叫做条件注释。ie会进行分析的。



https://stackoverflow.com/questions/41430406/what-is-the-meaning-of-lt-in-if-lt-ie-9