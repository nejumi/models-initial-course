# W&B Models 2時間講座 スライド制作ブリーフ

作成日: 2026-05-16

この Markdown は、Claude Design で W&B Models 版の 2 時間講座スライドデックを作成するための詳細指示です。Weave course のように、repo のハンズオン教材とスライドが対応するコースを想定します。序盤では、W&B 未利用または利用が進んでいない研究者が「次の実験から、とりあえず残せる」状態になることを最初の成功体験にし、その後に Integration、Artifacts、Tables/media、Sweeps、Automations、Reports へ進みます。

## 結論

本講座は、最初にログイン確認を済ませ、`wandb.init`、`run.log`、`wandb.finish` の基本構文を扱った後、`run.log_code` と `run.save` を含む最小テンプレートに進む構成にします。2 時間講座の序盤では、受講者が「次の実験から記録を残せる」状態になることを重視します。

ただし、既存の企画書はこの講座全体の企画書ではありません。そこから取り込むのは「時間のない研究者に、最小実装でまず価値を感じてもらう」という思想と、`run.log_code` / `run.save` を使った入口です。講座全体は W&B Models の体系的なコースとして、Integration、Artifacts、Tables/media、Sweeps、Automations、Reports まで扱います。

スライド作成時の方針は次の通りです。

- `run.save` は「まずは run に出力ファイルを紐づける入口」として扱う。再利用、バージョン管理、リネージまで必要になったら `wandb.Artifact` に進む、という順序にする。
- `run.save("outputs/*", policy="end")` は、glob が `save` 呼び出し時に展開されるため、出力ファイルを作った後に呼ぶ、と明示する。
- `run.log_code(".")` はデフォルトでは主に Python ソースなどを保存する機能として紹介し、秘密情報、大容量データ、API キーを含めない注意を入れる。
- Integration セクションでは「W&B は多くの OSS / 研究 repo に既に組み込まれており、数行または設定 1 つでつながる」ことを中心に扱う。ハンズオンは Hugging Face Trainer にする。LeRobot など Physical AI の例は、発展例として名前を紹介する程度に留める。
- Artifacts、Tables/media、Sweeps は 2 時間の中で最低限のコードと画面確認まで扱う。
- Automations と Reports は後半で、共有や運用に進むための機能として紹介する。Automations は権限やプランに依存するため、画面デモまたは概念中心でよい。

## 参照する repo 内資料

- `Workshop_W&B (日本語）.pdf`: 既存の W&B ワークショップ構成。事前準備、ログイン、基本機能、Artifacts、Tables、Sweeps、Reports の順序を参考にする。
- `InfoTech 研究者様向け使い方講座ご提案_企画書.pdf`: 講座全体の企画書ではなく、序盤 getting started に取り込む参考資料。MLOps 全体説明ではなく、個人研究、短スパン試行、PoC に最適化した最小実装に絞る思想を借りる。
- `WandB_Fun_Book_v3.0.0_ebook.pdf`: W&B Models の体系的な背景資料。Experiments、Artifacts、Tables、Reports、Sweeps の辞書として扱う。

## 想定受講者

- OSS や公開コードをまず動かして、当たりをつけたい研究者
- PoC や先行開発で、短いサイクルの比較と判断を回したい人
- 少人数チームで、結果、コード、出力ファイルの最低限の再現性を残したい人
- 専任 MLOps 担当ではなく、今ある Python スクリプトや notebook に少しだけ足して価値を得たい人

## 講座の約束

受講者が講座後にできる状態:

- W&B にログインできるか確認できる
- 自分のコードに `wandb.init`、`run.log`、`run.log_code`、`run.save` を追加できる
- W&B App 上で run、metrics、config、files、code を確認できる
- Hugging Face Trainer の W&B integration を実行し、PyTorch Lightning、TRL、LeRobot などにも同様の integration があることを理解できる
- `run.save` と `wandb.Artifact` の使い分けがわかる
- Table と media で定性評価や誤り分析を残すイメージが持てる
- Sweeps、Automations、Reports を次に使う機能として把握できる

## 中心メッセージ

講座全体のキーフレーズ:

