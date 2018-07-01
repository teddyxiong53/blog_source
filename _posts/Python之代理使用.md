---
title: Python之代理使用
date: 2018-06-30 12:18:14
tags:
	- Python

---



想要写一个自动爬取ssr地址的脚本。但是第一步，就是需要可以让脚本可以通过代理去访问对应的网站。

第一种方式是使用Python3的urllib标准库。第二种是利用非常好用的requests库。

#urllib使用代理

```
import urllib.request as request

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "https://127.0.0.1:1080"
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

opener = request.build_opener(request.ProxyHandler(proxies))
request.install_opener(opener)

req = request.Request("https://doub.io", headers=headers)
resp = request.urlopen(req)

print (resp.read().decode())
```



# requests使用代理

```
import requests

proxies = {
    "http": "http://127.0.0.1:1080",
    "https": "https://127.0.0.1:1080"
}

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
}

resp = requests.get("https://doub.io", proxies=proxies)
print(resp.text)
```



requests比urllib好用。因为requests还支持sock5代理。





# 参考资料

1、Python：爬虫如何翻墙并保存获取到的数据？

https://segmentfault.com/q/1010000008986220