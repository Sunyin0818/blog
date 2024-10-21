---
title: Win11 LTSC 2024 侧边栏OneDrive
category:
  - resource
tags:
  - windows
publish: true
date: 2024-10-21 14:46:09
lastmod: 2024-10-21 17:36:55
---

# 问题

win11 ltsc不带OneDrive，手动安装完成后，点击文件资源管理器侧边栏的OneDrive没反应


# 解决

> 解决方案来自这篇[博客](https://www.zcuo.com/archives/ltsc-onedrive)

将以下内容保存为 `onedriver.reg`文件，双击导入注册表，然后在任务管理器中重新启动windows资源管理器

**注意，一定要重启windows资源管理器**

一开始我只是关闭重新打开explorer，发现用户目录下出现了两个一样的OneDrive目录