> 重い仕組みを作る前に、後で困らない痕跡を残す。

受講者向けの最小モデル:

1. Run を始める
2. 指標を記録する
3. コードと出力物を残す
4. Run を閉じる

くだけた表現は使わず、スライド本文では「迷ったら残すテンプレート」「まず残る状態を作る」と表現する。

## 推奨講座構成

このブリーフの主対象は 2 時間講座です。60 分や 90 分への短縮は後でできますが、まず 2 時間で成立する modular deck を作成します。

### 2 時間版の基本配分

- 0-8 分: オープニング。今日のゴール、W&B Models の価値、講座の地図。
- 8-18 分: ログイン、API key、Public Cloud / Dedicated Cloud、project 作成確認。
- 18-35 分: `wandb.init`、`run.log`、`finish`、config、metrics の基本。
- 35-50 分: 「これだけ覚えればなんとかなる」getting started。`run.log_code` と `run.save` でコードと出力物を残す。
- 50-62 分: W&B App で run を見る。charts、config、files、code、2 run 比較。
- 62-78 分: Integration。多数の OSS / 研究 repo が W&B に対応していることを示し、Hugging Face Trainer の `report_to="wandb"` を実行する。LeRobot など Physical AI の例は発展例として短く触れる。
- 78-92 分: Artifacts。`run.save` との違い、`add_file` / `add_dir` / `add_reference`、dataset/model/eval outputs の版管理、lineage。
- 92-106 分: Tables と media。授業では代表例を実行し、notebook には Image、overlay、Table、Audio、Video、HTML、Object3D、Molecule、Histogram、Plotly/custom charts の動く例を置く。
- 106-114 分: Sweeps。random search の最小例と、条件比較の自動化。
- 114-120 分: Automations、Reports、まとめ。長時間学習の通知、結果共有、次に試す repo 課題。

時間に余裕がある場合は、Integration demo と Tables/media のどちらかを live 実行にします。時間が押した場合は、Integration demo は事前実行済み run の画面確認に切り替え、getting started と Artifacts / Tables の理解を優先します。

### 2 時間内で live にしたいもの

- login check の 1 run 作成
- minimal template の実行
- 2 run 比較
- Table/media の代表例 logging

### 2 時間内では画面確認や概念説明でもよいもの

- HF Trainer tiny demo の実学習
- Sweep agent の複数 run 完走
- Automations の Slack / Webhook 実発火
- Reports の完成版共有

### repo/course としてのモジュール構成

1. `00_login_check`: 認証確認と project 作成
2. `01_minimal_tracking`: `init`、`log`、`finish`、config、metrics
3. `02_save_everything_first`: `log_code`、`run.save`、outputs 保存
4. `03_integrations_overview`: 多数の integration pattern、HF Trainer 実行例、発展例として LeRobot など
5. `04_artifacts`: `add_file`、`add_dir`、`add_reference`、`use_artifact`、lineage
6. `05_tables_media`: Image、overlay、Table、Audio、Video、HTML、Object3D、Molecule、Histogram、Plotly/custom charts、誤り分析
7. `06_sweeps`: sweep config と agent
8. `07_automations_reports`: Automations と Reports による共有、通知

## Claude Design への基本デザイン指示

- 日本語の 16:9 スライドデックにする。
- 2 時間講座の master deck として 55-70 枚程度にする。各セクションの先頭に module divider を入れ、後から 60 分版や 90 分版へ削れる構造にする。
- 営業資料ではなく、研究者向けの実務ハンズオン資料として作る。
- トーンは「軽い、実用的、すぐ試せる」。大げさな MLOps 図解や抽象論を増やしすぎない。
- W&B の黄色、黒、白をアクセントに使う。全面を黄色にしない。
- コードは大きく読みやすく、1 スライド 1 コード概念にする。
- W&B UI のスクリーンショットは、実画像がない場合は `[Screenshot placeholder: ...]` として枠だけ置く。架空の UI を細かく捏造しない。
- 公開 repo 用の資料では、特定企業名、内部表記、Confidential 表記を入れない。内部版が必要な場合だけタイトルやフッターに追加する。
- スライドは「残す -> 比べる -> 共有する -> 自動化する」の流れが見えるようにする。

