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



multi接口是对easy接口的封装，可以实现同时并发访问多个url。



# 源码编译

直接configure之后make就好了。

example在docs目录下，进去make就好了。

把所有例子按照顺序看一遍。

10-at-a-time

这个是同时下载多个文件。测试multi接口的。

chkspeed

这个是用下载的方式进行测速的。

# post方式

看看post方式跟httpbin.org交互的情况。

post json的方式需要设置这个才行。

```
curl_slist *plist = curl_slist_append(NULL,   "Content-Type:application/json;charset=UTF-8");  
	curl_easy_setopt(curl, CURLOPT_HTTPHEADER, plist);  
```



我对内存泄露是比较担心的，所以我不想频繁分配然后再销毁。

所以我要创建一个handle长时间不销毁。



curl_global_init这个里面基本没做什么，多次调用也没有关系。

而且可以不调用，因为curl_easy_init里会检查，发现没有调用过curl_global_init，会自己调用一次。

核心数据结构：Curl_easy。

会组成双向链表。

结构体内部还是比较复杂的。不细看了。



我现在比较关系的是，post或者get请求得到的内容，放在什么位置，多次调用会不会导致多次重复分配导致内存泄露？

默认是直接打印出来的，如果你想要保存，就设置WRITEFUNCTION和WRITEDATA这2个选项。

```
		std::stringstream out;
        void* curl = curl_easy_init();
        // 设置URL
        curl_easy_setopt(curl, CURLOPT_URL, "http://172.21.1.121:4000/api/officeZone1/tempHum/allDevices/last");
        // 设置接收数据的处理函数和存放变量
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, write_data);
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &out);
```

实现的回调函数类似这样：

```
size_t write_data(void *ptr, size_t size, size_t nmemb, void *stream) {
    string data((const char*) ptr, (size_t) size * nmemb);
    *((stringstream*) stream) << data << endl;
    return size * nmemb;
}
```

碰到一个问题，就是返回这个。是因为我直接把string传递给curl了。应该用c_str()来传递。

```
curl_easy_perform() failed: Couldn't resolve host name
```



# multi的用法

multi接口是对easy接口的封装。是为了支持并发访问。

涉及的结构体是：CURLM。

```
CURLM *cm;
cm = curl_multi_init();
curl_multi_setopt(cm, CURLMOPT_MAXCONNECTS, 10);
for (int i=0; i<URL_NUM; i++) {
    CURL *hdl = curl_easy_init();
    //xxx
    curl_multi_add_handle(cm, hdl);
}
int ret = -1;
fd_set rset, wset, eset;
long timeout;
int max_fd;
struct timeval tv;
while(ret ) {
    curl_multi_perform(cm, &ret);
    if(ret) {
        FD_ZERO(&rset);
        FD_ZERO(&wset);
        FD_ZERO(&eset);
        if(curl_multi_fdset(cm, &rset, &wset, &eset, &max_fd)) {
            return -1;
        }
        if(curl_multi_timeout(cm, &timeout)) {
            return -1;
        }
        if(timeout == -1) {
            timeout = 100;
        }
        if(max_fd == -1) {
            sleep(timeout/100);
        } else {
            
        }
        
    }
}
```



# get请求





看avs里的使用，curl_easy_perform是阻塞执行的。

是的，easy接口是同步执行，multi接口是异步执行。



libcurl上传的两种方式：

1、直接上传。类似form表单的方式。我现在就是需要这种。

2、上传二进制流。



CURLFORM_COPYNAME 什么意思？

curl_addform是用来给multipart/formdata添加一个section的。

你需要先理解multipart。

每一个部分由一个name和一个content组成。

如果对应的这个部分是用来存放文件的，有一个content-type和一个filename。

```
CURLFORM_COPYNAME
	这个表示curl会把这个name拷贝走。你可以不再管了。
	被拷贝而分配的空间，会在curl_formfree的时候被释放掉。
	对应的CURLFORM_PTRNAME
	这样不会拷贝，所以你得自己继续维持这个name对应内存的有效性。
CURLFORM_COPYCONTENTS
	
```

# 基本示例分析

libcurl是一个C语言库，用于进行网络数据传输，支持多种协议，如HTTP、HTTPS、FTP、SCP、SFTP等。开发者可以使用libcurl在其应用程序中实现网络通信，从而实现下载、上传和其他网络数据传输操作。以下是关于libcurl开发的一般步骤：

1. **安装libcurl**：
   在开始使用libcurl之前，你需要确保在你的系统上安装了libcurl库。你可以从libcurl的官方网站（https://curl.se/download.html）下载最新版本的源代码，并根据文档中的指南进行编译和安装。

2. **包含头文件**：
   在你的C或C++代码中包含libcurl的头文件，通常是 `curl/curl.h`。这些头文件包含了libcurl的函数和数据结构的声明。

   ```c
   #include <curl/curl.h>
   ```

3. **初始化libcurl**：
   在你的应用程序中，需要调用`curl_global_init`来初始化libcurl。这通常在应用程序的启动部分执行一次。

   ```c
   CURLcode res = curl_global_init(CURL_GLOBAL_DEFAULT);
   if (res != CURLE_OK) {
       fprintf(stderr, "curl_global_init() failed: %s\n", curl_easy_strerror(res));
       return 1;
   }
   ```

4. **创建CURL句柄**：
   在使用libcurl进行网络请求之前，需要创建一个CURL句柄，该句柄用于配置和执行请求。

   ```c
   CURL *curl = curl_easy_init();
   if (!curl) {
       fprintf(stderr, "Failed to create CURL handle\n");
       return 1;
   }
   ```

5. **配置请求**：
   使用`curl_easy_setopt`函数来配置CURL句柄以定义你的请求，包括URL、请求方法、请求头、请求体等。

   ```c
   curl_easy_setopt(curl, CURLOPT_URL, "https://example.com/api/resource");
   curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L); // 使用GET方法
   ```

6. **执行请求**：
   使用`curl_easy_perform`函数来执行网络请求。

   ```c
   CURLcode res = curl_easy_perform(curl);
   if (res != CURLE_OK) {
       fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
   }
   ```

7. **处理响应**：
   一旦请求完成，你可以使用libcurl提供的函数来处理响应数据，包括响应头和响应体。

8. **清理资源**：
   最后，需要清理CURL句柄和全局curl环境。

   ```c
   curl_easy_cleanup(curl);
   curl_global_cleanup();
   ```

这只是一个简单的libcurl开发示例，libcurl提供了更多的选项和功能，可以根据具体的需求来进行配置。你可以参考libcurl的文档和示例代码来进一步了解其功能和用法。



# 参考资料

1、使用libcurl下载文件小例

https://www.cnblogs.com/rainbow70626/p/7618378.html

2、libcurl下载文件

https://www.cnblogs.com/meteoric_cry/p/3681546.html

3、官网示例合集

https://curl.haxx.se/libcurl/c/example.html

4、Curl使用（一）

https://blog.csdn.net/yujunan/article/details/8713176

5、c语言libcurl库的异步用法

https://www.cnblogs.com/zhaoyl/p/4001151.html

6、libcurl基本知识、post、get请求 -- libcurl

https://blog.csdn.net/cy_cai/article/details/41941161

7、libcurl使用easy模式阻塞卡死等问题的完美解决

https://www.cnblogs.com/bigben0123/p/3192978.html

8、使用multi curl进行http并发访问

https://www.cnblogs.com/bigben0123/p/3154406.html

9、

https://blog.csdn.net/breaksoftware/article/details/45874197

10、libcurl上传文件

https://cloud.tencent.com/developer/article/1365309