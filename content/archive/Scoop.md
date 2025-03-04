---
title: Scoop
category:
  - archive
tags:
  - 工具折腾
  - windows
publish: true
date: 2024-08-27 15:06:18
lastmod: 2024-12-13 17:12:05
---
# 1. 安装

## 1.1. 设置环境变量

将Scoop安装到自定义目录

```powershell
$env:SCOOP='C:\Scoop'
[Environment]::SetEnvironmentVariable('SCOOP', $env:SCOOP, 'User')
```

将Scoop配置为将全局程序安装到自定义目录

```powershell
$env:SCOOP_GLOBAL='C:\Scoop\GlobalApps'
[Environment]::SetEnvironmentVariable('SCOOP_GLOBAL', $env:SCOOP_GLOBAL, 'Machine')
```

## 1.2. 开始安装

在 PowerShell 中输入下面内容，保证允许本地脚本的执行

```powershell
set-executionpolicy remotesigned -scope currentuser
```

然后执行下面的命令安装 Scoop

```powershell
Invoke-Expression (New-Object System.Net.WebClient).DownloadString('https://get.scoop.sh')
# 或
iwr -useb get.scoop.sh | iex
```

静待脚本执行完成就可以了，安装成功

## 1.3. 设置代理

```powershell
scoop config proxy 127.0.0.1:7890
```

# 2. 重装系统恢复软件

+ 重装系统之前,先完整复制用户目录下的scoop文件夹到别的地方

> Tips: 我安装的时候一般习惯把scoop安装到非系统盘，例如`D:\repository\Scoop`，这样重装的时候以上步骤就可以省略了



- [1.1 设置环境变量](#1.1%20设置环境变量)]
- 允许脚本执行

```powershell
set-executionpolicy remotesigned -s currentuser
```

- 双击用户变量中的path，新建一个路径，填入`%SCOOP%\shims`
- 管理员权限powershell中运行

```powershell
scoop reset *
```

# 3. bukcet推荐

## 3.1. 南大镜像

用处不大，下载链接还是指向GitHub，只是让搜索速度变快

```powershell
extras     https://mirror.nju.edu.cn/git/scoop-extras.git
java       https://mirror.nju.edu.cn/git/scoop-java.git
main       https://mirror.nju.edu.cn/git/scoop-main.git
nerd-fonts https://mirror.nju.edu.cn/git/scoop-nerd-fonts.git
```

## 3.2. 个人常用

```powershell
scoop bucket add dorado https://github.com/chawyehsu/dorado
```