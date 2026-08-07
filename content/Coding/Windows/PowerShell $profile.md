---
title: PowerShell $profile
slug: powershell-profile
date: 2026-03-25 18:12:12
lastmod: 2026-04-19 22:22:01
publish: true
tags:
  - Coding
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
# starship
Invoke-Expression (&starship init powershell)

# Typora重置试用时间
# Set-ItemProperty "HKCU:\SOFTWARE\Typora\" -Name IDate -Value $(Get-Date -Format 'yyyy/MM/dd')

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
