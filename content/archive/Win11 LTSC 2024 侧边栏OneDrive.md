---
title: Win11 LTSC 2024 侧边栏OneDrive
categories:
  - archive
tags:
  - windows
publish: true
date: 2024-10-21 14:46:09
lastmod: 2025-03-26 15:41:54
---

# 问题

win11 ltsc不带OneDrive，手动安装完成后，出现了两个问题

+ （必现）点击文件资源管理器侧边栏的OneDrive没反应
+ （偶现）出现了两个OneDrive


# 解决

## 1. 问题1 无法点击 OneDrive 选项

将以下内容保存为 `onedriver.reg`文件，双击导入注册表，然后在**任务管理器中重新启动windows资源管理器**



```ini
Windows Registry Editor Version 5.00

[HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\FolderDescriptions\{A52BBA46-E9E1-435f-B3D9-28DAA648C0F6}]

"Attributes"=dword:00000001

"Category"=dword:00000004

"DefinitionFlags"=dword:00000040

"Icon"=hex(2):25,00,53,00,79,00,73,00,74,00,65,00,6d,00,52,00,6f,00,6f,00,74,\ 00,25,00,5c,00,73,00,79,00,73,00,74,00,65,00,6d,00,33,00,32,00,5c,00,69,00,\ 6d,00,61,00,67,00,65,00,72,00,65,00,73,00,2e,00,64,00,6c,00,6c,00,2c,00,2d,\ 00,31,00,30,00,34,00,30,00,00,00

"LocalizedName"=hex(2):40,00,25,00,53,00,79,00,73,00,74,00,65,00,6d,00,52,00,\ 6f,00,6f,00,74,00,25,00,5c,00,53,00,79,00,73,00,74,00,65,00,6d,00,33,00,32,\ 00,5c,00,53,00,65,00,74,00,74,00,69,00,6e,00,67,00,53,00,79,00,6e,00,63,00,\ 43,00,6f,00,72,00,65,00,2e,00,64,00,6c,00,6c,00,2c,00,2d,00,31,00,30,00,32,\ 00,34,00,00,00

"LocalRedirectOnly"=dword:00000001

"Name"="OneDrive"

"ParentFolder"="{5E6C858F-0E22-4760-9AFE-EA3317B67173}"

"ParsingName"="shell:::{018D5C66-4533-4307-9B53-224DE2ED1FE6}"

"RelativePath"="OneDrive"
 
```

## 2. 问题2 出现两个 OneDrive 选项

打开注册表编辑器，转到如下路径
```ini
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Explorer\Desktop\NameSpace
```

展开 NameSpace

删除非`OneDrive-Personal`项

# 参考

> [https://www.landiannews.com/archives/106309.html](https://www.landiannews.com/archives/106309.html)




