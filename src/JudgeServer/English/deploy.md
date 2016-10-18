# Deploy

Reuqirements:

  - docker >= 1.12
  - docker-compose >= 1.8

Three environment variables below must be set manully in `docker-compose.yml`
 
  - `service_discovery_url`
  - `judger_token`
  - `service_url`

`judge_server` will send heartbeat request to `service_discovery_url` every five seconds.
  
`service_url` is used to tell server to send task to this url(`judge_server`).

Example of `docker-compose.yml`

```yml
version: "2"
services:
    judge_server:
        image: judge_server
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
            - /data/JudgeServer/tests/test_case:/test_case:ro
            - /data/log:/log
            - /data/JudgeServer:/code:ro
        environment:
            - judger_token=token
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

