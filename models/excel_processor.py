import json
import logging

import pandas as pd
from typing import List, Dict, Any, Tuple

from easybd.conf import JDBCConf
from easybd.datax import DataXReaderType
from easybd.datax.datax_type import DataXWriterType
from easybd.db.ddl import DDLType
from easybd.excel import Excel
from models.excelModel import ExcelModel, ExcelInfo


class ExcelProcessor:
    def __init__(self, file_path: str, excel_info: ExcelInfo=None):
        """
        初始化Excel处理器

        Args:
            file_path: Excel文件路径
        """
        self.file_path = file_path
        self.excel_file = pd.ExcelFile(file_path)
        # 读取所有 sheet 到字典，避免后续重复读文件
        self.sheets_df = {sheet: pd.read_excel(self.file_path, sheet_name=sheet) for sheet in
                          self.excel_file.sheet_names}
        self.excel_info = excel_info


    def to_dml(self):
        t = Excel(self.file_path, sheet_name=self.excel_info.sheetName, table_name=self.excel_info.tableName)
        return t.to_dml2()

    def to_ddl(self):
        t = Excel(self.file_path, sheet_name=self.excel_info.sheetName, table_name=self.excel_info.tableName)
        db_type = self.excel_info.sqlConf.dbType.upper()
        print(db_type)
        ddl_type: DDLType = DDLType.__members__.get(self.excel_info.sqlConf.dbType.upper())
        ddl_json = t.to_ddl2(ddl_type)
        return ddl_json

    def to_datax(self):
        sheet_name = self.excel_info.sheetName
        table_name = self.excel_info.tableName
        datax_conf = self.excel_info.dataXConf
        reader_type = datax_conf.readerType
        writer_type = datax_conf.writerType
        print(datax_conf)
        if sheet_name not in self.sheets_df:
            raise ValueError(f"Sheet {sheet_name} 不存在")
        try:
            parameter = json.loads(datax_conf.parameter)
            print(parameter)
        except Exception as e:
            print("datax 未配置")

        rt: DataXReaderType = DataXReaderType.__members__.get(reader_type)
        wt: DataXWriterType = DataXWriterType.__members__.get(writer_type)


        source_host = "10.200.10.22"
        source_port = 5432
        source_db = "schooletl"
        source_user = "postgres"
        source_password = "Pgsql@2024"
        jdbc_conf = JDBCConf("pgsql", source_host, source_port, source_db, source_user, source_password)

        target_host = "47.97.35.199"
        target_port = 54321
        target_db = "tx"
        target_user = "postgres"
        target_password = "Pgsql@2024"
        target_jdbc_conf = JDBCConf("pgsql", target_host, target_port, target_db, target_user, target_password)

        t = Excel(self.file_path, sheet_name=sheet_name, table_name=table_name)
        datax_json = t.to_datax(rt, wt, t.table_meta[0], jdbc_conf, target_jdbc_conf)
        if isinstance(datax_json, str):
            datax_json = json.loads(datax_json)  # 只做一次解析
        # 数据库更改
        if rt == DataXReaderType.PGSQL or rt == DataXReaderType.MYSQL:
            logging.info("开始替换reader 配置======")
            datax_json['job']['content'][0]['reader']['parameter']['connection'][0]['jdbcUrl'][0] = parameter[
                'readerJdbcUrl']
            datax_json['job']['content'][0]['reader']['parameter']['username'] = parameter['readerUserName']
            datax_json['job']['content'][0]['reader']['parameter']['password'] = parameter['readerPassword']
        if rt == DataXReaderType.SRAPI:
            datax_json['job']['content'][0]['reader']['parameter']['appId'] = parameter['appId']
            datax_json['job']['content'][0]['reader']['parameter']['appSecret'] = parameter['appSecret']
            datax_json['job']['content'][0]['reader']['parameter']['compId'] = parameter['compId']
            datax_json['job']['content'][0]['reader']['parameter']['debug'] = False
            datax_json['job']['content'][0]['reader']['parameter']['body'] = parameter['body']
        if wt == DataXWriterType.PGSQL or wt == DataXWriterType.CLICKHOUSE:
            logging.info("开始替换 writer 配置======")
            datax_json['job']['content'][0]['writer']['parameter']['connection'][0]['jdbcUrl'] = parameter['writerJdbcUrl']
            datax_json['job']['content'][0]['writer']['parameter']['username'] = parameter['writerUserName']
            datax_json['job']['content'][0]['writer']['parameter']['password'] = parameter['writerPassword']
        # if reader_type == DataXReaderType.HIKAPI:
        #     if isinstance(datax_json, str):
        #         datax_json = json.loads(datax_json)
        #     hikapiConf = json.loads(dataxModel.hikapiConf)
        #     print(f"hikapiConf : {hikapiConf}")
        #     datax_json['job']['content'][0]['reader']['parameter']['host'] = hikapiConf['host']
        #     datax_json['job']['content'][0]['reader']['parameter']['appKey'] = hikapiConf['appKey']
        #     datax_json['job']['content'][0]['reader']['parameter']['appSecret'] = hikapiConf['appSecret']
        #     datax_json['job']['content'][0]['reader']['parameter']['jsonData'] = hikapiConf['jsonData']
        #     if writer_type == DataXWriterType.STREAM:
        #         datax_json['job']['content'][0]['reader']['parameter']['page']["ifPage"] = False
        #     datax_json = json.dumps(datax_json)
        datax_json = json.dumps(datax_json)
        print(datax_json)

        return datax_json

    def get_cols(self, sheet_name: str):
        """
                获取指定 sheet 的所有列名

                Args:
                    sheet_name: sheet名称

                Returns:
                    列名列表
                """
        if sheet_name not in self.sheets_df:
            raise ValueError(f"Sheet {sheet_name} 不存在")
        return list(self.sheets_df[sheet_name].columns)

    def get_tables(self, sheet_name: str):
        """
                获取指定 sheet 的所有列名

                Args:
                    sheet_name: sheet名称

                Returns:
                    列名列表
                """
        if sheet_name not in self.sheets_df:
            raise ValueError(f"Sheet {sheet_name} 不存在")
        df = self.sheets_df[sheet_name]
        table_list = df[['表名', '表备注']].drop_duplicates().apply(lambda x: tuple(x), axis=1).values.tolist()
        return table_list

    def get_sheets(self):
        """获取所有 sheet 名称"""
        return self.excel_file.sheet_names

    def filter_data(self, sheet_name:str = None):
        df = self.sheets_df[sheet_name].copy()
        try:
            for step in self.excel_info.transformSteps:
                if step.action == "filter":
                    df = df[eval(step.expr, {"__builtins__": {}}, {"df": df})]
                elif step.action == "assign":
                    exec(step.expr, {"__builtins__": {}}, {"df": df})
                elif step.action == "rename":
                    df = df.rename(columns=step.expr)
                elif step.action == "dropna":
                    df = df.dropna(subset=step.expr)
                else:
                    return {"error": f"不支持的操作类型: {step.action}"}
        except Exception as e:
            return {"error": f"处理数据失败: {str(e)}"}
        return df

    def to_json(self, excel_info: ExcelInfo):
        df = self.sheets_df[self.excel_file.sheet_names[0]].copy()
        try:
            for step in excel_info.transformSteps:
                if step.action == "filter":
                    df = df[eval(step.expr, {"__builtins__": {}}, {"df": df})]
                elif step.action == "assign":
                    exec(step.expr, {"__builtins__": {}}, {"df": df})
                elif step.action == "rename":
                    df = df.rename(columns=step.expr)
                elif step.action == "dropna":
                    df = df.dropna(subset=step.expr)
                else:
                    return {"error": f"不支持的操作类型: {step.action}"}
        except Exception as e:
            return {"error": f"处理数据失败: {str(e)}"}

        return df.to_json(orient='records', force_ascii=False)

    def concat_columns(self, sheet_name:str, selected_columns: List[str],
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
        if sheet_name not in self.sheets_df:
            return f"错误：Sheet {sheet_name} 不存在"
        df = self.filter_data(sheet_name)
        print(df)
        for col in selected_columns:
            if col not in df.columns:
                return f"错误：列 {col} 不存在于数据中"
        try:
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

