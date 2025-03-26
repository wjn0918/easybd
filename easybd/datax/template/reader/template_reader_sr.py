import json
import logging

from easybd.db import ETLTableInfo
from easybd.datax.template import hive2datax


class TemplateReaderSr:
    """
    海康api reader
    """

    def __call__(self, *args):
        if len(args) < 2:
            logging.warning("参数缺失")
            return {}
        table_info: ETLTableInfo = args[0]
        columns = table_info.table_info.table_fields

        template_reader_hdfs = {
            "name": "srapireader",
            "parameter": {
                "appId": "xyeiwdwmzezuek52qtnfjn57xwgixddp",
                "appSecret": "ZNYF4UjoBlwHPn_wlEpXwGzH2h3eLDKm37Y_g6zR8bMrXNe2m9y802iKgWCidCh3",
                "compId": "fbc84d69b8f682ca33c3e32a877111e9",
                "dataPath": "result.records",
                "debug": False,
                "body": {
                    "tag": "733",
                    "current": "1",
                    "size": "1000",
                    "search": "",
                    "timenode": "",
                    "orderBy": "xh",
                    "isAsc": "1"
                },
                "columns": columns
            }
        }
        return template_reader_hdfs
