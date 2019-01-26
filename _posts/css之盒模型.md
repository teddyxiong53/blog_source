---
title: css之盒模型
date: 2018-12-24 10:38:27
tags:
	- css
---



从外到内：

margin、border、padding。

记忆方法：mbp。MacBook Pro的缩写。



margin后面完整的是跟4个参数：

```
body {
  margin: 1px 1px 1px 1px;
}
```

表示从上、右、下、左这种顺时针方向的值。简略写法是写2个。

```
body {
  margin: auto;/*表示4个方向都是自动*/
  margin: 0 auto;/*等价于0 auto 0 auto，上下为0，左右为auto。*/
}
```



参考资料

1、

http://www.ituring.com.cn/book/tupubarticle/3782

2、CSS中：margin:auto与margin: 0 auto;有什么区别 

https://zhidao.baidu.com/question/197906506.html