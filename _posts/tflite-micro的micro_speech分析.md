---
title: tflite-micro的micro_speech分析
date: 2021-09-26 14:53:33
tags:
	- npu

---

--

这个例子跟我的应用场景很接近，所以值得深入分析。

我进行本地的训练。在colab上是训练不了的。

下载数据集。之前下载了train.zip。1.3G。

我放在这里：

```
/home/amlogic/jupyter_work/audio_classify/train
```

下面有这些子目录：

```
bed  bird  cat  dog  down  eight  five  four  go  happy  house  left  marvin  nine  no  off  on  one  right  seven  sheila  six  stop  three  tree  two  up  wow  yes  zero
```

先要有一个验证环境。

micro_speech带了一个可以识别yes/no的tflite模型。

先把这个模型用起来。可以用espeak来进行测试。



还是直接根据这个说明来做。

https://www.tensorflow.org/tutorials/audio/simple_audio

下载的是mini_speech的数据，只有174M。

里面就这8个单词的

```
down  go  left  no    right  stop  up  yes
```

总共8000个文件，每个单词1000个文件。

按8:1:1来划分数据集。

epoch设置为10，看看在笔记本上用CPU训练要多久。也就1分钟左右。

数据量确实很小。

训练后的准确率在85%左右。

直接把simple_audio里的代码按顺序粘贴到jupyter里运行，依次执行，很顺利，也很快。

我把模型保存出来。然后另外写一个jupyter来进行预测。

```
!mkdir saved_model
model.save('saved_model/my_model')
```



保存的文件是这样：

```
amlogic@amlogic-BAD-INDEX:~/jupyter_work/saved_model$ tree -h
.
└── [4.0K]  my_model
    ├── [4.0K]  assets
    ├── [173K]  saved_model.pb
    └── [4.0K]  variables
        ├── [ 19M]  variables.data-00000-of-00001
        └── [2.4K]  variables.index
```

模型文件173K。

