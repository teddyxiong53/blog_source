---
title: 微信开发之订阅号获取一个新的ssr端口
date: 2020-04-29 22:05:22
tags:		
	- 微信

---

1

有个服务器用来翻墙，但是端口用不了几天，就会被封掉。ip是不会被封掉的。

所以每次换一个端口号，就能正常使用，但是修改端口号，需要登录到服务器执行几条命令，也比较麻烦。

所以想要用手机点击一下就可以获取一个修改后的端口。

开始我是打算用python来做的。

架构是这样：

```
手机安装qpython
服务器上安装mqtt服务器
通过手机发布mqtt消息，触发服务器执行脚本，执行完之后，把新的ssr连接回复过来。
```

这种方式从技术上来说没有什么问题。

但是如果我要把这个功能分享给其他人用，就不是很方便。

最方便的，肯定是跟微信结合。这样不需要安装新的软件，通过按钮或者发消息的方式来获取，使用起来也很方便。

我之前注册了订阅号，因为长时间没有使用，所以都被自动注销了，重新激活。

服务器，用nodejs写微信公众号后台程序。

代码就是这个样子。当前这样可以返回当前的目录信息。验证通路是通的。

```javascript
const express = require('express');
var wechat = require('wechat');
var spawn = require('child_process').spawnSync;

const app = express();
var config = {
    token: '',
    appid: '', 
    encodingAESKey: '', 
    checkSignature: false 
};
app.use(express.query());
app.use('/', wechat(config, function (req, res, next) {
        var result = spawn('ls', ['-l'])
        var out = result.stdout
        res.reply({
                    content: out,
                    type: 'text'
                                    });
}));
const port = 80;
app.listen(port);
console.log(`Server listening at :${port}`);
```

接下来，我需要把上面执行的ls操作替换成我的脚本就好了。

接下来就是写bash脚本。

这个就需要把当前ssrmu.sh这个脚本的逻辑看懂。基于这个修改一个简易版本出来。

调用的ssr代码都在/usr/local/shadowsocksr目录下。

mujson_mgr.py这个脚本就是进行用户管理的。

下面这样，是列出当前的用户。

```
python mujson_mgr.py -l
```

查看这个脚本的帮助信息。

```
-a 添加并编辑用户
-d 删除用户
-e 编辑用户

-u name 指定用户名字
-p port 指定端口号
-k password 指定密码

```

够用了。我就用这几个选项应该可以了。

在ssrmu.sh里，添加用户是Modify_Config这个函数处理。

Add_port_user

```
match_add=$(python mujson_mgr.py -a -u "${ssr_user}" -p "${ssr_port}" -k "${ssr_password}" -m "${ssr_method}" -O "${ssr_protocol}" -G "${ssr_protocol_param}" -o "${ssr_obfs}" -s "${ssr_speed_limit_per_con}" -S "${ssr_speed_limit_per_user}" -t "${ssr_transfer}" -f "${ssr_forbid}"|grep -w "add user info")
```

应该是执行这一句就可以添加用户了。

试一下。下面的命令可用。

```
python mujson_mgr.py -a -u "xxx" -p "20000" -k "88889999" -m "aes-128-ctr" -O "auth_aes128_md5" -G "" -o "plain" 
```

信息是存储在mudb.json里。

执行后不需要重启，直接就可以用的。



其他的流程都通了。发现设置香港服务器为微信的url，会设置不超过，提示url超时。

是因为我的这个服务器，没有把80端口加入到防火墙的安全组里，加入了就好了。

现在流程都通了。基本功能已经实现。

接下来看看wechat这个模块的代码。完善一下功能。



微信官方的例子是用python给出来的。

相比于js，python我可能算是用得更加顺手一点，所以，就用python来做算了。

把默认的python版本配置为python3，Ubuntu16.04的默认的python3版本是3.5。

用flask来做webapp。

安装：

```
python -m pip install flask
```

新建一个server.py。写入下面的内容。

```
from flask import Flask
from flask import request

import hashlib
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        token = 'XXX' #这里填入你在微信后台填的token
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr','')
        list = [token, timestamp, nonce]
        list.sort()
        s = list[0] + list[1] + list[2]
        hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        print("hascode:{}, signature:{}".format(hashcode, signature))
        if hashcode == signature:
            return echostr
        else:
            return ''

```

执行：

```
export FLASK_APP=server.py
flask run
```

然后微信后台，填入我们的服务器地址，token等内容，进行设置，可以看到设置成功。

微信会往我们的服务器的80端口发送一个请求，让我们验证后返回结果给它。这样来验证我们服务器是否可用。

上面的代码运行正常，可以在服务器控制台看到下面这样的打印：

