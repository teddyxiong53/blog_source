---
title: 树莓派之使用pi-gen编译系统
date: 2024-02-28 20:05:17
tags:
	- 树莓派

---

--

代码在这里：

https://github.com/RPi-Distro/pi-gen



```
# Example for building a lite system
echo "IMG_NAME='raspios'" > config
touch ./stage3/SKIP ./stage4/SKIP ./stage5/SKIP
touch ./stage4/SKIP_IMAGES ./stage5/SKIP_IMAGES
sudo ./build.sh  # or ./build-docker.sh
```

