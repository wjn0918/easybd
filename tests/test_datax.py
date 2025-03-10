from easybd.datax import DataX


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


DataX(job_name,job_content)