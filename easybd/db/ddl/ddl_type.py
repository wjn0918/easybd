from enum import Enum

from easybd.db.ddl.ddl_clickhouse import DDLClickHouse
from easybd.db.ddl.ddl_hive import DDLHive
from easybd.db.ddl.ddl_pgsql import DDLPgSql
from easybd.db.ddl.ddl_mysql import DDlMysql


class DDLType(Enum):
    HIVE = DDLHive()
    PGSQL = DDLPgSql()
    MYSQL = DDlMysql()
    CLICKHOUSE = DDLClickHouse()