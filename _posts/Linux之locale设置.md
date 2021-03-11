---
title: Linux之locale设置
date: 2021-03-11 17:37:51
tags:
	- Linux

---

--

LC_CALL=C

在很多的shell脚本中，我们经常会看见某一句命令的前面有一句“LC_ALL=C”

SAR_CMD="LC_ALL=C sar -u -b 1 5 | grep -i average "

这到底是什么意思？

LC_ALL=C 是为了去除所有本地化的设置，让命令能正确执行。



在Linux中通过locale来设置程序运行的不同语言环境，

locale由ANSI C提供支持。

locale的命名规则为<语言>_<地区>.<字符集编码>，

如zh_CN.UTF-8，zh代表中文，CN代表大陆地区，UTF-8表示字符集。



在locale环境中，有一组变量，代表国际化环境中的不同设置：

1.    LC_COLLATE
定义该环境的排序和比较规则

2.    LC_CTYPE
用于字符分类和字符串处理，控制所有字符的处理方式，包括字符编码，字符是单字节还是多字节，如何打印等。是最重要的一个环境变量。

3.    LC_MONETARY
货币格式

4.    LC_NUMERIC
非货币的数字显示格式

5.    LC_TIME
时间和日期格式

6.    LC_MESSAGES
提示信息的语言。另外还有一个LANGUAGE参数，它与LC_MESSAGES相似，但如果该参数一旦设置，则LC_MESSAGES参数就会失效。LANGUAGE参数可同时设置多种语言信息，如LANGUANE="zh_CN.GB18030:zh_CN.GB2312:zh_CN"。

7.    LANG
LC_*的默认值，是最低级别的设置，如果LC_*没有设置，则使用该值。类似于 LC_ALL。

8.    LC_ALL
它是一个宏，如果该值设置了，则该值会覆盖所有LC_*的设置值。注意，LANG的值不受该宏影响。

"C"是系统默认的locale，"POSIX"是"C"的别名。所以当我们新安装完一个系统时，默认的locale就是C或POSIX。



```
locale的设定：   
LC_ALL和LANG优先级的关系： LC_ALL > LC_* >LANG   
1、如果需要一个纯中文的系统的话，设定LC_ALL= zh_CN.XXXX，或者LANG=zh_CN.XXXX都可以。  
2、如果只想要一个可以输入中文的环境，而保持菜单、标题，系统信息等等为英文界面，那么只需要设定 LC_CTYPE＝zh_CN.XXXX，LANG=en_US.XXXX就可以了。  
3、假如什么也不做的话，也就是LC_ALL，LANG和LC_*均不指定特定值的话，系统将采用POSIX作为lcoale，也就是C locale。  
LANG和LANGUAGE的区别：   
LANG - Specifies the default locale for all unset locale variables  
LANGUAGE - Most programs use this for the language of its interface  
LANGUAGE是设置应用程序的界面语言。而LANG是优先级很低的一个变量，它指定所有与locale有关的变量的默认值  
```



参考资料

1、

https://www.cnblogs.com/wajika/p/6592659.html