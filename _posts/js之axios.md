---
title: js之axios
date: 2019-01-27 15:07:28
tags:
	- js

---



看vue的官网教程时，看到提到了axios这个异步库。

了解一下。

可以支持在html头部包含的方式，也可以用nodejs模块的方式。

也就是说，可以用在前端，也可以用在后端。



axios是一个基于promise的http库。

特性：

1、拦截Request和response。

2、转换Request数据和response数据。

3、取消请求。

4、自动转换json数据。



get请求

```
axios.get('https://httpbin.org/get',{
	//参数2是配置选项
	a:1,
	b:2
})
.then(function(res) {
	console.log(res.data)
})
.catch(function(err) {
	console.log(err)
})
```





# 参考资料

1、中文说明

https://www.kancloud.cn/yunye/axios/234845

2、中文文档

http://axios-js.com/zh-cn/docs/index.html