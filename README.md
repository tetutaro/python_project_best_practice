# Python の開発環境構築と開発の進め方

このドキュメントは、プログラム言語として Python を使うプロジェクトにおける開発環境構築および開発の進め方のベストプラクティスだと考えるものをまとめたものである。

開発環境構築に当たり、以下の点を基本方針として心掛けた。

* 開発者の環境に依存せず、誰もが同等の条件で開発・テストが出来るように、Python 仮想環境を作成する
* 開発の助けになるよう、自動文法チェック・自動プログラム整形・自動プログラム補完・ユニットテスト・自動ドキュメント生成が出来るような環境を構築する
* Python 仮想環境の設定は、[PEP 518](https://peps.python.org/pep-0518/) にあるように、なるべく全てを pyproject.toml に一元的に記述し、それのみを参照すれば良いようにする

以下の文章で `> hoge` という記述は、ターミナルで "hoge" というコマンドを打つ、ということ。

# 新規 Python プロジェクトの作成

* 準備の準備、準備がすべて完了している
* GitHab もしくは GitLab で repository を作る
    * repository の名前には `-` （ハイフン）は使わず、`_`（アンダースコア）を使うものとする
* 作った repository をローカルに clone する
* clone したディレクトリに移動
* この repository の setup.sh を叩く

setup.sh を叩くコマンド（コピーして使用する用）
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/tetutaro/python_project_best_practice/main/setup.sh)"
```

# 既存プロジェクトに参加する

* 準備の準備、準備がすべて完了している
* repository を clone する
* clone したディレクトリに移動
* この repository の update.sh を叩く

update.sh を叩くコマンド（コピーして使用する用）
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/tetutaro/python_project_best_practice/main/update.sh)"
```

# 準備の準備

最も基本となる Python とツールのインストールを行う。ある程度使っているマシンであれば、このセクションで言及されているツール等は既にインストール済みだろう。

## OS のパッケージ管理ツールの設定

* Linux の場合
    * yum, apt などが既に設定されているはず
* Mac の場合
    * `> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
        * 念の為に [Homebrew のサイト](https://brew.sh/index_ja) をチェックして上記コマンドが正しいか確認する

## 必要なツールのインストール

* make, git, curl, Python3, pipx を入れる
* Linux の場合
    * make, curl と Python3 は既に入っている（と思う）
    * `> yum install git` もしくは `> apt install git`
    * `> python3 -m pip install --user pipx`
    * `> python3 -m pipx ensurepath`
* Mac の場合
    * `> brew install automake git curl python@3 pipx`
    * `> pipx ensurepath`

# 準備

Python の仮想環境は pyenv で管理を行う。また、pyproject.toml に情報を一元化するため、Python パッケージの管理には poetry を用いる。ここではこれらのインストール・設定を行う。

## pyenv, poetry のインストール

* pyenv のインストール
    * `> git clone https://github.com/pyenv/pyenv.git ~/.pyenv`
* pyenv plugin のインストール
    * `> mkdir -p ~/.pyenv/plugins`
    * `> git clone https://github.com/pyenv/pyenv-virtualenv.git ~/.pyenv/plugins/pyenv-virtualenv`
    * `> git clone https://github.com/pyenv/pyenv-update.git ~/.pyenv/plugins/pyenv-update`
* poetry のインストール
    * `> pipx install poetry`
* poetry plugin のインストール
    * `> poetry self add "poetry-dynamic-versioning[plugin]"`

## pyenv, poetry の設定

シェルとして ZSH を使っている場合、以下の項目を `~/.zshrc` に加える。

```zsh
export PYENV_ROOT="${HOME}/.pyenv
export PATH="${PYENV_ROOT}/bin:${HOME}/.local/bin:$PATH"
eval "$(pyenv init --path)"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
```

また、以下のコマンドを実行する。

* `> poetry config virtualenvs.path "${HOME}/.pyenv/versions"`
* `> poetry config virtualenvs.prompt "{project_name}"`

## pyenv, poetry 自体のアップデート

* `> pyenv update`
* `> poetry self update`

## 特定バージョンの Python をインストールする

