---
title: C库函数自己简单实现
date: 2018-03-09 14:26:22
tags:
	- C语言

---



面试中总是碰到一些要求实现库函数的题目。现在就自己理一遍。

# 字符串相关



## atoi

这个是实现，我的直观想法是，从最低位开始处理。是这样。

```
#include <string.h>

int myatoi(char *s)
{
    int len = strlen(s);
    int i=len-1;
    int j=0;
    int sum=0;
    int cur = 0;//当前处理位
    while(i>=0) {
        int d = s[i] - '0';
        j = cur;
        while(j>0) {
            d = d*10;
            j--;
        }
        sum += d;
        i --;
        cur++;
    }
    return sum;
}

void main() {
    int a = myatoi("123");
    printf("a:%d \n", a);
}
```

这个当然是有很多多余的东西。还有些情况没有处理的。

第一个问题是，循环变量太多了。而且有2个循环。

先缩减循环。能不能改成一个。

内部循环用来算出当前位的权重。又不能用pow这个幂函数。

musl里只有一个循环，是从最高位开始处理的。

## itoa

是atoi的逆函数。

```
char *myitoa(char *p, int n)
{
    char buf[100] = {0};
    int d = 0;
    int i=0;
    while(n > 0) {
        buf[i] = n%10 + '0';
        i++;
        n=n/10;
    }
    int j=0;
    for(j=0; i>0; j++) {
        p[j] = buf[i-1];
        i--;
    }
    return p;
}
```

也写得很不好。



