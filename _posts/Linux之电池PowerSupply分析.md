---
title: Linux之电池PowerSupply分析
date: 2022-08-18 13:55:33
tags:
	- Linux

---

--

# linux标准的Power Supply接口

Linux 标准的电源供应（Power Supply）接口是通过 sysfs 文件系统提供的。该接口允许用户和应用程序访问关于系统上电源供应的信息，如电池状态、电源适配器状态等。这个接口的位置通常位于 `/sys/class/power_supply` 目录下。

以下是一些常见的电源供应接口文件和相关信息：

- `/sys/class/power_supply/BAT0/`：这是电池 `BAT0` 的目录，其中包含了关于电池的信息。
- `status`：电池的状态，例如 "Charging"、"Discharging"、"Full" 等。
  - `capacity`：电池的容量百分比。
  - `energy_now` 和 `energy_full`：当前电量和总电量（单位：微焦耳）。
  - `power_now`：当前电量消耗速率（单位：微瓦特）。
  
- `/sys/class/power_supply/AC/`：这是交流电源适配器的目录，其中包含了关于适配器的信息。

  - `online`：适配器是否连接，值为 0 或 1。

这些接口提供了对电池和适配器状态的访问，有助于应用程序、工具或脚本监控系统电源供应的情况。请注意，不同的系统可能具有不同的接口和文件名，具体细节可能会有所不同。

值得注意的是，sysfs 在现代 Linux 系统中已经逐渐被 systemd 或 udev 替代，因此在一些发行版中，特定的信息可能通过不同的方式暴露出来。建议查阅特定发行版的文档或相关资源以获取更准确的信息。