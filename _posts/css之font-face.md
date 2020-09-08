---
title: css之font-face
date: 2020-09-05 11:22:17
tags:
	- css

---

1

主要作用是，网页上使用的字体，在用户的电脑上可能没有。

如果没有font-face机制，那么某些字体在用户的浏览器上就显示不出来。严重影响使用体验。

既然客户电脑上没有我们用的字体，那么我们把字体放在服务器上，用户用到对应的字体时，引用我们服务器上的字体文件不就好了。

除了这个作用，font-face还有一个作用，就是对字体名字进行简写。

相当于起别名。

```
@font-face {
　　font-family: 'YT';   /*声明一个名为yt的字体变量*/
　　src: url('YourWebFontName.eot')，local('YourFontName.eot');
}然后在任何需要使用YT字体的地方就可以直接使用以下：
h1{font-family:YT;}
```

不同浏览器使用的字体文件格式不同。

为了兼容主流的浏览器。需要把所欲浏览器的都兼顾到。

浏览器可以分为3大类：

1、火狐。用ttf或otf格式。

2、chrome。用svg格式。

3、IE。用eot格式。

所以一个完整的是这样写：

```
@font-face {
font-family: 'YourWebFontName';
src: url('YourWebFontName.eot'); /* IE9 Compat Modes */
src: url('YourWebFontName.eot?#iefix') format('embedded-opentype'), /* IE6-IE8 */
         url('YourWebFontName.woff') format('woff'), /* Modern Browsers */
         url('YourWebFontName.ttf')  format('truetype'), /* Safari, Android, iOS */
         url('YourWebFontName.svg#YourWebFontName') format('svg'); /* Legacy iOS */
}
```





参考资料

1、浅谈@font-face

https://www.cnblogs.com/liAnran/p/11606977.html