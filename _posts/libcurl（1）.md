---
title: libcurl（1）
date: 2018-05-09 23:30:27
tags:
	- libcurl

---



安装：

```
sudo apt-get install libcurl4-openssl-dev
```

简单的例子。

```

#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <sys/types.h>
#include <pthread.h>
#include "curl/curl.h"

#include "curl/easy.h"


size_t WriteData(const char *ptr, size_t size, size_t nmemb, FILE *stream)
{
    if (!ptr || !stream) {
        return 0;
    }


    return fwrite(ptr, size, nmemb, stream);
}

int main()
{
    CURL *pHandler = curl_easy_init();
    FILE *pFile = fopen("./xx", "wb+");
    curl_easy_setopt(pHandler, CURLOPT_WRITEFUNCTION, WriteData);
    curl_easy_setopt(pHandler , CURLOPT_WRITEDATA, pFile);
    curl_easy_setopt(pHandler , CURLOPT_URL, "http://192.168.0.105/xx");
    curl_easy_setopt(pHandler , CURLOPT_FAILONERROR, 1);
    curl_easy_setopt(pHandler , CURLOPT_TIMEOUT, 60);
    curl_easy_setopt(pHandler , CURLOPT_NOSIGNAL, 1);

    CURLcode codeRet = curl_easy_perform(pHandler);
    long retcode = 0;

    curl_easy_getinfo(pHandler, CURLINFO_RESPONSE_CODE , &retcode);
    curl_easy_cleanup(pHandler);
    if (codeRet == CURLE_OK && (retcode == 200 || retcode == 304 || retcode == 204)) {
        //下载成功
        printf("download ok\n");
    } else{
        //下载失败
        printf("download fail\n");
    }
    fclose(pFile);
}
```



在基于libcurl的程序里，主要采用回调的方式来工作。

用户在启动传输之前，设置好各种参数和回调函数。

在满足调节时，自动调用回调函数来完成任务。

curl_global_init是一定要调用的。

curl_easy_init和curl_easy_cleanup是分配和释放内存的。

curl_easy_setopt和curl_easy_perform是主要的工作函数。

curl_easy_getinfo用来获取返回值。



# 参考资料

1、使用libcurl下载文件小例

https://www.cnblogs.com/rainbow70626/p/7618378.html

2、libcurl下载文件

https://www.cnblogs.com/meteoric_cry/p/3681546.html

3、官网示例合集

https://curl.haxx.se/libcurl/c/example.html

4、Curl使用（一）

https://blog.csdn.net/yujunan/article/details/8713176