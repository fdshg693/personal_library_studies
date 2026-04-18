# A2A / ADK エージェントの Cloud Run デプロイ用 Makefile
# 参考: https://adk.dev/deploy/cloud-run/#deploy-using-gcloud

# ==== .env の読み込み ====
# この Makefile と同階層の .env を読み込む。
# 優先順位: .env > shell の環境変数 > デフォルト値
# (`include` による代入は環境変数より優先される。shell 側を優先したい場合は
#  `make -e` を付けて実行するか、.env から該当行を消して shell で export する)
ENV_FILE := $(dir $(lastword $(MAKEFILE_LIST))).env
ifneq (,$(wildcard $(ENV_FILE)))
    include $(ENV_FILE)
    export
endif

# ==== 設定 (環境変数 / .env で上書き可) ====
GOOGLE_CLOUD_PROJECT     ?= your-gcp-project-id
GOOGLE_CLOUD_LOCATION    ?= us-central1
SERVICE_NAME             ?= capital-agent-service
GOOGLE_GENAI_USE_VERTEXAI ?= True
# Vertex AI を使わず API キー方式にする場合はこちらを設定
GOOGLE_API_KEY           ?=

# ==== 便利コマンド ====
.PHONY: help auth config env enable-apis grant-roles update-env setup install run deploy deploy-adk logs describe url open delete clean

help:
	@echo "利用可能なターゲット:"
	@echo "  make auth         - gcloud にログイン"
	@echo "  make config       - gcloud のプロジェクトを設定"
	@echo "  make env          - 必要な環境変数を表示"
	@echo "  make enable-apis  - Vertex AI / Cloud Run など必要な API を有効化"
	@echo "  make grant-roles  - Cloud Run のサービスアカウントに必要なロールを付与"
	@echo "  make update-env   - デプロイ済みサービスの環境変数を更新"
	@echo "  make setup        - enable-apis + grant-roles をまとめて実行"
	@echo "  make install      - requirements.txt を pip でインストール"
	@echo "  make run          - ローカルで FastAPI サーバを起動"
	@echo "  make deploy       - gcloud run deploy で Cloud Run にデプロイ"
	@echo "  make deploy-adk   - adk CLI で Cloud Run にデプロイ"
	@echo "  make logs         - Cloud Run のログを表示"
	@echo "  make describe     - サービスの詳細を表示"
	@echo "  make url          - デプロイ済みサービスの URL を取得"
	@echo "  make open         - URL をブラウザで開く"
	@echo "  make delete       - Cloud Run サービスを削除"
	@echo "  make clean        - ローカルの生成物を削除"

# gcloud 認証
auth:
	gcloud auth login
	gcloud auth application-default login

# プロジェクト設定
config:
	gcloud config set project $(GOOGLE_CLOUD_PROJECT)

# 現在の設定値を確認
env:
	@echo "GOOGLE_CLOUD_PROJECT      = $(GOOGLE_CLOUD_PROJECT)"
	@echo "GOOGLE_CLOUD_LOCATION     = $(GOOGLE_CLOUD_LOCATION)"
	@echo "SERVICE_NAME              = $(SERVICE_NAME)"
	@echo "GOOGLE_GENAI_USE_VERTEXAI = $(GOOGLE_GENAI_USE_VERTEXAI)"
	@echo "GOOGLE_API_KEY            = $(if $(GOOGLE_API_KEY),***set***,(unset))"

# 必要な Google Cloud API を一括有効化
enable-apis:
	gcloud services enable \
		aiplatform.googleapis.com \
		run.googleapis.com \
		cloudbuild.googleapis.com \
		artifactregistry.googleapis.com \
		iam.googleapis.com \
		--project=$(GOOGLE_CLOUD_PROJECT)

