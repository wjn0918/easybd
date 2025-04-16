from easybd.db import Mysql

def test_mysql():
    mysql = Mysql("192.168.3.204", "3306", "root", "Mysql@2023", "cs", ["t_a", "t_b"])
    mysql.table_info_to_excel("demo.xlsx")



from easybd.db import PostgreSql

def test_pg():
    pg = PostgreSql("192.168.3.205", "5432", "postgres", "Pgsql@2024", "park-preview", "public",
                    table_names=["t_dict", "t_visitor_apply"])
    pg.table_info_to_excel("demo.xlsx")


if __name__ == '__main__':
    test_pg()