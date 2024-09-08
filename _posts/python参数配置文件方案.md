---
title: python参数配置文件方案
date: 2024-09-07 16:41:17
tags:
	- python

---

--

在 Python 中，最简单的参数文件通常可以使用以下几种方式来实现：

### 1. **JSON 文件**
JSON 格式简单易读，适合存储结构化数据。

**示例：`config.json`**
```json
{
    "host": "localhost",
    "port": 8080,
    "debug": true
}
```

**读取 JSON 配置的示例代码：**
```python
import json

with open('config.json') as f:
    config = json.load(f)

print(config['host'])
print(config['port'])
```

### 2. **YAML 文件**
YAML 格式更为简洁，适合复杂配置，易于人类阅读。

**示例：`config.yaml`**
```yaml
host: localhost
port: 8080
debug: true
```

**读取 YAML 配置的示例代码：**
```python
import yaml

with open('config.yaml') as f:
    config = yaml.safe_load(f)

print(config['host'])
print(config['port'])
```

**注意**：需要安装 `PyYAML` 库：
```bash
pip install pyyaml
```

### 3. **INI 文件**
INI 文件格式简单，适合存储简单的键值对。

**示例：`config.ini`**
```ini
[settings]
host = localhost
port = 8080
debug = true
```

**读取 INI 配置的示例代码：**
```python
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

print(config['settings']['host'])
print(config['settings']['port'])
```

### 4. **Python 文件**
直接使用 `.py` 文件定义配置，也是一种常见方式。

**示例：`config.py`**
```python
host = 'localhost'
port = 8080
debug = True
```

**读取 Python 配置的示例代码：**
```python
import config

print(config.host)
print(config.port)
```

### 总结
- **简单配置**：选择 JSON。
- **复杂配置**：选择 YAML。
- **INI 格式**：适合较为简单的键值对存储。
- **Python 文件**：适合直接在代码中使用配置。

根据你的需求选择最合适的格式即可。
