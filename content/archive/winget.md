---
title: winget换源
categories:
  - archive
tags:
  - windows
publish: true
date: 2024-08-27 15:06:12
lastmod: 2025-07-17 11:32:54
---

# 1. 换源

> [!NOTE] 提示
> 目前winget的默认源已加cdn，可无需修改

> 参考[科大镜像站说明](https://mirrors.ustc.edu.cn/help/winget-source.html)

默认的winget source如下

```powershell
❯ winget source list
名称    参数                                          显式
-----------------------------------------------------------
msstore https://storeedgefd.dsx.mp.microsoft.com/v9.0 false
winget  https://cdn.winget.microsoft.com/cache        false
```

# 设置代理


> [!NOTE] 可在win11的开发者选项中启用sudo命令

先开启配置（需要管理员权限）
```powershell
sudo winget settings --enable ProxyCommandLineOptions
```

设置代理
```powershell
winget settings set DefaultProxy http://127.0.0.1:7089
```

重置
```powershell
winget settings reset DefaultProxy
```

