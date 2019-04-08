---
title: java之Retention元注解
date: 2019-04-08 14:00:30
tags:
	- java

---



```
Retention
	这个是说明注解保留的位置
	@Retention(RetentionPolicy.SOURCE) 
	有3个地方：SOURCE、CLASS、RUNTIME。
	默认是CLASS。
Target
	说明注解作用的目标。
	@Target(ElementType.TYPE)  
Document
	说明这个注解将被包含在javadoc里。
Inherited
	说明子类可以继承父类的注解。
```



参考资料

1、java注解(四种元注解：@Retention @Target @Document @Inherited)

https://wisfly.iteye.com/blog/2289443