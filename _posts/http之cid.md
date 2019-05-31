---
title: http之cid
date: 2019-05-29 16:25:51
tags:
	- http

---

1

简单说，cid是一种协议。

指定资源的位置，但是是以id的方式，所以比较简洁。

```
[writeString=--___dueros_dcs_v1_boundary___
Content-Disposition: form-data; name="metadata"
Content-Type: application/json; charset=utf-8

{"directive":{"header":{"namespace":"ai.dueros.device_interface.voice_output","name":"Speak","dialogRequestId":"d38c839c-ea29-4cc5-865b-3acee647063a","messageId":"NWJiZWlYTNlMGUxMDY0NjU="},"payload":{"token":"eyJib3RfaWQiOiJ1cyIsInJlc3VsdF90b2tlb6Ijg3ODUxODY5NmE0OTk5MTk5YmJkMDc1MjM2MTY2NjRjIiwiYm90X3Rva2VuIjoibnVsbCJ9","format":"AUDIO_MPEG","url":"cid:239533"}}} 注意这里。

--___dueros_dcs_v1_boundary___
Content-Type: application/octet-stream
Content-Disposition: form-data; name="audio"
Content-ID: <239533>  注意这里。

]
```



参考资料

1、cid

https://www.cid-protocol.org/co/home.html

2、

https://www.cid-protocol.org/docs/spec/web/co/04_BasicConcepts.html