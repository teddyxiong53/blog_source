---
title: libcurl（3）源代码分析
date: 2018-10-17 20:06:51
tags:
	- 网络
---



我暂时之关注头文件提供的接口。

```
curl.h  curlver.h  easy.h  mprintf.h  multi.h  stdcheaders.h  system.h  typecheck-gcc.h
```

# easy.h

简单操作四步走：

curl_easy_init

curl_easy_setopt

curl_easy_perform

curl_easy_cleanup

发送接收：

curl_easy_send

curl_easy_recv

涉及结构体：

##CURL

在curl.h里。这个可以理解为void 类型就好了。不过一般是一个指针，相当于void * 。

```
typedef struct Curl_easy CURL;
/* just to please curl_base64.h we create a fake struct */
struct Curl_easy {
  int fake;
};
```

## CURLoption

```
  CINIT(TLS13_CIPHERS, STRINGPOINT, 276),
  CINIT(PROXY_TLS13_CIPHERS, STRINGPOINT, 277),

  /* Disallow specifying username/login in URL. */
  CINIT(DISALLOW_USERNAME_IN_URL, LONG, 278),

  CURLOPT_LASTENTRY /* the last unused */
} CURLoption;
```

接近300个选项。



# curl.h

这里定义了很多的回调类型。



# multi.h

这个头文件也值得研究。







# 参考资料

1、Python 的PyCurl模块使用

https://www.cnblogs.com/i-it/p/4181243.html