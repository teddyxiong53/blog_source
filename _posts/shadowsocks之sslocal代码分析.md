---
title: ssr之sslocal代码分析
date: 2019-01-03 09:52:59
tags:
	- ssr

---



````
可以学习到的东西：
1、getopt。
2、json解析。
3、daemon用法。
	把日志定向的方法。
4、signal处理。
5、每个文件加测试代码的方法。
6、锁文件操作。
7、pwd模块用法。
8、lru cache实现。
9、构造函数里调用其他函数。
10、替换标准库的函数，打补丁。
	patch_socket
11、读取解析一个文件的内容。
	hosts和resolv.conf
12、errno获取和判断。
````

测试方法可以改成这样：

sslocal和ssserver都跑在localhost上。就wget www.baidu.com。

服务器端

```
hlxiong@hlxiong-VirtualBox:~/work/test/ssr/shadowsocks-master/shadowsocks$ python ./server.py -c config.json -v
INFO: loading config from config.json
2019-01-12 13:37:16 WARNING  warning: server set to listen on localhost:2333, are you sure?
2019-01-12 13:37:16 INFO     loading libcrypto from libcrypto.so.1.0.0
2019-01-12 13:37:16 INFO     starting server at localhost:2333
2019-01-12 13:37:16 DEBUG    server sock fd:3
2019-01-12 13:37:16 DEBUG    using event model: epoll
2019-01-12 13:37:26 DEBUG    tcprelay _sweep_timeout
2019-01-12 13:37:36 DEBUG    tcprelay _sweep_timeout
2019-01-12 13:37:46 DEBUG    tcprelay _sweep_timeout
2019-01-12 13:37:47 DEBUG    event:1, fd:3
2019-01-12 13:37:47 DEBUG    accept
2019-01-12 13:37:47 DEBUG    client address:('127.0.0.1', 38646)
2019-01-12 13:37:47 DEBUG    event:1, fd:8
2019-01-12 13:37:47 DEBUG    sock == self._local_sock
2019-01-12 13:37:47 DEBUG    _on_local_read
2019-01-12 13:37:47 DEBUG    local read len:173
2019-01-12 13:37:47 INFO     connecting www.baidu.com:80 from 127.0.0.1:38646
2019-01-12 13:37:47 DEBUG    resolve :www.baidu.com
2019-01-12 13:37:47 DEBUG    resolving www.baidu.com with type 1 using server 127.0.0.1
2019-01-12 13:37:47 DEBUG    ./../shadowsocks/asyncdns.pyc handle_event 356
2019-01-12 13:37:47 DEBUG    remote_addr:14.215.177.39, remote_port:80
2019-01-12 13:37:47 DEBUG    event:4, fd:9
2019-01-12 13:37:47 DEBUG    sock == self._remote_sock
2019-01-12 13:37:47 DEBUG    _on_remote_write
2019-01-12 13:37:47 DEBUG    write to sock, len:140
2019-01-12 13:37:47 DEBUG    event:1, fd:9
2019-01-12 13:37:47 DEBUG    sock == self._remote_sock
2019-01-12 13:37:47 DEBUG    _on_remote_read
2019-01-12 13:37:47 DEBUG    write to sock, len:2797
2019-01-12 13:37:57 DEBUG    tcprelay _sweep_timeout
2019-01-12 13:38:00 DEBUG    event:1, fd:8
2019-01-12 13:38:00 DEBUG    sock == self._local_sock
2019-01-12 13:38:00 DEBUG    _on_local_read
2019-01-12 13:38:00 DEBUG    local read len:0
2019-01-12 13:38:00 DEBUG    destroy: www.baidu.com:80
2019-01-12 13:38:00 DEBUG    destroying remote
```

客户端：