## スライド構成案

以下は論理構成です。Claude Design では module divider、hands-on instruction、screenshot placeholder、recap を足して 55-70 枚程度に展開してください。

### 1. タイトル

タイトル: W&B Models 2時間講座

サブタイトル: 研究コードに数行足して、実験を後から追える形で残す

ビジュアル: W&B の run 画面、コード、出力ファイルが 1 つの run に集まる概念図。

### 2. 今日できるようになること

メッセージ: 今日の前半は「次の実験から W&B を足せること」、後半は W&B Models の主要機能を研究ワークフローに接続すること。

箇条書き:

- ログインできる
- metrics と config を残せる
- コードと出力ファイルを run に紐づけられる
- 既存ライブラリ連携の入口がわかる
- Tables、Artifacts、Sweeps、Reports の使い所がわかる

### 3. 研究でよく起きる困りごと

メッセージ: 実験が失敗するより、「良かった実験を後から追えない」ことが痛い。

例:

- どの条件が良かったかわからない
- 出力ファイルとコードが別々に散る
- notebook のセル実行順が残らない
- 比較結果を共同研究者に渡しづらい

### 4. W&B Models の価値を 3 語で

タイトル: 残す、比べる、共有する

3 カラム:

- 残す: metrics、config、code、outputs
- 比べる: runs、Tables、media、Sweeps
- 共有する: Reports、リンク、Automations

### 5. 今日の最小メンタルモデル

メッセージ: Run は「実験 1 回分の研究ノート」。

図:

`Run = config + metrics + code + outputs + environment`

### 6. 事前準備チェック

内容:

- `pip install -U wandb`
- W&B アカウント
- API key
- Public Cloud または Dedicated Cloud の URL
- notebook または Python script

### 7. ログイン確認

コード:

```bash
wandb login
```

Dedicated Cloud の場合:

```bash
export WANDB_BASE_URL="https://<your-host>.wandb.io"
wandb login
```

補足: notebook では `wandb.login()` でもよい。API key を notebook に直書きしない。

### 8. ログインできたか確認する

コード:

```python
import wandb

with wandb.init(project="login-check") as run:
    run.log({"ok": 1})
```

見せる画面: W&B App に `login-check` project と 1 run ができていること。

### 9. Entity / Project / Run

メッセージ: 最初は `project` だけ決めればよい。組織や team の運用は後でよい。

図:

`Entity / Project / Run`

注意: 社内環境では entity が指定される場合がある。初回は管理者の案内に従う。

### 10. 最初の 3 つの API

タイトル: `init`、`log`、`finish`

コード:

```python
import wandb

run = wandb.init(project="research-demo", config=cfg)
run.log({"train/loss": loss, "val/acc": acc})
run.finish()
```

### 11. おすすめは context manager

メッセージ: `with` を使うと `finish` 忘れが減る。

コード:

```python
import wandb

with wandb.init(project="research-demo", config=cfg) as run:
    run.log({"train/loss": loss, "val/acc": acc})
```

### 12. `config` は実験条件

例:

```python
cfg = {
    "model": "tiny-model",
    "lr": 1e-4,
    "batch_size": 8,
    "seed": 42,
}
```

メッセージ: あとから比較したい条件は config に入れる。

### 13. metrics は名前で整理する

コード:

```python
run.log({
    "train/loss": train_loss,
    "val/loss": val_loss,
    "val/acc": val_acc,
})
```

メッセージ: `/` を使うと UI 上でまとまりやすい。

### 14. ここまでで見えるもの

W&B App の run overview、charts、config、system metrics のスクリーンショットプレースホルダー。

話すこと: 数行だけで、手元の print や spreadsheet より後から追いやすくなる。

### 15. これだけ覚えればなんとかなる

タイトル: 迷ったら残すテンプレート

大きくコードを表示:

```python
import wandb

with wandb.init(project="research-demo", config=cfg) as run:
    run.log_code(".")

    results = train_or_evaluate(cfg)
    run.log({
        "train/loss": results["train_loss"],
        "val/acc": results["val_acc"],
    })

    # outputs/ の中身を作った後に呼ぶ
    run.save("outputs/*", base_path=".", policy="end")
```

