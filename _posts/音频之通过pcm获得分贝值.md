---
title: 音频之通过pcm获得分贝值
date: 2018-07-11 10:53:02
tags:
	- 音频

---





Android录音时，根据PCM数据获取音量值（单位分贝）

https://blog.csdn.net/newnewfeng/article/details/50234769





https://blog.csdn.net/ywl5320/article/details/79516092

pcm编码

https://baike.baidu.com/item/pcm%E7%BC%96%E7%A0%81/10865033?fr=aladdin



PCM分析及音量控制

https://blog.csdn.net/qq_29028177/article/details/72723746

声道

https://baike.baidu.com/item/%E5%A3%B0%E9%81%93/2119484



正弦波听起来是什么声音？

是蜂鸣器的那种声音。



DTMF生成。

https://wenku.baidu.com/view/265598f7700abb68a982fb66.html



Audacity生成的1000Hz的正弦波。导出为wav文件。16bit的。时长设置位3s。得到大小位259K的文件。

```
}
hlxiong@hlxiong-VirtualBox:~/work/tmp$ ffprobe -v quiet -print_format json -show_format -show_streams 1.wav
{
    "streams": [
        {
            "index": 0,
            "codec_name": "pcm_s16le",
            "codec_long_name": "PCM signed 16-bit little-endian",
            "codec_type": "audio",
            "codec_time_base": "1/44100",
            "codec_tag_string": "[1][0][0][0]",
            "codec_tag": "0x0001",
            "sample_fmt": "s16",
            "sample_rate": "44100",
            "channels": 1,
            "bits_per_sample": 16,
            "r_frame_rate": "0/0",
            "avg_frame_rate": "0/0",
            "time_base": "1/44100",
            "duration_ts": 132300,
            "duration": "3.000000",
            "bit_rate": "705600",
            "disposition": {
                "default": 0,
                "dub": 0,
                "original": 0,
                "comment": 0,
                "lyrics": 0,
                "karaoke": 0,
                "forced": 0,
                "hearing_impaired": 0,
                "visual_impaired": 0,
                "clean_effects": 0,
                "attached_pic": 0
            }
        }
    ],
    "format": {
        "filename": "1.wav",
        "nb_streams": 1,
        "nb_programs": 0,
        "format_name": "wav",
        "format_long_name": "WAV / WAVE (Waveform Audio)",
        "duration": "3.000000",
        "size": "264644",
        "bit_rate": "705717",
        "probe_score": 99
    }
}
```



amixer用法 arecord声音录制 

http://blog.sina.com.cn/s/blog_4fc4edc00101bvsw.html

arecord 使用

https://blog.csdn.net/outstanding_yzq/article/details/8126350

音频PCM数据存储方式

https://blog.csdn.net/tanningzhong/article/details/50669340



```
[aa bb][aa bb]
声道0   声道1
pcm的存放顺序是这样的。

```



幅值和分贝关系。

计算分贝与幅度关系

https://blog.csdn.net/hehui211/article/details/47663223

生成特定分贝的音频波形

https://www.cnblogs.com/wangguchangqing/p/6197590.html

```
  dB=20∗log(A)
```



Python解析wav并画出波形。





为什么麦克风的灵敏度是负数，灵敏度－30dB和 －40dB这两个参数哪个属于高灵敏度

http://ask.zol.com.cn/q/1928758.html



-30dB表示的含义。
人耳感觉到的响度，跟声音功率的关系是对数关系。
0dB表示600欧姆负载下，输出1mW的功率。
所对应的电压是0.775V。



https://zh.wikipedia.org/wiki/%E5%88%86%E8%B2%9D





WAV文件中的数据与dB之间的关系 

http://blog.sina.com.cn/s/blog_533074eb0101dc0j.html



wav文件里存放的是电压幅值信号。只要把电压信号重现在小喇叭上，就可以逼真地重现wav文件了。

喇叭上发出的声音，其实就是驱动喇叭的电压的变化，对于pc上的数字开关喇叭，只有0和1这2种状态。

为1的时候，纸盆向外运动，为0的时候，纸盆向内回到正常位置。

但是因为纸盆有惯性，当我们给1的时候，纸盆向外运动有一个延迟，还没有达到最外面的位置，我们再给0，纸盆转而向内运动。

根据这个特性，我们通过控制喇叭向外运动的时间，就可以间接地控制纸盆运动的幅度，从而根据wav文件里的值来控制喇叭声音大小。



db和幅值的计算关系。

```
dB = 20 * log10(amplitude)
```



How can I calculate audio dB level?

https://stackoverflow.com/questions/2445756/how-can-i-calculate-audio-db-level



分贝仪。

https://www.zhihu.com/question/39070608

手机上也可以用软件来测试。



计算wav文件的rms。

https://rosettacode.org/wiki/Averages/Root_mean_square#Python

