# W&B Models 講座のスライド制作メモ

講師・スライド制作者向けの資料です。受講者の実行手順は README と Notebook に記載します。
コード例とファイル名は、現在の Notebook を参照してください。

## 2時間の進め方

- 0–10分: 接続先と API key を設定し、最初の run を確認。
- 10–25分: 道路画像を短く学習し、loss と予測マスクを W&B で見る。
- 25–40分: init / log と config。基本の1 runと比較用の2 runsを作る。
- 40–50分: 実行したコードと、その出力ファイルを保存する。
- 50–60分: Trainer の連携を試し、自動記録された loss を確認。
- 60–80分: Artifact の登録と利用。作成 run と利用 run の関係を確認。
- 80–100分: 画像と Table。時間があれば音声・動画なども試す。
- 100–110分: grid search で学習率3条件を実行。
- 110–120分: Report に書く内容、通知の用途、質問。

## スライドの作り方

日本語・16:9。コードは1枚につき1つの操作を扱い、読める文字サイズにします。
画面例には実際の実行結果を使います。未取得の画面は「画面取得待ち」と明記します。
教材に含まれない資料や、出典未確認の利用者数は参照しません。

## 各章で伝えること

- **環境設定**: 標準は Multi-tenant SaaS。Dedicated Cloud は WANDB_BASE_URL と、その接続先の API key を使う。
- **セグメンテーション**: 公開 CamVid tiny で U-Net を2エポック学習する。CPUでも動く。まず結果を見て、API の説明は基礎編で行う。
- **基本記録**: config は実験条件、log は指標。with ブロック終了時に run も終了する。例の数値は学習結果ではない。
- **コードと出力**: log_code には実際に実行する evaluate.py を渡す。run.save は出力ファイルを作った後に呼ぶ。
- **Trainer**: report_to="wandb" で学習指標が自動記録される。
- **Artifacts**: add_file / add_dir はファイルを登録、add_reference は参照先を登録。file:// は元のファイルにアクセスできる環境でのみ使える。
- **Tables / Media**: 画像と Table を必須演習にし、その他の形式は参照例として案内する。
- **Sweep**: Notebook と configs/sweep.yaml は同じ grid search。lr は0.01、0.03、0.1、指標は val/loss の最小化。練習用の計算式であり、学習率の優劣を示す実験ではない。
- **Reports**: 比較の目的、条件、結果、代表例、次の実験を書く。
- **Automations**: 完了・失敗・Artifact の変更などに応じた通知を紹介する。設定できる機能は接続先のプラン・権限で確認する。

## 公開前の確認

1. make test と make test-offline を実行する。
2. 利用できる接続先で全 Notebook を実行し、未確認の接続先や環境を記録する。
3. W&B App で保存コード・ファイル、画像・動画・分子構造、Artifact、Sweep を確認する。
4. スライドのコード、指標名、run 数を Notebook と合わせる。
5. API key や内部データが出力・画面に含まれていないことを確認する。

## 公式資料

- [Run](https://docs.wandb.ai/models/ref/python/experiments/run)
- [Hugging Face 連携](https://docs.wandb.ai/models/integrations/huggingface)
- [Sweeps](https://docs.wandb.ai/models/sweeps)
- [Automations](https://docs.wandb.ai/models/automations)