メッセージ: まずは「条件、指標、コード、出力物」が 1 つの run に残れば勝ち。

### 16. `run.log_code` は何を残すか

内容:

- 現在のコード状態を W&B Artifact として残す
- デフォルトでは主に `.py`、requirements、Dockerfile などを対象にする
- notebook や特定拡張子を含めたい場合は `include_fn` を使う
- 秘密情報、大容量データ、社外秘ファイルを含めない

簡単コード:

```python
run.log_code(
    ".",
    include_fn=lambda path: path.endswith((".py", ".ipynb", ".yaml")),
)
```

### 17. `run.save` は何を残すか

内容:

- run の Files に出力ファイルを紐づける
- `outputs/*.json`、`outputs/*.csv`、`outputs/*.txt`、`outputs/*.png` などに向く
- `policy="end"` は run 終了時にアップロードする
- glob は `save` を呼んだ時点で展開されるため、出力後に呼ぶ

コード:

```python
run.save("outputs/*", base_path=".", policy="end")
```

### 18. まず保存しておくと後で助かるもの

2 カラム:

残すべき:

- config
- metrics
- training log
- eval results
- generated samples
- plots
- checkpoints の小さいもの
- 実行したコード

注意が必要:

- API keys
- personal data
- huge raw datasets
- credential files
- vendor restricted files

### 19. ハンズオン 1: 既存コードに足す

指示:

- `import wandb`
- `cfg` を作る
- `with wandb.init(...):` で囲む
- train loop の中で `run.log`
- 最後に `run.log_code` と `run.save`

ビジュアル: Before / After のコード差分。

### 20. W&B App で確認する

見せる場所:

- Runs table
- Charts
- Config
- Files
- Code artifact
- System metrics

補足: ここでは、受講者が次の実験に追加する具体的な手順を確認できるようにする。

### 21. 2 回走らせて比較する

メッセージ: W&B の価値は 1 run ではなく、2 run 目から見えやすい。

デモ:

- `lr` か `seed` を変えてもう一度実行
- Runs table で並べる
- metric chart で比較

### 22. Integration の考え方

タイトル: W&B は「足す」だけでなく「既に入っている」

メッセージ: 多くの OSS / 研究 repo は W&B integration を持っている。自分で training loop に `run.log` を書く代わりに、設定で W&B を有効化できるケースが多い。

例:

- Hugging Face Transformers / TRL: `report_to="wandb"`
- PyTorch Lightning: `WandbLogger`
- Keras: W&B callback
- LeRobot: `wandb.enable` / `WandBConfig` / `WandBLogger`
- その他の CLI / training repo: `WANDB_PROJECT`、`WANDB_ENTITY`、`WANDB_MODE`

この章では「世界中の 5 万以上の repo に W&B が統合されている」というメッセージを入口にし、Hugging Face Trainer をハンズオンの実行例として扱う。数値を外部公開資料で使う場合は、公開前に最新の出典確認を入れる。

### 23. Integration pattern 早見表

表:

| Pattern | よくある設定 | 受講者に伝えること |
| --- | --- | --- |
| Trainer integration | `report_to="wandb"` | framework が metrics を自動で送る |
| Logger object | `logger=WandbLogger(...)` | logger を差し替えるだけでよい |
| Config flag | `wandb.enable=true` | OSS repo 側の config を有効化する |
| Callback | `WandbCallback` | training lifecycle に W&B を差し込む |
| Env vars | `WANDB_PROJECT`, `WANDB_ENTITY` | CLI 実行でも project を制御できる |

### 24. Hugging Face Trainer の実行例

Hugging Face Trainer の実行例:

```python
args = TrainingArguments(
    output_dir="outputs/hf-demo",
    report_to="wandb",
    run_name="hf-demo-001",
    logging_steps=1,
    max_steps=10,
)
trainer = Trainer(model=model, args=args, train_dataset=train_dataset)
trainer.train()
```

