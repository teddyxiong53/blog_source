---
title: XR872之httpclient代码分析
date: 2020-07-07 10:17:51
tags:
	- XR872

---

1

这个库的作者是noyasoft@netvision.net.il

github上找不到。

是同步方式执行的。

发送完之后，就阻塞等待回复。这样处理简单直观。

我只需要关注HTTPCUsr_api.c 。

把httpc命令打开，测试一下这个命令。

```
httpc ssl-post https://auth.iflyos.cn/oauth/ivs/device_code client_id=e3150fb6-592e-47ca-80fd-c737e245f077&scope=user_ivs_all&scope_data=%7B%22user_ivs_all%22%3A%20%7B%22device_id%22%3A%20%20%2220200001%22%7D%7D
```

出错了。

```
WAR drop=1099, fctl=0x00d0.
[HTTPC][ERR]Recv Response failed..
[cmd ERR] HTTPC_post_test():252, http request err..
```

我还是需要先在Linux上测试一下这个httpclient。

在sourceforge上找到这个代码。

https://sourceforge.net/projects/chttpclient/

代码跑起来没有什么参考意义。



post需要带上证书。

httpc ssl-post url  cert。

最后一个参数是证书。

讯飞的证书怎样获得呢？

```
//httpc ssl-post(0) url(1) data(2)
```

使用chrome浏览器，打开讯飞的网站，点击那个锁的图标就可以看到证书，然后导出成文件就可以得到了。

post的用法，可以参考src/net/cloud/aliyun的代码。这个也是https post请求。

证书需要在post之前，通过函数设置进去：

```
HTTPC_Register_user_certs(iflyos_https_get_certs);
```

post函数里放的是要发送的数据。

要设置header，这样：

```
HTTPC_request(clientParams, alink_get_heads)
```

基本流程：

```
HTTPC_open
HTTPC_request
HTTPC_get_request_info 
	这个是检查返回code
HTTPC_read
	取得返回的结果。
HTTPC_close
```

可以成功对讯飞官网进行post请求。





参考资料

1、

