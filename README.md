# vita_back

## 環境構築

### pyenv

1. pyenv-winのインストール

* chocolateyでpyenv-winをインストール
  https://community.chocolatey.org/packages?q=pyenv

### poetry

1. pyenvで、pythonのバージョン指定

```
pyenv local 3.10.5
```

2. pooetryのインストール

```
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

3. 環境変数指定

```
[System.Environment]::SetEnvironmentVariable('path', $env:APPDATA + "\Python\Scripts;" + [System.Environment]::GetEnvironmentVariable('path', "User"),"User")
```

4. 仮想環境のディレクトリをプロジェクト内に設定

```
poetry config virtualenvs.in-project true
```

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

## strawberryでのgraphqlサーバーの起動

``` bash
poetry run strawberry server src.main
```
