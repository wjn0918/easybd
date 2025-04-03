a = '{     "readerJdbcUrl": "jdbc:postgresql://10.200.10.22:5432/schooletl",     "readerUserName": "postgres",     "readerPassword": "Pgsql@2024",     "writerJdbcUrl": "jdbc:postgresql://192.168.3.205:5432/schooletl",     "writerUserName": "postgres",     "writerPassword" "Pgsql@2024"  }'


import json

b = json.loads(a)

print(b)