メッセージ: この講座のハンズオンでは Hugging Face Trainer を実行する。PyTorch Lightning、TRL、LeRobot などは、既存 framework / repo から W&B に接続できる発展例として短く紹介する。初回講座では、LeRobot の設定手順や robotics 固有の学習手順は扱わない。

### 25. `run.save` から Artifacts へ

タイトル: 使い回すものは Artifact にする

対比表:

- `run.save`: その run の出力ファイルを残す。初回、個人実験、メモ用途に便利。
- `wandb.Artifact`: データ、モデル、評価結果をバージョン管理し、別 run から使う。リネージを残す。

### 26. Artifact の基本パターン

```python
import wandb

artifact = wandb.Artifact("research-dataset", type="dataset")
artifact.add_file("metrics.json", name="metrics/metrics.json")
artifact.add_dir("dataset", name="dataset")
artifact.add_reference("s3://bucket/raw-data", name="references/raw-data")

with wandb.init(project="research-demo", job_type="create-artifact") as run:
    logged = run.log_artifact(artifact, aliases=["latest"])
    logged.wait()
```

使う場面:

- `add_file`: 単一の評価結果、設定、metric summary
- `add_dir`: dataset snapshot、checkpoint directory、benchmark outputs
- `add_reference`: S3/GCS/HTTP/NFS など、W&B にアップロードせず URI と checksum を追いたい大容量データ
- `use_artifact`: 別 run から同じ dataset/model/eval outputs を使い、lineage を残す

### 27. Lineage を見せる

ビジュアル: dataset artifact -> training run -> model artifact -> eval run の DAG。

メッセージ: 「どのデータから、どのモデルができて、どの評価に使われたか」が追える。

### 28. Table は定性評価の置き場

メッセージ: 研究では scalar metric だけでは足りない。生成例、誤り例、画像、音声、HTML を並べて見る。

例:

- prompt / prediction / reference / score
- image / mask / prediction
- audio / spectrogram / label
- video / failure type / comment

### 29. Table の最小コード

```python
table = wandb.Table(columns=["id", "prompt", "prediction", "score"])

for row in examples:
    table.add_data(
        row["id"],
        row["prompt"],
        row["prediction"],
        row["score"],
    )

run.log({"eval/samples": table})
```

### 30. Media logging リファレンス

コード例は、notebook の `05_tables_media.ipynb` と対応させる。授業中に全て live 実行する必要はないが、repo には全て実行済みの例として残す。

```python
run.log({
    "image/pil": wandb.Image(pil_image),
    "audio/from_numpy": wandb.Audio(audio, sample_rate=sample_rate),
    "video/from_file": wandb.Video("demo.gif", fps=4, format="gif"),
    "html/from_string": wandb.Html("<b>example</b>"),
    "object3d/xyzrgb": wandb.Object3D.from_numpy(points),
    "molecule/from_pdb": wandb.Molecule("water.pdb"),
    "histogram/auto": wandb.Histogram(values),
    "plotly/loss": wandb.Plotly(fig),
})
```

必ず触れる media:

- Image: PIL / NumPy array / file path
- Image overlay: bounding boxes / segmentation masks
- Table: text、score、image、audio、HTML を同じ行に置く
- Audio: NumPy array / WAV file path
- Video: NumPy array / GIF file path
- HTML: string / file
- Object3D: point cloud / lidar scene
- Molecule: PDB / SMILES
- Histogram
- Plotly と `wandb.plot` の line、scatter、bar、histogram、confusion matrix

ビジュアル: Table 内に text、score、image、audio、HTML が並ぶスクリーンショットプレースホルダー。

### 31. Table で誤り分析する

デモ:

- score が低い順に並べる
- failure type で filter
- prompt と prediction を見比べる
- 気づきを Report に貼る

### 32. Sweeps は「比較実験の自動化」

メッセージ: 1 つずつ手で条件を変える代わりに、探索空間と評価指標を宣言する。

初回講座では random search だけでよい。

### 33. Sweep の最小コード

