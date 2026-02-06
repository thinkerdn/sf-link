"""
Salesforce API クライアント
Salesforceへの接続とデータ操作を行うクラス
"""

import os
import requests
from simple_salesforce import Salesforce
from dotenv import load_dotenv


class SalesforceClient:
    """Salesforce APIとの接続を管理するクライアントクラス"""
    
    def __init__(self):
        """環境変数から認証情報を読み込み、Salesforceに接続"""
        load_dotenv()
        
        self.username = os.getenv('SF_USERNAME')
        self.password = os.getenv('SF_PASSWORD')
        self.security_token = os.getenv('SF_SECURITY_TOKEN')
        self.domain = os.getenv('SF_DOMAIN', 'login')
        self.consumer_key = os.getenv('SF_CONSUMER_KEY')
        self.consumer_secret = os.getenv('SF_CONSUMER_SECRET')
        
        # OAuth認証を使用する場合
        if self.consumer_key and self.consumer_secret:
            if not all([self.username, self.password, self.consumer_key, self.consumer_secret]):
                raise ValueError("OAuth認証に必要な環境変数が設定されていません。")
        # ユーザー名・パスワード認証を使用する場合
        else:
            if not all([self.username, self.password, self.security_token]):
                raise ValueError("環境変数が設定されていません。.envファイルを確認してください。")
        
        self.sf = None
        self.connect()
    
    def connect(self):
        """Salesforceに接続"""
        try:
            # OAuth 2.0認証を使用（Consumer KeyとSecretが設定されている場合）
            if self.consumer_key and self.consumer_secret:
                print("OAuth 2.0認証を使用して接続中...")
                session_id, instance = self._get_oauth_token()
                self.sf = Salesforce(
                    instance=instance,
                    session_id=session_id
                )
            # 従来のユーザー名・パスワード認証を使用
            else:
                print("ユーザー名・パスワード認証を使用して接続中...")
                self.sf = Salesforce(
                    username=self.username,
                    password=self.password,
                    security_token=self.security_token,
                    domain=self.domain
                )
            
            print(f"✓ Salesforceに正常に接続しました (ユーザー: {self.username})")
            return True
        except Exception as e:
            print(f"✗ Salesforce接続エラー: {e}")
            print("\nヒント:")
            print("- SOAP APIが無効な場合は、OAuth 2.0認証を使用してください")
            print("- Connected Appを作成し、Consumer KeyとSecretを.envに設定してください")
            print("- 詳細はREADME.mdの「OAuth 2.0認証の設定」セクションを参照してください")
            # 接続失敗時は例外を発生させる
            raise ConnectionError(f"Salesforceへの接続に失敗しました: {e}")
    
    def _get_oauth_token(self):
        """OAuth 2.0トークンを取得"""
        token_url = f"https://{self.domain}.salesforce.com/services/oauth2/token"
        
        data = {
            'grant_type': 'password',
            'client_id': self.consumer_key,
            'client_secret': self.consumer_secret,
            'username': self.username,
            'password': self.password + (self.security_token or '')
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            oauth_response = response.json()
            instance_url = oauth_response['instance_url']
            # instance_urlから instance部分を抽出（例: https://na1.salesforce.com -> na1.salesforce.com）
            instance = instance_url.replace('https://', '').replace('http://', '')
            return oauth_response['access_token'], instance
        else:
            raise Exception(f"OAuth認証失敗: {response.text}")
    
    def query(self, soql):
        """
        SOQLクエリを実行
        
        Args:
            soql (str): 実行するSOQLクエリ
            
        Returns:
            dict: クエリ結果
        """
        if self.sf is None:
            raise ConnectionError("Salesforceに接続されていません。接続を確認してください。")
        
        try:
            result = self.sf.query(soql)
            print(f"✓ クエリ実行成功: {result['totalSize']}件のレコードを取得")
            return result
        except Exception as e:
            print(f"✗ クエリ実行エラー: {e}")
            return None
    
    def query_all(self, soql):
        """
        SOQLクエリを実行（全レコード取得）
        
        Args:
            soql (str): 実行するSOQLクエリ
            
        Returns:
            dict: クエリ結果（全レコード）
        """
        if self.sf is None:
            raise ConnectionError("Salesforceに接続されていません。接続を確認してください。")
        
        try:
            result = self.sf.query_all(soql)
            print(f"✓ クエリ実行成功: {result['totalSize']}件のレコードを取得")
            return result
        except Exception as e:
            print(f"✗ クエリ実行エラー: {e}")
            return None
    
    def describe_object(self, object_name):
        """
        オブジェクトのメタデータを取得
        
        Args:
            object_name (str): オブジェクト名（例: 'Account', 'Contact'）
            
        Returns:
            dict: オブジェクトのメタデータ
        """
        if self.sf is None:
            raise ConnectionError("Salesforceに接続されていません。接続を確認してください。")
        
        try:
            metadata = getattr(self.sf, object_name).describe()
            print(f"✓ {object_name}のメタデータ取得成功")
            return metadata
        except Exception as e:
            print(f"✗ メタデータ取得エラー: {e}")
            return None
    
    def get_object_fields(self, object_name):
        """
        オブジェクトのフィールド一覧を取得
        
        Args:
            object_name (str): オブジェクト名
            
        Returns:
            list: フィールド名のリスト
        """
        metadata = self.describe_object(object_name)
        if metadata:
            fields = [field['name'] for field in metadata['fields']]
            return fields
        return []