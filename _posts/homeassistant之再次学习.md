---
title: homeassistant之再次学习
date: 2019-11-09 15:26:49
tags:
	- python

---

1

基于venv来进行学习使用。

从github下载代码。

进入到代码目录，创建一个名为venv的环境。

```
python3 -m venv venv
```

激活venv。

```
source ./venv/bin/activate
```

安装所有依赖：

```
pip install -r requirements_all.txt
```

安装总是在apcaccess这个地方卡住了，换了豆瓣和阿里的源都是如此。

我把这个包先注释掉看看。

还有一些包是从github下载的。

依赖的东西真的是非常多。

在googlemaps这一步又卡住了。

网上查了一下，你在安装A的时候，A需要自动安装B，B这个的下载，还是走pypi的通路，而不是走国内源。

所以，解决办法是，修改你的venv的package_index.py文件。

把这个index_url默认值改成阿里的。

```
class PackageIndex(Environment):
    """A distribution index that scans web pages for download URLs"""

    def __init__(
            self, index_url="http://mirrors.aliyun.com/pypi/simple", hosts=('*',),
```

再试一次看看。

还是一样的卡住。

不是改参数默认值，在到下面再赋值一次为阿里的源。

这样就可以了。

执行homeassistant的安装：

```
python setup.py install
```

提示了错误。

```
sudo apt-get install python-dev
```

```
‘libpython3.6-dev’ 找到任何软件包
```

可以看到是在安装yarl这一步出错的。

```
pip install yarl
```

这样安装就可以了。

然后hass启动就可以了。

默认是启动在8123端口，但是我的电脑上这个端口给了polipo了。不能通过传递参数来指定端口。

所以我把polipo 停掉。

现在可以启动homeassistant了。



现在策略改为，实现功能为主，先尽量不要看代码。

```
hass.io
用来把你的树莓派变成一个智能家居中心。
你可以专注于集成你的设备和编写自动化。

hass.io的优势
1、免费开源。
2、针对树莓派优化。
3、100%的本地自动化。
4、易于安装和更新。基于hassos和docker。
5、有管理web界面。
6、容易创建备份。
7、一键安装大量流行的插件。
```

hassos是基于buildroot构建的。地址在这里。

https://github.com/home-assistant/hassos/releases

```
安装方法
把下载的镜像烧录到sd卡。对于树莓派，建议SD卡至少32GB。
	
可选操作
设置wifi信息或者设置静态ip。
在配置分区里，network/my-network文件里进行配置。

网络配置方法
hassos使用NetworkManager来控制网络。
在后面的版本，你可以通过ui来配置。
当前还只能通过配置文件来做。

一个my-network文件的模板是这样
[connection]
id=my-network
uuid=72111c67-4a5d-4d5c-925e-f8ee26efb3c3
type=802-11-wireless

[802-11-wireless]
mode=infrastructure
ssid=MY_SSID
# Uncomment below if your SSID is not broadcasted
#hidden=true

[802-11-wireless-security]
auth-alg=open
key-mgmt=wpa-psk
psk=MY_WLAN_SECRET_KEY

[ipv4]
method=auto

[ipv6]
addr-gen-mode=stable-privacy
method=auto
```

```
第一次开机，hassos会自动下载homeassistant的最新版本。
这个时间可能要20分钟左右。
你可以选择运行指定版本的homeassistant
hassio ha update --version=0.xx.x

```



参考资料

1、

https://home-assistant.cc/installation/general/

2、pip install 卡住不动的解决方案

https://blog.csdn.net/weixin_41579863/article/details/81568060