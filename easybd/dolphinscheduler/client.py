import requests
import json

token = "080d2dfc2c03e6c36206cfeb06a786da"
project_code = "18431384874816"
base_url = "http://192.168.3.204:12345/dolphinscheduler"




def create_wf(wk_name:str):
    headers = {
        "token": token
    }
    r = requests.get(
        "http://192.168.3.204:12345/dolphinscheduler/projects/18431384874816/task-definition/gen-task-codes?genNum=1",
        headers=headers)
    task_code = json.loads(r.text)['data'][0]
    task_name = "cs"
    taskDefinitionJson = [{"code":task_code,"delayTime":"0","description":"","environmentCode":10921715154496,"failRetryInterval":"1","failRetryTimes":"0","flag":"YES","name":task_name,"taskParams":{"localParams":[],"rawScript":"cs","resourceList":[]},"taskPriority":"MEDIUM","taskType":"SHELL","timeout":0,"timeoutFlag":"CLOSE","timeoutNotifyStrategy":"","workerGroup":"default","cpuQuota":-1,"memoryMax":-1,"taskExecuteType":"BATCH"}]
    taskRelationJson = [{"name":"","preTaskCode":0,"preTaskVersion":0,"postTaskCode":task_code,"postTaskVersion":0,"conditionType":"NONE","conditionParams":{}}]
    locations = [{"taskCode":task_code,"x":407.84661865234375,"y":-29.71307373046875}]
    name = wk_name
    tenantCode = "default"


    form_data = {
        "name": wk_name,                      # 工作流名称
        "tenantCode": "default",
        "description": "",                    # None 不行，传空字符串
        "globalParams": json.dumps([]),
        "timeout": "0",
        "executionType": "PARALLEL",
        "taskRelationJson": json.dumps(taskRelationJson),
        "taskDefinitionJson": json.dumps(taskDefinitionJson),
        "locations": json.dumps(locations)
    }

    # 5. 注意 DS 要求 form 方式，不是 json
    headers = {
        "token": token,
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"
    }

    # 6. 提交创建工作流定义
    url = f"{base_url}/projects/{project_code}/process-definition"
    r = requests.post(url, data=form_data, headers=headers)

    print("请求返回状态:", r.status_code)
    print("返回内容:", r.text)