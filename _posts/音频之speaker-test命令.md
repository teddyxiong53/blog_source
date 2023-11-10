---
title: 音频之speaker-test命令
date: 2019-05-16 15:38:11
tags:
	- 音频
---



--

这个也是alsa utils的一个。

基本格式：

```
speaker-test [options] ...
```

选项：

```
-D, --device
	指定设备。
-r, --rate
	指定频率，单位hz。
-c, --channels
	指定通道数。
-f, --frequency
	指定频率。
-F, --format
	指定格式。
-b, --buffer
	us为单位。ring buffer的大小。
-p, --period
	us为单位。period的单位。
-P, --nperiods
	周期数。
-t, --test
	可以是sine和pink、wav。
-l, --nloops
	指定测试周期。0表示无限。
-s, --speaker
	单喇叭测试。1表示left，2表示right。
-w, --wavfile
	在-t后面是wav时，要加上这个参数来指定播放哪个wav文件。
-W, --wavdir
	指向一个包含wav文件的目录。
-m, --chmap
	指定通道映射。
-S, --scale
	指定百分比，默认80。
	
```



# 测试soundbar

现在有一个8声道的soundbar。

```
speaker-test -t pink -c 8
```

最大支持16通道。

```
static const char *const channel_name[MAX_CHANNELS] = {
  /*  0 */ N_("Front Left"),
  /*  1 */ N_("Front Right"),
  /*  2 */ N_("Rear Left"),
  /*  3 */ N_("Rear Right"),
  /*  4 */ N_("Center"),
  /*  5 */ N_("LFE"),
  /*  6 */ N_("Side Left"),
  /*  7 */ N_("Side Right"),
  /*  8 */ N_("Channel 9"),
  /*  9 */ N_("Channel 10"),
  /* 10 */ N_("Channel 11"),
  /* 11 */ N_("Channel 12"),
  /* 12 */ N_("Channel 13"),
  /* 13 */ N_("Channel 14"),
  /* 14 */ N_("Channel 15"),
  /* 15 */ N_("Channel 16")
};
```

是怎么把声音输出到对应的喇叭上的？

我把时间设置长一点，8秒。方便我插拔对应的喇叭线。

当前的default声卡指向了哪个？

就是喇叭这个tdmc的。hw02的。

speaker-test怎么设置从不同的喇叭输出的？

加上-d，表示debug。

-s表示测试指定的喇叭。从0开始编号。

我是通过hdmi线，把soundbar连接到ubuntu电脑，在音频设置那里，输出设备选择为hdmi的时候，可以看到有3个hdmi输出配置可选。

分别是：

stereo

5.1

7.1

这个应该就是edid的配置信息。

而且都不用speaker-test，直接点test就有图形界面的测试。很直观的。

点击left的时候，串口打印

```
# [13628.516882@2]- id=1 set inskew=2
[13628.518083@2]- audio_ddr_mngr: toddrs[0] registered by device ff642000.audiobus:tdmb
[13628.522342@2]- aml_set_tdm_mclk:set mpll_freq: 24576000
[13628.527507@2]- aml_set_tdm_mclk:set mpll_freq: 24576000
[13628.532806@2]- asoc-aml-card auge_sound: tdm prepare capture
[13628.538483@0]- asoc-aml-card auge_sound: TDM[1] Capture enable
[13628.676583@2]- Not init audio effects
[13628.676871@1]- audio_ddr_mngr: frddrs[0] registered by device ff642000.audiobus:tdmc
[13628.684008@1]- aml_set_tdm_mclk:set mpll_freq: 24576000
[13628.687703@1]- aml_set_tdm_mclk:set mpll_freq: 24576000
[13628.717611@2]- asoc-aml-card auge_sound: TDM[2] Playback enable
```

点击right的时候，打印

```
# [13666.681589@1]- id=1 set inskew=2
[13666.682467@1]- audio_ddr_mngr: toddrs[0] registered by device ff642000.audiobus:tdmb
[13666.687181@1]- aml_set_tdm_mclk:set mpll_freq: 24576000
[13666.692239@1]- aml_set_tdm_mclk:set mpll_freq: 24576000
[13666.697483@1]- asoc-aml-card auge_sound: tdm prepare capture
[13666.703267@0]- asoc-aml-card auge_sound: TDM[1] Capture enable
[13666.841518@0]- Not init audio effects
[13666.841824@3]- audio_ddr_mngr: frddrs[0] registered by device ff642000.audiobus:tdmc
[13666.849019@3]- aml_set_tdm_mclk:set mpll_freq: 24576000
[13666.852593@3]- aml_set_tdm_mclk:set mpll_freq: 24576000
[13666.881666@1]- asoc-aml-card auge_sound: TDM[2] Playback enable
```

串口打印没有什么不同。

用speaker-test来测试不同的喇叭。

```
speaker-test -t pink -c 8 -s 7
```

改变最后的一个喇叭编号就可以了。

如果要同时播放多个的，那就写多条命令后台执行。

测试了可以。不会出现打开失败的。

这个命令可以自动依次测试8个喇叭。就是播报单词。

```
speaker-test -t wav -c 8
```

# 测试命令大全

speaker-test是一个用于测试音频输出设备（如扬声器）的命令行工具。下面是一些speaker-test的常用测试命令的示例，以尽可能全面地展示其功能：

1. 测试默认声道和采样率：
   ````
   speaker-test -t wav
   ```

2. 测试指定声道和采样率：
   ````
   speaker-test -c 2 -r 48000
   ```

3. 测试指定声道、采样率和持续时间：
   ````
   speaker-test -c 6 -r 44100 -l 10
   ```

4. 测试左声道：
   ````
   speaker-test -c 1 -l 1 -twav -lwav/left.wav
   ```

5. 测试右声道：
   ````
   speaker-test -c 1 -l 1 -twav -rwav/right.wav
   ```

6. 测试立体声：
   ````
   speaker-test -c 2 -l 1 -twav -lwav/left.wav -rwav/right.wav
   ```

7. 测试环绕声（5.1声道）：
   ````
   speaker-test -c 6 -l 1 -twav -cwav/front_left.wav -lwav/front_right.wav -rwav/rear_right.wav -lwav/rear_left.wav -swav/center.wav -swav/lfe.wav
   ```

8. 测试指定设备编号：
   ````
   speaker-test -D sysdefault:CARD=1
   ```

9. 测试指定设备名称：
   ````
   speaker-test -D hw:0,0
   ```

这些命令示例可以帮助您进行不同设置和配置的音频输出设备测试。请注意，具体命令可能因系统配置和硬件支持而有所变化，请根据您的实际环境和需求进行相应的调整。