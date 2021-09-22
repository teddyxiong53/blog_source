---
title: npu之nemo
date: 2021-09-17 14:45:33
tags:
	- npu

---

--

现在研究机器学习在音频上的应用。发现nemo是个好工具，把这些相关的课题都集中起来了。

看看怎么使用Jasper模型来进行ASR识别。

nemo支持中文语音的训练。

nemo的数据层可以跟kaldi兼容。

预训练的模型打包为后缀名为.nemo的文件，包含了pytorch checkpoint。



关于ASR经常被问到的一些问题

```
有没有方法在nemo里添加领域相关的词汇？

Quartznet和Jasper都是基于字符的。提供的预训练模型，输出小写的英文字母。

用户可以重新进行训练，使用一个包含大写字母和标点符号的字典。

nemo目录支持哪些语言？

几种广泛使用的语言都支持了。
```

下载代码：

```
git clone https://github.com/NVIDIA/NeMo
```

然后创建一个虚拟Python环境，并激活。

安装依赖：

```
cd NeMo
./reinstall.sh
```

安装需要一段时间。



先想办法跑起来。

看asr的例子。

speech_to_label.py  不带参数，运行看看。

```
[NeMo W 2021-09-17 15:34:32 optimizers:47] Apex was not found. Using the lamb optimizer will error out.
[NeMo W 2021-09-17 15:34:44 experimental:28] Module <class 'nemo.collections.asr.data.audio_to_text_dali._AudioTextDALIDataset'> is experimental, not ready for production and is not fully supported. Use at your own risk.
[NeMo I 2021-09-17 15:34:45 speech_to_label:127] Hydra config: name: MatchboxNet-3x1x64-v1
```

从后门的打印看，这个就是谷歌的那30个单词的分类。

这个也被分类到ASR里了。不过无所谓。

```
GPU available: False, used: False
TPU available: False, using: 0 TPU cores
IPU available: False, using: 0 IPUs
```

最后是出错了。

是需要带参数的，打开speech_to_label.py看看。

里面的注释部分写的很详细。

任务1是speech command。

首先要准备dataset。

要使用process_speech_commands_data.py这个脚本。

这个脚本的用法是：

```
python process_speech_commands_data.py \
    --data_root=<absolute path to where the data should be stored> \
    --data_version=<either 1 or 2, indicating version of the dataset> \
    --class_split=<either "all" or "sub", indicates whether all 30/35 classes should be used, or the 10+2 split should be used> \
    --rebalance \
    --log
```

对应的下载地址是：

```
URL_v1 = "http://download.tensorflow.org/data/speech_commands_v0.01.tar.gz"
URL_v2 = "http://download.tensorflow.org/data/speech_commands_v0.02.tar.gz"
```

这个数据还是很大的。

但是我现在并不想训练，我只是想进行预测而已。

不用下载这个数据吧。

但是speech_to_label.py里就是一个训练的逻辑。

那就不看这个文件。

speech_to_text_infer.py这个才是预测用的。

这个脚本可以使用的参数有：

```
--asr-model
	默认值是QuartzNet15x5Base-En
--dataset
	评估数据。

```

还有一个vad_infer.py的脚本



nemo的主要设计目的就是进行简化训练的。



这样来使用预训练的模型。

```
import nemo.collections.asr as nemo_asr

model = nemo_asr.models.EncDecCTCModel.from_pretrained(model_name="QuartzNet15x5Base-En")
```

这样会自动下载nemo文件放到下面的目录里：

```
~/.cache/torch/NeMo/NeMo_1.3.0/QuartzNet15x5Base-En/
```



参考资料

1、

