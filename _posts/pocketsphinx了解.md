---
title: pocketsphinx了解
date: 2017-11-20 21:28:20
tags:
	- pocketsphinx

---



官方帮助信息在这：https://cmusphinx.github.io/wiki/tutorial/

# 1. 叮当里如何使用的sphinx

sphinx是一个stt引擎。

叮当里的写法值得学习。为了对接不同的stt引擎。写了一个抽象类AbstractSTTEngine。其他的具体引擎都是继承了这个类。

AbstractSTTEngine一共7个方法：

```
1、get_config。
2、get_instance
3、get_passive_instance
4、get_active_instance
5、get_music_instance。get instance这几个函数都是差不多的。
6、is_available
7、transcribe（转录的意思，把语音转成文字）

```

我们再看PocketSphinxSTT这个类做了些什么？

```
首先是__init__和__del__函数。先不管。
1、get_config函数。
	想要从profile.yml里得到hmm_dir这个参数，但是实际上我们没有配置。
	这样不报错。
	看构造函数里的参数，就有这么一个，是在hmm_dir="/usr/local/share/" +
                 "pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k"
2、is_available
	这个就是检查了这个Python模块是否存在。
就覆盖上面这2个接口。

```

上面那个hmm_dir目录下的内容是这样的：

```
pi@raspberrypi:/usr/local/share/pocketsphinx/model/hmm/en_US/hub4wsj_sc_8k$ ls -lh
total 5.0M
-rw-r--r-- 1 root staff  186 Nov 16 16:29 feat.params
-rw-r--r-- 1 root staff 3.0M Nov 16 16:29 mdef
-rw-r--r-- 1 root staff  40K Nov 16 16:29 means
-rw-r--r-- 1 root staff  411 Nov 16 16:29 noisedict
-rw-r--r-- 1 root staff 1.9M Nov 16 16:29 sendump
-rw-r--r-- 1 root staff 2.5K Nov 16 16:29 transition_matrices
-rw-r--r-- 1 root staff  40K Nov 16 16:29 variances
```

这些文件的说明在这里：https://cmusphinx.github.io/wiki/acousticmodelformat/

这个页面说的是声学模型格式。

```
1、只支持三音素的上下文。
后面的看不太懂。先忽略。
```

构造函数里，这一步是比较重要的。

```
self._decoder = ps.Decoder(hmm=hmm_dir, logfn=self._logfile,
                                   **vocabulary.decoder_kwargs)
```

ps是import PocketSphinx as ps得到的。

Decoder是一个重要的类。

我们理一下sphinx被构造的过程：

```
1、dingdang.py的构造函数里：
self.mic = Mic(
            self.config,
            tts_engine_class.get_instance(),
            stt_passive_engine_class.get_passive_instance(),
            stt_engine_class.get_active_instance())
stt_passive_engine_class.get_passive_instance()这里。
这个函数抽象类统一实现的。sphinx没有进行覆盖。
这个函数：
{
	输入：cls。
	处理：从static/keyword_phrases文件里取得内容，里面就是10来个单词，是be、with这些简单单词。
		然后调用cls的get_instance函数。
	输出：返回cls的get_instance函数的结果。
}
2、get_instance函数。
	这个很重要。这个里面构造了对应的子类的cls。
	返回的就是类的实例。
```

上面说完了sphinx的构造。然后我们看sphinx如何进行监听行为的。

是在mic.py里的passiveListen函数里。这个函数被死循环调用。

passiveListen函数：

```
实际上是先录音，再分析录音文件。
过程里是一个录音文件的处理过程。先不细看。
```

之后是调用到sphinx的transcribe函数：

```
传递进来的是一个wav文件，要跳过前面44字节的头部。后面就是纯数据了。
data = fp.read()
self._decoder.start_utt()
self._decoder.process_raw(data, False, True)
self._decoder.end_utt()

result = self._decoder.get_hyp()
```



