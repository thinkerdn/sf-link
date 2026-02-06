"""
Salesforce to CSV エクスポートアプリケーション
Salesforceからデータを取得してCSVファイルに出力する
"""

from salesforce_client import SalesforceClient
from csv_exporter import CSVExporter


def main():
    """メイン処理"""
    print("=" * 70)
    print("Salesforce to CSV エクスポートアプリケーション")
    print("=" * 70)
    print()
    
    try:
        # Salesforceクライアントの初期化
        print("【1】Salesforceに接続中...")
        client = SalesforceClient()
        print()
        
        # CSV出力クラスの初期化
        exporter = CSVExporter(output_dir='output')
        print()
        
        # エクスポートするデータの選択
        print("【2】エクスポートするデータを選択してください")
        print("-" * 70)
        print("1. Account（取引先）")
        print("2. Contact（取引先責任者）")
        print("3. Opportunity（商談）")
        print("4. Lead（リード）")
        print("5. Case（ケース）")
        print("6. カスタムクエリを入力")
        print("7. 複数オブジェクトを一括エクスポート")
        print("-" * 70)
        
        choice = input("選択してください (1-7): ").strip()
        print()
        
        if choice == '1':
            # Accountのエクスポート
            print("【3】Accountデータを取得中...")
            limit = input("取得件数を指定してください（空欄で全件）: ").strip()
            
            if limit and limit.isdigit():
                soql = f"SELECT Id, Name, Type, Industry, Phone, Website, BillingCity, BillingCountry FROM Account LIMIT {limit}"
            else:
                soql = "SELECT Id, Name, Type, Industry, Phone, Website, BillingCity, BillingCountry FROM Account"
            
            result = client.query_all(soql)
            if result:
                exporter.export_query_result(result, object_name='Account')
        
        elif choice == '2':
            # Contactのエクスポート
            print("【3】Contactデータを取得中...")
            limit = input("取得件数を指定してください（空欄で全件）: ").strip()
            
            if limit and limit.isdigit():
                soql = f"SELECT Id, FirstName, LastName, Email, Phone, Title, AccountId, Account.Name FROM Contact LIMIT {limit}"
            else:
                soql = "SELECT Id, FirstName, LastName, Email, Phone, Title, AccountId, Account.Name FROM Contact"
            
            result = client.query_all(soql)
            if result:
                exporter.export_query_result(result, object_name='Contact')
        
        elif choice == '3':
            # Opportunityのエクスポート
            print("【3】Opportunityデータを取得中...")
            limit = input("取得件数を指定してください（空欄で全件）: ").strip()
            
            if limit and limit.isdigit():
                soql = f"SELECT Id, Name, StageName, Amount, CloseDate, AccountId, Account.Name FROM Opportunity LIMIT {limit}"
            else:
                soql = "SELECT Id, Name, StageName, Amount, CloseDate, AccountId, Account.Name FROM Opportunity"
            
            result = client.query_all(soql)
            if result:
                exporter.export_query_result(result, object_name='Opportunity')
        
        elif choice == '4':
            # Leadのエクスポート
            print("【3】Leadデータを取得中...")
            limit = input("取得件数を指定してください（空欄で全件）: ").strip()
            
            if limit and limit.isdigit():
                soql = f"SELECT Id, FirstName, LastName, Company, Email, Phone, Status, LeadSource FROM Lead LIMIT {limit}"
            else:
                soql = "SELECT Id, FirstName, LastName, Company, Email, Phone, Status, LeadSource FROM Lead"
            
            result = client.query_all(soql)
            if result:
                exporter.export_query_result(result, object_name='Lead')
        
        elif choice == '5':
            # Caseのエクスポート
            print("【3】Caseデータを取得中...")
            limit = input("取得件数を指定してください（空欄で全件）: ").strip()
            
            if limit and limit.isdigit():
                soql = f"SELECT Id, CaseNumber, Subject, Status, Priority, Origin, AccountId, Account.Name FROM Case LIMIT {limit}"
            else:
                soql = "SELECT Id, CaseNumber, Subject, Status, Priority, Origin, AccountId, Account.Name FROM Case"
            
            result = client.query_all(soql)
            if result:
                exporter.export_query_result(result, object_name='Case')
        
        elif choice == '6':
            # カスタムクエリ
            print("【3】カスタムSOQLクエリを入力してください")
            print("例: SELECT Id, Name FROM Account WHERE Industry = 'Technology'")
            soql = input("SOQL: ").strip()
            
            if soql:
                result = client.query_all(soql)
                if result:
                    object_name = input("出力ファイル名（拡張子なし）: ").strip() or 'custom_query'
                    exporter.export_query_result(result, object_name=object_name)
        
        elif choice == '7':
            # 複数オブジェクトの一括エクスポート
            print("【3】複数オブジェクトのデータを取得中...")
            
            # 各オブジェクトのデータを取得
            data_dict = {}
            
            print("  - Accountデータを取得中...")
            account_result = client.query_all("SELECT Id, Name, Type, Industry, Phone FROM Account LIMIT 100")
            if account_result:
                data_dict['Account'] = account_result
            
            print("  - Contactデータを取得中...")
            contact_result = client.query_all("SELECT Id, FirstName, LastName, Email, Phone FROM Contact LIMIT 100")
            if contact_result:
                data_dict['Contact'] = contact_result
            
            print("  - Opportunityデータを取得中...")
            opportunity_result = client.query_all("SELECT Id, Name, StageName, Amount, CloseDate FROM Opportunity LIMIT 100")
            if opportunity_result:
                data_dict['Opportunity'] = opportunity_result
            
            print()
            print("【4】CSVファイルを出力中...")
            exported_files = exporter.export_multiple_objects(data_dict)
            
            # サマリーレポートの作成
            print()
            print("【5】サマリーレポートを作成中...")
            exporter.create_summary_report(data_dict)
            
            print()
            print(f"✓ 合計 {len(exported_files)} 個のファイルを出力しました")
        
        else:
            print("✗ 無効な選択です")
        
        print()
        print("=" * 70)
        print("処理が完了しました")
        print("=" * 70)
        
    except ValueError as e:
        print(f"\n設定エラー: {e}")
        print("\n.envファイルを作成し、Salesforceの認証情報を設定してください。")
        print("詳細はREADME.mdを参照してください。")
    except Exception as e:
        print(f"\nエラーが発生しました: {e}")


if __name__ == "__main__":
    main()