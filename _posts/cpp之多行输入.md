---
title: cpp之多行输入
date: 2019-12-14 10:32:25
tags:
	- cpp

---

1

因为比较少用命令行采集用户输入的方式。但是做算法题，有些是需要进行输入的。所以把这一块梳理一下。

# C语言里的方式

先从C语言的看起。C语言能用的，在c++里也能用。

函数有这些：

```
gets
	这个是最基本的。
	gets是有缓冲区的。按下回车键后，就代表输入结束了。
	gets从缓冲区里读取内容。
	函数原型：
	char *gets(char *s);
	参数：s是一个buffer。
	返回值：跟s是一样的。但是我测试不一样。
	用法：
	char str[100];
    gets(str);
    printf("str:%s, len:%d\n", str, strlen(str));
    如果直接给一个回车，那么strlen是0 。
    因为换行符会被丢弃，并在最后加上一个\0 。
    代码里的实现是这样：
    			if ((*p++ = c) == '\n') break;
                }
                if (s) *p = 0;
    测试情况：
    char str[100];
    char *result = gets(str);
    printf("str:%p, result:%p\n", str, result);
    str:0x7fff199f5290, result:0x199f5290
    把str定义为static的正常了。总之栈上的不行。
    gets是不安全的。
    因为可以任意任意长度，导致破坏栈。
    所以有了安全版本的gets_s。
gets_s
	用法跟gets一样。只是不会溢出。
fgets
	gets的内部，就是调用了fgets
	fgets(s, INT_MAX, stdin);//是这样实现gets的。
scanf
	这个是输入数字。
	scanf也可以输入字符串。跟gets的区别是：scanf是以空格作为结束检测的。
	所以scanf不能输入含有空格的字符串。
getchar
	输入单个字符。
	内部实现是调用return fgetc(stdin);
	最容易理解的字符输入函数是 getchar()，它就是scanf("%c", c)的替代品
```

C语言的持续输入是这样：

```
int main()
{
    static char str[100] = {0};
    while(strlen(gets(str))) {
        printf("str:%s\n", str);
    }
    printf("end\n");
}
```

上面说的都是标准C库的函数。

gcc扩展了一个getline函数。

```
getline
	
```

# C++ 的输入方式 

## 最简单的方式，一次输入多个int

```
int main() {
	int a,b;
    cin >> a >> b;
    cout <<a + b <<endl;
}
```

## 连续输入

```
int main()
{
    int a,b;
    while(cin >> a >> b) {
        cout <<a + b <<endl;
    }
}
```

要结束，你是需要给stdin造一个EOF，我看网上很多都是说用ctrl+z。但是Linux下，这个是把程序给stop了。而不是结束stdin。查了一下，Linux，是用ctrl+d。

## 一次运行，需要输入多组数据，组数由第一个输入的数据决定

这个是很常用的要求。

这样来实现：

```
int main()
{
    int a,b;
    int n;
    cin >> n;
    for(int i=0; i<n; i++) {
        cin >> a >> b;
        cout <<a + b <<endl;
    }
}
```

## 不说明有多少组数据，但是用特殊的内容表示结束

例如，以-1、0表示结束这样。

下面是以2个0表示结束的例子。

```
int main()
{
    int a,b;
    while(cin >> a >> b && (a||b)) {
        cout << a+b << endl;
    }
}
```



参考资料

1、C++输入多行数据

https://www.cnblogs.com/jingshikongming/p/9921646.html

2、gets函数

https://baike.baidu.com/item/gets/787649?fr=aladdin

3、C语言输入字符和字符串（所有函数大汇总）

http://c.biancheng.net/view/1796.html

4、ACM题目中输入数据的处理（C++版）

这篇文章特别好。作者在CSDN，排名12 。

https://blog.csdn.net/sxhelijian/article/details/8978850

5、while(cin>>str)无法结束的问题（原） 

http://dsdm.bokee.com/6149239.html