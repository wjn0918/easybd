
import pandas as pd

from api.data_ly import *
import json


def transformer_data(df, end_num, columns=['value', 'title']):
  """
  :param df:
  :param end_num:
  :param columns: 需要返回的列
  :return:
  """

  df['key'] = df['value'].str[0:end_num]
  return df.groupby('key').apply(
    lambda x: x[columns].to_dict('records')
  ).to_dict()



if __name__ == '__main__':

  # regionData['provinces'] = data_pro
  # 拼接市
  cities = transformer_data(pd.DataFrame(data_city), 2)

  areas = transformer_data(pd.DataFrame(data_area), 4)

  nt = transformer_data(pd.DataFrame(data_nt), 6, ['value', 'title', "imgSrc"])

  r = json.dumps(areas,ensure_ascii=False)

  with open('data.json', 'w', encoding='utf8') as fw:

    fw.write(r)






"""

const regionData = {
  // 省级数据
  provinces: [
    {code: '11', name: '北京市'},
    {code: '12', name: '天津市'},
    // ...
  ],
  
  // 市级数据，按省级code分组
  cities: {
    '11': [
      {code: '1101', name: '北京市'},
      // ...
    ],
    '12': [
      {code: '1201', name: '天津市'},
      // ...
    ]
  },
  
  // 县级数据，按市级code分组
  counties: {
    '1101': [
      {code: '110101', name: '东城区'},
      // ...
    ],
    // ...
  },
  
  // 乡级数据，按县级code分组
  towns: {
    '110101': [
      {code: '110101001', name: '东华门街道'},
      // ...
    ],
    // ...
  }
}
"""