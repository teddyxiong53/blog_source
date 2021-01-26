---
title: html之input标签
date: 2019-01-22 11:05:55
tags:
	- html

---



```
type
	button
	checkbox
	file
	hidden
	image
	password
	radio
	reset
	submit
	text
```

# input是否必须放在form里

不是必须的，单独使用没必要写在form标签内，

但是假如你需要利用input标签收集用户信息并发送给后端，建议是写在form标签内

没有放在form中或**没有name属性**，那么form提交的时候会**忽略这个元素。**



input标签外是否添加form标签需要按情形区分：

应用场景的区别：

1.所有向后台提交数据（包括原生和ajax提交）的input都建议用form包裹，

2.如果**只是用来做前台交互效果则不推荐使用form包裹**。

但提交数据时，其实也可以不用form包裹input标签：

1.如果有form标签，在点击提交铵钮时，**浏览器自动收集参数，并打包一个http请求到服务器**，完成表单提交。

在这一过程中，浏览器会根据method的不同，将参数编码后，放在urI中(get)，或者放在请求的data中(post)。然后发送到服务器。



2.如果没有form，post方式的提交要使用ajax手工完成。get方式的提交需要自己拼接url。



参考资料

1、

http://www.w3school.com.cn/tags/tag_input.asp

2、

https://www.imooc.com/qadetail/300404?t=477023

3、input标签之外是否一定添加form标签

https://www.cnblogs.com/jokes/p/9884958.html