---
title: PVE导出虚拟机至Esxi
categories:
  - area
tags:
  - AIO
publish: true
date: 2025-11-25 08:45:44
lastmod: 2025-11-25 10:23:50
---
> PVE版本：`8.4.1`
> Esxi版本：`6.0.0`
> 虚拟机：`Ubuntu 18.04`


# PVE导出

## 备份

先对要导出的虚拟机备份

![image-20251125100024909.jpg](image-20251125100024909.jpg)

模式选择`停止`

![image-20251125100131331.jpg](image-20251125100131331.jpg)

## 转换为vmdk

ssh至pve
```bash
cd /var/lib/vz/dump
```

检查一下
```bash
root@pve:/var/lib/vz/dump# ls
vzdump-qemu-107-2025_11_24-16_37_34.log      vzdump-qemu-107-2025_11_24-16_37_34.vma.zst.notes
vzdump-qemu-107-2025_11_24-16_37_34.vma.zst
```

解压备份出来的文件
```bash
zstd -d vzdump-qemu-107-2025_11_24-16_37_34.vma.zst
```

通过vma命令转换成raw后缀的磁盘文件
```bash
vma extract vzdump-qemu-107-2025_11_24-16_37_34.vma extract
```

用qemu-img把raw转换vmdk
```bash
cd extract/
qemu-img convert -f raw -O vmdk disk-drive-scsi0.raw disk-drive-scsi0.vmdk
```

`disk-drive-scsi0.vmdk`就是我们需要的文件

# Esxi导入

将`disk-drive-scsi0.vmdk`上传至Esxi服务器

## 转换

> 语法：`vmkfstools -d [格式] -i 原文件.vmdk 目标文件.vmdk` 

```bash
vmkfstools -d thin -i /vmfs/volumes/raid/disk-drive-scsi0.vmdk /vmfs/volumes/raid/disk-drive-ubuntu.vmdk
```

**参数说明**：
+ `-d thin`： 转换为精简置备（节省空间）
+ `-d eagerzeroedthick`：转换为完全零厚置备（适合 FT 等高级功能）


## 新建虚拟机

新建虚拟机，最后一步的时候，**把默认磁盘删掉**，添加转换后的磁盘文件作为虚拟机的磁盘即可




