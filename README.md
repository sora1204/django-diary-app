# Django 日記アプリ

## アプリ概要

Django で作成したシンプルな日記アプリです。  
日記の一覧表示、詳細表示、新規作成、編集、削除に加えて、ログイン状態に応じた表示切り替えや、作成者だけが編集・削除できる権限制御を実装しています。

## 使用技術

- Python 3.14
- Django 6.0.4
- SQLite3
- HTML
- CSS

## 主な機能

- 日記の一覧表示
- 日記の詳細表示
- 日記の新規作成
- 日記の編集
- 日記の削除
- ユーザー新規登録
- ログイン / ログアウト
- ログインユーザーと作成者の一致判定による編集・削除制御
- 作成日時 / 更新日時の表示

## セットアップ方法

1. 任意のディレクトリでこのリポジトリを取得します。
2. 仮想環境を作成して有効化します。
3. `.env.example` をコピーして `.env` を作成します。
4. `requirements.txt` を使って必要なパッケージをインストールします。
5. マイグレーションを適用します。

## 環境変数

GitHub に公開するため、`SECRET_KEY` はリポジトリに直書きせず `.env` から読み込むようにしています。

PowerShell では次のように `.env` を用意してください。

```powershell
Copy-Item .env.example .env
```

`.env` の中では最低限 `DJANGO_SECRET_KEY` を設定してください。

## 実行方法

```bash
python -m venv .venv
.venv\Scripts\activate
Copy-Item .env.example .env
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

ブラウザで `http://127.0.0.1:8000/` にアクセスするとアプリを確認できます。

## 今後の改善案

- 検索機能やカテゴリ機能の追加
- ページネーション対応
- テストコードの拡充
- 画像投稿やプロフィール機能の追加
- 本番環境を意識したデプロイ設定の追加
