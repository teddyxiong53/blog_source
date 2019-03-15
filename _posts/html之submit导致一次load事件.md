---
title: html之submit导致一次load事件
date: 2019-03-15 17:33:11
tags:
	- html

---





看《锋利的jquery》的示例代码，

```
  <script type="text/javascript">
  $(document).ready(function(){

  	$("#commentForm").validate({meta: "validate"});
   
  });
  </script>
```

觉得这里有点奇怪。为什么在ready里进行验证呢？

验证是在提交之后才对呀。

事实上，在点击submit的时候，会重新产生一次ready事件。

