import xlsxwriter
from sqlalchemy import create_engine, text
import pandas as pd
import xlsxwriter as xw
import io
import re
import clickhouse_connect


class BaseDB:
    def __init__(self, url, *args):
        self.engine = create_engine(url, echo=True)
        self.connection = self.engine.connect()
        self.table_comment_sql = args[0]
        self.table_column_sql = args[1]
        self.table_info = self._get_table_info()
        self.metadata = self._get_table_comments()
        self.current_row = 0  # 统计sheet 当前行

    def _get_table_comments(self):
        """
        获取表名 表备注 表行数
        :return:
        """
        result = self.connection.execute(
            text(self.table_comment_sql).execution_options(autocommit=True))  # MySQL可能需要autocommit=True
        metadata = []
        for row in result:
            table_info = {}
            print(f"Table: {row.TABLE_NAME}, Comment: {row.TABLE_COMMENT}")
            table_info["table_name"] = row.TABLE_NAME
            table_info["table_comment"] = row.TABLE_COMMENT
            table_info["table_rows"] = row.TABLE_ROWS
            metadata.append(table_info)
        return metadata

    def _col2json(self, data: pd.DataFrame, all_table_col_list: list):
        """
        列信息转为json
        :param data:
        :return:
        """
        table_name = data.name
        data = data.reset_index(drop=True)
        cols = []
        for i, _ in enumerate(data["COLUMN_NAME"]):
            col_info = {}
            col_info["col_name"] = data["COLUMN_NAME"][i]
            col_info["col_type"] = data["COLUMN_TYPE"][i]
            col_info["col_comment"] = data["COLUMN_COMMENT"][i]
            cols.append(col_info)
        all_table_col_list.append({"table_name": table_name, "table_cols": cols})

    def _get_table_column(self):
        """
        获取数据库表的列信息
        :param sql:
        :return:
        """
        result = self.connection.execute(
            text(self.table_column_sql).execution_options(autocommit=True))  # MySQL可能需要autocommit=True
        all_table_cols = []
        pd.DataFrame(result).groupby("TABLE_NAME").apply(lambda data: self._col2json(data, all_table_cols))
        return all_table_cols

    def _get_table_info(self) -> pd.DataFrame:
        """
        获取表名，表备注，列名，数据类型，列备注
        :return:
        """
        table_column = pd.DataFrame(self._get_table_column())
        table_comment = pd.DataFrame(self._get_table_comments())
        table_info = table_comment.join(
            table_column.set_index("table_name"),
            on="table_name"
        )
        return table_info

    def _add_table_cell(self, data, sheet_table):
        table_name = data["table_name"]
        table_comment = data["table_comment"]
        table_rows = data["table_rows"]
        sheet1_title = ["表名", "表备注", "数据量"]
        # add title
        for i, item in enumerate(sheet1_title):
            sheet_table.write(0, i, item, self.title_format)
        # 添加表名和表备注
        sheet_table.write(data.name + 1, 0, table_name)
        sheet_table.write(data.name + 1, 1, table_comment)
        sheet_table.write(data.name + 1, 2, table_rows)

    def _add_cell(self, data, *sheets):
        title = ["表名", "表备注", "字段名称", "字段类型", "字段备注", "来源表", "来源表备注", "来源表别名", "来源字段",
                 "来源字段类型",
                 "来源字段备注", "字段映射", "where", "where 说明", "left join", "left_join说明"]  # 设置表头
        table_name = data["table_name"]
        table_comment = data["table_comment"]
        table_rows = data["table_rows"]
        col_info = data["table_cols"]
        print(table_name, table_comment, col_info)
        sheet1_title = ["表名", "表备注", "数据量"]
        sheet_table = sheets[0]
        # add title
        for i, item in enumerate(sheet1_title):
            sheet_table.write(0, i, item, self.title_format)
        # 添加表名和表备注
        sheet_table.write(data.name + 1, 0, table_name)
        sheet_table.write(data.name + 1, 1, table_comment)
        sheet_table.write(data.name + 1, 2, table_rows)

        sheet_table_col = sheets[1]
        # 添加title
        if self.current_row == 0:
            for i, item in enumerate(title):
                sheet_table_col.write(self.current_row, i, item, self.title_format)
            self.current_row += 1
        # 添加col信息
        for col in col_info:
            sheet_table_col.write(self.current_row, 0, table_name)
            sheet_table_col.write(self.current_row, 1, table_comment)
            sheet_table_col.write(self.current_row, 2, col["col_name"])
            sheet_table_col.write(self.current_row, 3, col["col_type"])
            sheet_table_col.write(self.current_row, 4, col["col_comment"])
            self.current_row += 1

    def table_info_to_excel(self, file_name, only_table=False):
        """
        数据库表结构信息导出为excel
        :param file_name:
        :param only_table: 仅导出表信息
        :return:
        """
        workbook = xw.Workbook(file_name, {'nan_inf_to_errors': True})  # 创建工作簿
        sheet1 = workbook.add_worksheet("表")  # 创建子表
        sheet2 = workbook.add_worksheet("表元数据")  # 创建子表

        # 设置格式
        self.title_format = workbook.add_format({'bold': True, 'bg_color': '#5B9BD5'})
        if only_table:
            self.table_info.apply(lambda data: self._add_table_cell(data, sheet1), axis=1)
        else:
            self.table_info.apply(lambda data: self._add_cell(data, sheet1, sheet2), axis=1)

        workbook.close()  # 关闭表

    def table_info_to_excel_io(self, only_table=False) -> io.BytesIO:
        """
        数据库表结构信息导出为excel，写入内存返回bytes
        :param only_table: 仅导出表信息
        :return: Excel文件的bytes内容
        """
        output = io.BytesIO()  # 内存流

        workbook = xlsxwriter.Workbook(output, {'nan_inf_to_errors': True})  # 以流创建工作簿
        sheet1 = workbook.add_worksheet("表")  # 创建子表
        sheet2 = workbook.add_worksheet("表元数据")  # 创建子表

        # 设置格式
        self.title_format = workbook.add_format({'bold': True, 'bg_color': '#5B9BD5'})
        if only_table:
            self.table_info.apply(lambda data: self._add_table_cell(data, sheet1), axis=1)
        else:
            self.table_info.apply(lambda data: self._add_cell(data, sheet1, sheet2), axis=1)

        workbook.close()
        output.seek(0)  # 回到流开头

        return output


    PG_TO_CH_TYPE = {
        'integer': 'Int32',
        'int': 'Int32',
        'bigint': 'Int64',
        'smallint': 'Int16',
        'serial': 'Int32',
        'bigserial': 'Int64',
        'boolean': 'UInt8',
        'text': 'String',
        'character varying': 'String',
        'varchar': 'String',
        'timestamp without time zone': 'DateTime',
        'timestamp with time zone': 'DateTime',
        'timestamptz': 'DateTime',
        'date': 'Date',
        'double precision': 'Float64',
        'real': 'Float32',
        'numeric': 'Float64',
        "bool": "UInt8",
    }

    def _clean_pg_type(self, pg_type: str) -> str:
        # 去除括号及其内容，如 varchar(36) -> varchar
        cleaned = re.sub(r"\(.*?\)", "", pg_type)

        # 去除非字母字符（如末尾数字或长度说明），如 varchar36 -> varchar
        cleaned = re.sub(r"[^a-zA-Z]+", "", cleaned)

        return cleaned.strip().lower()

    def generate_clickhouse_ddl(self,table_name, columns_df: pd.DataFrame):
        ddl_cols = []
        for _, row in columns_df.iterrows():
            name = row["col_name"]
            raw_type = row["col_type"]
            pg_type = self._clean_pg_type(raw_type)  # 👈 清理类型字符串

            ch_type = self.PG_TO_CH_TYPE.get(pg_type)
            if not ch_type:
                raise ValueError(f"未映射 PostgreSQL 类型：{pg_type}")
            ddl_cols.append(f"`{name}` {ch_type}")
        col_def = ', '.join(ddl_cols)
        ddl = f"CREATE TABLE IF NOT EXISTS {table_name} ( {col_def}) ENGINE = MergeTree ORDER BY tuple();"
        return ddl

    # === 检查并在 ClickHouse 中创建表 ===

    def sync_clickhouse_table(self, ch_cfg, table_name):
        client = clickhouse_connect.get_client(
            host=ch_cfg['host'],
            port=ch_cfg['port'],
            username=ch_cfg['username'],
            password=ch_cfg['password']
        )

        existing_tables = client.query(f"SHOW TABLES FROM {ch_cfg['database']}").result_rows
        table_exists = any(row[0] == table_name for row in existing_tables)

        columns_df = pd.DataFrame(self.table_info['table_cols'].to_list()[0])[['col_name', 'col_type']]

        if table_exists:
            print(f"✅ 表 `{table_name}` 已存在于 ClickHouse。")
        else:
            ddl = self.generate_clickhouse_ddl(table_name, columns_df)
            print(f"📝 创建 ClickHouse 表 SQL：\n{ddl}")
            client.command(f"USE {ch_cfg['database']}")
            client.command(ddl)
            print(f"✅ 已在 ClickHouse 创建表 `{table_name}`。")




if __name__ == '__main__':
    df = pd.DataFrame([{"a": 1, "COLUMN_NAME": 2}, {"a": 1, "COLUMN_NAME": 3}])
