---
title: markdown转word加页眉和水印
date: 2022-05-19 17:20:01
tags:

	- markdown

---

--

md2pdf这个不行。太简单，不支持加水印等操作。

使用typora先将markdown转为html格式， 然后再使用wkhtmltopdf 工具将html文件转换为最终的pdf格式，并添加页眉页脚以及水印等信息。

```
wkhtmltopdf http://google.com google.pdf
```

wkhtmltopdf安装不成功。



查看ubuntu安装的字体有哪些

```
fc-list :lang=zh
```

```sh
#!/bin/sh
message1="请输入正确格式，如：./genpdf.sh <srcfile> <buildname>"
message2="例如文件：./genpdf.sh README.md readme"
message3="例如目录：./genpdf.sh anasinc/department/ depart"
if [ $# -eq 0 ]       ##判断参数是否存在
then
    echo $message1
    echo $message2
    echo $message3
    exit                     ##不存在退出
fi
if [ x$1 = x ]       ##判断参数1是否存在
then
    echo $message1
    echo $message2
    echo $message3
    exit                     ##不存在退出
fi
if [ x$2 = x ]       ##判断参数2是否存在
then
    echo $message1
    echo $message2
    echo $message3
    exit                     ##不存在退出
fi
srcfile=$1
buildname=$2
currentdir=$(pwd)

if [ -d $1 ]
then
    # 如果源文件参数是目录，则获取目录下所有.md文档
    cd $1
    srcfile=$(ls | sed "s:^:`pwd`/:")
fi

echo $srcfile

cd $currentdir

pandoc -N  --variable fontsize=12pt ${srcfile} --latex-engine=xelatex --toc -o build/${buildname}.pdf --highlight-style kate -V mainfont="宋体 CN" -V sansfont="宋体 CN" -V monofont="宋体 CN"

```



```
./genpdf.sh ./第一章_数学基础.md 1.pdf
```

这个md比较复杂，有很多公式，转换失败了。

换一个简单的。

需要手动创建build目录。

可以转换成功。但是格式全是乱的。

这条路走不通。



参考资料

1、

这个有操作性。脚本都给了。

https://romantic-hoover-f991f1.netlify.app/study/markdown2pdf/

2、

https://zcong1993.github.io/md2pdf/#/zh/

3、

https://segmentfault.com/a/1190000018988358