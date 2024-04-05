# Build

## Container Image

### API

```bash
git clone https://github.com/QingdaoU/OnlineJudge.git
cd OnlineJudge
docker buildx build . -t oj-image/backend:1.6.0 --load
```

### Judge Server

```bash
git clone https://github.com/QingdaoU/JudgeServer.git
cd JudgeServer
docker buildx build . -t oj-image/judge:1.6.0 --load
```
