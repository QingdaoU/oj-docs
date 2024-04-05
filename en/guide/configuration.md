# Configuration

## Environment variables

### Web Backend

| Name | Default Value | Description |
| ---- | ------------- | ----------- |
| POSTGRES_HOST | `postgres` | Postgres connection host |
| POSTGRES_PORT | `5432` | Postgres connection port |
| POSTGRES_DB | `onlinejudge` | Postgres database name |
| POSTGRES_USER | `onlinejudge` | Postgres user name |
| POSTGRES_PASSWORD | `onlinejudge` | Postgres user password |
| REDIS_HOST | `redis` | Redis connection host |
| REDIS_PORT | `6379` | Redis connection port |
| JUDGE_SERVER_TOKEN | (empty) | Password used in judge server authentication |

### Judge Server

| Name | Default Value | Description |
| ---- | ------------- | ----------- |
| JUDGE_SERVER_TOKEN | (empty) | Password used in judge server authentication |
| BACKEND_URL | (empty) | Judge server will send heartbeats to this URL (API server) every five seconds |
| SERVICE_URL | (empty) | API server will send tasks to this URL (judge server) |
| judger_debug | (empty) | If value is 1, enable debug logging, judge cases will not be deleted |
