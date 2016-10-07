There are two methods to deplloy this server depending on the scene.

# Containers are in the same host and can be linked

Example of `docker-compose.yml`

```yml
oj_web_server:
    environment:
        - judger_token=SOME TOKEN
    ports:
        - "0.0.0.0:8000:8080"

judge_server:
    links:
        - oj_web_server:oj_web_server
    ports:
        - "127.0.0.1::8080"
```

When containers are linked, `judge_server` can get environment variable `OJ_WEB_SERVER_ENV_judger_token` as token， get `OJ_WEB_SERVER_PORT_8080_TCP_ADDR` as server ip， get `OJ_WEB_SERVER_PORT_8080_TCP_PORT` as server port. As a result, `judge_server` can send heartbeat request to `oj_web_server`.
 
# Containers are deployed in multi hosts
 
 Three environment variables below must be set manully in `docker-compose.yml`
 
  - `service_discovery_url`
  - `judger_token`
  - `service_url`

  `judge_server` will send heartbeat request to `service_discovery_url`.
  
  `service_url` is used to tell server to send task to this url(`judge_server`).

Example of `docker-compose.yml`

```yml
judge_server:
    - environment
        - judger_token=SOME TOKEN
        - service_discovery_url=http://onlinejudge.com/api/judge_server
        - service_url=http://1.2.3.4:8005
    - ports:
        - "0.0.0.0:8005:8080"
```

# Heartbeat request

 - Method `POST`
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