```python
sweep_config = {
    "method": "random",
    "metric": {"name": "val/acc", "goal": "maximize"},
    "parameters": {
        "lr": {"values": [1e-5, 3e-5, 1e-4]},
        "batch_size": {"values": [4, 8]},
    },
}

sweep_id = wandb.sweep(sweep_config, project="research-demo")
wandb.agent(sweep_id, train, count=3)
```

注意: `train()` の中で `wandb.init(config=...)` し、`wandb.config` を読む。

### 34. Automations は「見張り番」

メッセージ: 長時間学習や共有運用では、条件を満たしたときの通知、失敗時の通知、artifact 作成後の webhook 起動が使える。

例:

- `loss` が閾値を下回ったら Slack 通知
- run が failed/crashed になったら通知
- model artifact に alias が付いたら downstream job を起動

注意: プラン、権限、Slack/Webhook 設定に依存するため、初回は概念と画面紹介でよい。

### 35. Reports は「実験結果の共有ノート」

メッセージ: run 画面のグラフや Table を、説明付きで共同研究者に共有する。

見せるもの:

- chart
- run comparison
- Table
- Markdown note
- link sharing

### 36. Report の作り方

手順:

1. Project から Report 作成
2. Chart や Table を追加
3. 何を試したか、何がわかったかを書く
4. 共有リンクを出す

### 37. 推奨ワークフロー

タイトル: 最初の 1 週間はこれだけ

1. すべての実験に `wandb.init`
2. 主要 metric を `run.log`
3. `run.log_code(".")`
4. `outputs/` を作って `run.save`
5. 良かった run を Report に貼る

### 38. 発展ワークフロー

タイトル: 慣れてきたら

1. 再利用する dataset/model を Artifact にする
2. 生成例や誤り分析を Table にする
3. 比較したい条件を Sweep にする
4. 長時間学習や共有運用を Automation にする

### 39. repo の推奨構成

```text
.
├── README.md
├── notebooks/
│   ├── 00_login_check.ipynb
│   ├── 01_minimal_tracking.ipynb
│   ├── 02_save_everything_first.ipynb
│   ├── 03_integrations_overview.ipynb
│   ├── 04_artifacts.ipynb
│   ├── 05_tables_media.ipynb
│   ├── 06_sweeps.ipynb
│   └── 07_automations_reports.ipynb
├── scripts/
│   ├── train_minimal.py
│   ├── train_hf_sft.py
│   ├── log_artifact.py
│   ├── log_table_media.py
│   └── create_report_example.py
├── configs/
│   └── sweep.yaml
├── outputs/
│   └── .gitkeep
└── slides/
```

メッセージ: スライドと repo のハンズオンは同じ順番にする。

### 40. Q&A 用スライド

よくある質問:

- 社内の Dedicated Cloud では login はどうするか
- API key はどこに置くか
- 大きいファイルは保存してよいか
- notebook でも使えるか
- offline 環境ではどうするか
- 複数人で project を共有できるか
- `run.save` と Artifact はどちらを使うか

### 41. まとめ

メッセージ:

前半でまず覚えるのは 4 つ。

```python
wandb.init(...)
run.log(...)
run.log_code(".")
run.save("outputs/*", policy="end")
```

締め: 次の実験から、あとで困らない状態にする。

### 42. Appendix: よく使う snippets

複数スライドに分けてよい:

- login
- basic run
- minimal template
- Artifact
- Table
- Sweep
- Integration example: Hugging Face Trainer

### 43. Appendix: セキュリティ注意

内容:

- API key を notebook や git に書かない
- secrets、credential、個人情報を `log_code` や `run.save` に含めない
- 大容量データは Artifact reference や社内ストレージ運用を検討する
- 社内 Dedicated Cloud の URL と entity/project 命名規則に従う

### 44. Appendix: 使い分け早見表

表:

| やりたいこと | まず使うもの |
| --- | --- |
| loss や accuracy を残す | `run.log` |
| 実験条件を残す | `config` |
| 実行コードを残す | `run.log_code` |
| その run の出力物を残す | `run.save` |
| データやモデルを再利用、版管理する | `wandb.Artifact` |
| 生成例や誤り例を並べる | `wandb.Table` |
| 条件探索を回す | Sweeps |
| 閾値や完了で通知する | Automations |
| 結果を説明付きで共有する | Reports |

