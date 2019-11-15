---
title: homeassistant之Floorplan界面
date: 2019-11-15 11:50:49
tags:
	- homeassistant

---

1

Floorplan是一个很直观的hass界面。

安装

从这里下载代码。只有100K左右。十几个文件。

https://github.com/pkozul/ha-floorplan/tree/master

然后解压，把panel_custom.yaml、panels、www这3个文件（或目录）拷贝到.homeassistant目录下。

在configuration.yaml里，增加：

```
panel_custom:
  - name: floorplan
    sidebar_title: 我的家
    sidebar_icon: mdi:home
    config: !include floorplan.yaml
```

然后重启hass。可以看到侧边栏有一个“我的家”，点进去就可以了。

默认这个房子的布局跟你的家里的布局肯定是不同的。

所以接下来就是修改这个图。

这个图是svg格式的。所以我们就需要制作svg图片。

我们先跳过这一步。

接下来是修改floorplan.yaml文件。











参考资料

1、图形化控制界面（Floorplan）

https://www.hachina.io/docs/3170.html