---
title: java之泛型
date: 2017-12-27 11:24:20
tags:
	- java

---



# 1. 为什么需要泛型

我们先看一个简单的例子。

```
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Test {

	public static void main(String[] args) {
		List list = new ArrayList();
		list.add("abc");
		list.add(100);
		for(int i=0; i<list.size(); i++) {
			String str = (String)list.get(i);
			System.out.println(str);
		}
	}
}
```

这个编译阶段正常，但是运行会报错。因为会试图把一个Integer转成一个String。

从上面的代码中，主要的问题是：

把一个对象放到集合中后，集合不会记住对象的类型，当我们从集合中再次取出对象时，对象的编译类型变成了Object类型。但是运行时类型仍然为本来的类型。

那么如何解决这个问题呢？java给出的解决方案就是泛型。

```
List<String> list = new ArrayList();
		list.add("abc");
		list.add(100);
```

这样，在编译时，这个代码就报错了。便于我们提早发现问题。



# 2. 泛型的定义

泛型，就是参数化类型。

说到参数，我们最熟悉的就是函数的参数。



#3. 泛型的分类

E：Element。在集合中使用。因为集合中存放的是元素。

T：Type。Java类。

K：Key。键。

V：Value。

N：Number。

?：表示不确定的java类型。List和List<?>是等价的。

S、U、V：第二、第三、第四种类型。（什么意思？）

用了泛型后，就不用强制转换了。类型转换效率比较低。

还可以这样组合使用：

```
Collection<? extends E>
```



