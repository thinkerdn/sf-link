"""
CSV出力機能
SalesforceのデータをCSVファイルに出力するクラス
"""

import pandas as pd
from datetime import datetime
import os


class CSVExporter:
    """SalesforceデータをCSVに出力するクラス"""
    
    def __init__(self, output_dir='output'):
        """
        初期化
        
        Args:
            output_dir (str): CSV出力先ディレクトリ
        """
        self.output_dir = output_dir
        self._ensure_output_dir()
    
    def _ensure_output_dir(self):
        """出力ディレクトリが存在しない場合は作成"""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"✓ 出力ディレクトリを作成しました: {self.output_dir}")
    
    def export_query_result(self, query_result, filename=None, object_name='data'):
        """
        クエリ結果をCSVファイルに出力
        
        Args:
            query_result (dict): Salesforceクエリの結果
            filename (str): 出力ファイル名（省略時は自動生成）
            object_name (str): オブジェクト名（ファイル名生成に使用）
            
        Returns:
            str: 出力されたファイルのパス
        """
        if not query_result or query_result.get('totalSize', 0) == 0:
            print("✗ 出力するデータがありません")
            return None
        
        try:
            # レコードをDataFrameに変換
            records = query_result['records']
            
            # 'attributes'フィールドを除外（Salesforce内部情報）
            cleaned_records = []
            for record in records:
                cleaned_record = {k: v for k, v in record.items() if k != 'attributes'}
                cleaned_records.append(cleaned_record)
            
            df = pd.DataFrame(cleaned_records)
            
            # ファイル名の生成
            if filename is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{object_name}_{timestamp}.csv"
            
            # .csv拡張子がない場合は追加
            if not filename.endswith('.csv'):
                filename += '.csv'
            
            # フルパスの生成
            filepath = os.path.join(self.output_dir, filename)
            
            # CSVファイルに出力（UTF-8 BOM付き - Excelで文字化けしないように）
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            print(f"✓ CSVファイルを出力しました: {filepath}")
            print(f"  - レコード数: {len(df)}")
            print(f"  - カラム数: {len(df.columns)}")
            print(f"  - カラム: {', '.join(df.columns.tolist())}")
            
            return filepath
            
        except Exception as e:
            print(f"✗ CSV出力エラー: {e}")
            return None
    
    def export_multiple_objects(self, data_dict):
        """
        複数のオブジェクトのデータを一括でCSV出力
        
        Args:
            data_dict (dict): {オブジェクト名: クエリ結果} の辞書
            
        Returns:
            list: 出力されたファイルパスのリスト
        """
        exported_files = []
        
        for object_name, query_result in data_dict.items():
            filepath = self.export_query_result(
                query_result,
                object_name=object_name
            )
            if filepath:
                exported_files.append(filepath)
        
        return exported_files
    
    def create_summary_report(self, data_dict, filename='summary_report.csv'):
        """
        複数オブジェクトのサマリーレポートを作成
        
        Args:
            data_dict (dict): {オブジェクト名: クエリ結果} の辞書
            filename (str): 出力ファイル名
            
        Returns:
            str: 出力されたファイルのパス
        """
        try:
            summary_data = []
            
            for object_name, query_result in data_dict.items():
                if query_result:
                    total_size = query_result.get('totalSize', 0)
                    records = query_result.get('records', [])
                    columns = len(records[0].keys()) - 1 if records else 0  # -1 for 'attributes'
                    
                    summary_data.append({
                        'オブジェクト名': object_name,
                        'レコード数': total_size,
                        'カラム数': columns
                    })
            
            df = pd.DataFrame(summary_data)
            filepath = os.path.join(self.output_dir, filename)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            print(f"✓ サマリーレポートを出力しました: {filepath}")
            return filepath
            
        except Exception as e:
            print(f"✗ サマリーレポート出力エラー: {e}")
            return None