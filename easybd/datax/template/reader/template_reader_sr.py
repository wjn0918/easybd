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
        columns_lower = [col.lower() for col in columns]

        template_reader_hdfs = {
            "name": "srapireader",
            "parameter": {
                "appId": "",
                "appSecret": "",
                "compId": "",
                "dataPath": "result.records",
                "debug": False,
                "body": {

                },
                "columns": columns_lower
            }
        }
        return template_reader_hdfs
