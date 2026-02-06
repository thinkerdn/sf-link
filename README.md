# Salesforce to CSV エクスポートアプリケーション

PythonでSalesforce APIを呼び出し、データをCSVファイルに出力するアプリケーションです。

## 機能

- Salesforceへの認証と接続（OAuth 2.0対応）
- 主要オブジェクトのデータをCSVエクスポート
  - Account（取引先）
  - Contact（取引先責任者）
  - Opportunity（商談）
  - Lead（リード）
  - Case（ケース）
- カスタムSOQLクエリによる柔軟なデータ取得
- 複数オブジェクトの一括エクスポート
- サマリーレポートの自動生成
- UTF-8 BOM付きCSV出力（Excel対応）

## 必要な環境

- Python 3.7以上
- Salesforceアカウント（本番環境またはサンドボックス）
- SalesforceセキュリティトークンまたはConnected App

## セットアップ

### 1. 依存パッケージのインストール

```bash
pip install -r requirements.txt
```

### 2. 環境変数の設定

`.env.example`ファイルを`.env`にコピーして、Salesforceの認証情報を設定します。

```bash
copy .env.example .env
```

### 3. 認証方法の選択

#### 方法A: ユーザー名・パスワード認証（従来の方法）

`.env`ファイルを編集：

```env
SF_USERNAME=your_username@example.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token
SF_DOMAIN=login  # サンドボックスの場合は 'test'
```

**セキュリティトークンの取得方法：**
1. Salesforceにログイン
2. 右上のユーザーアイコン → **設定**
3. **私の個人情報** → **私のセキュリティトークンのリセット**
4. メールで送られてくるトークンをコピー

#### 方法B: OAuth 2.0認証（推奨 - SOAP APIが無効な場合）

**Connected Appの作成手順：**

1. Salesforceにログイン
2. **設定** → **アプリケーション** → **アプリケーションマネージャ**
3. **新規接続アプリケーション**をクリック
4. 以下の情報を入力：
   - **接続アプリケーション名**: Python CSV Exporter
   - **API 参照名**: 自動入力
   - **取引先責任者メール**: あなたのメールアドレス
5. **API (OAuth 設定の有効化)** にチェック
6. **コールバック URL**: `https://login.salesforce.com/services/oauth2/success`
7. **選択した OAuth 範囲**に以下を追加：
   - `Full access (full)`
   - `Perform requests at any time (refresh_token, offline_access)`
8. **保存**をクリック
9. **コンシューマの詳細を管理**から**Consumer Key**と**Consumer Secret**をコピー

`.env`ファイルに設定：

```env
SF_USERNAME=your_username@example.com
SF_PASSWORD=your_password
SF_SECURITY_TOKEN=your_security_token  # OAuth使用時は省略可
SF_DOMAIN=login
SF_CONSUMER_KEY=your_consumer_key
SF_CONSUMER_SECRET=your_consumer_secret
```

## 使い方

### 基本的な使用方法

```bash
python main.py
```

アプリケーションを起動すると、以下のメニューが表示されます：

```
1. Account（取引先）
2. Contact（取引先責任者）
3. Opportunity（商談）
4. Lead（リード）
5. Case（ケース）
6. カスタムクエリを入力
7. 複数オブジェクトを一括エクスポート
```

### 使用例

#### 例1: Accountデータのエクスポート

```
選択してください (1-7): 1
取得件数を指定してください（空欄で全件）: 100
```

→ `output/Account_20260206_191234.csv` が生成されます

#### 例2: カスタムクエリの実行

```
選択してください (1-7): 6
SOQL: SELECT Id, Name, Industry FROM Account WHERE Industry = 'Technology'
出力ファイル名（拡張子なし）: tech_accounts
```

→ `output/tech_accounts_20260206_191234.csv` が生成されます

#### 例3: 複数オブジェクトの一括エクスポート

```
選択してください (1-7): 7
```

→ 以下のファイルが生成されます：
- `output/Account_20260206_191234.csv`
- `output/Contact_20260206_191234.csv`
- `output/Opportunity_20260206_191234.csv`
- `output/summary_report.csv`（サマリー）

### プログラムからの使用

```python
from salesforce_client import SalesforceClient
from csv_exporter import CSVExporter

# クライアントの初期化
client = SalesforceClient()
exporter = CSVExporter(output_dir='output')

# データの取得
result = client.query_all("SELECT Id, Name FROM Account LIMIT 10")

# CSVに出力
exporter.export_query_result(result, object_name='Account')
```

## 出力ファイル

### ファイル形式

