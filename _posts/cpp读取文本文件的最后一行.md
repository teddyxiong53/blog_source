---
title: cpp读取文本文件的最后一行
date: 2020-05-26 16:08:08
tags:
	- cpp

---



```
#include <fcntl.h>
#include <stdio.h>

int main(int argc, char **argv)
{
    FILE *fp;
    char sline[1024];
    size_t rd;
    int i;

    char *file = argv[1];
    fp = fopen(file, "r");
    if (fp == NULL)
    {
        //printf("%d,[%s]\n", errno, strerror(errno));
        return 0;
    }

    fseek(fp, 0, SEEK_END);
    if (ftell(fp) > 1023)
        fseek(fp, -1023, SEEK_CUR);
    else
        fseek(fp, -ftell(fp), SEEK_CUR);

    memset(sline, 0, sizeof(sline));
    rd = fread(sline, 1, 1023, fp);
    if (sline[rd - 1] == '\n')
        sline[rd - 1] = 0;

    for (i = (1023 > rd ? rd : 1023); i >= 0; i--)
    {
        if (sline[i] == '\n')
        {
            break;
        }
    }
    if (i < 0)
    {
        printf("this line is too long....\n");
        return 0;
    }
    printf("last line is:\n%s\n", sline + i + 1);

    return 0;
}

```



参考资料

1、c++读取文件最后一行

https://blog.csdn.net/bestzone/article/details/96892002

