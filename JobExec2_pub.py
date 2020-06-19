params = {}
params['apikey'] = 'xxxxxxxx'
params['token_url'] = "https://iam.cloud.ibm.com/oidc/token"
params['token_data'] = "apikey=" + params['apikey'] + "&grant_type=urn:ibm:params:oauth:grant-type:apikey"
params['token_headers'] = { "Content-Type" : "application/x-www-form-urlencoded" }
params['project_id'] = "xxxxxxxx"
params['url'] = "https://api.dataplatform.cloud.ibm.com"

import requests

#IAMのトークン取得
iam_response  = requests.post( params['token_url'], headers=params['token_headers'], data=params['token_data'] )
bearer_token = "Bearer " + iam_response.json()["access_token"]

project_id =params['project_id']
url=params['url']
headers = {
    'Authorization': bearer_token,
    'Content-Type': 'application/json'
}

# Job list取得
response = requests.get(url+"/v2/jobs?project_id="+project_id, headers=headers).json()
response

MyJobName="JobTestJob"
job_id=next(v['metadata']['asset_id'] for v in response['results'] if v['metadata']['name'] ==MyJobName)
job_id

#ジョブ実行のパラメーター
jobrunpost = {
  "job_run": {
      "configuration" : {
          "env_variables" :  ["MYENV1=100"] 
      }
  }
}

# Run job
response = requests.post(url+"/v2/jobs/"+job_id+"/runs?project_id="+project_id, headers=headers, json=jobrunpost).json()

# Job run id
job_run_id = response['metadata']['asset_id']

#Jobの終了を確認
import time
retry_times=12
retry_sleep=3
    
for i in range(retry_times):
    response = requests.get(url+"/v2/jobs/"+job_id+"/runs/"+job_run_id+"?project_id="+project_id, headers=headers).json()
    jobstatus = response['entity']['job_run']['state']
    print(jobstatus)
    if jobstatus not in ['Starting', 'Running']: 
        break
    time.sleep(retry_sleep)
    if i==retry_times-1:
        print("Time up")