# Cloud Run のデフォルトサービスアカウント (<プロジェクト番号>-compute@...) に
# Vertex AI 呼び出し用のロールを付与
grant-roles:
	@PROJECT_NUMBER=$$(gcloud projects describe $(GOOGLE_CLOUD_PROJECT) --format='value(projectNumber)'); \
	SA="$${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"; \
	echo "サービスアカウント: $$SA にロールを付与します"; \
	gcloud projects add-iam-policy-binding $(GOOGLE_CLOUD_PROJECT) \
		--member="serviceAccount:$$SA" \
		--role="roles/aiplatform.user" \
		--condition=None; \
	gcloud projects add-iam-policy-binding $(GOOGLE_CLOUD_PROJECT) \
		--member="serviceAccount:$$SA" \
		--role="roles/run.invoker" \
		--condition=None

# デプロイ済み Cloud Run サービスの環境変数を上書き更新
update-env:
	gcloud run services update $(SERVICE_NAME) \
		--region=$(GOOGLE_CLOUD_LOCATION) \
		--project=$(GOOGLE_CLOUD_PROJECT) \
		--update-env-vars="GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT),GOOGLE_CLOUD_LOCATION=$(GOOGLE_CLOUD_LOCATION),GOOGLE_GENAI_USE_VERTEXAI=$(GOOGLE_GENAI_USE_VERTEXAI)"

# 初期セットアップ (API 有効化 + ロール付与)
setup: enable-apis grant-roles
	@echo "セットアップ完了。続けて make deploy-adk を実行してください。"

# 依存インストール (ローカル実行用)
install:
	pip install -r requirements.txt

# ローカル起動
run:
	PORT=8080 python main.py

# gcloud を使った Cloud Run デプロイ
deploy:
	gcloud run deploy $(SERVICE_NAME) \
		--source . \
		--region $(GOOGLE_CLOUD_LOCATION) \
		--project $(GOOGLE_CLOUD_PROJECT) \
		--allow-unauthenticated \
		--set-env-vars="GOOGLE_CLOUD_PROJECT=$(GOOGLE_CLOUD_PROJECT),GOOGLE_CLOUD_LOCATION=$(GOOGLE_CLOUD_LOCATION),GOOGLE_GENAI_USE_VERTEXAI=$(GOOGLE_GENAI_USE_VERTEXAI)"

# adk CLI を使ったデプロイ (推奨)
deploy-adk:
	adk deploy cloud_run \
		--project=$(GOOGLE_CLOUD_PROJECT) \
		--region=$(GOOGLE_CLOUD_LOCATION) \
		--service_name=$(SERVICE_NAME) \
		--with_ui \
		--a2a \
		.

# ログ確認
logs:
	gcloud run services logs read $(SERVICE_NAME) \
		--region $(GOOGLE_CLOUD_LOCATION) \
		--project $(GOOGLE_CLOUD_PROJECT) \
		--limit 50

# サービス詳細
describe:
	gcloud run services describe $(SERVICE_NAME) \
		--region $(GOOGLE_CLOUD_LOCATION) \
		--project $(GOOGLE_CLOUD_PROJECT)

# URL 取得
url:
	@gcloud run services describe $(SERVICE_NAME) \
		--region $(GOOGLE_CLOUD_LOCATION) \
		--project $(GOOGLE_CLOUD_PROJECT) \
		--format='value(status.url)'

# ブラウザで開く
open:
	xdg-open "$$($(MAKE) -s url)" 2>/dev/null || \
	  explorer.exe "$$($(MAKE) -s url)" 2>/dev/null || \
	  echo "ブラウザを手動で開いてください: $$($(MAKE) -s url)"

# サービス削除
delete:
	gcloud run services delete $(SERVICE_NAME) \
		--region $(GOOGLE_CLOUD_LOCATION) \
		--project $(GOOGLE_CLOUD_PROJECT) \
		--quiet

# ローカル生成物を削除
clean:
	rm -f sessions.db
	find . -type d -name __pycache__ -exec rm -rf {} +