- **エンコーディング**: UTF-8 BOM付き（Excelで文字化けしない）
- **ファイル名**: `{オブジェクト名}_{タイムスタンプ}.csv`
- **出力先**: `output/` ディレクトリ

### CSVファイルの内容

- 1行目: カラム名（フィールド名）
- 2行目以降: データレコード
- Salesforce内部情報（attributes）は除外

## プロジェクト構成

```
sf-link/
├── .env.example          # 環境変数のサンプルファイル
├── .gitignore           # Gitで無視するファイルの設定
├── README.md            # このファイル
├── requirements.txt     # 依存パッケージのリスト
├── salesforce_client.py # Salesforce APIクライアント
├── csv_exporter.py      # CSV出力機能
├── main.py             # メインアプリケーション
└── output/             # CSV出力先ディレクトリ（自動生成）
```

## クラスリファレンス

### SalesforceClient

Salesforce APIとの接続を管理するクラス

**主要メソッド:**
- `query(soql)`: SOQLクエリを実行（最大2000件）
- `query_all(soql)`: SOQLクエリを実行（全件取得）
- `describe_object(object_name)`: オブジェクトのメタデータを取得
- `get_object_fields(object_name)`: オブジェクトのフィールド一覧を取得

### CSVExporter

SalesforceデータをCSVに出力するクラス

**主要メソッド:**
- `export_query_result(query_result, filename, object_name)`: クエリ結果をCSV出力
- `export_multiple_objects(data_dict)`: 複数オブジェクトを一括出力
- `create_summary_report(data_dict, filename)`: サマリーレポートを作成

## トラブルシューティング

### SOAP APIが無効というエラー

```
INVALID_OPERATION: SOAP API login() is disabled by default in this org.
```

このエラーが発生した場合、以下のいずれかの方法で解決できます：

#### 解決方法1: SOAP APIを有効化する（管理者権限が必要）

1. Salesforceにシステム管理者としてログイン
2. **設定** → **セキュリティ** → **セッションの設定**
3. **API アクセス**セクションで以下を確認：
   - **SOAP API を使用したログインを有効化** にチェックを入れる
4. **保存**をクリック

**注意:** この設定を変更するには、システム管理者権限が必要です。権限がない場合は、組織の管理者に依頼するか、下記の解決方法2を使用してください。

#### 解決方法2: OAuth 2.0認証を使用する（推奨）

管理者権限がない場合や、セキュリティポリシーでSOAP APIを有効化できない場合は、OAuth 2.0認証を使用してください。

→ 上記「方法B: OAuth 2.0認証」の手順に従ってConnected Appを作成し、Consumer KeyとSecretを設定してください。

### OAuth認証エラー（invalid_client_id）が発生する場合

```
OAuth認証失敗: {"error":"invalid_client_id","error_description":"client identifier invalid"}
```

このエラーは、Consumer Key（Client ID）が無効または正しくないことを示しています。

#### 原因と解決方法

**1. Consumer Keyのコピーミス**
- Consumer Keyに余分なスペースや改行が含まれていないか確認
- Consumer Keyを再度コピー＆ペーストして確認

**2. 環境の不一致（本番 vs サンドボックス）**

Connected Appを作成した環境と、`.env`の`SF_DOMAIN`設定が一致している必要があります。

**本番環境でConnected Appを作成した場合:**
```env
SF_DOMAIN=login
```

**サンドボックス環境でConnected Appを作成した場合:**
```env
SF_DOMAIN=test
```

**確認方法:**
- ユーザー名に`.sandbox`や特殊なドメインが含まれている場合はサンドボックス
- Connected Appを作成したSalesforce環境のURLを確認
  - `https://login.salesforce.com` → 本番環境
  - `https://test.salesforce.com` または `https://[instance].sandbox.my.salesforce.com` → サンドボックス

**3. Connected Appが承認されていない**

Connected App作成直後は、使用できるまで数分かかる場合があります。

**解決方法:**
1. 5-10分待ってから再試行
2. Connected Appの設定を確認：
   - **設定** → **アプリケーション** → **接続アプリケーション**
   - 該当のアプリを選択
   - **状態**が「有効」になっているか確認

**4. Consumer KeyとSecretの再取得**

Consumer KeyまたはSecretが正しくない可能性があります。

**手順:**
1. **設定** → **アプリケーション** → **アプリケーションマネージャ**
2. 該当のConnected Appの右側の▼をクリック → **参照**
3. **API (OAuth 設定の有効化)** セクションで**コンシューマ鍵を管理**をクリック
4. Consumer KeyとConsumer Secretを再度コピー
5. `.env`ファイルを更新

