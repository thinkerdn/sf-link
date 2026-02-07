"""
環境変数を出力するスクリプト
"""

import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()

print("=" * 60)
print("Salesforce 環境変数の値")
print("=" * 60)

# 各環境変数を取得して出力
sf_username = os.getenv('SF_USERNAME')
sf_password = os.getenv('SF_PASSWORD')
sf_security_token = os.getenv('SF_SECURITY_TOKEN')
sf_domain = os.getenv('SF_DOMAIN', 'login')
sf_consumer_key = os.getenv('SF_CONSUMER_KEY')
sf_consumer_secret = os.getenv('SF_CONSUMER_SECRET')

print(f"SF_USERNAME: {sf_username}")
print(f"SF_PASSWORD: {sf_password}")
print(f"SF_SECURITY_TOKEN: {sf_security_token}")
print(f"SF_DOMAIN: {sf_domain}")
print(f"SF_CONSUMER_KEY: {sf_consumer_key}")
print(f"SF_CONSUMER_SECRET: {sf_consumer_secret}")
print("=" * 60)

# 設定状況の確認
print("\n設定状況:")
print("-" * 60)
if sf_username:
    print("✓ SF_USERNAME: 設定済み")
else:
    print("✗ SF_USERNAME: 未設定")

if sf_password:
    print("✓ SF_PASSWORD: 設定済み")
else:
    print("✗ SF_PASSWORD: 未設定")

if sf_security_token:
    print("✓ SF_SECURITY_TOKEN: 設定済み")
else:
    print("✗ SF_SECURITY_TOKEN: 未設定")

print(f"✓ SF_DOMAIN: {sf_domain} (デフォルト値)")

if sf_consumer_key:
    print("✓ SF_CONSUMER_KEY: 設定済み")
else:
    print("✗ SF_CONSUMER_KEY: 未設定")

if sf_consumer_secret:
    print("✓ SF_CONSUMER_SECRET: 設定済み")
else:
    print("✗ SF_CONSUMER_SECRET: 未設定")

print("-" * 60)

# 認証方式の判定
print("\n認証方式:")
print("-" * 60)
if sf_consumer_key and sf_consumer_secret:
    print("→ OAuth 2.0認証が利用可能")
    if sf_username and sf_password:
        print("  (Consumer KeyとSecretが設定されています)")
    else:
        print("  ⚠ ユーザー名またはパスワードが未設定です")
elif sf_username and sf_password and sf_security_token:
    print("→ ユーザー名・パスワード認証が利用可能")
else:
    print("⚠ 認証情報が不完全です")
print("-" * 60)