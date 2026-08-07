---
title: Scoop
slug: scoop
date: 2026-03-25 18:12:12
lastmod: 2026-03-25 18:12:12
publish: true
tags:
  - Coding
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
iwr -useb get.scoop.sh | iex
```

静待脚本执行完成就可以了，安装成功

## 1.3. 设置代理

```powershell
scoop config proxy 192.168.31.5:7890
```

# 2. bukcet推荐

## 2.1. 官方必备

使用`scoop bucket known`查看所有官方的bucket

```plaintext
main
extras
versions
nirsoft
sysinternals
php
nerd-fonts
nonportable
java
games
```

可以使用`scoop add <bucket_name>`添加`bucket`，其中`main`一般会默认添加。
我常用的还有：

```powershell
scoop bucket add extras
scoop bucket add versions
scoop bucket add nerd-fonts
scoop bucket add java
```

## 2.2. 第三方

```powershell
scoop bucket add dorado https://github.com/chawyehsu/dorado
```


# 3. 重装系统恢复软件

+ 重装系统之前,先完整复制用户目录下的scoop文件夹到别的地方
- [设置环境变量](Scoop.md#1.1%20设置环境变量)
- 允许脚本执行

```powershell
set-executionpolicy remotesigned -s currentuser
```

- 双击用户变量中的path，新建一个路径，填入`%SCOOP%\shims`
- 管理员权限powershell中运行

```powershell
scoop reset *
```

软件就都恢复了
