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

#post方式

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