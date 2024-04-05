# Backup & Restore

## Database

- backup

  ```bash
  docker compose exec -T oj-postgres pg_dumpall -c -U onlinejudge > "db-$(date -Iseconds).sql"

  # zstd
  docker compose exec -T oj-postgres pg_dumpall -c -U onlinejudge | zstd -o "db-$(date -Iseconds).sql.zst"
  ```

- restore

  ```bash
  docker compose exec -T oj-postgres psql < "<backup file>"

  # zstd
  zstd -d "<backup file>" | docker compose exec postgres psql
  ```

## Testcase

- backup

  ```bash
  tar -cf "testcase-$(date -Iseconds).tar" data/backend/test_case

  # zstd
  tar --zstd -cf "testcase-$(date -Iseconds).tar.zst" data/backend/test_case
  ```

- restore

  ```bash
  tar -xf "<backup file>"

  # zstd
  tar --zstd -xf "<backup file>"
  ```
