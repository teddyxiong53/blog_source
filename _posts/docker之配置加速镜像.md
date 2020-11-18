---
title: docker之配置加速镜像
date: 2018-01-18 12:52:50
tags:
	- docker

---



我一直喜欢使用阿里云的服务，所以就选择阿里云的加速。

1、先到阿里云注册开发者账号。网站在这里：<https://dev.aliyun.com/>

这个我之前就已经注册过了。

2、进入到加速器页面。

<https://cr.console.aliyun.com/#/accelerator>

这个界面有告诉你怎么操作。

修改/etc/docker/daemon.json。

把下面的所有内容直接粘贴到shell执行

```
sudo mkdir -p /etc/docker
sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://0ebmeoa9.mirror.aliyuncs.com"]
}
EOF
sudo systemctl daemon-reload
sudo systemctl restart docker
```

