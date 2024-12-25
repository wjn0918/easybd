from enum import Enum

from easybd.db.ddl.ddl_hive import DDLHive
from easybd.db.ddl.ddl_pgsql import DDLPgSql
from easybd.db.ddl.ddl_mysql import DDlMysql


class DDLType(Enum):
    HIVE = DDLHive()
    PgSql = DDLPgSql()
    Mysql = DDlMysql()