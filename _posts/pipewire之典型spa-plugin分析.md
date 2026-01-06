---
title: pipewire之典型spa-plugin分析
date: 2025-09-29 10:50:37
tags:
	- 音频
---

--

现在需要编写spa plugin代码，找几个自带的spa plugin典型来深入分析一下。

# spa\plugins\volume\volume.c

这个非常典型，又便于非常，因为是纯软件的，而且可以对应一种最简单的信号处理的逻辑。

首先是文件构成：

```
plugin.c
volume.c
```

就这么2个文件。

后面我自己写plugin都采用这种格式。

自己写的话，就直接拷贝plugin.c的内容。然后改一下里面的factory变量的名字。

plugin.c的就这些。

看volume.c的内容。

入口是plugin.c里引用的spa_handle_factory。

```
struct spa_handle_factory spa_volume_factory
```

自己写就是spa_xxx_factory这样命名。

总共6个字段：

```
3个基本信息：
版本号
name
info dict

3个函数：
get_size
init
enum_interface_info
```

init是最重要的入口函数。

但是get_size和enum_interface_info比较简单，所以先说这2个。

get_size很简单，就是把内部的impl结构体的size返回就可以了。主要是用来指定分配user_data，在各个callback里作为user_data来传递的。

enum_interface_info一般也是只有一个SPA_TYPE_INTERFACE_Node的。

你写的时候，也就直接copy volume.c里的写法就可以。

struct impl里面，尽量都是结构体变量，而不是指针变量。

impl_init的参数

```
5个参数：
spa_handle_factory
spa_handle： impl一定是spa_handle的子类（就是spa_handle是第一个成员变量），分配的内存就是get_size。
info：可以是NULL。
support
n_support
```

impl_init的逻辑

```
首先给handle的2个函数指针赋值：
get_interface
clear

this指针指向handle。转成impl指针。就可以操作这个内存了。

support找到log，赋值给this->log

遍历info字典。找到里面的clock.quantum-limit字段，赋值给impl。

hooks初始化。

impl->node->iface通过SPA_INTERFACE_INIT初始化。
	这个是最重要的。这里的impl_node，就包含了大量的函数指针，这个后面分析。
	
info_all
	这个只会有flags和params变化的。
然后是spa_node_info的初始化。
	1个输入port
	1个输出port
	flag是RT的。
	info的params有2个：PropInfo和Props
	Props就2个：volume和mute。
	
接下来是input port的初始化。port结构体是这里自定义的。就叫struct port。
	direction 是input
	id是0
	info_all也是只有flags和params
	params有5个：
		EnumFormat
		Meta
		IO
		Format
		Buffers
然后是output port的初始化。
	跟input的一样。
	
```

到这里总结，主要就是struct impl结构体的初始化。

基本没有逻辑调用。

接下来就是看impl_node的函数指针：

```
总共15个函数：
add_listener
set_callbacks
sync

enum_params
set_param
set_io
send_command

add_port
remove_port
port_enum_params
port_set_param
port_use_buffers
port_set_io
port_reuse_buffer

process
```



```
add_listener
	node被创建的时候被调用。
	例如你用pw-cli创建node的时候，或者wireplumber创建node的时候。
	对于volume，就是把node和2个port的info都emit出去。
set_callbacks
	目前是空实现。
sync

enum_params
	
set_param
set_io
send_command

add_port
	不支持
remove_port
	不支持
port_enum_params
port_set_param
	只有设置format这一种。
port_use_buffers
	为端口分配绑定buffer
port_set_io
	配置port的io区域。
port_reuse_buffer
	通知输出端口可以重用port。
process
	node处理主函数，实现input消耗/output生成。
```

现在需要使用一下volume这个插件，才能理解里面的代码逻辑。

Volume 插件定义了以下默认值： volume.c:24-29

- 默认采样率：48000 Hz
- 默认声道数：2
- 默认音量：1.0（线性值）
- 默认静音状态：false

spa-inspect查看。

