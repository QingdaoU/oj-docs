# Upgrade

## Minor Updates

If no breaking changes between two versions, we can just update deploy config and restart.

```bash
git pull
git checkout $version
docker compose up -d
```
