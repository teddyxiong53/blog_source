---
title: busybox之init.d目录分析
date: 2018-01-30 09:35:27
tags:
	- busybox

---



我们先看一个典型的init.d目录。

```
S01logging
S20urandom
S40network
S50sharing
S60testing
rcS
```



#rcS

rcS是总的文件，会把所有S开头的脚本文件依次执行一遍，按照数字编号的顺序。

```
#!/bin/sh

for i in /etc/init.d/S??*; do
    [ ! -f "$i" ] && continue #忽略软链接文件
    
    case "$i" in 
        *.sh)
            (
                #不直接调用，前面做这2步，是为了脚本加速。
                trap -s INT QUIT TSTP
                set start #具体用途不清楚，效果就是在环境变量里增加了一条'_'=start
                . $i
            )
            ;;
        *)
            $i start
            ;;
done
```

实际情况，都是走下面这一个分支的，没有带sh后缀名。

# S01logging

就是启动了/sbin/syslogd和/sbin/klogd这2个守护进程。

# S20urandom

产生urandom种子的。

内容写得有点多。不看了。

# S40network

这个简单，分析一下结构。

就是要实现start、stop、restart这3个参数的处理。

```
#!/bin/sh

mkdir -p /run/network

case "$1" in
    start)
        printf "Starting network: "
        /sbin/ifup -a
        [ $? = 0 ] && echo "OK" || echo "FAIL"
        ;;
       
    stop)
        printf "Stopping network: "
        /sbin/ifdown -a
        [ $? = 0 ] && echo "OK" || echo "FAIL"
        ;;
    restart|reload)
        "$0" stop
        "$0" start
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        ;;
esac

exit $?
```

