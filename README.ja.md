# txt2sduml

sequencediagram.org の書式で記述されたテキストファイルからシーケンス図の画像を生成する。

## 要件

- Python (>=3.8)
- pip (>=21)

## 依存モジュール

- Playwright

## 動作原理

ヘッドレスブラウザで sequencediagram.org を開き、指定したファイルのソースをエディターに貼り付けてからシーケンス図を SVG でダウンロードする。

## インストール

[リリース](../../releases/latest)からダウンロードして

```shell
$ pip install txt2sduml-0.1.0-py3-none-any.whl
```

初回は Playwright のインストールが必要。

playwright コマンドは txt2sduml の依存関係解決時にインストールされるが、場合によっては PATH を通さないとインストールされた playwright, txt2sduml が見つからない可能性がある。

```shell
$ playwright install
```

## アップグレード

新しいパッケージを[リリース](../../releases/latest)からダウンロードして

```shell
$ pip install --upgrade txt2sduml-0.1.0-py3-none-any.whl
```

