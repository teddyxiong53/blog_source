---
title: yocto之yoe项目分析
date: 2023-12-11 17:39:51
tags:
	- yocto

---

--

这个还是挺好的一个项目，非常适合用来深入研究yocto的定制。

对树莓派进行了很好的支持，所以做实验也方便。

另外，作者热心帮我解决了一个问题，所以对这个项目的好感大增。

决定投入精力深入研究一下。

# yoe的名字含义

yoe就是Yocto + OpenEmbeded。

# 编译rpi4-64

这个作为切入点。

```
source envsetup.sh rpi4-64
bitbake yoe-simple-image
```

## 工具命令

envsetup.sh向环境变量里导出了几个工具函数，可以很方便地使用，包括：

| 函数                                | 说明                                                         |
| ----------------------------------- | ------------------------------------------------------------ |
| yoe_add_layer                       | 添加一个layer。<br />2个参数：<br />url<br />branch          |
| yoe_build_all                       | 为这raspberrypi3 beaglebone 2个平台编译测试。                |
| yoe_check_install_dependencies      | 检测并安装bmaptool这个工具。它可以帮助加速镜像复制的过程，特别适用于大型镜像的复制和烧录。 |
| yoe_clean                           | 是直接把tmp目录删掉了。                                      |
| yoe_clean_sstate                    | 调用sstate-cache-management.sh脚本清空sstate                 |
| yoe_config_git_proxy                |                                                              |
| yoe_config_svn_proxy                |                                                              |
| yoe_console                         | `screen /dev/ttyUSB_${MACHINE} 115200`                       |
| yoe_create_tap_devices              | runqemu-gen-tapdevs                                          |
| yoe_feed_server                     | bitbake package-index<br />然后在ipk目录下，用http.server启动一个服务器。就是启动包管理服务器 |
| yoe_get_image_version               |                                                              |
| yoe_get_projects                    | 列出所有的项目。                                             |
| yoe_host_ip                         | 打印出host的ip地址。                                         |
| yoe_install_image                   | 烧录镜像，使用bmaptool                                       |
| yoe_remove_layer                    |                                                              |
| yoe_search_file                     | 查找文件，但是看起来没有什么用。                             |
| yoe_search_text                     | 也没有啥用                                                   |
| yoe_setup                           | 这个是第一次下载后的操作。会更新所有的git module。           |
| yoe_setup_feed_server               |                                                              |
| yoe_show_env                        | 目前只打印了一个MACHINE                                      |
| yoe_update_all                      | 更新所有的git仓库                                            |
| yoe_update_all_submodules_to_master |                                                              |

## git submodule

看.gitmodules文件里：

有16个仓库。

就相当于repo的管理了。

## conf\projects\rpi4-64\config.conf

定义了这些比较关键的变量：

| 变量                   | 说明                           |
| ---------------------- | ------------------------------ |
| MACHINE                | raspberrypi4-64                |
| DISTRO                 | yoe                            |
| YOE_PROFILE            | yoe-glibc-systemd-wayland      |
| LICENSE_FLAGS_ACCEPTED |                                |
| ENABLE_UART            | 1                              |
| ENABLE_I2C             | 1                              |
| DISABLE_RPI_BOOT_LOGO  | 1                              |
| DISABLE_SPLASH         | 1                              |
| IMAGE_FSTYPES          | wic.xz wic.bmap ext4.xz tar.xz |
| INITRAMFS_IMAGE_BUNDLE | 1                              |
| WKS_FILE               | yoe-sdimage.wks                |
| INITRAMFS_IMAGE        | yoe-initramfs-image            |
| IMAGE_BOOT_FILES       |                                |
| OBJCOPY                |                                |
| TEST_TARGET_IP         |                                |
| TEST_SERVER_IP         |                                |
| TEST_TARGET            |                                |
| IMG_VERSION            |                                |
| VC4DTBO                |                                |
|                        |                                |
|                        |                                |
|                        |                                |

## conf\projects\rpi4-64\layers.conf

| 层                |                                       |
| ----------------- | ------------------------------------- |
| meta-yoe          | 最上层                                |
| meta-raspberrypi  |                                       |
| meta-clang        |                                       |
| meta-elm-binary   | 这个是为了在recipe文件里使用elm语言。 |
| meta-qt6          |                                       |
| meta-openembedded | 下面的层都是在这个目录下              |
| meta-filesystems  |                                       |
| meta-gnome        |                                       |
| meta-initramfs    |                                       |
| meta-multimedia   |                                       |
| meta-networking   |                                       |
| meta-oe           |                                       |
| meta-perl         |                                       |
| meta-python       |                                       |
| meta-webserver    |                                       |
| meta-xfce         |                                       |
| poky/meta         | 这个是最基础的部分                    |

# 分析上面涉及到的layer

## meta-yoe

| 目录    | 说明                                                         |
| ------- | ------------------------------------------------------------ |
| classes | 增加了一个bec-image.bbclass文件，作用就是增加了systemd network的配置文件。 |
| conf    | 有一个distro目录和一个layer.conf文件。下面重点看看distro目录下的文件。里面比较重要的是yoe.inc文件。下面用一个单独的表格来分析里面的内容。 |
|         |                                                              |



yoe.inc文件

| 变量            | 说明                                        |
| --------------- | ------------------------------------------- |
| DISTRO_NAME     | Yoe Linux                                   |
| MAINTAINER      | Yoe Distro Community <http://yoedistro.org> |
| TARGET_VENDOR   | -yoe                                        |
| SDK_VENDOR      | -yoesdk                                     |
| DISTRO_VERSION  | 2023.10                                     |
| DISTRO_CODENAME | Hampshire                                   |
| SDK_NAME_PREFIX | yoe                                         |
| SDK_NAME        |                                             |
| SDKPATHINSTALL  |                                             |
| SDKEXTPATH      |                                             |
|                 |                                             |
|                 |                                             |