* `> pyenv install --list`
    * インストールできる Python バージョンのリストを表示
    * 最新のバージョン（[公式](https://www.python.org/downloads/)でリリースされているもの）が 3.11.1 だとすると、その１つ前のマイナーバージョン（11 → 10）で、最大のパッチバージョンのものが、一応安定していると思う
        * [セマンティックバージョニング](https://ja.wikipedia.org/wiki/%E3%82%BB%E3%83%9E%E3%83%B3%E3%83%86%E3%82%A3%E3%83%83%E3%82%AF%E3%83%90%E3%83%BC%E3%82%B8%E3%83%A7%E3%83%8B%E3%83%B3%E3%82%B0)は、「メジャーバージョン.マイナーバージョン.パッチバージョン」という表記
        * anaconda-x.x.x, miniconda-x.x.x, pypy-x.x, pyston-x.x.x, stackless-x.x.x といっぱい出てくるが、とりあえずこれらは無視して数字のものだけ考えれば良い
    * 例えば現時点での最新が 3.11.1 だとすると、3.10.9
    * 迷ったらとりあえずこれを入れておけば良い
    * 以下、3.10.9 を入れるものとする
* `> pyenv install 3.10.9`
    * Python 3.10.9 をインストール
* `> pyenv versions`
    * インストール済みのバージョン一覧を表示

### （余談）flake8 の設定のみが .flake8 に書いてある件について

* 一番最初に「なるべく設定を pyproject.toml にまとめる」と書いた
* 上記の setup.py を実行すると全ての環境設定・必要なパッケージのインストールが行われるが、flake8 の設定だけは .flake8 になっている
* これは、flake8 に pyproject.toml の設定を見に行く機能がないため
    * pyproject.toml の設定を見に行く [pyproject-flake8](https://github.com/csachs/pyproject-flake8) があるが、flake8 のバージョン依存関係を解決するのが難しかったり、そもそも上手く動かなかったりする
* なので、残念ながら flake8 の設定だけは .flake8 に記述することにする
    * [flake9](https://pypi.org/project/flake9/) というものもあるが、こちらが安定して動くようなら、切り替えても良いかもしれない

# プロジェクトの開発進行

プロジェクトの進め方（開発方法）をまとめる。

## パッケージの追加

* 動作に必要なパッケージ
    * `> poetry add <package>`
* 開発に必要なパッケージ
    * `> poetry add --group dev <package>`

## ユニットテストおよび文法チェック・型チェックを行う

* `> make tests`

## 自動生成されるドキュメントを更新する

* `> make docs`

## requirements.txt を更新する

Docker container を作るなど、必要な時に。

* `> make requirements`

## バージョン番号を更新して push する

* 変更を登録して commit する、もしくは branch から merge する
    * 変更の登録とコミット
        * `> git add [files]`
        * `> git commit`
    * main ブランチに develop ブランチの変更を取り込む:
        * `> git checkout main`
        * `> git merge develop`
* 現在の version, tag を確認する
    * `> git tag`
    * `> poetry version`
* バージョン番号を修正したタグを付け push する
    * `> make version-up VERSION=vX.X.X`
    * バージョン番号の先頭の `v` を忘れないこと
* バージョン番号を確認する
    * `> git tag`
    * `> poetry version`
    * 先頭の `v` を除いたバージョン番号が得られる

# 特殊なケース

通常は GitHub もしくは GitLab に remote repository を作成してから
プロジェクトを開始するが、それに当てはまらない特殊な場合。

## remote repository を作らない場合

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/tetutaro/python_project_best_practice/main/setup_local.sh)"
```

上記を行った後に必要な作業

* local repository の作成
    * `> git init`
* Python 仮想環境の作成
    * `> poetry shell`
* 開発用パッケージのインストール
    * `> poetry install`
* Python 仮想環境の設定
    * `> pyenv local [project]-XXX-pyXX`

## 後から sphinx の設定を行う場合

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/tetutaro/python_project_best_practice/main/setup_sphinx.sh)"
```

remote repository が無い状態のままだと、`docs/source/conf.py` がローカルのファイルを参照する設定になることに注意すること。

# 途中から poetry を使う

既存のプロジェクトでは、今まで poetry を使っていないこともある。そのプロジェクトに誰かが途中から加わる場合、環境構築がめんどくさい。そこでまずは、そのプロジェクトで poetry を使う（pyproject.toml を生成する）ように設定する。

以下の操作は既存プロジェクトで既にメンバーになっている人がやるべきで、新しく参加する人はこれら修正・変更が終わってから環境構築をする。

## GitHub, GitLab を使っていない場合

一刻も早く repository を作り、既存のソースコードを登録する。

repository を作れば、既存のソースコードを登録する方法が示されるので、それに従う。

## requirements.txt すらも無い場合

requirements.txt を作ることが最優先である。

何らかの Python 仮想環境を使っていれば、`> pip freeze > requirements.txt` で簡単に作れる。

そうではない場合は、ソースコードを見ながら、インストール済みの Python パッケージの中から必要なもの選んで requirements.txt を作るしか無い。

## requirements.txt から pyproject.toml を更新する

* poetry をインストールする
* プロジェクトディレクトリに行く
* `> poetry init --quiet`
* 生成された pyproject.toml を修正
    * 必要な設定を追加し、readme の設定を削除
* `> for package in $(cat requirements.txt); do poetry add --lock "${package}"; done`
    * （既にインストール済みだろうから）実際のインストールはせず、pyproject.toml のみを更新する
* `> poetry export --without-hashes -f requirements.txt -o requirements.txt`
    * requirements.txt の更新
* .gitignore に poetry.lock を追加する
* pyproject.toml, requirements.txt を add, commit, push する

# エディタの設定

* VIM
    * [python.vimrc](configs/python.vimrc) を `~/.vimrc` もしくは `~/.vim/vimrc` に加える。
    * VIM package manager としては [vim-plug](https://github.com/junegunn/vim-plug) を使う設定にしているので、他の manager を使う場合は Plug の部分を適切なものに読み替える。
