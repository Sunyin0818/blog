---
title: Caddy离线手动安装
categories:
  - resource
tags:
  - 工具折腾
publish: true
date: 2025-11-21 17:09:20
lastmod: 2025-11-25 10:27:16
---
> 参考[官方文档](https://caddyserver.com/docs/install)

# 1. 下载二进制文件
去下载即可 https://caddyserver.com/download

# 2. 安装为系统服务

## 2.1. 验证

+ `caddy`： 下载的二进制文件

```bash
sudo mv caddy /usr/bin/
caddy version
--V2.10.2 ...
```

Create a group named `caddy`:
```bash
sudo useradd --system \ 
--gid caddy \ 
--create-home \ 
--home-dir /var/lib/caddy \ 
--shell /usr/sbin/nologin \ 
--comment "Caddy web server" \ 
caddy
```

## 2.2. 安装为系统服务

创建systemd unit files

```bash
vi /etc/systemd/system/caddy.service
```

```ini
[Unit]
Description=Caddy
Documentation=https://caddyserver.com/docs/
After=network.target network-online.target
Requires=network-online.target

[Service]
Type=notify
User=caddy
Group=caddy
ExecStart=/usr/bin/caddy run --environ --config /etc/caddy/Caddyfile
ExecReload=/usr/bin/caddy reload --config /etc/caddy/Caddyfile --force
TimeoutStopSec=5s
LimitNOFILE=1048576
PrivateTmp=true
ProtectSystem=full
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE

[Install]
WantedBy=multi-user.target
```

# 3. Caddyfile

默认为`/etc/caddy/Caddyfile`

```caddyfile
:80 {
  # 要分发的文件目录（绝对路径，比如 /data/share）
  root * /data/share
  # 启用目录列表（让用户能看到文件夹结构）
  file_server browse
  encode gzip
}
```
