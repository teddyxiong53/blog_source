---
title: cpp之getline
date: 2020-10-17 16:14:30
tags:
	- cpp
---

1

在标准C库里，是没有getline这个函数的。

gcc扩展了标准C库，加入了getline这个函数，原型是这样：

```
ssize_t getline(char **lineptr, size_t *n, FILE* stream);
```

标准C库里有一个类似的函数，fgets。

fgets的缺点是：读取的时候，会把换行符也读取进来，使用不方便。

stdin的EOF是ctrl+D。

所以建议使用getline函数。

fgetc的用法：

```
int main()
{
    int ch;
    while ((ch = fgetc(stdin)) != EOF) {
        printf("%c\n", ch);
    }

    return 0;
}
```

fgets用法：

```
int main(int argc, char const *argv[])
{
    char buffer[10];
    int size = 10;
    while(fgets(buffer, size, stdin) != NULL) {
        printf("%s\n", buffer);
    }
    return 0;
}
```

C库的getline，返回-1表示读取完了。

c++的std::getline，返回false，表示读取完了。

C语言版本。

```
int main(int argc, char const *argv[])
{
    ssize_t read;
    char *buffer;
    size_t size = 0;
    while((read = getline(&buffer, &size, stdin)) != -1) {
        printf("%s", buffer);
    }
    return 0;
}
```

c++版本

```
#include <cstdio>

int main(int argc, char const *argv[])
{
    std::string buffer;
    while(std::getline(std::cin, buffer)) {
        printf("%s\n", buffer.c_str());
    }
    return 0;
}
```



参考资料

1、fgetc,fgets,getline用法

https://blog.csdn.net/teffi/article/details/53582166

2、C++中std::getline()函数的用法

https://blog.csdn.net/lzuacm/article/details/52691450