```
^Chlxiong@hlxiong-VirtualBox:~/work/test/ssr/shadowsocks-master/shadowsocks$ python local.py -c ./config.json -v
INFO: loading config from ./config.json
2019-01-12 13:37:32 WARNING  warning: server set to listen on localhost:2333, are you sure?
2019-01-12 13:37:32 INFO     loading libcrypto from libcrypto.so.1.0.0
2019-01-12 13:37:32 INFO     starting local at 127.0.0.1:1080
2019-01-12 13:37:32 DEBUG    server sock fd:3
2019-01-12 13:37:32 DEBUG    using event model: epoll
2019-01-12 13:37:42 DEBUG    tcprelay _sweep_timeout
2019-01-12 13:37:47 DEBUG    event:1, fd:3
2019-01-12 13:37:47 DEBUG    accept
2019-01-12 13:37:47 DEBUG    client address:('127.0.0.1', 33476)
2019-01-12 13:37:47 DEBUG    chosen server: localhost:2333
2019-01-12 13:37:47 DEBUG    event:1, fd:8
2019-01-12 13:37:47 DEBUG    sock == self._local_sock
2019-01-12 13:37:47 DEBUG    _on_local_read
2019-01-12 13:37:47 DEBUG    local read len:3
2019-01-12 13:37:47 DEBUG    write to sock, len:2
2019-01-12 13:37:47 DEBUG    event:1, fd:8
2019-01-12 13:37:47 DEBUG    sock == self._local_sock
2019-01-12 13:37:47 DEBUG    _on_local_read
2019-01-12 13:37:47 DEBUG    local read len:20
2019-01-12 13:37:47 DEBUG    cmd:1
2019-01-12 13:37:47 INFO     connecting www.baidu.com:80 from 127.0.0.1:33476
2019-01-12 13:37:47 DEBUG    write to sock, len:10
2019-01-12 13:37:47 DEBUG    resolve :localhost
2019-01-12 13:37:47 DEBUG    hit hosts: localhost
2019-01-12 13:37:47 DEBUG    remote_addr:127.0.0.1, remote_port:2333
2019-01-12 13:37:47 DEBUG    event:1, fd:8
2019-01-12 13:37:47 DEBUG    sock == self._local_sock
2019-01-12 13:37:47 DEBUG    _on_local_read
2019-01-12 13:37:47 DEBUG    local read len:140
2019-01-12 13:37:47 DEBUG    event:4, fd:9
2019-01-12 13:37:47 DEBUG    sock == self._remote_sock
2019-01-12 13:37:47 DEBUG    _on_remote_write
2019-01-12 13:37:47 DEBUG    write to sock, len:173
2019-01-12 13:37:47 DEBUG    event:1, fd:9
2019-01-12 13:37:47 DEBUG    sock == self._remote_sock
2019-01-12 13:37:47 DEBUG    _on_remote_read
2019-01-12 13:37:47 DEBUG    write to sock, len:2781
2019-01-12 13:37:57 DEBUG    tcprelay _sweep_timeout
```





lru cache是存放dns记录的。



可以到/usr/local/lib/python2.7/dist-packages/shadowsocks这个目录下，运行有测试函数的文件。

例如运行asyncdns.py。

```
hlxiong@hlxiong-VirtualBox:/usr/local/lib/python2.7/dist-packages/shadowsocks$ python asyncdns.py
None invalid hostname: invalid.@!#$%^&$@.hostname
None invalid hostname: tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolong.hostname
None invalid hostname: tooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooolong.hostname
('google.com', '172.217.27.142') None
('google.com', '172.217.27.142') None
('example.com', '93.184.216.34') None
('www.facebook.com', '31.13.64.49') None
('ns2.google.com', '216.239.34.10') None
('ipv6.google.com', '2404:6800:4012:1::200e') None
```



分析一个场景：

在浏览器里访问www.google.com的时候，这个过程是怎么实现的？

或者简单点，在命令行里ping www.google.com的时候，怎么处理的？



把sslocal的代码看一下。

我就看2.8.2的。因为Ubuntu默认安装的就是这个。

看setup.py里。

