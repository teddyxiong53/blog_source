---
title: js之axios
date: 2019-01-27 15:07:28
tags:
	- js

---



看vue的官网教程时，看到提到了axios这个异步库。

了解一下。

可以支持在html头部包含的方式，也可以用nodejs模块的方式。

也就是说，可以用在前端，也可以用在后端。

```
<div id="watch-example">
        <p>
        ask a yes/no question:
        <input v-model="question">
        </p>
        <p>{{answer}}</p>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/axios@0.12.0/dist/axios.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/lodash@4.13.1/lodash.min.js"></script>
    <script>
        var watchExampleVM = new Vue({
            el:"#watch-example",
            data: {
                question: "",
                answer: "I cannot give you an answer until you ask a question"
            },
            watch: {
                question: function(newQuestion, oldQuestion) {
                    this.answer = "waiting until you stopping typing ..."
                    this.debouncedGetAnswer()
                }
            },
            created() {//_.debounce是lodash里的工具函数。
                this.debouncedGetAnswer = _.debounce(this.getAnswer, 500)
            },
            methods: {
                getAnswer:function() {
                    if(this.question.indexOf("?") === -1) {
                        this.answer = "questions usally contain a question mark"
                        return
                    }
                    this.answer = "thinking ..."
                    var vm = this
                    axios.get("https://yesno.wtf/api").then(function(response) {
                        vm.answer = _.capitalize(response.data.answer)
                    })
                    .catch(function(error) {
                        vm.answer = "error, can not reach the api" + error;
                    })
                }
            },
        })
    </script>
```

# class与style绑定



# 参考资料

1、中文说明

https://www.kancloud.cn/yunye/axios/234845