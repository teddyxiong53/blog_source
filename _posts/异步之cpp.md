---
title: 异步之cpp
date: 2020-05-01 10:20:08
tags:
	- 异步

---



async会捕获所有的异常，保存到future里，然后在future.get()的时候再抛出来。

这个特性看起来不错，但是因为c++的异常不携带栈信息。所以这个会导致所有现场信息丢失。



可以说，**std::async帮我们将std::future、std::promise和std::packaged_task三者结合了起来。**

那么我就使用async这个类就够了。不去研究promise了。



std::async的本质是创建了一个线程。

```c++
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <thread>
#include <chrono>
#include <future>

std::string fetchDataFromDB(std::string recvData)
{
    std::cout << "fetchDataFromDB start, thread id:" << std::this_thread::get_id() << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(5));
    return "DB_" + recvData;
}

std::string fetchDataFromFile(std::string recvData)
{
    std::cout << "fetchDataFromFile start, thread id:" << std::this_thread::get_id() << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(3));
    return "File_" + recvData;
}

int main()
{
    std::cout << "main thread start" << std::endl;
    std::chrono::system_clock::time_point start = std::chrono::system_clock::now();
    std::future<std::string> resultFromDB = std::async(std::launch::async, fetchDataFromDB, "Data");
    std::future<std::string> resultFromFile = std::async(std::launch::deferred, fetchDataFromFile, "Data");

    std::string fileData = resultFromFile.get();//这个因为是deferred方式，get调用才开始执行。
    std::string dbData = resultFromDB.get();
    auto end  = std::chrono::system_clock::now();
    auto diff = std::chrono::duration_cast<std::chrono::seconds>(end-start).count();
    std::cout << "total use time is :" << diff <<std::endl;

    std::cout << "read from db:" << dbData << std::endl;
    std::cout << "read from file:" << fileData << std::endl;
    return 0;
}
```

可以查询future的执行状态。

```
#include <iostream>
#include <vector>
#include <algorithm>
#include <string>
#include <thread>
#include <chrono>
#include <future>

std::string fetchDataFromDB(std::string recvData)
{
    std::cout << "fetchDataFromDB start, thread id:" << std::this_thread::get_id() << std::endl;
    std::this_thread::sleep_for(std::chrono::seconds(5));
    return "DB_" + recvData;
}



int main()
{
    std::cout << "main thread start" << std::endl;
    std::chrono::system_clock::time_point start = std::chrono::system_clock::now();
    std::future<std::string> resultFromDB = std::async(std::launch::async, fetchDataFromDB, "Data");

    std::future_status status ;
    do {
        status = resultFromDB.wait_for(std::chrono::seconds(1));
        if(status == std::future_status::ready) {
            std::cout << "status is ready, now you can get the data" << std::endl;
            std::string result = resultFromDB.get();
            std::cout << result << std::endl;
        } else if(status == std::future_status::deferred) {
            std::cout << "deferred ..." << std::endl;

        } else if(status == std::future_status::timeout) {
            std::cout << "timeout ..." <<std::endl;
        }
    } while(status != std::future_status::ready);
    
    return 0;
}
```



参考资料

1、std::async()详解

https://blog.csdn.net/u012372584/article/details/97108417

2、c++11 future, promise, async

https://www.cnblogs.com/my_life/articles/7767536.html