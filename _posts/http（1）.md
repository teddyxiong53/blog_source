---
title: http（1）
date: 2018-05-07 20:28:56
tags:
	- http

---



http区分大小写吗？

根据RFC2616，HTTP Method是区分大小写的，而Header是不区分的。
所以 GET/POST/PUT等需要大写，而content-encoding/user-agent则不用。
http://www.ietf.org/rfc/rfc2616.txt
补充一句，URI是不区分大小写的，而且也不区分转义符

