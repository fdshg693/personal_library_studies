-- PostgreSQL 拡張機能の初期化スクリプト

-- クエリパフォーマンス分析用
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- 全文検索用（日本語対応）
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- UUID生成用
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- 暗号化関数
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- ベクトル検索用（AI/ML用途）
-- CREATE EXTENSION IF NOT EXISTS vector;  -- pgvectorが利用可能な場合

-- 地理空間データ用（必要に応じて）
-- CREATE EXTENSION IF NOT EXISTS postgis;

-- メッセージキュー用
-- CREATE EXTENSION IF NOT EXISTS pgq;

-- タイムスケールDB（時系列データ用）
-- CREATE EXTENSION IF NOT EXISTS timescaledb;

-- 初期化完了メッセージ
DO $$
BEGIN
    RAISE NOTICE 'PostgreSQL extensions initialized successfully!';
END $$;
