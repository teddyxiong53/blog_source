---
title: emlog（2）代码分析
date: 2018-08-27 22:22:53
tags:
	- php

---



在coment.php里。

```
<script>
$(document).ready(function(){
```

这个`$(document)`是什么？

是jQuery语法。

这个代码段表示在文档加载完成后，激活函数。

----------



`javascript:void(0) 含义`

表示啥也不干。



--------



```
setTimeout(hideActived,2600);
```

setTimeout函数是html DOC的函数。

相当于启动一个定时器，在指定ms后，执行对应的函数。

只执行一次。如果要多次执行。需要调用setInterval函数。或者在超时函数里再调用定时。

-------

```
function getChecked(node) {
	var re = false;
	$('input.'+node).each(function(i){
		if (this.checked) {
			re = true;
		}
	});
	return re;
}
```

each方法是jQuery的方法。



# 参考资料

1、jQuery 事件 - ready() 方法

http://www.w3school.com.cn/jquery/event_ready.asp

2、javascript:void(0) 含义

https://www.runoob.com/js/js-void.html

3、HTML DOM setTimeout() 方法

http://www.w3school.com.cn/jsref/met_win_settimeout.asp

