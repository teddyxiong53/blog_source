---
title: nodejs之log4js
date: 2023-10-01 11:15:11
tags:
	- nodejs
---

--

# 基本用法

```
const log4js = require('log4js');

log4js.configure("log4js.json");

const logger = log4js.getLogger();

logger.trace("trace");
logger.debug("debug");
logger.info("info");
logger.warn("warn");
logger.error("error");
logger.fatal("fatal");

```

配套的log4js.json文件：

```
{
    "appenders": {
        "console": {
            "type": "console"
        },
        "file": {
            "type": "file",
            "filename": "app.log"
        }
    },
    "categories": {
        "default": {
            "appenders": [
                "console",
                "file"
            ],
            "level": "debug"
        }

    }
}
```

输出是这样：

```
[2023-10-01T11:14:47.283] [DEBUG] default - debug
[2023-10-01T11:14:47.287] [INFO] default - info
[2023-10-01T11:14:47.288] [WARN] default - warn
[2023-10-01T11:14:47.288] [ERROR] default - error
[2023-10-01T11:14:47.289] [FATAL] default - fatal
```

