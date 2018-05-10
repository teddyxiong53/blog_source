---
title: c语言之整型提升
date: 2018-05-10 20:50:07
tags:
	- C语言

---



整型提升是C语言里的一项规定。

在进行表达式计算的时候，各种整型首先要提升为int类型。

如果int类型不足以表示，就提升为unsigned int类型。

然后再进行运算。

看一个例子。

```
int main(int argc, char const *argv[])
{
	unsigned char a = 200;
	unsigned char b = 100;
	unsigned char c = 0;
	c = a+b;
	printf("a+b:%d\n", a+b);
	printf("c:%d \n", c);
	return 0;
}
```

结果：

```
teddy@teddy-ubuntu:~/work/test/c-test$ ./a.out 
a+b:300
c:44 
```



# 参考资料

1、整型提升

https://baike.baidu.com/item/整型提升/16697764?fr=aladdin