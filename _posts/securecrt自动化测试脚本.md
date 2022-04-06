---
title: securecrt自动化测试脚本
date: 2022-03-14 14:20:25
tags:
	- securecrt

---

--

因为在串口交互中，[SecureCRT](https://so.csdn.net/so/search?q=SecureCRT&spm=1001.2101.3001.7020)使用的频率是比较高的，因此我们就用这个工具来实现脚本自动化，现在分享一个简单的，就是每一秒钟发送一条命令即可。

为了获取数据，需要一秒钟输入一条命令，持续可能是几个小时，甚至是几天，也或许是几十万次，如此重复的情况，人工做，可想而知是不可能的，因此，需要自动化。

脚本有两种方式来产生：

1、录制脚本。

SecureCrt有录制脚本的功能，录制完成后只需根据自己的实际情况略加修改和调整，十分方便，在这里以一个每两秒打印一次cat信息的脚本为例

2、自己写脚本。

支持3种语言：vbs、python、js。

```

//vbs
# $language = "VBScript"
# $interface = "1.0"

//js
# $language="JScript"
# $interface="1.0"

//python
# $language = "Python"
# $interface = "1.0"
```

我就看Python方式的

```

# $language = "python"
# $interface = "1.0"
#此方法表示你必须先登录一台服务器然后再去telnet到另外一台服务器
#主机的ip
host = '11.1.1.1'
#主机的用户名
user = 'root'
#主机的密码
passwd = 'password'

def main():
    #向屏幕光标后发送以下文字内容，\r表示回车执行
    crt.Screen.Send('telnet '+host+'\r')
    crt.Screen.WaitForString('login:')  
    crt.Screen.Send(user+"\r")
    crt.Screen.WaitForString('password:') 
    crt.Screen.Send(passwd+"\r")
    #使用默认弹窗提示信息
    crt.Dialog.MessageBox('登录成功!')

main()
```



参考资料

1、

https://blog.csdn.net/qq_33826580/article/details/89848203

