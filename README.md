# W&B Models 2時間コース

実験の指標、コード、出力ファイルを W&B に記録し、結果を比較するための教材です。

## 演習の順番

| 順番 | Notebook | 実行すること |
|---|---|---|
| 00 | [環境セットアップ](notebooks/00_setup/00_environment_setup.ipynb) | 接続先を設定し、1 run を作成 |
| 00b | [道路画像のセグメンテーション](notebooks/00_setup/01_segmentation_quickstart.ipynb) | U-Net を短く学習し、loss と予測マスクを W&B で見る |
| 01 | [基本の実験記録](notebooks/01_basics/01_minimal_tracking.ipynb) | 練習用の数値を記録。基本の1 runと比較用の2 runsを作成 |
| 02 | [コードと出力の保存](notebooks/01_basics/02_save_code_and_outputs.ipynb) | スクリプトを作成・実行し、コードと JSON / Markdown を保存 |
| 03 | [Hugging Face Trainer 連携](notebooks/02_integrations/01_integrations_overview.ipynb) | 小さなモデルを5 steps学習し、loss の自動記録を確認 |
| 04 | [Artifacts](notebooks/03_core/01_artifacts.ipynb) | ファイル・ディレクトリ・URI参照を登録し、別 run から利用 |
| 05 | [Tables と Media](notebooks/03_core/02_tables_media.ipynb) | 画像、音声、動画、Table、3D、分子構造、グラフを記録 |
| 06 | [Sweeps / Reports / Automations](notebooks/04_workflows/01_sweeps_reports_automations.ipynb) | 3条件の Sweep を実行。Report の構成と通知の用途を確認 |

Media は画像と Table を授業中に試し、残りを後から参照する使い方もできます。
Reports と Automations は説明のみです。通知設定には接続先の権限やプランが関係します。

## 接続先の設定

標準は **Multi-tenant SaaS** です。`WANDB_BASE_URL` が未設定または空欄なら `https://api.wandb.ai` を使います。

**Dedicated Cloud** の場合は、管理者から案内された接続先 URL を設定してください。
例: `https://your-org.wandb.io`。project や run のパスは付けません。
API key は **その接続先で発行したもの** を使います。

| 設定 | 内容 |
|---|---|
| `WANDB_API_KEY` | 接続先で発行した API key。ローカルでログイン済みなら省略可 |
| `WANDB_BASE_URL` | 任意。空欄は Multi-tenant SaaS、URL指定は Dedicated Cloud 等の接続先 |
| `WANDB_ENTITY` | 任意。実験を保存するチーム。空欄はアカウントの既定値 |
| `WANDB_PROJECT` | 任意。空欄は `models-initial-course` |

接続先を切り替えるときはカーネル／Colab ランタイムを再起動してください。

### Google Colab

各 Notebook の **Open in Colab** から開きます。
左サイドバーの **Secrets** に設定を登録し、Notebook からのアクセスを許可してください。
SaaS なら `WANDB_BASE_URL` の登録は不要です。他の任意設定は、それぞれ独立して読み込まれます。
共通コードは GitHub から取得するため、clone は不要です。

### ローカル

Python 3.10以上と [uv](https://docs.astral.sh/uv/getting-started/installation/) を用意します。

```bash
git clone https://github.com/nejumi/models-initial-course.git
cd models-initial-course
cp .env.example .env
# .env に接続先の API key と、必要な場合は Dedicated Cloud の URL を設定
uv venv --python 3.11 .venv
uv pip install --python .venv/bin/python -r requirements.txt
.venv/bin/python -m ipykernel install --prefix .venv --name models-initial-course --display-name "Models Course"
.venv/bin/jupyter lab
```

Notebook では **Models Course** カーネルを選び、上から実行します。
Windows では `.venv/bin/` を `.venv/Scripts/` に読み替え、環境ファイルをコピーしてください。
準備セルがリポジトリのルートに移動するため、Notebook のフォルダから開いても同じ `.env` と出力先を使います。
ローカルでは `.env` を読み込みます。すでに設定した環境変数を優先します。Colab では登録済みの Secrets を優先します。

## 実行環境

Python 3.10以上のローカルPC、Jupyter、Google Colabを想定しています。
GPU は必須ではありません。導入のセグメンテーションでは CUDA GPU があれば使い、なければ CPU で学習します。
初回はパッケージ、CamVid tiny、ResNet18 の重みをダウンロードします。
ネットワーク制限がある環境では、それぞれの配布元へのアクセスが必要です。

## 動作確認

```bash
make test
make test-offline
# GPU を使わない経路も確認する場合
.venv/bin/python scripts/execute_notebooks.py --offline --cpu
# 接続先と API key を設定して、Artifacts / Sweep を含む全教材を実行
make test-notebooks
```

オフライン検証は W&B への送信を止め、学習・ファイル生成・media のシリアライズを確認します。
パッケージやデータの初回ダウンロードにはインターネット接続が必要です。
サーバーへのアップロード、W&B App の表示、Artifact の取得、Sweep はオンライン確認が必要です。
実行結果と失敗セルの出力は `outputs/executed/` に保存されます。

[検証環境・結果・未確認の範囲](docs/validation.md) を記録しています。

## 教材を編集する方へ

[スライド制作メモ](docs/wandb-models-course-claude-design-brief.md) は講師・制作者向けです。

API key や `.env` を Notebook、Git、W&B の保存対象に含めないでください。
Artifact の `file://` 参照は同じファイルにアクセスできる環境でのみ利用できます。
