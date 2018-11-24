---
title: AirKiss技术原理
date: 2018-11-23 10:43:19
tags:
	- 微信
---



先看传统的方式，以智能摄像头为例。

第一次开机，摄像头是进入到AP模式，根据说明书上的地址，手机访问指定ip地址，其实就是摄像头上运行了一个web server。

我们把家里的路由器的名字和密码填入进去。然后摄像头进入到STA模式，去连接路由器，然后就好了。

这个方式，手机需要从路由器上断开，而且需要访问ip地址，这个对于普通用户不太友好。



AirKiss的基础原理是靠wifi模组的STA模式的混杂模式来做的。

混杂模式，就是不过滤MAC地址，把所有包都收下来。（本来一般都是不接收不是发给自己的包的）

这个方式，受到wifi信道的干扰特别大。



AirKiss局域网发现和AirKiss微信配网，是两个相对独立的模块。



# 配网流程

Linux下的代码总体是这样，需要对接的，用TODO标记了。

```
#include "airkiss.h"
airkiss_context_t akcontext;
const airkiss_config_t akconf = {
	(airkiss_memset_fn)&memset,
	(airkiss_memcpy_fn)&memcpy,
	(airkiss_memcmp_fn)&memcmp,
	(airkiss_printf_fn)&printf //set to 0 if you don't want to print
};

int cur_channel =1;

void *process_100ms_time(void *arg)
{
	pthread_detach(pthread_self());
	
	while(1) {
		if(cur_channel >= 13) {
			cur_channel = 1;
		} else {
			cur_channel ++;
		}
		wifi_set_channel(cur_channel);
		airkiss_change_channel(&akcontext);
		usleep(100*1000);
	}
}
int system_init_airkiss()
{
	// step 1. init
	int ret = 0;
	ret = airkiss_init(&akcontext, &akconf);
	if(ret < 0) {
		return -1;
	}
	#if AIRKISS_ENABLE_CRYPT
	char *key = "1234";//this is a string, whatever the content is
	airkiss_set_key(&akcontext, key, strlen(key);
	#endif
	wifi_station_disconnect();//TODO
	wifi_set_opmode(STATION_MODE);//TODO
	cur_channel = 1;
	wifi_set_channel(cur_channel);//TODO
	
	pthread_t pid;
	pthread_create(&pid, NULL, process_100ms_time, NULL);
	//set promiscuous mode
	wifi_set_promiscuous_rx_cb(wifi_promiscuous_rx);//TODO
	wifi_promiscuous_enable(1);//TODO
	
}
int main()
{
	system_init_airkiss();
}
```



参考资料

1、airkiss技术原理

https://blog.csdn.net/lb5761311/article/details/77945848

2、AirKiss2.0开发文档

https://iot.weixin.qq.com/wiki/new/index.html?page=4-1-2