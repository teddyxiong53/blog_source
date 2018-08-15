---
title: php之heredoc
date: 2018-08-15 21:28:32
tags:
	- php

---



php里的heredoc是用来引用字符串的一种方式。



语法是：

1、使用操作符`<<<`。

2、操作符后面紧跟标识符，之后重新起一行，输入要引用的字符串，可以包含变量。

3、新的一行，顶格写结束符。用分号结束。



举例：

```
<?php
$str = <<<ET
heredoc test

ET;
echo $str
?>
```

效果是输出：`heredoc test`这一行字符串。

ET是一个标签的名字。

这个是一般的命名。你可以改成其他的任意字符串。



# 参考资料

1、PHP heredoc 用法

https://www.cnblogs.com/igoogleyou/p/heredoc.html