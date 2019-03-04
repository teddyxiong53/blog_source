---
title: jquery在提交前检查表单
date: 2019-03-04 14:40:03
tags:
	- jquery
---





用在form添加onsubmit的方式。

```
function checkForm() {

      var name = $("#form_name").val()

      var age = $("#form_age").val()

      if(name == '' || name == null) {

        alert("请填写姓名")

        return false

      }

      if(age > 100 || age <= 0) {

        alert("请正确填写年龄")

        return false

      }

      return true

    }
```

```
<form action="http://192.168.56.101:3344" method="POST" onsubmit="return checkForm()">
```



参考资料

1、

https://blog.csdn.net/u014175572/article/details/51135053

2、

https://blog.csdn.net/m_nanle_xiaobudiu/article/details/79667661