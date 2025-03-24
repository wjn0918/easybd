from easybd.db import PostgreSql,Mysql

def test_pg():
    # pg = PostgreSql("192.168.3.205", "5432", "postgres", "Pgsql@2024", "park-preview", "public",
    #                 table_names=['ads_t_dp_ryzt'])

    pg = PostgreSql("192.168.3.205", "5432", "postgres", "Pgsql@2024", "park-preview", "public")
    pg.table_info_to_excel("demo.xlsx",True)


def test_mysql():
    m = Mysql("192.168.3.204","3306", "root", "Mysql@2023", "zjioc_202", ["vehicle_access"])
    m.table_info_to_excel("demo.xlsx")