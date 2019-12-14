---
title:算法之基本C库函数实现
date: 2019-12-13 13:12:37
tags:
	- 算法

---

1

```c
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <unistd.h>
#if 1
void *mymemcpy(void *dest, void *src, size_t n)
{
    unsigned char *d = (unsigned char *)dest;
    unsigned char *s = (unsigned char *)src;
    while (n > 0)
    {
        *d++ = *s++;
        n--;
    }
    return dest;
}

void *mymemset(void *dest, int c, size_t n)
{
    unsigned char *d = (unsigned char *)dest;
    while (n > 0)
    {
        n--;
        *d = c;
        d++;
    }
}

void *mymemmove(void *dest, void *src, size_t n)
{
    char *d = dest;
    char *s = src;
    if (d == s)
    {
        return d;
    }
    if (s + n <= d || d + n <= s)
    {
        return mymemcpy(d, s, n);
    }
    if (d < s)
    {
        while (n > 0)
        {
            *d++ = *s++;
            n--;
        }
    }
    else
    {
        while (n > 0)
        {
            n--;
            d[n] = s[n];
        }
    }
    return dest;
}

int mymemcmp(void *vl, void *vr, size_t n)
{
    unsigned char *l = vl;
    unsigned char *r = vr;
    int flag = 0;
    while (n > 0)
    {
        if (*l < *r)
        {
            return -1;
        }
        else if (*l > *r)
        {
            return 1;
        }
        l++;
        r++;
        n--;
    }
    return 0;
}
void *mymemchr(void *src, int c, size_t n)
{
    unsigned char *s = src;
    c = (unsigned char)c;

    while (s && (n > 0) && *s != c)
    {
        s++;
        n--;
    }
    if (n)
    {
        return (void *)s;
    }
    else
    {
        return NULL;
    }
}

char *mystrcpy(char *d, char *s)
{
    while (s && *s)
    {
        *d = *s;
        d++;
        s++;
    }
    return d;
}
char *mystrncpy(char *d, char *s, size_t n)
{
    while (n && (s) && (*s))
    {
        *d = *s;
        s++;
        d++;
        n--;
    }
    memset(d, 0, n);
    return d;
}
char *mystrcat(char *d, char *s)
{
    mystrcpy(d + strlen(d), s);
}

char *mystrstr(char *s1, char *s2)
{
    int i;
    int n1 = strlen(s1);
    int n2 = strlen(s2);
    if (n2 == 0)
    {
        return s1;
    }
    if (n1 == 0 || n1 < n2)
    {
        return NULL;
    }
    char *tmp;
    char s2_head = s2[0];
    int j = 0;
    for (i = 0; i <= n1 - n2; i++)
    {
        if (s2_head != s1[i])
        {
            continue;
        }

        //执行到这里，说明在s1里找到了s2_head
        for (j = 1; j < n2; j++)
        {
            if (s1[i + j] != s2[j])
            {
                break;
            }
        }
        //
        if (j < n2)
        {
            //说明后面有不相同的。
            return NULL;
        }
        else
        {
            return &s1[i];
        }
    }
    return NULL;
}
#endif

void test_mystrstr()
{
    char *s1 = "abcd";
    char *s2 = "";
    char *p = mystrstr(s1, s2);
    printf("result:%p, s1:%p, s2:%p(%s)\n", p, s1, s2, s2);
    s2 = "abcde";
    p = mystrstr(s1, s2);
    printf("result:%p, s1:%p, s2:%p(%s)\n", p, s1, s2, s2);
    s2 = "abcd";
    p = mystrstr(s1, s2);
    printf("result:%p, s1:%p, s2:%p(%s)\n", p, s1, s2, s2);
    s2 = "cd";
    p = mystrstr(s1, s2);
    printf("result:%p, s1:%p, s2:%p(%s)\n", p, s1, s2, s2);
    s2 = "cde";
    p = mystrstr(s1, s2);
    printf("result:%p, s1:%p, s2:%p(%s)\n", p, s1, s2, s2);
    s2 = "efghi";
    p = mystrstr(s1, s2);
    printf("result:%p, s1:%p, s2:%p(%s)\n", p, s1, s2, s2);
}

int myatoi(char *s)
{
    char c;
    int result = 0;
    while(s && *s) {
        c = *s;
        s++;
        if(c >= '0' && c <= '9') {
            result *= 10;
            result += c-'0';
        } else {
            break;
        }
    }
    return result;
}

float myatof(char *s)
{
    char c;
    float result = 0.0;
    int got_dot = 0;
    float after_dot_part = 0.0;
    int dot_bits = 0;
    while(s && *s) {
        c = *s;
        s++;
        if(got_dot && (c>='9' || c<='0')) {
            //已经有一个小数点，且当前字符不合法。
            break;
        }
        if(c == '.') {
            got_dot = 1;
            continue;
        }
        if(got_dot) {
            //当前已经有小数点了。
            if(c >= '0' && c <= '9') {
                after_dot_part *= 10;
                after_dot_part += c-'0';
                dot_bits += 1;
            }
        } else {
            if(c >= '0' && c <= '9') {
                result *= 10;
                result += c-'0';
            }
        }

    }
    while(dot_bits > 0) {
        after_dot_part /= 10;
        dot_bits --;
    }
    return result + after_dot_part;
}
void test_atoi()
{
    printf("%d\n", atoi("123"));
    printf("%d\n", atoi("abc"));
    printf("%d\n", atoi("123a"));
    printf("%d\n", atoi("a123"));
}
void test_myatoi()
{
    printf("%d\n", myatoi("123"));
    printf("%d\n", myatoi("abc"));
    printf("%d\n", myatoi("123a"));
    printf("%d\n", myatoi("a123"));
}
void test_atof()
{
    printf("%f\n", atof(".123"));
    printf("%f\n", atof("0.1a"));
    printf("%f\n", atof("0.123"));
    printf("%f\n", atof("a.1"));
    printf("%f\n", atof("1"));
    printf("%f\n", atof("1.1.1"));
    printf("%f\n", atof("12.3"));
}

void test_myatof()
{
    printf("%f\n", myatof(".123"));
    printf("%f\n", myatof("0.1a"));
    printf("%f\n", myatof("0.123"));
    printf("%f\n", myatof("a.1"));
    printf("%f\n", myatof("1"));
    printf("%f\n", myatof("1.1.1"));
    printf("%f\n", myatof("12.3"));
}
int main()
{
    //test_atoi();
    // test_myatoi();
    // test_atof();
    test_myatof();
}
```



参考资料

1、

