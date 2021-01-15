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



# 再分析

有些童鞋可能会说，dB就是声压级的单位嘛。

对，你在网上和教科书上都能看到，分贝就是声压级的单位这样的解释。

但实际上这样的回答并不严谨，因为dB也用来表示电压和功率啊，甚至钱你也可以用dB来表示！

![image-20210115111212141](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210115111212141.png)



它们都是用分贝来做单位，但它们表示的东西是不一样啊，所以才说dB就是声压级单位这样的回答并不严谨。（ 0dBRMB=1元）

**实际上我们单独把dB拎出来，它其实不表示任何东西。**

下面是dB的含义：dB是使用对数比例系统运算，描述两个测量值比值的单位。

db是描述比值关系的。

但为什么我们要用变化量这么巨大的dB来做单位呢？

原因很简单，因为我们需要用它去描述的东西，变化范围也是非常巨大的，例如声压、电压的变化范围就非常巨大了。所以在音频或者电子领域，为了方便地计算和更好地认知这些变化。



输出信号大于输入信号时，换算出来的dB值是正数的。

表示的是输出对输入的变化倍数。

输出等于输入的时候，是0dB。

只要提到dB那它一定是一个比值，也就是拿两只数值相除，然后再做对数运算后得到的结果，所以我们才会说：dB是使用对数比例系统运算，描述两个测量值比值的单位。



首先dB值可以很方便的描述一个变化非常巨大的范围，例如音频信号的变化范围就非常巨大了，所以我们还是拿推子来举栗。我们观察一下推子的刻度，这里标注最小的数字是-60dB（负无穷先忽略），也就是说推子在从0dB刻度到-60dB刻度的变化范围是60dB。

可以查到60dB对应的变化倍数是1000倍

但有了dB刻度就不一样了，我们直接把推子推大6dB就可以了，所有经过推子的信号都会变成原来的两倍，是不是很方便呢？

**而且我们人耳对声音的感知也是呈对数形式的**，也就是说假如用对数来描述声音大小变化的话，人是会比较容易明白。

所以归纳起来，音频设备使用dB做刻度的好处有三点。

第一，可以很方便地描述一个很大的变化范围

第二，不需要知道信号的具体数值

第三，人耳比较容易感知到



好了，看了这么久，你会发现dB值，跟地图上面的比例尺有点像。

它能把一个很大的变化范围，把一个很大的数字，变成用一个比较小的数字来表示。

而且dB值是个比值，它只表示了某事物的相对变化量。

但我们很多时候遇到的dB值后面还带了其他单位啊？例如dBu 、dBV、dBSPL等等。



它们确实能表示一个具体的数值啊，例如0dBu就确实地表示0.775v的电压大小啊？这又是怎么回事？



其实这就是怎么让分贝值与固定标准值建立联系的问题了，也就是说怎么用dB来表示具体多少伏、多少瓦、甚至多少钱的问题！

其实很简单，你还是套用刚刚那两个公式。以0dBu为栗，我们把相对电平公式中，L2这个测量值换成一个固定的标准值就可以了，例如0.775V。



因此，-3dB称为“**半功率点**”。接下来，我们说说-3dB的典型应用。



这个电平的dB值和我们日常生活中说的dB响度值不太一样。

我们日常生活说的音频响度，一般来说是0~140dB(好像也有书上写是-5dB—130dB)，0是最小声，140基本上是人耳能忍受的极限。

这个响度，是响度的绝对值，有点类似于水温从0~100度这样。



而Audition里的0dB刻度，则主要是用的相对值刻度。

数字音乐里用0dB表示满刻度，即声音的最响值，**相当于把整体响度刻度基准变了。**

**这套负dB的系统，不是用来测量绝对响度的，而是用来表达相对响度。**

这是为了使录音设备工作在正常的范围内而定的标准，让输入电平保持在0dB以下，

就可以保证电路不失真或是过载，录音工程师就可能记录一个很好的干净的未失真信号。



分贝最初使用是在电信行业，

是为了**量化**长导线传输电报和电话信号时的**功率损失**而开发出来的。

是为了纪念美国电话发明家亚历山大·格雷厄姆·贝尔（Alexander Graham Bell），

以他的名字命名的。虽然分贝定义为1/10贝尔，但单位“贝尔”（Bel）却很少用。



许多波形文件编辑器的垂直标度为分贝。 没有校准或参考测量，只需一个简单的计算即可：

```
dB = 20 * log10(amplitude)
```

在这种情况下，振幅表示为0到1之间的数字，其中1表示声音文件中的最大振幅。 例如，如果您有一个16位声音文件，则振幅可以高达32767。因此，您只需将采样值除以32767。（我们使用绝对值，仅使用正数。）因此，如果您的波达到峰值 在14731，然后：



```
while (i < pcmByteArray.size) {
    // 绝对值求和
    sum += if (sampleByte == 2) {
                // 根据大小端把两个byte转换成short
                val sample = byteToShort(isBigEndian, pcmArray[i], pcmArray[i + 1])
                Math.abs(sample.toInt()).toDouble()
            } else {
                Math.abs(pcmByteArray[i].toInt()).toDouble()
            }
            i += step
    }

// 基于平均采样点，计算出db值    
return (20 * log10(sum / (pcmByteArray.size / step))).toInt()
}

```



我要计算的rms db值。

rms是均方根值。

dBm是相对于1mW的功率比，dBu和dBV是分别相对于0.775V和1V的电压比。



首先我们分别累加每个采样点的数值，除以采样个数，得到声音平均能量值。



参考资料

1、

https://zhuanlan.zhihu.com/p/89081457

2、

https://www.zhihu.com/question/413255816/answer/1399601407

3、

https://www.zhihu.com/question/41026186/answer/1191420807

4、

https://community.adobe.com/t5/audition/audio-loudness-vs-audition-s-db-meter/td-p/9593866

5、什么是分贝dB？

https://zhuanlan.zhihu.com/p/22821588

6、信号处理-如何计算音频dB电平？

https://www.itranslater.com/qa/details/2582608256623444992

7、

https://juejin.cn/post/6844903815808811016

8、通过pcm音频数据计算分贝

https://blog.csdn.net/balijinyi/article/details/80284520