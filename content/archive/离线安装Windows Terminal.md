---
title: 离线安装Windows Terminal
category:
  - archive
tags:
  - 工具折腾
  - windows
publish: true
date: 2024-08-27 15:05:56
lastmod: 2024-12-13 17:08:28
---


> 来自: [离线安装Windows Terminal的简单笔记 - 哔哩哔哩](https://www.bilibili.com/read/cv26067666/)


# 1. 系统版本

Windows 10 20H2 19042

# 2. 安装前准备

在Github下载对应版本的[Windows 10预安装工具包](https://github.com/microsoft/terminal/releases/download/v1.18.3181.0/Microsoft.WindowsTerminal_1.18.3181.0_8wekyb3d8bbwe.msixbundle_Windows10_PreinstallKit.zip)，这里以`1.18.2822.0`版本为例。

下载后，将压缩包解压到任意目录。
结构如下
> 新版本中已不再包含VCLib

```powershell
Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a---          2023/10/10    20:18           2676 0ef1881c68144b78ad517d9e8e2aab5d_License1.xml
-a---          2023/10/10    20:18       21200306 0ef1881c68144b78ad517d9e8e2aab5d.msixbundle
-a---          2023/10/10    20:18            135 AUMIDs.txt
-a---          2023/10/10    20:18        5009871 Microsoft.UI.Xaml.2.8_8.2306.22001.0_arm__8wekyb3d8bbwe.appx
-a---          2023/10/10    20:18        5095367 Microsoft.UI.Xaml.2.8_8.2306.22001.0_arm64__8wekyb3d8bbwe.appx
-a---          2023/10/10    20:18        5123962 Microsoft.UI.Xaml.2.8_8.2306.22001.0_x64__8wekyb3d8bbwe.appx
-a---          2023/10/10    20:18        4753085 Microsoft.UI.Xaml.2.8_8.2306.22001.0_x86__8wekyb3d8bbwe.appx
-a---          2023/10/10    20:18            949 MPAP_0ef1881c68144b78ad517d9e8e2aab5d_001.provxml
```
# 3. 安装过程

进入解压文件目录后，在该目录以管理员身份打开PowerShell窗口，安装依赖。
## 3.1. 开启appx
```powershell
Import-Module Appx -UseWindowsPowerShell
```
## 3.2. 安装WinUI
```
Add-AppxPackage .\Microsoft.UI.Xaml.2.8_8.2306.22001.0_x64__8wekyb3d8bbwe.appx
```
## 3.3. 安装Windows Terminal
```
Add-ProvisionedAppxPackage -Online -PackagePath .\0ef1881c68144b78ad517d9e8e2aab5d.msixbundle -LicensePath .\0ef1881c68144b78ad517d9e8e2aab5d_License1.xml -CustomDataPath .\MPAP_0ef1881c68144b78ad517d9e8e2aab5d_001.provxml
```
安装完成，启动`终端`即可。

