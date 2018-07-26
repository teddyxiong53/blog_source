---
title: Linux之编码
date: 2018-07-25 14:10:28
tags:
	- Linux

---



我重点关注的是嵌入式Linux里的编码问题。



切入点是中文的ssid名字。

在Linux上用wpa_cli scan得到的名字是这样的。

```
c8:3a:35:4a:5e:30	2437	-28	[WPA-PSK-CCMP][WPA2-PSK-CCMP][ESS]	\xe7\x86\x8a\xe6\xb1\x89\xe8\x89\xaf-55
```

原文是：熊汉良-55 

这个是因为用了url编码导致的。

用这个在线工具可以进行测试。

http://tool.oschina.net/encode?type=4



最好是可以通过Linux命令行工具来实现编码和解码。



这一条编码是正常的。

```
echo '手机' |tr -d '\n' |od -An -tx1|tr ' ' %
```



算了，还是改成用C语言来实现的。

一个汉字的utf-8编码是3个字节的长度。



```
#include <stdlib.h>  
#include <string.h>  
#include <ctype.h>  
#include <sys/types.h>  
  

static unsigned char hexchars[] = "0123456789ABCDEF";  
  
static int url_htoi(char *s)  
{  
    int value;  
    int c;  
  
    c = ((unsigned char *)s)[0];  
    if (isupper(c))  
        c = tolower(c);  
    value = (c >= '0' && c <= '9' ? c - '0' : c - 'a' + 10) * 16;  
  
    c = ((unsigned char *)s)[1];  
    if (isupper(c))  
        c = tolower(c);  
    value += c >= '0' && c <= '9' ? c - '0' : c - 'a' + 10;  
  
    return (value);  
}  
  
  
char *url_encode(char const *s, int len, int *new_length)  
{  
    register unsigned char c;  
    unsigned char *to, *start;  
    unsigned char const *from, *end;  
      
    from = (unsigned char *)s;  
    end  = (unsigned char *)s + len;  
    start = to = (unsigned char *) calloc(1, 3*len+1);  
  
    while (from < end)   
    {  
        c = *from++;  
  
        if (c == ' ')   
        {  
            *to++ = '+';  
        }   
        else if ((c < '0' && c != '-' && c != '.') ||  
                 (c < 'A' && c > '9') ||  
                 (c > 'Z' && c < 'a' && c != '_') ||  
                 (c > 'z'))   
        {  
            to[0] = '%';  
            to[1] = hexchars[c >> 4];  
            to[2] = hexchars[c & 15];  
            to += 3;  
        }  
        else   
        {  
            *to++ = c;  
        }  
    }  
    *to = 0;  
    if (new_length)   
    {  
        *new_length = to - start;  
    }  
    return (char *) start;  
}  
  
  
int url_decode(char *buf, char *str, int len)  
{  
    char *dest = buf;  
    char *data = str;  
  
    while (len--)   
    {  
        if (*data == '+')   
        {  
            *dest = ' ';  
        }  
        else if (*data == '%' && len >= 2 && isxdigit((int) *(data + 1)) && isxdigit((int) *(data + 2)))   
        {  
            *dest = (char) url_htoi(data + 1);  
            data += 2;  
            len -= 2;  
        }   
        else   
        {  
            *dest = *data;  
        }  
        data++;  
        dest++;  
    }  
    *dest = '\0';  
    return 0;  
}  

int main()
{
	int encode_len = 0;
	char *str = "熊汉良";
	char *encode_str = url_encode(str, strlen(str), &encode_len);
	printf("%s \n", encode_str);
	printf("encode_len:%d \n", encode_len);
	char buf[100] = {0};
	int ret = url_decode(buf, encode_str, encode_len);
	printf("decode str: %s \n", buf);

}
```



但是这个是不能解决我的问题。



在使用utf-8编码的系统上。

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ echo "一" |grep "一"
一
```

命令行上一切正常。

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ locale
LANG=zh_CN.UTF-8
LANGUAGE=zh_CN:zh
LC_CTYPE="zh_CN.UTF-8"
LC_NUMERIC="zh_CN.UTF-8"
LC_TIME="zh_CN.UTF-8"
LC_COLLATE="zh_CN.UTF-8"
LC_MONETARY="zh_CN.UTF-8"
LC_MESSAGES="zh_CN.UTF-8"
LC_PAPER="zh_CN.UTF-8"
LC_NAME="zh_CN.UTF-8"
LC_ADDRESS="zh_CN.UTF-8"
LC_TELEPHONE="zh_CN.UTF-8"
LC_MEASUREMENT="zh_CN.UTF-8"
LC_IDENTIFICATION="zh_CN.UTF-8"
LC_ALL=
```

我把wpa_cli scan_result输出到文件里。在pc上打开文件。

```
c8:3a:35:4a:5e:30	2472	-20	[WPA-PSK-CCMP][WPA2-PSK-CCMP][ESS]	\xe7\x86\x8a\xe6\xb1\x89\xe8\x89\xaf-55
```



由上可知扫描结果中的中文并不是GBK编码，而是16进制的字符串 
这时我们就需要对结果进行转换了，命令很简单：echo -e



我觉得根本解决问题的办法，就是把系统的默认编码改成utf-8的。

这个改动涉及面比较广。

还是专注解决当前问题。



# 参考资料

https://blog.csdn.net/B_H_L/article/details/17956037



编码问题：unicode与utf-8，wchar_t与char

https://blog.csdn.net/freestyle4568world/article/details/49591739



linux busybox中文显示修改说明

https://blog.csdn.net/hclydao/article/details/79277582

在UTF-8中，一个汉字为什么需要三个字节？

https://blog.csdn.net/crslee/article/details/52041016

Unicode 是不是只有两个字节，为什么能表示超过 65536 个字符？

wpa_cli中文问题处理

https://blog.csdn.net/yizhan2012/article/details/76777390

C++实现中英文与UNICODE十六进制字符串互转

https://blog.csdn.net/brantyou/article/details/7306029



在Linux C编程中使用Unicode和UTF-8

http://docs.linuxtone.org/ebooks/C&CPP/c/apas03.html

添加字体与字符集locale支持（基于busybox文件系统）

https://www.cnblogs.com/cute/p/4961280.html

在C++11中，如何将一种编码的string转换为另一种编码的string？

https://www.zhihu.com/question/39186934