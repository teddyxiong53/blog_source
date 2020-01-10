---
title: shadowsocks之Linux终端使用
date: 2018-01-22 17:46:09
tags:
	- shadowsocks
	- Linux

---



1、安装polipo。

```
sudo apt-get install polipo
```

polipo是一个轻量级的缓存web代理程序。

2、安装shadowsocks。

```
sudo apt-get install shadowsocks
```

3、配置shadowsocks。在/etc/shadowsocks/config.json里。把账号信息配置进去。

4、运行sslocal。注意运行程序不是叫shadowsocks。

发现我配置加密方式为aes-128-ctr的时候，sslocal报错，说不支持这种方式。

我把刚才安装的shadowsocks卸载掉。用pip安装。

```
sudo pip install shadowsocks
```

这样安装的shadowsocks是2.8.2的。

启动没有报错。

```
sslocal -c /etc/shadowsocks/config.json
```

一个ssr的配置文件是这样：

```
{
    "server": "64.137.198.70",
    "server_port": 5556,
    "local_address": "127.0.0.1",
    "local_port": 1080,

    "password": "doub.io/sszhfx/*doub.ws/sszhfx/*5556",
    "method": "chacha20",
    "protocol": "auth_sha1_v4",
    "protocol_param": "",
    "obfs": "tls1.2_ticket_auth",
    "obfs_param": "",
    "speed_limit_per_con": 0,
    "speed_limit_per_user": 0,

    "timeout": 120,
    "udp_timeout": 60,
    "dns_ipv6": false,
    "connect_verbose_info": 0,
    "redirect": "",
    "fast_open": false
}
```



5、现在配置polipo。

修改/etc/polipo/config文件;

```
socksParentProxy = "localhost:1080"
socksProxyType = socks5
```

6、启动polipo服务。

```
sudo service polipo stop
sudo service polipo start
```

7、测试一下。

```
http_proxy=http://localhost:8123 curl www.google.com
```

已经可以正常访问google了。

为了方便使用，我们把http_proxy这部分加一个别名。

在`~/.bashrc`最后加上：

```
alias hp="http_proxy=http://localhost:8123"
```

然后:

```
. ~/.bashrc
```

现在

```
hp curl www.google.com
```

不用这么麻烦，直接export就好了。



# proxychains

polipo已经不再更新了。所以换成proxychains。

安装：

```
sudo apt-get install proxychains
```

配置：

```
sudo vim /etc/proxychains.conf
```

在最后面加上这样一行：

```
socks5 127.0.0.1 1080
```

socks4那一行注释掉。

但是碰到了问题，就是dns不能解析。

```
sudo apt-get install dnsutils
```

还是不行。

又看到一个解释：

```
理论上来说，proxychains不支持udp的，而且dns包基于udp协议，linux上基本所有要操作udp协议的软件都要root权限或者net_admin的capability
```

但是我用sduo来执行，也不行。

编辑这个文件：

```
/usr/lib/proxychains3/proxyresolv 
```

修改默认的4.2.2.2为9.9.9.9（ibm的dns地址）。还是不行。

到/etc/proxychains.conf里把proxy_dns这一行注释掉。也不行。

当前用的是3.1版本。使用proxychains-ng的看看。这个要自己编译。

https://sourceforge.net/projects/proxychains-ng/files/proxychains-ng-4.12.tar.xz/download?use_mirror=ayera

编译后，sudo make install后，/etc目录下，没有看到conf文件。

```
sudo make install-config
```

是安装到这里了。

```
./tools/install.sh -D -m 644 src/proxychains.conf /usr/local/etc/proxychains.conf
```



我把电脑上安装的shadowsocks卸载掉。安装下面这个文章重新来一遍。

https://cndaqiang.github.io/2017/09/28/ubuntu1604-ssr/

在自己的目录下，手动启动。

现在结合proxychains正常了。



# 换一种思路

思路就是：虚拟机通过pc机运行的ssr，pc为虚拟机提供代理服务。

修改上面的hp这个alias为：

```
alias hp='http_proxy=http://192.168.190.1:1080'
```

然后测试一下：

```
teddy@teddy-ubuntu:~$ hp ping google.com
```

可以下载谷歌的首页下来。

如果不带hp，则不行。

我的手机平板都可以通过这种方式来上网。

而我的pc当前承担是任务，可以转到我的树莓派上来。

对于https的。我还需要加上一个：

```
alias hps='https_proxy=http://192.168.190.1:1080'
```





# 参考资料

1、VMWare虚拟机通过主机shadowsocks代理上网

https://blog.csdn.net/u010726042/article/details/53187937

2、手机不安装软件实现翻墙（VPS和PC端已成功配置好SSR的前提下）

https://therealinternet.ml/index.php/2017/10/03/%e6%89%8b%e6%9c%ba%e4%b8%8d%e5%ae%89%e8%a3%85%e8%bd%af%e4%bb%b6%e5%ae%9e%e7%8e%b0%e7%bf%bb%e5%a2%99%ef%bc%88vps%e5%92%8cpc%e7%ab%af%e5%b7%b2%e6%88%90%e5%8a%9f%e9%85%8d%e7%bd%ae%e5%a5%bdssr%e7%9a%84/