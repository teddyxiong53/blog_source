---
title: Linux管理之批量跨服务器拷贝文件
date: 2017-07-25 23:29:03
tags:
---

因为scp需要输入密码和一个yes。所以还是要靠expect来实现密码的自动输入。

```
#!/bin/bash
expect -c "
spawn scp root@1.2.3.4:/root/1.log /root
expect {
\"*assword\" {set timeout 300; send \"password\r\";}
\"yes/no\" {send \"yes\r\"; exp_continue;}
}
expect eof"
```

