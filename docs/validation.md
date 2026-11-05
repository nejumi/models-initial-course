# 検証記録（2026-11-05）

## 実行環境と結果

Python 3.11.15、wandb 0.31.0、fastai 2.8.12、PyTorch 2.15.0、
torchvision 0.29.2、Transformers 4.57.6 で確認しました。

| 確認項目 | 結果 |
|---|---|
| 接続先設定・Colab Secrets・依存解決・ファイル形式などの回帰テスト | 10件成功 |
| 全8 Notebook のオンライン実行 | 成功。学習は SUNK の H100 で実行 |
| CPU 実行 | 6 Notebook 成功。同計算ノードで GPU を無効化して実行 |
| 単体 Python スクリプト2本 | CPU・W&B offline で成功 |
| clone なしの Notebook 起動 | 空の作業フォルダで共通コードを GitHub から取得し、コード・出力保存の演習に成功 |
| W&B 保存内容 | コード、JSON、4行の予測Table、Artifact取得、3条件のSweepをAPIで確認 |
| パッケージ依存関係 | `uv pip check` 成功 |

オンライン実行には `WANDB_BASE_URL=https://api.wandb.ai` と、この環境の既存ログインを使いました。
CPU の offline 実行では、サーバーが必要な Artifact の取得と Sweep の2冊を除外しています。
これら2冊はオンライン実行で確認しました。

セグメンテーションは52枚で学習し、12枚で検証しました。2エポックの H100 実行では、
検証 loss が1.91から1.53へ下がり、正解・予測マスクを含むTableをアップロードできました。
これは動作確認用の小規模な実験です。データや分割の制約があるため、モデルの実用的な性能を示すものではありません。

## 修正した主な問題

- 未登録の Colab Secret が1つあると、後続のチーム・プロジェクト設定を読めなかった。
- 接続先を明示したログインがなく、Dedicated Cloud の設定方法も不足していた。
- パッケージの検出が import の可否だけに依存し、バージョン条件や media extras を確認していなかった。
- Colab 単体で開くと、保存対象のコードが存在しないことがあった。
- 分子構造の PDB に改行ではなく `\\n` が入り、正しいファイルにならなかった。
- 添付の学習例が特定アカウントの BDD Artifact と古い依存関係に依存していた。
- fastai の標準 W&B callback が、今回の fastcore との組み合わせで設定の変換時に停止した。
  指標のみを送る小さな callback に変更した。
- 3D scene の作成を、以前からある `wandb.Object3D` コンストラクタと対応する配列形式に揃えた。
- 長い制作指示、未提供資料への参照、実際のコードと異なる Sweep の説明を整理した。
  練習用の合成指標と実際の学習結果を区別する説明も追加した。

## 未確認の範囲

Dedicated Cloud の実サーバーでは未実行です。URL の既定値・検証・ログインへの受け渡しはテストしています。
Google Colab の実サービス、Windows、macOS、別の Python バージョンでは未実行です。
Notebook のコードは CUDA 固有の処理を前提とせず、CPU に切り替えられます。

W&B の保存データは API で確認しました。各メディアのブラウザ上の描画は未確認です。

## 再実行

```bash
make test
make test-offline
.venv/bin/python scripts/execute_notebooks.py --offline --cpu --output-dir outputs/executed-cpu
# 接続先を設定してオンライン実行
make test-notebooks
```

GitHub Actions でも、CPU 版 PyTorch を使って回帰テストと offline の Notebook 実行を行います。
