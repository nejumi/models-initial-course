# W&B Models 2時間コース

W&B Models の基本を 2 時間で学ぶための教材リポジトリです。スライドの座学と notebook の演習が同じ順番で進むように構成しています。

## コース構成

| # | Notebook | スライドで学ぶこと | 実際に動かすこと |
|---|---|---|---|
| 00 | [環境セットアップ](notebooks/00_setup/00_environment_setup.ipynb) | ログイン、API key、Entity / Project / Run | W&B に 1 run 作成して疎通確認 |
| 01 | [init / log / finish](notebooks/01_basics/01_minimal_tracking.ipynb) | Run は実験ノート、config と metrics | 合成データで 2 runs を記録し比較 |
| 02 | [迷ったら残すテンプレート](notebooks/01_basics/02_save_code_and_outputs.ipynb) | `run.log_code` と `run.save` | JSON / Markdown を run に保存し、コードを記録 |
| 03 | [Integrations Overview](notebooks/02_integrations/01_integrations_overview.ipynb) | 既存 framework / OSS からの W&B 連携 | Hugging Face Trainer の W&B integration を実行 |
| 04 | [Artifacts](notebooks/03_core/01_artifacts.ipynb) | `run.save` と Artifact の使い分け、lineage | `add_file` / `add_dir` / `add_reference` と `use_artifact` |
| 05 | [Tables と Media](notebooks/03_core/02_tables_media.ipynb) | 定性評価、誤り分析、media logging | Image / overlay / Table / Audio / Video / HTML / 3D / Molecule / Plot を log |
| 06 | [Sweeps / Reports / Automations](notebooks/04_workflows/01_sweeps_reports_automations.ipynb) | 条件探索、共有、自動化 | 小さな sweep を 3 runs 実行し、Report/Automation の型を確認 |


## Notebook の方針

- 00-03 は初学者が章の焦点にすぐ入れるよう、W&B の本題コードを短くしています。
- 04 Artifacts と 05 Tables/Media は、講座後にも参照できる実例集として、近い API パターンを複数含めています。
- Colab で notebook 単体を開いた場合でも動くよう、共通 helper は必要に応じて GitHub raw から取得します。ローカルで `git clone` することは必須ではありません。

## セットアップ

### ローカル

```bash
cp .env.example .env
# .env に WANDB_API_KEY を設定
uv venv .venv
uv pip install --python .venv/bin/python -r requirements.txt
```

### Google Colab

各 notebook 上部の **Open in Colab** ボタンから開き、左サイドバーの **Secrets** に以下を登録してください。

| 変数 | 必須 | 説明 |
|---|---:|---|
| `WANDB_API_KEY` | yes | W&B API key |
| `WANDB_BASE_URL` | no | Dedicated Cloud URL。SaaS の場合は未設定 |
| `WANDB_ENTITY` | no | team / user entity。未設定なら default entity |
| `WANDB_PROJECT` | no | project 名。未設定なら `models-initial-course` |

## 関連資料

スライドデック作成用のブリーフは [docs/wandb-models-course-claude-design-brief.md](docs/wandb-models-course-claude-design-brief.md) にあります。

単体で参照しやすい media logging サンプルとして、[WandBのマルチメディア、全部logするColabサンプル](WandBのマルチメディア、全部logするColabサンプル%20(1).ipynb) も置いています。内容は course の [Tables と Media](notebooks/03_core/02_tables_media.ipynb) と揃えています。

## 注意

- API key を notebook や git に書かないでください。
- `run.log_code` や `run.save` で `.env`、credential、大容量データを保存しないでください。
- Integration notebook では、外部モデルをダウンロードしない小さな Hugging Face Trainer を使います。実際の研究コードでは、TRL、PyTorch Lightning、LeRobot など、利用している framework や repo の W&B integration 設定を確認してください。
