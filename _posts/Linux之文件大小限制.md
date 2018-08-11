---
title: Linux之文件大小限制
date: 2018-08-06 17:36:38
tags:
	- Linux

---



要生成log文件，但是要限制文件大小。

```
/tmp # syslogd -h
syslogd: invalid option -- 'h'
BusyBox v1.26.2 (2018-08-03 10:09:39 CST) multi-call binary.

Usage: syslogd [OPTIONS]

System logging utility
(this version of syslogd ignores /etc/syslog.conf)

        -n              Run in foreground
        -R HOST[:PORT]  Log to HOST:PORT (default PORT:514)
        -L              Log locally and via network (default is network only if -R)
        -O FILE         Log to FILE (default: /var/log/messages, stdout if -)
        -s SIZE         Max size (KB) before rotation (default:200KB, 0=off)
        -b N            N rotated logs to keep (default:1, max=99, 0=purge)
        -l N            Log only messages more urgent than prio N (1-8)
        -S              Smaller output
```

syslogd其实默认就支持的。



# 参考资料

用linux来控制log文件的大小和数量

http://www.voidcn.com/article/p-rpnupfte-pg.html

Linux日志文件总管——logrotate

https://linux.cn/article-4126-1.html