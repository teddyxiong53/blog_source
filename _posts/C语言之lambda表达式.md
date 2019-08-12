---
title: C语言之lambda表达式
date: 2019-08-09 17:41:19
tags:
	- C语言

---

1

最近在琢磨C语言实现简单异步操作的方法。

就想到了C语言能否实现lambda表达式。

我们能够做这些的基础，是gcc对C语言标准进行的扩展。

我们编译运行下面的代码，如果输出结果为1，则说明你的编译器支持实现lambda功能。

```
#include <stdio.h>

int main(){

	int a = ({1;});

	printf("%d\n",a);

	return 0;
}
```

下面开始一步步深入。

我们把代码改成下面的样子。

```
int main(){
	int a = ({
    char *s = "hello";
    printf("%s\n",s);
    1;
  });
  printf("%d\n", a);
	return 0;
}
```

```
({
//这个包含的，是一个块级作用域。
//而且还可以返回一个值。
})
```

既然可以返回一个值，那么我们返回一个函数呢？也是可以的。

下面这个就是一个匿名函数。

```
int main(){
	({
    void hello() {
      printf("hello\n");
    }
    hello;
  })();

	return 0;
}
```

然后我们用宏来改写这个匿名函数。

```
#define $(rt, fb) ({ \
  rt this fb; \
  this; \
})
int main(){
	$(void,() {
    printf("hello\n");
  })();

	return 0;
}
```

用宏改写过，是不是看起来有点眼熟了呢？

但是当前还美中不足，虽然函数可以自执行，但是还不能保存到一个变量里。

看了一下，觉得并不实用。先暂停。



参考资料

1、c语言奇淫技巧之lambda表达式

http://blog.aoshiguchen.com/#yDeDW9

2、C 语言也有 lambda 表达式吗？

https://www.zhihu.com/question/275877582