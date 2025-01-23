---
title: PVE下飞牛扩容
category:
  - area
tags:
  - PVE
publish: true
date: 2025-01-23 11:43:43
lastmod: 2025-01-23 13:58:34
---
# 背景

PVE安装的飞牛，原有分配了一个200G数据盘，和一个1T的媒体盘

媒体太多不够放了，遂在PVE中调整磁盘大小，增加了200G

但是飞牛中不能正常使用扩充的容量

版本信息：

+ fnOS：`0.8.36`
+ PVE：`8.2.7`


# 解决方案

首先使用 `fdisk -l`查询磁盘信息得到相关内容如下：

![](/_assets/Pasted%20image%2020250123114441.png)


![](/_assets/Pasted%20image%2020250123114531.png)


## 扩展分区

使用 `fdisk /dev/sdc`编辑分区表，输入 `p`查询当前分区表：

![](/_assets/Pasted%20image%2020250123114826.png)

使用 `d`命令删除分区

![](/_assets/Pasted%20image%2020250123115028.png)

`n`命令新建分区（不删除原有的LVM标记）

![](/_assets/Pasted%20image%2020250123115052.png)

`t`命令修改分区类型为`42`（Linux Raid），跟飞牛原有的保持一致

![](/_assets/420c6fdd023f0637bf407486b21be4ab_MD5.png)

![](/_assets/Pasted%20image%2020250123115139.png)

![](/_assets/Pasted%20image%2020250123115235.png)

修改完成后我们使用 `w`保存并退出

![](/_assets/Pasted%20image%2020250123115251.png)

至此，我们成功为分区扩容，可以使用 `fdisk -l`查看

![](/_assets/Pasted%20image%2020250123115321.png)

接下来我们要对LVM进行扩容

## 扩展LVM

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

### 扩展PV

使用 `pvdisplay`查看当前PV，发现与该存储空间相关的一个PV如下

![](/_assets/Pasted%20image%2020250123120325.png)

先让PV卷使用底层磁盘全部空间

```bash
 mdadm --grow /dev/md1 --size=max
```
![](/_assets/Pasted%20image%2020250123120231.png)

然后使用 `pvresize /dev/md1`扩展

![](/_assets/Pasted%20image%2020250123120449.png)

此时再次 `pvdisplay`得到

![](/_assets/Pasted%20image%2020250123120527.png)

使用 `vgdisplay`查看VG

![](/_assets/Pasted%20image%2020250123120558.png)

至此，PV与VG扩容成功（VG不需要手动调整）

### 扩容LV

使用 `lvdisplay`查看当前LV

![](/_assets/Pasted%20image%2020250123120731.png)

将当前LV扩容，扩容的大小为所属的VG的所有空余空间，命令为
```bash
lvresize -l +100%FREE /dev/trim_526c72bb_b792_47a0_98de_fc3a1419269d/0
```

![](/_assets/Pasted%20image%2020250123120824.png)

此时 `lvdisplay`

![](/_assets/Pasted%20image%2020250123120849.png)

至此，LV扩容成功

## 调整文件系统

在完成上述操作后，我们再次查看nas的web界面发现仍未扩容，原因是虽然LV扩容成功，但文件系统仍旧没有使用扩容的空间。我们可以使用 `df -h`查看

![](/_assets/Pasted%20image%2020250123120925.png)

因此我们还需对文件系统进行调整使其使用新分配的空间。

```bash
btrfs filesystem resize max /vol2
```

![](/_assets/Pasted%20image%2020250123135608.png)

之后使用 `df -h`查看

![](/_assets/Pasted%20image%2020250123135639.png)

此时再回到web界面查看发现扩容成功~

![](/_assets/Pasted%20image%2020250123135715.png)


# 总结


首先在fdisk中扩展分区（d, n），其次扩展pv（`pvresize`），lv（`lvresize`），最后调整文件系统大小（`btrfs filesystem resize max`）



# 参考

感谢论坛的帖子，评论区帮我排了个雷

[虚拟机磁盘大小扩容后调整存储空间](https://club.fnnas.com/forum.php?mod=viewthread&tid=4513&highlight=)

