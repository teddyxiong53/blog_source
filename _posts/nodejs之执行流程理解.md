---
title: nodejs之执行流程理解
date: 2020-12-28 09:13:30
tags:
- nodejs
---

1

下面只是我自己的理解，为了方便自己进行思考。

因为我是做C语言编程的。

对于select等io多路复用机制用得比较多。所以就从这个角度来看。

我们写在app.js里的代码，相当于这样的：

```
void init() {
	//app.js里的代码，相当于放在这里的。
}
void main()
{
	init();
	while(1) {
		select()
		if(没有回调需要处理了) {
			break;
		}
	}
}
```



参考资料

1、

