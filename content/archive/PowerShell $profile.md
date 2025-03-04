---
title: PowerShell $profile
category:
  - archive
tags:
  - 工具折腾
  - windows
publish: true
date: 2024-08-27 15:05:56
lastmod: 2024-12-13 17:14:20
---


# 1. 安装模块

```powershell
# 命令智能提醒和快捷键
Install-Module -Name PSReadLine -AllowClobber -Force
# git命令提醒
Install-Module posh-git
```

# 2. 配置文件

```powershell
# gsudo 新版win11已支持sudo功能 不需要了
# Import-Module gsudoModule
# starship
Invoke-Expression (&starship init powershell)

# Typora重置试用时间
Set-ItemProperty "HKCU:\SOFTWARE\Typora\" -Name IDate -Value $(Get-Date -Format 'yyyy/MM/dd')

Set-Alias vim nvim

# 导入posh-git，用于提示git命令
Import-Module posh-git

# 类linux快捷键
Set-PSReadLineKeyHandler -Chord "Tab" -Function MenuComplete
Set-PSReadLineKeyHandler -Chord "Ctrl+u" -Function BackwardKillInput
Set-PSReadLineKeyHandler -Chord "Ctrl+a" -Function HistorySearchForward
Set-PSReadLineKeyHandler -Chord "Ctrl+e" -Function HistorySearchBackward
# 启用预测 IntelliSense
# Set-PSReadLineOption -PredictionSource HistoryAndPlugin
set-PSReadLineOption -PredictionViewStyle ListView

# scoop
# 增强scoop搜索
Invoke-Expression (&scoop-search --hook)
# scoop命令别名
Set-Alias scu update-all-scoop
Set-Alias sco get-app-info
Set-Alias scs search-scoop
Set-Alias sci install-scoop
Set-Alias scr uninstall-scoop
function update-all-scoop { scoop update * }
function get-app-info ($app) { scoop info $app }
function search-scoop ($app) { scoop search $app }
function install-scoop ($app) { scoop install $app }
function uninstall-scoop ($app) { scoop uninstall $app }
```