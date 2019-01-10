---
title: python之getopt
date: 2019-01-10 10:59:22
tags:		
	- python

---



直接看例子就好了。

```
import getopt
import sys
shortopts = "hd:s:b:k:l:m:c:t:vqp:"
longopts = ["help", "fast-open", "pid-file=", "log-file=", "user=", "version"]

optlist, args = getopt.getopt(sys.argv[1:], shortopts, longopts)


print optlist
print args
```

这是从ssr的代码里弄出来的。

看看对参数的解析的情况。

```
python test1.py -h -d daemon_flag -b local_address -l local_port -s server_address -p server_port -k password -m method -c config_file -t timeout -v -q  --help --fast-open --pid-file=xx.pid --log-file=xx.log --user=xx --version
[('-h', ''), ('-d', 'daemon_flag'), ('-b', 'local_address'), ('-l', 'local_port'), ('-s', 'server_address'), ('-p', 'server_port'), ('-k', 'password'), ('-m', 'method'), ('-c', 'config_file'), ('-t', 'timeout'), ('-v', ''), ('-q', ''), ('--help', ''), ('--fast-open', ''), ('--pid-file', 'xx.pid'), ('--log-file', 'xx.log'), ('--user', 'xx'), ('--version', '')]
[]
```

-d的可能取值是：start、stop、restart。

