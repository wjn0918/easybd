import pandas as pd
import json
import re
from typing import List, Dict, Any, Tuple


class ExcelProcessor:
    def __init__(self, file_path: str):
        """
        初始化Excel处理器

        Args:
            file_path: Excel文件路径
        """
        self.file_path = file_path
        self.excel_file = pd.ExcelFile(file_path)

    def concat_columns(self, sheet_name: str, selected_columns: List[str],
                       concat_template: str) -> str:
        """
        根据模板拼接指定列

        Args:
            sheet_name: sheet名称
            selected_columns: 前端选择的列
            concat_template: 拼接模板
        Returns:
            处理结果
        """
        try:
            # 读取数据
            df = pd.read_excel(self.file_path, sheet_name=sheet_name)

            # 初始化结果列为空字符串
            df['r'] = ''

            # 记录当前模板字符串
            current_template = concat_template

            # 按照selected_columns的顺序处理每一列
            for i, col in enumerate(selected_columns):
                if col not in df.columns:
                    return {'error': f'列 {col} 不存在于数据中'}

                # 查找列名在模板中的位置
                if col in current_template:
                    # 分割模板，获取前缀和后缀
                    parts = current_template.split(col, 1)  # 只分割第一次出现的位置
                    prefix = parts[0]  # 列名前的部分

                    if len(parts) > 1:
                        suffix = parts[1]  # 列名后的部分
                        current_template = suffix  # 更新剩余模板
                    else:
                        suffix = ''
                        current_template = ''

                    # 拼接到结果列
                    if i == 0:
                        # 第一列：前缀 + 列数据
                        df['r'] = prefix + df[col].astype(str)
                    else:
                        # 后续列：累加前缀 + 列数据
                        df['r'] = df['r'] + prefix + df[col].astype(str)

                    # 如果是最后一列，添加剩余的后缀
                    if i == len(selected_columns) - 1 and current_template:
                        df['r'] = df['r'] + current_template

            # 处理空值
            df['r'] = df['r'].replace('nan', '')
            lines = df['r'].tolist()
            final_string = '\n'.join(lines)
            return final_string

        except Exception as e:
            print(f"拼接过程中出现错误: {e}")
            return  f'拼接失败: {str(e)}'

# 测试和使用示例
def template_parsing():
    """测试模板解析功能"""
    processor = ExcelProcessor('C:\\Users\\wjn_0\\Desktop\\cs.xlsx')  # 假设存在测试文件
    selected_columns = ["A","B"]

    test_templates = [
        '"A":"B"',  # A列:B列
    ]

    print("模板解析测试:")
    for template in test_templates:
        parsed = processor.concat_columns("Sheet3",selected_columns, template)
        print(parsed)


if __name__ == '__main__':
    # 运行模板解析测试
    template_parsing()