```
    entry_points="""
    [console_scripts]
    sslocal = shadowsocks.local:main
    ssserver = shadowsocks.server:main
    """,
```



还是通过写的方式来读。

先新建一个ssr目录。在这个下面写。

下面新建shadowsocks目录。新建local.py。从头部开始写，可以看到依赖了shell.py。

新建shell.py。shell.py依赖了common.py。

common.py没有依赖自己写的文件了，算是底层的一个工具文件。

好，就从common.py开始写。

每个文件开始都从future模块引入了几个新的特性。

```
ord是根据字符求ascii码。
chr的根据int值得到字符。
```

```
def compat_chr(d):
    if bytes == str: #在python2里是True，在python3里是False
        return _chr(d)
    return bytes([d])
```



sslocal这个脚本是在哪里写的呢？

是在debian目录下。

```
#!/usr/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'shadowsocks==2.8.2','console_scripts','sslocal'
__requires__ = 'shadowsocks==2.8.2'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('shadowsocks==2.8.2', 'console_scripts', 'sslocal')()
    )
```

在setup.py里有这样写，应该就是setuptools生成的。

```
    entry_points="""
    [console_scripts]
    sslocal = shadowsocks.local:main
    ssserver = shadowsocks.server:main
    """,
```



2.8.2版本还是完全正常可用的。

我这样执行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/ssr/shadowsocks-master/shadowsocks$ python local.py -c /etc/shadowsocks/config.json
INFO: loading config from /etc/shadowsocks/config.json
2019-01-11 16:08:07 INFO     loading libcrypto from libcrypto.so.1.0.0
2019-01-11 16:08:07 INFO     starting local at 127.0.0.1:1080
2019-01-11 16:08:34 INFO     connecting www.google.com:80 from 127.0.0.1:33226
```

另外一个shell窗口，

```
wget www.google.com
```

可以正常工作。

所以可以在这个代码上加调试信息。

也不用加，执行时，加上-v选项就好了。

还是访问谷歌首页看看。

```
^Chlxiong@hlxiong-VirtualBox:~/work/test/ssr/shadowsocks-master/shadowsocks$ python local.py -c /etc/shadowsocks/config.json -v
INFO: loading config from /etc/shadowsocks/config.json
2019-01-11 16:12:03 INFO     loading libcrypto from libcrypto.so.1.0.0
2019-01-11 16:12:03 INFO     starting local at 127.0.0.1:1080
2019-01-11 16:12:03 DEBUG    using event model: epoll
2019-01-11 16:12:32 DEBUG    accept
2019-01-11 16:12:32 DEBUG    chosen server: 144.34.xxx.xx:xx
2019-01-11 16:12:32 INFO     connecting www.google.com:80 from 127.0.0.1:33236
```

当前Linux上没有做任何的区分，即使访问百度，也都统一经过了ssr。

过了大概一分钟，就会销毁。

```
2019-01-11 16:16:54 INFO     connecting www.baidu.com:80 from 127.0.0.1:33242
2019-01-11 16:17:39 DEBUG    destroy: www.baidu.com:80
2019-01-11 16:17:39 DEBUG    destroying remote
2019-01-11 16:17:39 DEBUG    destroying local
```

关键是状态机的切换。

看tcprelay.py里，

```
_handle_dns_resolved
# as sslocal:
# stage 0 SOCKS hello received from local, send hello to local
# stage 1 addr received from local, query DNS for remote
# stage 2 UDP assoc
# stage 3 DNS resolved, connect to remote
# stage 4 still connecting, more data from local received
# stage 5 remote connected, piping local and remote
```

在_on_local_read

```
elif is_local and self._stage == STAGE_INIT:
            # TODO check auth method
            self._write_to_sock(b'\x05\00', self._local_sock)
            self._stage = STAGE_ADDR
            return
```

```
handle_event
	_on_local_read
```

首先是local sock，收到了wget发来的信息。



总体上，还是一个网络server的架构。

先监听一个socket，接收连接，处理消息。

基于select机制。





