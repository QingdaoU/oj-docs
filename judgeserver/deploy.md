# Deploy

Reuqirements:

  - docker >= 1.12
  - docker-compose >= 1.8

Docker images:

  - docker pull registry.cn-hangzhou.aliyuncs.com/onlinejudge/judge_server

Three environment variables below must be set manually in `docker-compose.yml`
 
  - `SERVICE_URL`
  - `BACKEND_URL`
  - `TOKEN`

`judge_server` will send heartbeat request to `backend_url` every five seconds.
  
`service_url` is used to tell server to send task to this url(`judge_server`).

# Heartbeat request

  - `Method`: `POST`
  - `X-JUDGE-SERVER-TOKEN`: `sha256(token).hex`
  - `Content-Type`: `application/json`

Request data

```js
 {
    "judger_version": "2.0.1",
    "hostname": "c45acd557074",
    "running_task_number": 2,
    "cpu_core": 1,
    "memory": 30.3,
    "action": "heartbeat",
    "cpu": 0,
    "service_url": null or "http://1.2.3.4:8005"
}
```

If everything is OK, you should give a JSON response as follows

```js
{
    "data": "success",
    "error": null
}
```

