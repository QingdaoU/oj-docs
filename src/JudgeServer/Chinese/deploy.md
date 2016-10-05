# 同主机link场景

  oj_web_server和judge_server在同一台服务器上，而且judge_server中link oj_web_server。
 
 oj_web_server需要设置环境变量`judger_token`，这样`judge_server`就可以在`OJ_WEB_SERVER_ENV_judger_token`环境变量中得到token，在`OJ_WEB_SERVER_PORT_8080_TCP_ADDR`得到ip，在`OJ_WEB_SERVER_PORT_8080_TCP_PORT`得到端口，从而每5秒向该ip发送心跳包，在HTTP头中携带了`X-JUDGE-SERVER-TOKEN`，值为token的sha256。
 
# 跨主机场景
 
 如果不在同一台服务器上，需要手动设置judge_server的下面四个环境变量
 
  - `service_discovery_url`
  - `judger_token`

  通过以上两个环境变量这样就可以向该url发送心跳包了
  
  - `service_host`
  - `service_port`

  因为跨主机的情况下，oj_web_server是无法得知judge_server的ip和端口的，需要主动的设置，然后在心跳包中会带上这两个信息，让oj_web_server能够主动访问。此时judge_server只能使用固定端口映射。


