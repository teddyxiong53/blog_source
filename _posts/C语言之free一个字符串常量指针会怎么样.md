---
title: C语言之free一个字符串常量指针会怎么样
date: 2022-12-06 11:26:19
tags:
	- C语言

---

--

最近在用cjson写一些代码，关于cJSON_Delete释放的时候，如果碰到了字符串常量会怎样？

所以需要看看free一个字符串常量指针会有什么后果。

测试代码如下：

```
int main(int argc, char const *argv[])
{
    const char *s  = "abc";
    free(s);
    // printf("s after free:%s", s);
    return 0;
}
```

运行会crash掉。提示是invalid pointer。



参考资料

1、

