---
title: PVE下飞牛扩容
date: 2026-03-25 18:12:12
lastmod: 2026-03-25 18:12:12
publish: true
tags:
  - AIO
---



# 1. 背景

PVE安装的飞牛，原有分配了一个200G数据盘，和一个1T的媒体盘

媒体太多不够放了，遂在PVE中调整磁盘大小，增加了200G

但是飞牛中不能正常使用扩充的容量

版本信息：

+ fnOS：`0.8.36`
+ PVE：`8.2.7`


# 2. 解决方案

首先使用 `fdisk -l`查询磁盘信息得到相关内容如下：

![](/images/image-e5f3cecf-3ac3-418f-8cbc-3a8cf0d67760.png)


![](/images/image-dd504e6c-bc1e-485b-8ee2-0e0fc568df6e.png)


## 2.1. 扩展分区

使用 `fdisk /dev/sdc`编辑分区表，输入 `p`查询当前分区表：

![](/images/image-998dd04b-ec09-4b2d-98b8-c26653d7859a.png)

使用 `d`命令删除分区

![](/images/image-1f07b73e-14e6-4ef7-9a14-595c50e4f0a3.png)

`n`命令新建分区，`remove the signature`选择`N`，不删除原有的LVM标记，其余回车即可

`t`命令修改分区类型为`42`（Linux Raid），跟飞牛原有的保持一致

![](/images/image-739bd75f-95cf-44c0-8884-4161f595881a.png)

![](/images/image-c665ceae-6836-4c34-8d7b-afe9319f06b0.png)

![](/images/image-e79b8a09-db62-4d87-a89e-f62ec5ea5b1a.png)

修改完成后我们使用 `w`保存并退出

![](/images/image-40e49586-52e8-47a1-a587-837180f7885c.png)

至此，我们成功为分区扩容，可以使用 `fdisk -l`查看

![](/images/image-961de75b-dc93-4637-85fa-20526dba26b4.png)

接下来我们要对LVM进行扩容

## 2.2. 扩展LVM

在[Debian官网的LVM介绍](https://wiki.debian.org/LVM)中我们可以得知LVM的结构如下：

```null
||-------------------------OS----------------------------||
||-------------------------LVM---------------------------||
||  LV-1 (/)    |LV-2 (swap)|  LV 3 (/home) | LV-4 (/tmp)|| Logical Volumes(LV)
||------------------------------------------|------------||
||                  VG 1                    |    VG 2    || Volume Groups(VG)
||------------------------------------------|------------||
||  /dev/sda2 |    /dev/sda3    | /dev/sdb2 | /dev/sdd4  || Physical Volumes(PV)
||-------------------------------------------------------||

```

因此我们的思路为：先扩展PV，再扩展LV

### 2.2.1. 扩展PV

使用 `pvdisplay`查看当前PV，发现与该存储空间相关的一个PV如下

![](/images/image-03c61506-28d6-4148-b5ec-42c7047408e6.png)

先让PV卷使用底层磁盘全部空间

```bash
 mdadm --grow /dev/md1 --size=max
```
![](/images/image-11c15f6a-35e1-49d0-9ef4-fde53c648dcf.png)

然后使用 `pvresize /dev/md1`扩展

![](/images/image-3fdaa6ab-b944-4567-90fa-1fd51d3abbed.png)

此时再次 `pvdisplay`得到

![](/images/image-fa7a0ff7-1095-4c0b-9440-233ea15322c1.png)

使用 `vgdisplay`查看VG

![](/images/image-4a229c20-4221-4808-9e5f-72af155bb656.png)

至此，PV与VG扩容成功（VG不需要手动调整）

### 2.2.2. 扩容LV

使用 `lvdisplay`查看当前LV

![](/images/image-64ebb048-424f-41ea-876e-24438fa7645b.png)

将当前LV扩容，扩容的大小为所属的VG的所有空余空间，命令为
```bash
lvresize -l +100%FREE /dev/trim_526c72bb_b792_47a0_98de_fc3a1419269d/0
```

![](/images/image-fd5459bf-78a5-4ad9-a6f0-4b067c4824ec.png)

此时 `lvdisplay`

![](/images/image-64cdbd6c-16aa-4ccd-b187-98dbb216099c.png)

至此，LV扩容成功

## 2.3. 调整文件系统

在完成上述操作后，我们再次查看nas的web界面发现仍未扩容，原因是虽然LV扩容成功，但文件系统仍旧没有使用扩容的空间。我们可以使用 `df -h`查看

![](/images/image-3bb8710c-a4a2-4d14-99db-3f584db35a5c.png)

因此我们还需对文件系统进行调整使其使用新分配的空间。

```bash
btrfs filesystem resize max /vol2
```

![](/images/image-9c6916c5-8f0d-4f57-a3eb-c203239e1e34.png)

之后使用 `df -h`查看

![](/images/image-cef7a433-4ffc-4e3c-8bb7-acd88354cda7.png)

此时再回到web界面查看发现扩容成功~

![](/images/image-de0f5dca-6529-4177-b617-d1ebf96ba5ea.png)


# 3. 总结


首先在fdisk中扩展分区（d, n），其次扩展pv（`pvresize`），lv（`lvresize`），最后调整文件系统大小（`btrfs filesystem resize max`）



# 4. 参考

感谢论坛的帖子，评论区帮我排了个雷

[虚拟机磁盘大小扩容后调整存储空间](https://club.fnnas.com/forum.php?mod=viewthread&tid=4513&highlight=)