```
203.205.219.188 - - [02/May/2020 11:21:33] "GET /?signature=xxx&echostr=xx&timestamp=1588389729&nonce=1344242655 HTTP/1.0" 200 -
```



当用户向我们的公众号发消息的时候，微信服务器会把消息组织成xml格式，post到我们的服务器地址上。

消息分类：

```
文本  text
图片  image
语音  voice
视频  video
小视频 shortvideo
地理位置  location
链接  link
```

我们先看微信文本自动回复的。

文本消息的xml格式是这样：

```
<xml>
	<ToUserName></ToUserName>
	<FromUserName>
	<CreateTime>
	<MsgType>
	<Conten>
	<MsgId>
</xml>
```

我们需要在python代码里做的，就是解析这个xml数据。

```
from flask import Flask
from flask import request
from mytemplate import reply_template
import time
import xml.etree.cElementTree as et

import hashlib
app = Flask(__name__)
app.debug = True

@app.route('/', methods=['GET', 'POST'])
def wechat():
    if request.method == 'GET':
        token = 'xiong'
        data = request.args
        signature = data.get('signature','')
        timestamp = data.get('timestamp', '')
        nonce = data.get('nonce', '')
        echostr = data.get('echostr','')
        list = [token, timestamp, nonce]
        list.sort()
        s = list[0] + list[1] + list[2]
        hashcode = hashlib.sha1(s.encode('utf-8')).hexdigest()
        print("hascode:{}, signature:{}".format(hashcode, signature))
        if hashcode == signature:
            return echostr
        else:
            return ''
    if request.method == 'POST':
        xmldata = request.args
        xml_rec = et.fromstring(xmldata)
        ToUserName = xml_rec.find('ToUserName').text
        FromUserName = xml_rec.find('FromUserName').text
        CreateTime = xml_rec.find('CreateTiem').text
        MsgType = xml_rec.find('MsgType').text
        Content = xml_rec.find("MsgType").text
        MsgId = xml_rec.find('MsgId').text

        return reply_template(MsgType) % (FromUserName, ToUserName, int(time.time()), Content)

```

新建一个mytemplate.py

```
text_str = '''<xml>
                <ToUserName>![CDATA[%s]]</ToUserName>
                <FromUserName>![CDATA[%s]]</FromUserName>
                <CreateTime>%s</CreateTime>
                <MsgType>![CDATA[text]]</MsgType>
                <Content>![CDATA[%s]]</Content>
                </xml>'''

def reply_template(type):
    if type == 'text':
         return text_str
```

还是参考官网的来写吧。

因为远程到服务器上写代码调试不方便。

所以我还是在我的mackbook上启动ngrok。

```
./ngrok http 5000
```

会得到一个临时的：

```
http://xxxx.ngork.com --> http://localhost:5000
```

把http://xxxx.ngork.com 配置到微信后台上去。

可以配置成功。

如果提示失败，多试几次就好了（前提是你本地以及启动对应的flask程序了）。微信要对你配置的地址发送一个东西，期望得到一个预期的回复才认为你的服务器是有效的。

```
TypeError: a bytes-like object is required, not 'ImmutableMultiDict'
```

当前的写法，在收到微信消息的时候，服务端会报这个。

```
xmldata = request.args
```

这个得到的是一个dict，而不是一个str。

把这个dict打印出来，是这样：

```
signature 55b5ac7b5dd1429e340e774339c9fe3933265d27
timestamp 1588427603
nonce 1845494189
openid oCls90VbNcf1ZzUwIABMUXJnuTco
```

没有什么有效的信息。

```
request.get_data()
```

这个得到的才是xml数据。

目前没有报错，但是还是得不到正确的回复。

所以我先还是完全按照微信官网的教程走一遍。

在pycharm里新建一个wechat_dyh的项目。

python选择virtualenv的，版本为2.7。然后按照web-py（也在图形界面下安装）。

我把代码提交到这个地址了。

<https://github.com/teddyxiong53/wechat_dyh>

然后新建main.py。写入下面的内容：

```

```

这个是验证web.py的基本工作是否正常。

然后就是要保证验证服务器通过。新增一个handle.py。

然后是做微信回复。

新增receive.py和reply.py这2个文件。



参考资料

1、微信公共平台Node库

https://doxmate.cool/node-webot/wechat/index.html

2、微信官方文档

<https://developers.weixin.qq.com/doc/offiaccount/Getting_Started/Getting_Started_Guide.html>

3、Python3-Flask-微信公众号开发-2

https://blog.csdn.net/li_will/article/details/73611359

4、Python3-Flask-微信公众号开发-3

https://blog.csdn.net/LI_will/article/details/73613811