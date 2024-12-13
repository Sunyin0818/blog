---
title: WSL2
category:
  - archive
tags:
  - windows
publish: true
date: 2024-08-27 15:06:18
lastmod: 2024-12-13 17:05:56
---
WSL 是 Windows 下的Linux子系统，可以代替虚拟机来运行 Linux 系统，占用资源少，使用方便，下面说一下如何对已发布子系统进行迁移。一种情况是针对同一个系统，更换安装的位置；另一种情况跟换机器或重装系统后的迁移。

网上查了基本都是使用` LxRunOffline` 工具，进入 [Github](https://github.com/DDoSolitary/LxRunOffline/releases) 下载 ZIP 包，其实只用 wsl 命令也可以实现。

# 1. 命令说明

在 Windows 的 PowerShell 中输入:

```bash
wsl --help
```

可以看到关于这个命令的使用帮助说明

# 2. 操作

## 2.1. 终止正在运行的分发或虚拟机

```bash
wsl --shutdown
```

## 2.2. 对需要迁移的分发或虚拟机导出

```bash
wsl --export docker-desktop-data D:\repository\wsl\docker-desktop-data\docker-desktop-data.tar
```

## 2.3. 卸载分发版或虚拟机

> （如果是要重装系统或换机器安装，这一步可以省略，但是要将上一步导出的文件保存好）

```bash
wsl --unregister docker-desktop-data
```

## 2.4. 导入新的分发版或虚拟机

```bash
wsl --import docker-desktop-data D:\repository\wsl\docker-desktop-data\ D:\repository\wsl\docker-desktop-data\docker-desktop-data.tar --version 2
```

> 最后的选项“--version 2”可以省略，则采用默认版本导入。如果导出的是WSL2，而这里设置的是“--version 1”，还可以将其版本降为WSL1，这样就实现了子系统的迁移 ，注意文件存放的路径一定不能错。


# 3. 一键脚本

```powershell
# target: 期望迁移的目录 
$target = "D:\repository\wsl"
# mode: backup or reloaction
$mode = "relocation"
$distro = 'Ubuntu-20.04', 'docker-desktop-data', 'docker-desktop'

function Log {
    param (
        $content
    )
    Write-Host $content -ForegroundColor Green
}

function StartLoop {
    try {
        Log "mode: $mode " 
        StopWSL
        foreach ($image in $distro) {
            # relocation: 导出+注销+导入
            # backup: 导出
            Log "handle image: $image" 
            if ("backup" -eq $mode) {
                ExportImage $image
            }
            if ("relocation" -eq $mode) {
                ExportImage $image
                ImportImage $image
            }
        }
        if ("relocation" -eq $mode) {
            ClearImages
        }
    }
    catch {
        throw "GetAlWSL Error"
    }
}

function StopWSL {
    try {
        Log "Stop docker ..." 
        net stop "com.docker.service" 
        Log "Stop wsl ..." 
        wsl --shutdown  
    }
    catch {
        throw "StopWSL Error"
    }
}

function ExportImage {
    param (
        [String]$imagename
    )
    try {
        Log "export to: $target\$imagename.tar" 
        wsl --export $imagename $target\$imagename.tar 
    }
    catch {
        throw "Export $imagename Error"
    }
}

function ImportImage {
    param (
        [string]$imagename
    )
    try {
        Log "unregister: $imagename" 
        wsl --unregister $imagename

        Log "import from $target\$imagename.tar" 
        New-Item -Path "$target\$imagename" -ItemType Directory -Force | Out-Null
        wsl --import $imagename $target\$imagename\ $target\$imagename.tar --version 2 
    }
    catch {
        throw "Import $imagename Error"
    }
}

function ClearImages {
    $isdel = Read-Host "delele all exported images? (y or n)" 
    if ("y" -eq $isdel) {
        foreach ($image in $distro) {
            Log "clear $target\$image.tar" 
            Remove-Item $target\$image.tar -recurse 
        }
    }
}

StartLoop
Log "---Finish---" 
```

# 4. FAQ

## 4.1. WSL 2 需要更新其内核组件

导入后提示“WSL 2 需要更新其内核组件”，访问[旧版 WSL 的手动安装步骤](https://docs.microsoft.com/zh-cn/windows/wsl/install-manual)，下载更新包安装即可

![](/_assets/e8878120c4ca3177a8e0469d95772af0_MD5.png)

## 4.2. 默认用户问题

导出再导入之后，会有默认用户变成root的问题，解决办法如下：
进入分发版Linux，然后编辑 /etc/wsl.conf 添加下面的内容，然后**重启wsl生效**

```shell
[user]
default=用户名
```

如果是原生安装的，powershell执行一下即可

```powershell
ubuntu2004.exe config --default-user user001
```

