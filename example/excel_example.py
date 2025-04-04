from easybd.conf import JDBCConf
from easybd.datax import DataXReaderType
from easybd.datax.datax_type import DataXWriterType
from easybd.db.ddl import DDLType
from easybd.excel import Excel


if __name__ == '__main__':
    # f = "D:\wjn\gitee\jzDataMigrate\jz2.xlsm"
    f = "D:\wjn\gitee\schooletl-tx\doc\表结构.xlsx"
    t = Excel(f, sheet_name='ods', table_name="ods_sjzx_dwt_gxxs_xsjbsjzl")
    # ddl = t.to_ddl2(DDLType.PgSql)
    # print(ddl)

    # source_host = "172.23.0.193"
    # source_port = 5432
    # source_db = "school"
    # source_user = "postgres"
    # source_password = "Pgsql@2024"
    # jdbc_conf = JDBCConf("pgsql", source_host, source_port, source_db, source_user, source_password)

    # source_host = "172.31.24.131"
    # source_port = 5432
    # source_db = "school"
    # source_user = "postgres"
    # source_password = "Pgsql@2024"
    # jdbc_conf = JDBCConf("pgsql", source_host, source_port, source_db, source_user, source_password)

    source_host = "10.200.10.22"
    source_port = 5432
    source_db = "schooletl"
    source_user = "postgres"
    source_password = "Pgsql@2024"
    jdbc_conf = JDBCConf("pgsql", source_host, source_port, source_db, source_user, source_password)


    # target_host = "47.97.35.199"
    # target_port = 54321
    # target_db = "jz"
    # target_user = "postgres"
    # target_password = "Pgsql@2024"
    # target_jdbc_conf = JDBCConf("pgsql", target_host, target_port, target_db, target_user, target_password)

    target_host = "47.97.35.199"
    target_port = 54321
    target_db = "tx"
    target_user = "postgres"
    target_password = "Pgsql@2024"
    target_jdbc_conf = JDBCConf("pgsql", target_host, target_port, target_db, target_user, target_password)

    r = t.to_datax(DataXReaderType.PGSQL, DataXWriterType.PGSQL, t.table_meta[0], jdbc_conf, target_jdbc_conf)
    print(r)

    # r = t.to_json_array2()
    # print(r)