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

明天再看。

