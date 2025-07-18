from easybd.db import TableInfo


class DDLClickHouse:
    def __call__(self, table: TableInfo):

        table_name = table.table_name
        table_name_comment = table.table_comment
        table_fields = table.table_fields
        table_fields_comment = table.table_fields_comment
        table_fields_type = table.table_fields_type
        fields = []
        fields_comment = []

        for i in range(0, len(table_fields)):
            # column_name = camel_to_snake(table_fields[i])
            column_name = table_fields[i]
            column_comment = "" if isinstance(table_fields_comment[i], float) else table_fields_comment[i]
            tft_upper = table_fields_type[i].upper()
            if tft_upper == "NUMBER" or tft_upper.startswith("TINYINT") or tft_upper.startswith("INT") or tft_upper.startswith("NUMERIC") or tft_upper.startswith("BIGINT"):
                column_type = "int"
            elif tft_upper == "BOOL":
                column_type = "BOOLEAN"
            elif tft_upper in ("STRING", 'MEDIUMTEXT') or tft_upper.startswith("TIMESTAMPTZ"):
                column_type = "String"
            elif tft_upper.startswith("VARCHAR"):
                column_type = tft_upper
            else:
                column_type = "text"
            field = f"{column_name.lower()} {column_type} COMMENT '{column_comment}'"
            field_comment = f"COMMENT ON COLUMN {table_name}.{column_name} IS '{column_comment}';"
            fields.append(field)
            fields_comment.append(field_comment)
        all_field = ",\t".join(fields)
        all_field_comment = "\r\n".join(fields_comment)
        sqls = f"""
-- {table_name}
CREATE TABLE IF NOT EXISTS {table_name}({all_field}) ENGINE = MergeTree() ORDER BY tuple();
;

                """
        return sqls
