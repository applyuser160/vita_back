# vita_back

## 環境構築

### direnv

#### windows

1. direnvのインストール

* 下記のサイトを参考
  https://loochs.org/blog/computer/shell/direnv-installation-for-windows/

2. プロジェクト(vita_back)直下に、`.envrc`を作成

``` .envrc
export PYTHONPATH="{プロジェクトの絶対パス}"
# 例: export PYTHONPATH="/d/Desktop/vita_back"
```

3. git bashにて、`direnv allow`で`.envrc`の読み込み

## Graphql Schema出力

``` bash
poetry run strawberry export-schema vita.src.main:schema > schema.graphql
```
