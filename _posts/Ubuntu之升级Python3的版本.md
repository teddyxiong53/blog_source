---
title: Ubuntu之升级Python3的版本
date: 2018-06-10 23:12:51
tags:
	- Ubuntu

---



手动安装HomeAssistant，提示我的Python3的版本太低。要升级。



操作方法如下：

```
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
sudo rm /usr/bin/python3
sudo ln -s /usr/bin/python3.6 /usr/bin/python3
```



# 参考资料

1、ubuntu14.04 升级python3.4到3.6

https://blog.csdn.net/u012551524/article/details/80419441