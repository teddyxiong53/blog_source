---
title: lvgl之lvgl-pad项目记录
date: 2024-05-01 08:38:49
tags:
	- lvgl

---

--

# 5月1日

## 先搭建开发运行环境

都在虚拟机下运行。

虚拟机用virtualbox。

虚拟机系统用lubuntu。没有用过lxde这个桌面系统。

比较小巧的系统我都愿意尝试一下。



然后把lvgl linux framebuffer的 环境跑起来。

https://github.com/lvgl/lv_port_linux_frame_buffer

看这个项目已经更新到lvglv9版本。所以也是一直在跟进lvgl版本的。

这个是官方的移植。

fb的移植细节看这篇博客。

https://blog.lvgl.io/2018-01-03/linux_fb

帧缓冲器设备是一个非常低级的界面，用于在屏幕上显示某些内容。说到嵌入式 GUI，直接使用帧缓冲区而不是窗口管理器有几个原因：

简单 只需将像素写入内存

快速 没有窗口管理器，这意味着快速启动和更少的开销

便携式 独立于发行版，每个 Linux 系统都有一个帧缓冲器设备，因此它与所有系统兼容

我还是用vscode 仿真的方式。

https://github.com/lvgl/lv_port_pc_vscode

这个已经跑起来了。

靠fitten code这个ai插件配合阅读一下代码。

## 直接使用图片

在Linux下使用lvgl时，可以直接从文件系统加载资源而不是将资源转换为数组。LVGL提供了文件系统支持，使您可以加载图像、字体和样式表等资源，而无需将它们转换为数组。

以下是加载资源的一般步骤：

为资源创建目录：在您的项目中创建一个目录，用于存放LVGL所需的资源文件，如图像文件（.png、.jpg）、字体文件（.ttf）等。

初始化文件系统驱动：在LVGL中，您可以选择使用不同的文件系统驱动，根据您的实际需求选择合适的驱动，比如使用标准C库函数作为文件系统驱动（LV_USE_FS_STDIO），或者使用POSIX文件系统驱动（LV_USE_FS_POSIX）等。根据您的选择，初始化相应的文件系统驱动。

加载资源：使用LVGL提供的函数从文件系统加载资源，比如使用 lv_img_create_from_file 加载图像，使用 lv_font_load 加载字体等。通过指定资源文件的路径，LVGL可以在运行时从文件系统中读取所需资源。

下面是一个简单的示例，演示了如何在LVGL中从文件系统加载图像：

// 初始化文件系统驱动

```
lv_fs_drv_t my_fs_drv;
lv_fs_drv_init(&my_fs_drv);
lv_fs_drv_register(&my_fs_drv, "/");
```

```
// 加载图像
lv_obj_t * img1 = lv_img_create(lv_scr_act(), NULL); // 创建图像对象
lv_img_set_src(img1, "S:/path_to_your_image/image.png"); // 从文件系统加载图像
```


总结：通过使用LVGL提供的文件系统支持功能，您可以在Linux下使用LVGL，并直接从文件系统加载资源而不是将资源转换为数组。

lv_img_set_src有自动识别能力，因为传递的第二个参数是void *的，内部会解析这个是不是ascii字符串，如果是，说明是文件路径。

## 直接使用字体

是的，LVGL允许您从文件系统中加载字体文件，而不必将字体文件转换为数组。您可以通过使用LVGL提供的函数，从文件系统加载字体文件并在应用中使用它们。

以下是一个简单的示例，演示了如何在LVGL中从文件系统加载字体文件：

// 初始化文件系统驱动
lv_fs_drv_t my_fs_drv;
lv_fs_drv_init(&my_fs_drv);
lv_fs_drv_register(&my_fs_drv, "/");

// 加载字体
lv_font_t * my_font = lv_font_load("S:/path_to_your_font/font.ttf"); // 从文件系统加载字体

// 创建文本对象并应用加载的字体
lv_obj_t * label = lv_label_create(lv_scr_act(), NULL);
lv_label_set_text(label, "Hello, LVGL!");
lv_obj_set_x(label, 50);
lv_obj_set_y(label, 20);
lv_obj_set_style_local_text_font(label, LV_LABEL_PART_MAIN, LV_STATE_DEFAULT, my_font); // 应用加载的字体
上述示例中，lv_font_load 函数用于从文件系统加载字体文件，并将其分配给指针 my_font。然后，创建了一个文本对象，通过 lv_obj_set_style_local_text_font 函数应用了加载的字体。

总结：LVGL允许您在Linux下使用文件系统加载字体文件，并在应用中直接使用它们，而不必将字体文件转换为数组。

## 把lvgl vscode sim的看了一下

我觉得可以做2个改造：

1、把lvgl的代码直接内置。

2、把cmake的改成xmake的。

先实现当前的效果再说。

## 看一下把C函数转成lua接口函数的方式

https://github.com/FASTSHIFT/C2Lua

先把这个代码逻辑看一下。

