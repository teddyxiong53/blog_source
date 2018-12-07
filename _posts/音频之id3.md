---
title: 音频之id3
date: 2018-12-06 09:45:28
tags:
	- 音频
typora-root-url: ..\
---



# 什么是ID3

id3是位于一个mp3文件的开头或者末尾的信息。

包含了这个文件的：

1、歌手。

2、标题。

3、专辑名称。

4、年代。

5、风格。



有2个版本，v1和v2。

v1版本是在mp3文件的末尾128个字节。

以TAG这3个字符开头。

v2版本，则放在了开头。增加了歌词，图片这种大容量信息。



id3是一种metadata容器。



v1版本是1996年发明的。

流派定义了79种。winamp这个软件扩展到了125中。

但是国内用户基本不关注流派信息。

v1版本放在末尾，有个明显问题，就是通过流媒体的方式进行收听的时候，开始是拿不到末尾的信息的。

在1997年，做了一个小是改进，升级为1.1版本。就是增加了曲目序号。用了一个字节，考虑到一张专辑里的歌曲几乎不肯超过255首，所以够用了。

C语言的定义是这样：

```
char Title[30];
char Artist[30];
char Album[30];
char Year[4];
char Comment[30];
char Genre;
```



v2版本有4个子版本，但是用得多是就是2.3的。



# python获取id3信息

先安装依赖库。

```
sudo pip install mutagen
```

也可以直接分析文件内容。

```
def getID3(filename):
	fp = open(filename, 'r')
	fp.seek(-128, 2)
 
	fp.read(3) # TAG iniziale
	title	= fp.read(30)
	artist	= fp.read(30)
	album	= fp.read(30)
	anno	= fp.read(4)
	comment = fp.read(28)
	 
	fp.close()
 
	return {'title':title, 'artist':artist, 'album':album, 'anno':anno}
	
print getID3("1.mp3")
```



参考资料

1、ID3

https://baike.baidu.com/item/ID3/1196982?fr=aladdin



