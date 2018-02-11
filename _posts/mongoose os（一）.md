---
title: mongoose os（一）
date: 2018-02-10 17:37:37
tags:
	- mongoose

---



看rt-thread的代码，看到mongoose os这个东西。

官网介绍在这里。

https://cesanta.com/docs/overview/intro.html

1、mongoose是一个用C语言写的网络库。

2、算是一个嵌入式网络编程的瑞士军刀。

3、它实现了事件驱动的非阻塞API。

4、基于它事件驱动实现了tcp/udp/mqtt/coap/websocket的server和client。

5、已经支持了PicoTCP 和lwip协议栈。

6、方便集成，就一个mongoose.c和一个mongoose.h文件。



# 一个http server的例子

我们通过这个例子来看mg的简单用法。

```
#include "mongoose.h"

static const char * s_http_port = "8888";

static void ev_handler(struct mg_connection *conn, int ev, void  *p)
{
	if(ev == MG_EV_HTTP_REQUEST)
	{
		struct http_message *hm = (struct http_message *)p;
		mg_send_head(conn, 200, hm->message.len, "Content-Type: text/plain");
		mg_printf(conn, "%.*s", (int)hm->message.len, hm->message.p);
	}
}
int main()
{
	struct mg_mgr mgr;
	struct mg_connection *conn;
	mg_mgr_init(&mgr, NULL);
	conn = mg_bind(&mgr, s_http_port, ev_handler);
	mg_set_protocol_http_websocket(conn);
	while(1)
	{
		mg_mgr_poll(&mgr, 100);
		
	}
	mg_mgr_free(&mgr);
	return 0;
}
```

用法还是很简单的。

