from easybd.db.ddl import DDLType
from easybd.excel import Excel


# e = Excel("D:\wjn\gitee\schooletl-tx\doc\表结构.xlsx")
# table = e.get_table("ods_hik_region")

# def test_ddl2pg():
#     r = e.to_ddl(DDLType.PgSql, table.table_info)
#     print(r)
#
# def test_to_json_array():
#     e.to_json_array(table)


def test_ddl2pg():
    # t = Excel("D:\wjn\gitee\schooletl-tx\doc\表结构.xlsx", sheet_name="ads", table_name="ads_t_dp_xsssjc")
    # t = Excel("D:\wjn\yx\schooletl\doc\sr\etl_schema.xlsx", table_name="ods_sr_hz_hik_person")
    t = Excel("D:\wjn\gitee\schooletl\scripts\表结构_江西.xls", sheet_name="ods_new", table_name="ods_org")


    ddl = t.to_ddl2(DDLType.Mysql)
    print(ddl)

# if __name__ == '__main__':
#     t = Excel("D:\wjn\gitee\schooletl-tx\doc\表结构.xlsx", table_name="ads_t_dp_xsssjc")
#     # t = Excel("D:\wjn\yx\schooletl\doc\sr\etl_schema.xlsx", table_name="ods_sr_hz_hik_person")
#     ddl = t.to_ddl2(DDLType.PgSql)
#     print(ddl)
#     # print(t.to_json_array2())