## 主要コードスニペット

### 最小テンプレート

```python
import wandb

cfg = {
    "lr": 1e-4,
    "batch_size": 8,
    "seed": 42,
}

with wandb.init(project="research-demo", config=cfg) as run:
    run.log_code(".")

    for step in range(num_steps):
        loss, acc = train_one_step()
        run.log({"train/loss": loss, "val/acc": acc})

    write_outputs("outputs/")
    run.save("outputs/*", base_path=".", policy="end")
```

### Integration example: HF Trainer

```python
import os

os.environ["WANDB_PROJECT"] = "research-demo-sft"
os.environ["WANDB_LOG_MODEL"] = "end"

from transformers import TrainingArguments, Trainer

args = TrainingArguments(
    output_dir="outputs/hf-demo",
    report_to="wandb",
    run_name="hf-demo-001",
    logging_steps=1,
    max_steps=10,
)

trainer = Trainer(
    model=model,
    args=args,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
)

trainer.train()
```

### Artifact

```python
artifact = wandb.Artifact("research-dataset", type="dataset")
artifact.add_file("metrics.json", name="metrics/metrics.json")
artifact.add_dir("dataset", name="dataset")
artifact.add_reference("s3://bucket/raw-data", name="references/raw-data")

with wandb.init(project="research-demo", job_type="create-artifact") as run:
    logged = run.log_artifact(artifact, aliases=["latest"])
    logged.wait()
```

### Table / Media

```python
with wandb.init(project="research-demo") as run:
    table = wandb.Table(columns=["id", "prompt", "prediction", "score", "image", "audio", "html"])
    table.add_data(
        "sample-001",
        prompt,
        prediction,
        score,
        wandb.Image(image),
        wandb.Audio(audio, sample_rate=sample_rate),
        wandb.Html("<b>review</b>"),
    )
    run.log({"eval/mixed_media_table": table})
```

### Sweep

```python
def train():
    with wandb.init(project="research-demo") as run:
        cfg = wandb.config
        score = train_model(lr=cfg.lr, batch_size=cfg.batch_size)
        run.log({"val/acc": score})

sweep_config = {
    "method": "random",
    "metric": {"name": "val/acc", "goal": "maximize"},
    "parameters": {
        "lr": {"values": [1e-5, 3e-5, 1e-4]},
        "batch_size": {"values": [4, 8]},
    },
}

sweep_id = wandb.sweep(sweep_config, project="research-demo")
wandb.agent(sweep_id, train, count=3)
```

## 必要なスクリーンショット

実 UI を捏造せず、以下をプレースホルダーとして置く。後で実 screenshots に差し替える。

- W&B login 成功後の project page
- 1 run の overview
- metrics chart
- config panel
- Files panel に `outputs/` がある状態
- Code artifact 画面
- Runs table で 2 run を比較している画面
- Integration demo run の chart
- Artifact lineage
- Table に text / image / score が並ぶ画面
- Sweep の parallel coordinates または sweep overview
- Automation 設定画面
- Report 作成画面

## Claude Design にそのまま渡すプロンプト

以下を Claude Design に貼り付ける。

