---
title: Linux之环境变量梳理
date: 2018-04-12 20:54:19
tags:
	- Linux

---



```
declare -x CLASSPATH=".:/usr/lib/jvm/jdk1.6.0_45/lib:/usr/lib/jvm/jdk1.6.0_45/jre/lib"
declare -x HOME="/home/teddy"
declare -x JAVA_HOME="/usr/lib/jvm/jdk1.6.0_45"
declare -x JRE_HOME="/usr/lib/jvm/jdk1.6.0_45/jre"
declare -x LANG="en_US.UTF-8"
declare -x LC_ADDRESS="zh_CN.UTF-8"
declare -x LC_IDENTIFICATION="zh_CN.UTF-8"
declare -x LC_MEASUREMENT="zh_CN.UTF-8"
declare -x LC_MONETARY="zh_CN.UTF-8"
declare -x LC_NAME="zh_CN.UTF-8"
declare -x LC_NUMERIC="zh_CN.UTF-8"
declare -x LC_PAPER="zh_CN.UTF-8"
declare -x LC_TELEPHONE="zh_CN.UTF-8"
declare -x LC_TIME="zh_CN.UTF-8"
declare -x LD_LIBRARY_PATH=":/usr/local/minigui"
declare -x LESSCLOSE="/usr/bin/lesspipe %s %s"
declare -x LESSOPEN="| /usr/bin/lesspipe %s"
declare -x LOGNAME="teddy"
declare -x MAIL="/var/mail/teddy"
declare -x OLDPWD
declare -x PATH="/home/teddy/bin:/home/teddy/.local/bin:/usr/lib/jvm/jdk1.6.0_45/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/home/teddy/.env/tools/scripts:/home/teddy/tools"
declare -x PKG_CONFIG_PATH=":/usr/local/lib/pkgconfig"
declare -x PWD="/home/teddy"
declare -x SHELL="/bin/bash"
declare -x SHLVL="1"
declare -x SSH_CLIENT="192.168.190.1 14633 22"
declare -x SSH_CONNECTION="192.168.190.1 14633 192.168.190.137 22"
declare -x SSH_TTY="/dev/pts/3"
declare -x TERM="vt100"
declare -x USER="teddy"
declare -x XDG_RUNTIME_DIR="/run/user/1000"
declare -x XDG_SESSION_ID="109"
```

