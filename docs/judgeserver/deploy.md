# Deploy

Reuqirements:

  - docker >= 1.12
  - docker-compose >= 1.8

Docker images:

  - docker pull qduoj/judge_server (from Docker Hub)
  - docker pull registry.cn-hangzhou.aliyuncs.com/v-image/judge_server && docker tag registry.cn-hangzhou.aliyuncs.com/v-image/judge_server qduoj/judge_server (from Aliyun mirror)

Three environment variables below must be set manually in `docker-compose.yml`
 
  - `service_discovery_url`
  - `service_url`

You should manually create `token.txt` to store `judger_token`.

`judge_server` will send heartbeat request to `service_discovery_url` every five seconds.
  
`service_url` is used to tell server to send task to this url(`judge_server`).

Example of `docker-compose.yml`

```yaml
version: "2"
services:
    judge_server:
        image: qduoj/judge_server
        cpu_quota: 90000
        read_only: true
        cap_drop:
            - SETPCAP
            - MKNOD
            - NET_BIND_SERVICE
            - SYS_CHROOT
            - SETFCAP
            - FSETID
        tmpfs:
            - /tmp
            - /judger_run:exec,mode=777
            - /spj:exec,mode=777
        volumes:
            - $PWD/tests/test_case:/test_case:ro
            - /data/log:/log
            - $PWD/server:/code:ro
            - $PWD/token.txt:/token.txt
        environment:
            - service_discovery_url=https://virusdefender.net/service.php
            - service_url=http://1.2.3.4:12358
        ports:
            - "0.0.0.0:12358:8080"
```

# Heartbeat request

  - `Method`: `POST`
  - `X-JUDGE-SERVER-TOKEN`: `sha256(token)`
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
    "err": null
}
```

