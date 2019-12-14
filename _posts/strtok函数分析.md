---
title: strtok函数分析
date: 2019-12-13 11:08:37
tags:
	- C库

---

1

之前没有怎么用过strtok这个函数，现在用了一下，出现了段错误。

分析一下原因。

```
int main()
{
    char str[80] = "This is - www.runoob.com - website";
    const char s[2] = "-";
    char *token;

    /* 获取第一个子字符串 */
    token = strtok(str, s);

    /* 继续获取其他的子字符串 */
    while (token != NULL)
    {
        printf("%s\n", token);
		//首次调用时，s指向要分解的字符串，之后再次调用要把s设成NULL。
        token = strtok(NULL, s);
    }

    return (0);
}
```

测试代码是这样。

运行会段错误。

strtok的函数原型是这样：

```
char *strtok(char *s, char *delim);
```

算法思路是：

把delim对应的字符，替换成'\0'。

上面的代码会出错，是因为栈上的数组，被优化成了静态的常量指针。

而strtok会对s的内容进行修改，常量修改当然会出错。

把str放到全局变量就正常了。

或者你先定义数组，然后用strcpy的方式把内容拷贝过去也行。

反正是要绕过编译器的这种默认的优化。

**首次调用时，s指向要分解的字符串，之后再次调用要把s设成NULL。**

这个函数的实现还有点麻烦。

参考资料

1、strtok段错误

http://blog.chinaunix.net/uid-30086959-id-5211786.html

