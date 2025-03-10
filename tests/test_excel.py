from easybd.conf import JDBCConf
from easybd.datax import DataXReaderType
from easybd.datax.datax_type import DataXWriterType
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
    t = Excel("D:\wjn\yx\schooletl\doc\sr\etl_schema.xlsx", table_name="ods_sr_hz_hik_person")
    # t = Excel("D:\wjn\gitee\schooletl\scripts\表结构_江西.xls", sheet_name="ads_new", table_name="ads_student")
    # t = Excel("D:\wjn\gitee\jzDataMigrate\jz2.xlsm", sheet_name='ods', table_name="ods_tx2_bsdt_zkbxx")

    source_host = "172.23.0.193"
    source_port = 5432
    source_db = "school"
    source_user = "postgres"
    source_password = "Pgsql@2024"
    jdbc_conf = JDBCConf("pgsql", source_host, source_port, source_db, source_user, source_password)

    r = t.to_datax(DataXReaderType.HDFS, DataXWriterType.PGSQL, t.table_meta[0], jdbc_conf)
    ddl = t.to_ddl2(DDLType.PgSql)
    print(ddl)
    print(t.to_json_array2())


    print(r)

    assert 1 == 1



#

# if __name__ == '__main__':
#     t = Excel("D:\wjn\gitee\schooletl-tx\doc\表结构.xlsx", table_name="ads_t_dp_xsssjc")
#     # t = Excel("D:\wjn\yx\schooletl\doc\sr\etl_schema.xlsx", table_name="ods_sr_hz_hik_person")
#     ddl = t.to_ddl2(DDLType.PgSql)
#     print(ddl)
#     # print(t.to_json_array2())