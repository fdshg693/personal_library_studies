FROM postgres:16-alpine

# 環境変数の設定
ENV POSTGRES_USER=postgres
ENV POSTGRES_PASSWORD=postgres
ENV POSTGRES_DB=testdb
ENV PGDATA=/var/lib/postgresql/data/pgdata

# タイムゾーンの設定
ENV TZ=Asia/Tokyo

# 日本語ロケールのサポート
RUN apk add --no-cache \
    tzdata \
    && cp /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone

# カスタム設定ファイル用ディレクトリ
RUN mkdir -p /docker-entrypoint-initdb.d

# ポート公開
EXPOSE 5432

# ヘルスチェック
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
    CMD pg_isready -U $POSTGRES_USER -d $POSTGRES_DB || exit 1

# データボリューム
VOLUME ["/var/lib/postgresql/data"]
