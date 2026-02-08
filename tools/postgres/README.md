# PostgreSQL Docker 環境

開発・学習用の PostgreSQL Docker 環境です。パフォーマンスチューニング済みの設定と、管理ツール（pgAdmin）も含まれています。

## 📋 目次

- [クイックスタート](#クイックスタート)
- [構成](#構成)
- [接続情報](#接続情報)
- [基本操作](#基本操作)
- [パフォーマンスチューニング](#パフォーマンスチューニング)
- [監視とメンテナンス](#監視とメンテナンス)
- [発展的な使い方](#発展的な使い方)
- [トラブルシューティング](#トラブルシューティング)

---

## 🚀 クイックスタート

### 1. 起動

```bash
cd tools/postgres
docker-compose up -d
```

### 2. 接続確認

```bash
# PostgreSQLに接続
docker-compose exec postgres psql -U postgres -d testdb

# または
psql -h localhost -U postgres -d testdb
```

### 3. 停止

```bash
docker-compose down

# データも削除する場合
docker-compose down -v
```

---

## 📦 構成

```
tools/postgres/
├── Dockerfile              # PostgreSQLイメージ定義
├── docker-compose.yml      # サービス構成
├── postgresql.conf         # チューニング済み設定ファイル
├── init/                   # 初期化スクリプト
│   ├── 01_create_extensions.sql
│   └── 02_create_sample_tables.sql
└── README.md
```

### 含まれるサービス

- **PostgreSQL 16**: メインデータベース
- **pgAdmin 4**: Web ベースの管理ツール（オプション）

---

## 🔐 接続情報

### PostgreSQL

| 項目         | 値        |
| ------------ | --------- |
| ホスト       | localhost |
| ポート       | 5432      |
| ユーザー     | postgres  |
| パスワード   | postgres  |
| データベース | testdb    |

**接続文字列例:**

```
postgresql://postgres:postgres@localhost:5432/testdb
```

### pgAdmin

- URL: http://localhost:5050
- Email: admin@example.com
- Password: admin

---

## 🛠️ 基本操作

### データベース管理

```sql
-- データベース一覧
\l

-- テーブル一覧
\dt

-- テーブル構造確認
\d users

-- データベース作成
CREATE DATABASE mydb;

-- データベース削除
DROP DATABASE mydb;
```

### パフォーマンス分析

```sql
-- 実行中のクエリ確認
SELECT pid, usename, application_name, state, query, query_start
FROM pg_stat_activity
WHERE state != 'idle'
ORDER BY query_start;

-- スロークエリ統計（pg_stat_statements）
SELECT
    calls,
    total_exec_time,
    mean_exec_time,
    query
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;
```

---

## ⚡ パフォーマンスチューニング

### 1. メモリ設定の調整

現在の設定は **2GB システムメモリ** を想定しています。

#### メモリ別推奨設定

**4GB メモリの場合** (`postgresql.conf` を編集):

```conf
shared_buffers = 1GB
effective_cache_size = 3GB
work_mem = 32MB
maintenance_work_mem = 256MB
```

**8GB メモリの場合**:

```conf
shared_buffers = 2GB
effective_cache_size = 6GB
work_mem = 64MB
maintenance_work_mem = 512MB
```

**計算式:**

- `shared_buffers`: システムメモリの 25%
- `effective_cache_size`: システムメモリの 50-75%
- `work_mem`: (RAM - shared_buffers) / (max_connections \* 3)
- `maintenance_work_mem`: システムメモリの 5-10%（最大 2GB）

### 2. ストレージタイプ別の最適化

#### SSD の場合（デフォルト）

```conf
random_page_cost = 1.1
effective_io_concurrency = 200
```

#### HDD の場合

```conf
random_page_cost = 4.0
effective_io_concurrency = 2
```

### 3. 接続数の調整

```conf
max_connections = 100        # 軽い負荷
max_connections = 200        # 中程度の負荷
max_connections = 300        # 高負荷
```

**注意**: 接続数を増やす場合は `work_mem` を減らす必要があります。

### 4. クエリプランの最適化

```sql
-- 統計情報の更新
ANALYZE;

-- テーブル全体の統計更新
VACUUM ANALYZE table_name;

-- インデックスの最適化
REINDEX INDEX index_name;

-- クエリプランの確認
EXPLAIN ANALYZE
SELECT * FROM users WHERE email = 'user1@example.com';
```

### 5. インデックス戦略

```sql
-- B-tree インデックス（デフォルト、一般的な検索用）
CREATE INDEX idx_users_email ON users(email);

-- 部分インデックス（条件付き）
CREATE INDEX idx_active_users ON users(email) WHERE active = true;

-- 複合インデックス
CREATE INDEX idx_users_name_email ON users(last_name, first_name, email);

-- GIN インデックス（配列・JSONB用）
CREATE INDEX idx_tags_gin ON articles USING GIN(tags);

-- GiST インデックス（全文検索用）
CREATE INDEX idx_content_gist ON articles USING GiST(to_tsvector('english', content));

-- インデックスの使用状況確認
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

---

## 📊 監視とメンテナンス

### 1. データベースサイズの監視

```sql
-- データベースサイズ
SELECT
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
ORDER BY pg_database_size(pg_database.datname) DESC;

-- テーブルサイズ
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
```

### 2. 接続数の監視

```sql
-- 現在の接続数
SELECT count(*) FROM pg_stat_activity;

-- データベース別接続数
SELECT
    datname,
    count(*) as connections
FROM pg_stat_activity
GROUP BY datname
ORDER BY connections DESC;
```

### 3. キャッシュヒット率

```sql
-- キャッシュヒット率（95%以上が理想）
SELECT
    sum(heap_blks_read) as heap_read,
    sum(heap_blks_hit) as heap_hit,
    sum(heap_blks_hit) / (sum(heap_blks_hit) + sum(heap_blks_read)) as ratio
FROM pg_statio_user_tables;
```

### 4. デッドタプルの確認

```sql
-- デッドタプルの確認
SELECT
    schemaname,
    tablename,
    n_live_tup,
    n_dead_tup,
    round(n_dead_tup * 100.0 / NULLIF(n_live_tup + n_dead_tup, 0), 2) AS dead_ratio
FROM pg_stat_user_tables
WHERE n_dead_tup > 0
ORDER BY n_dead_tup DESC;
```

### 5. VACUUM の実行

```sql
-- 通常の VACUUM
VACUUM table_name;

-- 完全な VACUUM（テーブルロック発生）
VACUUM FULL table_name;

-- ANALYZE も同時実行
VACUUM ANALYZE table_name;

-- 自動 VACUUM の設定確認
SELECT
    relname,
    last_vacuum,
    last_autovacuum,
    last_analyze,
    last_autoanalyze
FROM pg_stat_user_tables
ORDER BY last_autovacuum;
```

---

## 🚀 発展的な使い方

### 1. パーティショニング

大規模テーブルの管理に有効です。

```sql
-- 範囲パーティショニング（日付別）
CREATE TABLE measurements (
    id SERIAL,
    measured_at TIMESTAMP NOT NULL,
    temperature FLOAT,
    humidity FLOAT
) PARTITION BY RANGE (measured_at);

-- 月別パーティション作成
CREATE TABLE measurements_2024_01 PARTITION OF measurements
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

CREATE TABLE measurements_2024_02 PARTITION OF measurements
FOR VALUES FROM ('2024-02-01') TO ('2024-03-01');

-- リストパーティショニング（地域別）
CREATE TABLE sales (
    id SERIAL,
    region TEXT,
    amount DECIMAL
) PARTITION BY LIST (region);

CREATE TABLE sales_asia PARTITION OF sales
FOR VALUES IN ('Japan', 'China', 'Korea');

CREATE TABLE sales_europe PARTITION OF sales
FOR VALUES IN ('UK', 'Germany', 'France');
```

### 2. レプリケーション

#### ストリーミングレプリケーション

`docker-compose.yml` に追加:

```yaml
postgres-replica:
  build: .
  container_name: personal_library_postgres_replica
  environment:
    POSTGRES_USER: postgres
    POSTGRES_PASSWORD: postgres
    PGDATA: /var/lib/postgresql/data/pgdata
  ports:
    - "5433:5432"
  command: |
    bash -c "
      until pg_basebackup --pgdata=/var/lib/postgresql/data/pgdata -R --slot=replication_slot --host=postgres --port=5432
      do
        echo 'Waiting for primary to connect...'
        sleep 1s
      done
      echo 'Backup done, starting replica...'
      postgres
    "
  depends_on:
    - postgres
  networks:
    - postgres_network
```

プライマリサーバーの設定（`postgresql.conf`）:

```conf
wal_level = replica
max_wal_senders = 10
max_replication_slots = 10
hot_standby = on
```

### 3. コネクションプーリング（PgBouncer）

`docker-compose.yml` に追加:

```yaml
pgbouncer:
  image: pgbouncer/pgbouncer:latest
  container_name: personal_library_pgbouncer
  environment:
    DATABASES_HOST: postgres
    DATABASES_PORT: 5432
    DATABASES_USER: postgres
    DATABASES_PASSWORD: postgres
    DATABASES_DBNAME: testdb
    PGBOUNCER_POOL_MODE: transaction
    PGBOUNCER_MAX_CLIENT_CONN: 1000
    PGBOUNCER_DEFAULT_POOL_SIZE: 25
  ports:
    - "6432:6432"
  depends_on:
    - postgres
  networks:
    - postgres_network
```

接続: `postgresql://postgres:postgres@localhost:6432/testdb`

### 4. 全文検索

```sql
-- 全文検索用カラム追加
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- トリガーで自動更新
CREATE TRIGGER tsvector_update BEFORE INSERT OR UPDATE
ON articles FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', title, content);

-- GINインデックス作成
CREATE INDEX idx_search_vector ON articles USING GIN(search_vector);

-- 検索実行
SELECT title, content
FROM articles
WHERE search_vector @@ to_tsquery('english', 'postgresql & performance');

-- 日本語全文検索（pg_bigm 拡張使用）
CREATE EXTENSION pg_bigm;
CREATE INDEX idx_content_bigm ON articles USING gin (content gin_bigm_ops);
SELECT * FROM articles WHERE content LIKE '%PostgreSQL%';
```

### 5. ベクトル検索（AI/ML用）

pgvector 拡張を使用:

```sql
-- 拡張機能の有効化
CREATE EXTENSION vector;

-- ベクトルカラムを持つテーブル
CREATE TABLE embeddings (
    id SERIAL PRIMARY KEY,
    content TEXT,
    embedding vector(1536)  -- OpenAI埋め込みの次元数
);

-- インデックス作成（IVFFlat）
CREATE INDEX ON embeddings USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- 類似検索
SELECT content
FROM embeddings
ORDER BY embedding <-> '[0.1, 0.2, ...]'::vector
LIMIT 5;
```

### 6. JSONB の活用

```sql
-- JSONBカラムを持つテーブル
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name TEXT,
    attributes JSONB
);

-- GINインデックス
CREATE INDEX idx_attributes ON products USING GIN(attributes);

-- データ挿入
INSERT INTO products (name, attributes) VALUES
('Laptop', '{"brand": "Dell", "ram": 16, "storage": "512GB SSD"}'),
('Mouse', '{"brand": "Logitech", "wireless": true, "dpi": 1600}');

-- クエリ
SELECT * FROM products WHERE attributes @> '{"brand": "Dell"}';
SELECT * FROM products WHERE attributes->>'wireless' = 'true';
SELECT * FROM products WHERE attributes->'ram' > '8';
```

### 7. マテリアライズドビュー

```sql
-- マテリアライズドビューの作成
CREATE MATERIALIZED VIEW user_statistics AS
SELECT
    date_trunc('day', created_at) as day,
    count(*) as user_count,
    count(*) FILTER (WHERE email LIKE '%@gmail.com') as gmail_users
FROM users
GROUP BY day;

-- インデックス作成
CREATE INDEX idx_user_stats_day ON user_statistics(day);

-- データ更新
REFRESH MATERIALIZED VIEW user_statistics;

-- 同時実行可能な更新
REFRESH MATERIALIZED VIEW CONCURRENTLY user_statistics;
```

### 8. 時系列データの最適化

TimescaleDB を使用する場合:

```sql
-- 拡張機能の有効化
CREATE EXTENSION timescaledb;

-- ハイパーテーブルの作成
CREATE TABLE sensor_data (
    time TIMESTAMPTZ NOT NULL,
    sensor_id INTEGER,
    temperature DOUBLE PRECISION,
    humidity DOUBLE PRECISION
);

SELECT create_hypertable('sensor_data', 'time');

-- 連続集約
CREATE MATERIALIZED VIEW sensor_data_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) as bucket,
    sensor_id,
    avg(temperature) as avg_temp,
    max(temperature) as max_temp,
    min(temperature) as min_temp
FROM sensor_data
GROUP BY bucket, sensor_id;
```

---

## 🐛 トラブルシューティング

### 問題: 接続できない

```bash
# コンテナの状態確認
docker-compose ps

# ログ確認
docker-compose logs postgres

# ポートの確認
netstat -an | findstr 5432
```

### 問題: パフォーマンスが遅い

1. **スロークエリの確認**

```sql
SELECT * FROM pg_stat_statements
ORDER BY total_exec_time DESC
LIMIT 10;
```

2. **インデックスの確認**

```sql
-- 未使用のインデックス
SELECT
    schemaname,
    tablename,
    indexname,
    idx_scan
FROM pg_stat_user_indexes
WHERE idx_scan = 0;
```

3. **VACUUM の実行**

```sql
VACUUM ANALYZE;
```

### 問題: ディスク容量不足

```sql
-- 不要なデータの削除
DELETE FROM old_table WHERE created_at < NOW() - INTERVAL '1 year';

-- VACUUM FULL でディスク領域回収
VACUUM FULL table_name;
```

### 問題: 設定変更が反映されない

```bash
# 設定再読み込み
docker-compose exec postgres psql -U postgres -c "SELECT pg_reload_conf();"

# または再起動
docker-compose restart postgres
```

---

## 📚 参考リソース

- [PostgreSQL 公式ドキュメント](https://www.postgresql.org/docs/)
- [PostgreSQL チューニングガイド](https://wiki.postgresql.org/wiki/Tuning_Your_PostgreSQL_Server)
- [PgTune](https://pgtune.leopard.in.ua/) - 設定自動生成ツール
- [pgAdmin ドキュメント](https://www.pgadmin.org/docs/)
- [explain.depesz.com](https://explain.depesz.com/) - クエリプラン可視化

---

## 📝 ライセンス

このプロジェクトは学習・開発用途に自由に使用できます。

---

## 🤝 貢献

改善提案やバグ報告は Issue または Pull Request でお願いします。
