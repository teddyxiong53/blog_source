---
title: 音频之wav文件头部分析
date: 2019-12-13 16:37:25
tags:
	- 音频

---

1

头部一共44个字节：

```
00到03：
	RIFF 这4个字符。
04到07
	int类型。文件长度。
08到0B
	WAVE这4个字符。
0C到0F
	fmt这3个字符，后面是一个空格。
10到13
	保留。但是看结构体里的名字，是fmt的size。目前看到是1 。
14到15
	2个字节。表示格式。1表示pcm
16到17
	2个字节。通道数。2或者1
18到1b
	4个字节，采样率。48000这样的数。
1c到1f
	4字节。传输速率。=ch * bit * sample_rate/8 = 2 * 16 * 48000/8 = 192000 
	播放软件根据这个值来估算buffer的大小。
20到21
	2字节。目前我在文件里看到的是04 。数据块的调整数。= ch * bit /8 = 2*16/8 = 4，对的上。
22到23
	2字节。采用位数。16位的。
24到27
	4字节。data这4个字符。
28到2b
	4字节。音频数据的长度。
```

在tinyalsa里，对应的结构体是：

```
struct wav_header {
    uint32_t riff_id;
    uint32_t riff_sz;
    uint32_t riff_fmt;
    uint32_t fmt_id;
    uint32_t fmt_sz;
    uint16_t audio_format;
    uint16_t num_channels;
    uint32_t sample_rate;
    uint32_t byte_rate;
    uint16_t block_align;
    uint16_t bits_per_sample;
    uint32_t data_id;
    uint32_t data_sz;
};
```



参考资料

1、wav文件头分析

https://blog.csdn.net/xieyanyi1/article/details/48207663