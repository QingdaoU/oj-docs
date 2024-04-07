# Quickstart

## Requirements

- Docker server
  - Docker Engine (Linux)
  - Docker Desktop (Windows, macOS and Linux)
  - Colima (macOS)
  - OrbStack (macOS)
  - (others)
- Docker client
- Docker compose plugin

## Steps

1. Get necessary files from [QingdaoU/OnlineJudgeDeploy](https://github.com/QingdaoU/OnlineJudgeDeploy) releases.

   ```bash
   git clone -b v1.6.1 https://github.com/QingdaoU/OnlineJudgeDeploy.git
   ```

2. Pull and start services.

   ```bash
   docker compose up -d
   ```

3. Done!

!> Default account is `root` / `rootroot`, **please change the password as soon as possible**.
