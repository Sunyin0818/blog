---
title: 全自动追剧方案-serr
categories:
  - area
tags:
  - NAS
publish: true
date: 2025-02-25 09:32:54
lastmod: 2025-03-05 10:27:09
---
```yaml
services:
  # 资源索引器（PT）
  # Jackett: https://hub.docker.com/r/linuxserver/jackett
  #  jackett:
  #    image: linuxserver/jackett:latest
  #    container_name: jackett
  #    hostname: jackett
  #    restart: unless-stopped
  #    environment:
  #      - PUID=1000 # UserID
  #      - PGID=1000 # GroupID
  #      - TZ=Asia/Shanghai
  #      - AUTO_UPDATE=true
  #    ports:
  #      - 9117:9117
  #    volumes:
  #      - ./jackett/config:/config

  # 资源索引器（BT）
  # Prowlarr: https://hub.docker.com/r/linuxserver/prowlarr
  prowlarr:
    image: linuxserver/prowlarr:latest
    container_name: prowlarr
    hostname: prowlarr
    restart: unless-stopped
    environment:
      - PUID=1000 # UserID
      - PGID=1000 # GroupID
      - TZ=Asia/Shanghai
    ports:
      - 9696:9696
    volumes:
      - ./prowlarr/config:/config

  # 资源索引器插件（解决 CloudFlare 5秒盾）
  # FlareSolverr: https://hub.docker.com/r/flaresolverr/flaresolverr
  flaresolverr:
    image: flaresolverr/flaresolverr:latest
    container_name: flaresolverr
    hostname: flaresolverr
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
      - LOG_LEVEL=info

  # 资源刮削器（电影）
  # Radarr: https://hub.docker.com/r/linuxserver/radarr
  radarr:
    image: linuxserver/radarr:latest
    container_name: radarr
    hostname: radarr
    restart: unless-stopped
    environment:
      - PUID=1000 # UserID
      - PGID=1000 # GroupID
      - TZ=Asia/Shanghai
    ports:
      - 7878:7878
    volumes:
      - ./radarr/config:/config
      - /vol2/1000/media:/media # 影音&下载根目录

  # 资源刮削器（电视剧&动漫）
  # Sonarr: https://hub.docker.com/r/linuxserver/sonarr
  sonarr:
    image: linuxserver/sonarr:latest
    container_name: sonarr
    hostname: sonarr
    restart: unless-stopped
    environment:
      - PUID=1000 # UserID
      - PGID=1000 # GroupID
      - TZ=Asia/Shanghai
    ports:
      - 8989:8989
    volumes:
      - ./sonarr/config:/config
      - /vol2/1000/media:/media # 影音&下载根目录

  # 资源聚合搜索
  # Jellyseerr: https://hub.docker.com/r/fallenbagel/jellyseerr
  jellyseerr:
    image: fallenbagel/jellyseerr:latest
    container_name: jellyseerr
    hostname: jellyseerr
    restart: unless-stopped
    environment:
      - TZ=Asia/Shanghai
      - LOG_LEVEL=debug
    ports:
      - 5055:5055
    volumes:
      - ./jellyseerr/config:/app/config

networks:
  default:
    name: media_center
    #external: true

```