```text
日本語の 16:9 スライドデックを作ってください。テーマは「W&B Models 2時間講座」です。対象は、W&B をまだ使っていない、または使い始められていない研究者、PoC 担当、少人数チームの ML 開発者です。

このデックは 2 時間講座用の master deck です。Weave course のように、repo のハンズオン教材とスライドが同じ順番で対応するコースを想定してください。スライド枚数は 55-70 枚程度にし、module divider を入れて、後から短縮版に削れる構造にしてください。

このコースの目的は、単なる初回ハンズオンだけではありません。前半では、今ある Python script / notebook に数行足して、次の実験から metrics、config、code、outputs を後から追える形で残せるようにします。後半では、Integration、Artifacts、Tables/media、Sweeps、Automations、Reports まで進み、W&B Models の全体像を研究ワークフローに接続します。

全体メッセージは「重い仕組みを作る前に、後で困らない痕跡を残す」です。流れは「残す -> 比べる -> 共有する -> 自動化する」にしてください。

2 時間の基本配分は以下です。

- 0-8 分: オープニング。今日のゴール、W&B Models の価値、講座の地図
- 8-18 分: ログイン、API key、Public Cloud / Dedicated Cloud、project 作成確認
- 18-35 分: `wandb.init`、`run.log`、`finish`、config、metrics の基本
- 35-50 分: 「これだけ覚えればなんとかなる」getting started。`run.log_code` と `run.save` でコードと出力物を残す
- 50-62 分: W&B App で run を見る。charts、config、files、code、2 run 比較
- 62-78 分: Integration。多数の OSS / 研究 repo が W&B に対応していることを示し、Hugging Face Trainer の `report_to="wandb"` を実行する。LeRobot など Physical AI の例は発展例として短く触れる
- 78-92 分: Artifacts。`run.save` との違い、dataset/model/eval outputs の版管理、lineage
- 92-106 分: Tables と media。授業では代表例を実行し、repo には Image、overlay、Table、Audio、Video、HTML、Object3D、Molecule、Histogram、Plotly/custom charts の動く例を置く
- 106-114 分: Sweeps。random search の最小例と、条件比較の自動化
- 114-120 分: Automations、Reports、まとめ。長時間学習の通知、結果共有、次に試す repo 課題

序盤で必ず、ログイン確認を行い、次に `wandb.init`、`run.log`、`finish` の基本を説明します。その後、「迷ったら残すテンプレート」として次の考え方を大きく扱ってください。

1. `wandb.init(project="research-demo", config=cfg)` で run を始める
2. `run.log({"train/loss": loss, "val/acc": acc})` で metrics を残す
3. `run.log_code(".")` でコードを残す
4. `run.save("outputs/*", base_path=".", policy="end")` で出力物を run に紐づける

ただし、`run.save` は出力ファイルを作った後に呼ぶこと、秘密情報や API key を保存しないこと、再利用やバージョン管理が必要なら `wandb.Artifact` に進むことを注意として入れてください。

デックは営業資料ではなく、実務ハンズオン資料として作ってください。W&B の黄色、黒、白をアクセントにし、コードを読みやすく、1 スライド 1 メッセージにしてください。W&B UI screenshot が必要な箇所は、架空 UI を作り込まず `[Screenshot placeholder: ...]` として差し替え枠を置いてください。

必ず含めるセクション:

- 今日のゴール
- 研究でよく起きる困りごと
- W&B Models の価値: 残す、比べる、共有する
- ログインと API key の確認
- Entity / Project / Run の最小説明
- `init`、`log`、`finish`
- context manager を使う理由
- config と metrics の名前付け
- 「迷ったら残すテンプレート」
- `run.log_code` の説明と注意
- `run.save` の説明と注意
- W&B App で run、chart、config、files、code を確認する流れ
- 2 run を比較する流れ
- Integration overview。Hugging Face Trainer を実行例として扱い、TRL、PyTorch Lightning、LeRobot などの integration は発展例として短く入れる
- `run.save` と `wandb.Artifact` の使い分け
- Artifact の `add_file` / `add_dir` / `add_reference` / `use_artifact` と lineage
- Table と media logging による定性評価、誤り分析。Image、overlay、Audio、Video、HTML、Object3D、Molecule、Histogram、Plotly/custom charts の実行例を repo に置く
- Sweeps の最小コード
- Automations の紹介。権限やプランに依存するので概念中心
- Reports による共有
- repo/course としての次の課題
- まとめと Q&A

スライド本文と speaker notes では、くだけた表現を避け、「迷ったら残すテンプレート」「まず残る状態を作る」と表現してください。

公開 repo 用の資料として、特定企業名、Confidential 表記、内部情報は入れないでください.
```

## 参考リンク

- W&B Python SDK `Run`: https://docs.wandb.ai/models/ref/python/experiments/run
- W&B Hugging Face Transformers integration: https://docs.wandb.ai/models/integrations/huggingface
- W&B Sweeps: https://docs.wandb.ai/models/sweeps
- W&B Automations: https://docs.wandb.ai/models/automations

