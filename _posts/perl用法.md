---
title: perl用法
date: 2021-05-11 20:04:34
tags:
	- perl
---

--

看京东shell脚本里，有不少的字符串处理是用perl来完成的。

perl作为一门语言，我是不太想投入精力去学习的。

所以，就把perl当成sed这样的字符串处理工具来学习一些常用的用法。

基本用法

```
Usage: perl [switches] [--] [programfile] [arguments]
```



perl字符串处理还是非常牛逼的。

我现在有这样一个需求：

这个需求就是多行字符串替换。

```
src_str="
static int aml_lcd_extern_add_mipi(struct aml_lcd_extern_driver_s *ext_drv)
{
"
dst_str="
static int aml_lcd_extern_add_mipi(struct aml_lcd_extern_driver_s *ext_drv)
{
	int result = -1;
	result = aml_lcd_extern_mipi_yy1821_probe(ext_drv);
	return result;
"
```

把src_str替换为dst_str。

用下面的就可以实现。

```
perl -i -p0e 's/static int aml_lcd_extern_add_mipi.*?{/static int aml_lcd_extern_add_mipi(struct aml_lcd_extern_driver_s *ext_drv){int result = -1;result = aml_lcd_extern_mipi_yy1821_probe(ext_drv);return result;/s' test.txt
```



参考资料

1、

https://unix.stackexchange.com/questions/181180/replace-multiline-string-in-files