**5. 正しいConnected Appを使用しているか確認**

複数のConnected Appがある場合、間違ったものを使用している可能性があります。

**確認方法:**
- Connected Appの名前を確認
- 最近作成したものを使用しているか確認

### OAuth認証エラー（invalid_grant）が発生する場合

```
OAuth認証失敗: {"error":"invalid_grant","error_description":"authentication failure"}
```

このエラーは以下の原因で発生します：

#### 1. セキュリティトークンの問題

OAuth 2.0のパスワードフローでは、パスワードとセキュリティトークンを結合する必要があります。

**解決方法:**
- `.env`ファイルで`SF_SECURITY_TOKEN`が正しく設定されているか確認
- セキュリティトークンをリセットして最新のものを使用
- パスワードを変更した場合は、セキュリティトークンも自動的にリセットされます

#### 2. Connected Appの設定不足

**確認事項:**
1. Connected Appで「**リラックスされた IP 制限を有効化**」を設定
   - Connected App → **編集** → **IP リラックス** を「**リラックスされた IP 制限を有効化**」に設定
2. OAuth設定で「**選択した OAuth 範囲**」に以下が含まれているか確認：
   - `Full access (full)`
   - `Perform requests at any time (refresh_token, offline_access)`
3. Connected Appの承認待ち状態を解除
   - 作成直後は承認待ちの場合があります
   - **設定** → **アプリケーション** → **接続アプリケーション** → 該当のアプリを選択
   - **編集** → **許可されているユーザー** を「**すべてのユーザーは自己承認**」に設定

#### 3. ユーザー権限の問題

**確認事項:**
- ユーザーがConnected Appを使用する権限を持っているか
- プロファイルまたは権限セットでAPI有効化されているか

#### 4. ドメインの設定

サンドボックス環境の場合：
```env
SF_DOMAIN=test
```

本番環境の場合：
```env
SF_DOMAIN=login
```

#### 5. パスワードに特殊文字が含まれる場合

パスワードに特殊文字（`!`, `@`, `#`, `$`など）が含まれる場合、正しくエンコードされない可能性があります。

**一時的な回避策:**
- パスワードを英数字のみに変更してテスト
- または、ユーザー名・パスワード認証（方法A）を使用

### 認証エラーが発生する場合（一般）

- ユーザー名、パスワード、セキュリティトークンが正しいか確認
- サンドボックス環境の場合、`SF_DOMAIN=test`に設定
- OAuth認証の場合、Consumer KeyとSecretが正しいか確認
- パスワードを最近変更した場合は、セキュリティトークンをリセット

### CSVファイルが文字化けする場合

- UTF-8 BOM付きで出力されているため、通常は文字化けしません
- Excelで開く場合は、ファイルをダブルクリックで開いてください
- それでも文字化けする場合は、「データ」→「テキストファイル」からインポート

### API制限について

Salesforceには1日あたりのAPI呼び出し制限があります。大量のデータを取得する場合は注意してください。

## 高度な使用例

### 特定の条件でフィルタリング

```python
# 特定の業種のAccountのみ取得
soql = "SELECT Id, Name, Industry FROM Account WHERE Industry = 'Technology'"
result = client.query_all(soql)
exporter.export_query_result(result, object_name='Tech_Accounts')
```

### 日付範囲でフィルタリング

```python
# 今月作成されたOpportunityを取得
soql = """
SELECT Id, Name, Amount, CloseDate 
FROM Opportunity 
WHERE CreatedDate = THIS_MONTH
"""
result = client.query_all(soql)
exporter.export_query_result(result, object_name='Opportunities_This_Month')
```

### リレーション先のデータも取得

```python
# ContactとそのAccountの情報を取得
soql = """
SELECT Id, FirstName, LastName, Email, 
       Account.Name, Account.Industry, Account.BillingCity
FROM Contact
"""
result = client.query_all(soql)
exporter.export_query_result(result, object_name='Contacts_With_Account')
```

## 参考リンク

- [Salesforce REST API ドキュメント](https://developer.salesforce.com/docs/atlas.ja-jp.api_rest.meta/api_rest/)
- [SOQL リファレンス](https://developer.salesforce.com/docs/atlas.ja-jp.soql_sosl.meta/soql_sosl/)
- [Simple Salesforce ライブラリ](https://github.com/simple-salesforce/simple-salesforce)
- [Pandas ドキュメント](https://pandas.pydata.org/docs/)

## ライセンス

このプロジェクトはMITライセンスの下で公開されています。