```
# spa-inspect /usr/lib/spa-0.2/volume/libspa-volume.so 
factory version:                1
factory name:           'volume'
factory info:
  none
factory interfaces:
 interface: 'Spa:Pointer:Interface:Node'
factory instance:
 interface: 'Spa:Pointer:Interface:Node'
node info: 00000005
max input ports: 1
max output ports: 1
enumerating: Spa:Enum:ParamId:PropInfo:
                Object: size 112, type Spa:Pod:Object:Param:PropInfo (262145), id Spa:Enum:ParamId:PropInfo (1)
                  Prop: key Spa:Pod:Object:Param:PropInfo:id (1), flags 00000000
                    Id 65539    (Spa:Pod:Object:Param:Props:volume)
                  Prop: key Spa:Pod:Object:Param:PropInfo:description (7), flags 00000000
                    String "The volume"
                  Prop: key Spa:Pod:Object:Param:PropInfo:type (3), flags 00000000
                    Choice: type Spa:Enum:Choice:Range, flags 00000000 28 4
                      Float 1.000000
                      Float 0.000000
                      Float 10.000000
                Object: size 80, type Spa:Pod:Object:Param:PropInfo (262145), id Spa:Enum:ParamId:PropInfo (1)
                  Prop: key Spa:Pod:Object:Param:PropInfo:id (1), flags 00000000
                    Id 65540    (Spa:Pod:Object:Param:Props:mute)
                  Prop: key Spa:Pod:Object:Param:PropInfo:description (7), flags 00000000
                    String "Mute"
                  Prop: key Spa:Pod:Object:Param:PropInfo:type (3), flags 00000000
                    Bool false
enumerating: Spa:Enum:ParamId:Props:
                Object: size 56, type Spa:Pod:Object:Param:Props (262146), id Spa:Enum:ParamId:Props (2)
                  Prop: key Spa:Pod:Object:Param:Props:volume (65539), flags 00000000
                    Float 1.000000
                  Prop: key Spa:Pod:Object:Param:Props:mute (65540), flags 00000000
                    Bool false
 input port: 00000000 info:
param: Spa:Enum:ParamId:EnumFormat: flags r-
values:
                 audio/raw
                           format : (Id) { S16LE }
                             rate : (Int) [ 1, 2147483647 ]
                         channels : (Int) [ 1, 2147483647 ]
param: Spa:Enum:ParamId:Meta: flags r-
values:
                Object: size 56, type Spa:Pod:Object:Param:Meta (262149), id Spa:Enum:ParamId:Meta (6)
                  Prop: key Spa:Pod:Object:Param:Meta:type (1), flags 00000000
                    Id 1        (Spa:Pointer:Meta:Header)
                  Prop: key Spa:Pod:Object:Param:Meta:size (2), flags 00000000
                    Int 32
param: Spa:Enum:ParamId:IO: flags r-
values:
                Object: size 56, type Spa:Pod:Object:Param:IO (262150), id Spa:Enum:ParamId:IO (7)
                  Prop: key Spa:Pod:Object:Param:IO:id (1), flags 00000000
                    Id 1        (Spa:Enum:IO:Buffers)
                  Prop: key Spa:Pod:Object:Param:IO:size (2), flags 00000000
                    Int 8
param: Spa:Enum:ParamId:Format: flags -w
param: Spa:Enum:ParamId:Buffers: flags --
 output port: 00000000 info:
param: Spa:Enum:ParamId:EnumFormat: flags r-
values:
                 audio/raw
                           format : (Id) { S16LE }
                             rate : (Int) [ 1, 2147483647 ]
                         channels : (Int) [ 1, 2147483647 ]
param: Spa:Enum:ParamId:Meta: flags r-
values:
                Object: size 56, type Spa:Pod:Object:Param:Meta (262149), id Spa:Enum:ParamId:Meta (6)
                  Prop: key Spa:Pod:Object:Param:Meta:type (1), flags 00000000
                    Id 1        (Spa:Pointer:Meta:Header)
                  Prop: key Spa:Pod:Object:Param:Meta:size (2), flags 00000000
                    Int 32
param: Spa:Enum:ParamId:IO: flags r-
values:
                Object: size 56, type Spa:Pod:Object:Param:IO (262150), id Spa:Enum:ParamId:IO (7)
                  Prop: key Spa:Pod:Object:Param:IO:id (1), flags 00000000
                    Id 1        (Spa:Enum:IO:Buffers)
                  Prop: key Spa:Pod:Object:Param:IO:size (2), flags 00000000
                    Int 8
param: Spa:Enum:ParamId:Format: flags -w
param: Spa:Enum:ParamId:Buffers: flags --
```

但是想要测试使用这个模组，找不到方法。

我试图用pw-cli create-node spa-node-factory来创建。

命令不报错。但是执行后，pw-cli ls Node查看不到。

这样写到pipewire.conf里可以看到。

```
{ factory = spa-node-factory            args = { factory.name = volume node.name = my-volume node.description = my-volume } }
```



# spa\plugins\test\fakesink.c



# spa\plugins\audiotestsrc\audiotestsrc.c

这个可以跑起来看效果。

默认是生成正弦波对外输出。

是靠定时器来生成数据。

只有output端口。

这个数据填充是在make_buffer函数里。

```
填充数据
启动定时器
	如果是live模式，则下一次超时的时间是计算出来的。
	否则是下一个ns超时。
	
```

在非 live 模式下设置 1 纳秒定时器看似频繁，但实际上这是一个巧妙的设计：

1. **立即触发**：1 纳秒实际上是让定时器立即触发，因为系统无法提供如此精确的纳秒级定时。
2. **异步处理**：这种设计用于异步模式（`this->async` 为 true）或非实时源，目的是尽快处理下一个缓冲区。

