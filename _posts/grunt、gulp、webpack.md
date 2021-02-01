---
title: grunt、gulp、webpack
date: 2021-01-28 09:33:11
tags:
	- 前端

---

--

# grunt

grunt出现比gulp早。

gulp是后起之秀。

他们的本质都是通过js来实现类似shell命令的一些功能。

例如调用jslint进行代码检查。

你可以手动在命令行输入jslint来检查，这样比较麻烦。

你可以把jslint规则写到Gruntfile.js里。

Gruntfile.js里这样写

```
module.exports = function(grunt) {
	grunt.initconfig({
		jslint: {
			src: 'src/test.js'
		}
		uglify:{}
	})
	grunt.loadnpmTasks('grunt-contrib-uglify')
	grunt.register('default', ['jslint'])
}
```

# gulp

gulp吸取了grunt的优点。

写法更加简洁。

通过流（stream）的概念来简化多个任务之间的配置和输出。

gulp可以配合各种插件做js压缩、css压缩、less编译，来进行自动化构建。

对应的文件是Gulpfile.js。

有了gulp，大家都慢慢抛弃grunt了。

一个例子

```
var gulp = require('gulp')
var jshint = require('gulp-jshint')
var uglify = require('gulp-uglify')

gulp.task('lint', function() {
	return gulp.src('src/test.js')
	.pipe(jshint())
	.pipe(jshint.reporter('default'))
})

gulp.task('compress', function() {
	return gulp.src('src/test.js')
	.pipe(uglify())
	.pipe(gulp.dest('build'))
})
gulp.task('default', ['lint', 'compress'])

```

# webpack

webpack在朝着全能型构建工具的方向发展。

通过配置文件webpack.config.js来进行配置。

一个例子

```
'use strict'
const path= require('path')
const webpack = require('webpack')
const HtmlWebpackPlugin = require('html-webpack-plugin')
const merge = require('webpack-merge')
const utils = require('./utils')

var config = {
	//入口
	entry: {
		app: './src/app.js'
	},
	//出口
	output: {
		path: config.build.assetsRoot,
		filename: '[name].js',
		publicPath: config.build.assetsPublicPath
	},
	//loader配置
	module: {
		rules: [
			{
				test: '/\.css$/',
				use: ['style-loader', 'css-loader']
			}
		]
	},
	//插件
	plugins: [
		new webpack.DefinePlugin({
			'process.env': require('../config/dev.env')
		}),
		new webpack.HotModuleReplacementPlugin(),
		new HtmlWebpackPlugin({
			filename: 'index.html',
			template: 'index.html',
			inject: true
		})
	]
}
module.exports = config

```



参考资料

1、Grunt、Gulp和Webpack区别

https://www.cnblogs.com/Ann-web-1/p/11444675.html