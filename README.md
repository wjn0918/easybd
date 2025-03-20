A common utils to use 

# db utils

## table info export to excel 

```python
from easybd.db import Mysql
mysql = Mysql("192.168.3.204", "3306", "root", "Mysql@2023", "cs", ["t_a", "t_b"])
mysql.table_info_to_excel("demo.xlsx")

```
<p align="center">
<img src="imgs/dbutil_mysql_01.png"  alt="image" width="300" height="auto">
<img src="imgs/dbutil_mysql_02.png"  alt="image" width="300" height="auto">
</p>


# excel utils
depend on above export excel to output some code,like : ddl, json files

```python
from easybd.conf import JDBCConf
from easybd.datax import DataXReaderType
from easybd.datax.datax_type import DataXWriterType
from easybd.db.ddl import DDLType
from easybd.excel import Excel


if __name__ == '__main__':
    t = Excel("D:\wjn\gitee\schooletl-tx\doc\表结构.xlsx", sheet_name='ads', table_name="t_dorm_access_record")
    ddl = t.to_ddl2(DDLType.HIVE)
    print(ddl)

    source_host = "172.23.0.193"
    source_port = 5432
    source_db = "school"
    source_user = "postgres"
    source_password = "Pgsql@2024"
    jdbc_conf = JDBCConf("pgsql", source_host, source_port, source_db, source_user, source_password)
    r = t.to_datax(DataXReaderType.PGSQL, DataXWriterType.HIVE, t.table_meta[0], jdbc_conf)
    print(r)
```


## DATAX UTILS

```python
from easybd.datax import DataX

import os
# 指定DATAX_HOME  或者在环境变量中配置
os.environ['DATAX_HOME'] = '/home/wjn/soft/datax'


job_name = 'hello_datax'
job_content = {
    "job": {
      "content": [
        {
          "reader": {
            "name": "streamreader",
            "parameter": {
              "sliceRecordCount": 10,
              "column": [
                {
                  "type": "long",
                  "value": "10"
                },
                {
                  "type": "string",
                  "value": "hello，你好，世界-DataX"
                }
              ]
            }
          },
          "writer": {
            "name": "streamwriter",
            "parameter": {
              "encoding": "UTF-8",
              "print": True
            }
          }
        }
      ],
      "setting": {
        "speed": {
          "channel": 5
         }
      }
    }
  }


datax = DataX(job_name,job_content)
datax.run()

```