虽然看起来频繁，但实际上：

- 系统会将 1 纳秒向上舍入到最小可支持的时间间隔
- 只有在有数据需要处理时才会真正频繁触发
- 当没有缓冲区可用时，定时器会被禁用：

```
	if (spa_list_is_empty(&port->empty)) {
		set_timer(this, false);
		spa_log_error(this->log, "%p: out of buffers", this);
		return -EPIPE;
	}
```

当reuse_buffer的时候，会重新打开timer。

```
static inline void reuse_buffer(struct impl *this, struct port *port, uint32_t id)
{
	struct buffer *b = &port->buffers[id];
	spa_return_if_fail(b->outstanding);

	spa_log_trace(this->log, "%p: reuse buffer %d", this, id);

	b->outstanding = false;
	spa_list_append(&port->empty, &b->link);

	if (!this->props.live)
		set_timer(this, true);//这里
}
```

这种 1 纳秒定时器的设计是 PipeWire 中常见的模式，用于在非实时场景下实现高效的异步数据处理。它并不会真正以纳秒级频率运行，而是让系统尽快调度下一次处理。



impl_node_port_use_buffers的理解

```
这个函数是在协商buffer的时候调用。
不会频繁调用的。
应该是连接的时候，调用一次。

首先是清理buffer。
检查have_format是否已经设置。

把协商得到的buffer，都挂入到自己的buffer list里（名字叫emtpy）
```

可以看到node的info里，固定为node.driver的。

```
static const struct spa_dict_item node_info_items[] = {
	{ SPA_KEY_MEDIA_CLASS, "Audio/Source" },
	{ SPA_KEY_NODE_DRIVER, "true" },
};

static void emit_node_info(struct impl *this, bool full)
{
	uint64_t old = full ? this->info.change_mask : 0;
	if (full)
		this->info.change_mask = this->info_all;
	if (this->info.change_mask) {
		this->info.props = &SPA_DICT_INIT_ARRAY(node_info_items);
		spa_node_emit_info(&this->hooks, &this->info);
		this->info.change_mask = old;
	}
}
```

# spa\plugins\support\null-audio-sink.c



# spa\plugins\ffmpeg\ffmpeg-dec.c

这个也是一个node。

这3个函数都是不支持。

```
static int impl_node_enum_params(void *object, int seq,
			uint32_t id, uint32_t start, uint32_t num,
			const struct spa_pod *filter)
{
	return -ENOTSUP;
}

static int impl_node_set_param(void *object,
					 uint32_t id, uint32_t flags,
					 const struct spa_pod *param)
{
	return -ENOTSUP;
}

static int impl_node_set_io(void *object, uint32_t id, void *data, size_t size)
{
	return -ENOTSUP;
}
static int
impl_node_set_callbacks(void *object,
				  const struct spa_node_callbacks *callbacks,
				  void *user_data)
{
	return 0;
}
static int
impl_node_add_port(void *object, enum spa_direction direction, uint32_t port_id,
		const struct spa_dict *props)
{
	return -ENOTSUP;
}

static int
impl_node_remove_port(void *object,
				enum spa_direction direction,
				uint32_t port_id)
{
	return -ENOTSUP;
}
```

连use_buffers都是这样的

```
static int
impl_node_port_use_buffers(void *object,
				     enum spa_direction direction,
				     uint32_t port_id,
				     uint32_t flags,
				     struct spa_buffer **buffers,
				     uint32_t n_buffers)
{
	if (object == NULL)
		return -EINVAL;

	if (!IS_VALID_PORT(object, direction, port_id))
		return -EINVAL;

	return -ENOTSUP;
}
```

node_process也是相当于什么也没做。

```
static int impl_node_process(void *object)
{
	struct impl *this = object;
	struct port *port;
	struct spa_io_buffers *output;

	if (this == NULL)
		return -EINVAL;

	port = &this->out_ports[0];

	if ((output = port->io) == NULL)
		return -EIO;

	if (!port->have_format) {
		output->status = -EIO;
		return -EIO;
	}
	output->status = SPA_STATUS_OK;

	return SPA_STATUS_OK;
}
```

reuse_buffer也是空的。

```
static int
impl_node_port_reuse_buffer(void *object, uint32_t port_id, uint32_t buffer_id)
{
	if (object == NULL)
		return -EINVAL;

	if (port_id != 0)
		return -EINVAL;

	return -ENOTSUP;
}
```



sync函数的实现，一般是这样：

```
static int impl_node_sync(void *object, int seq)
{
	struct impl *this = object;

	spa_return_val_if_fail(this != NULL, -EINVAL);

	spa_node_emit_result(&this->hooks, seq, 0, 0, NULL);

	return 0;
}
```

