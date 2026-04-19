import os
import requests
import glob
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

QRADAR_HOST = os.environ.get('QRADAR_HOST')
QRADAR_TOKEN = os.environ.get('QRADAR_SEC_TOKEN')

HEADERS = {
    'SEC': QRADAR_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

def deploy_rule(file_path):
    with open(file_path, 'r') as f:
        rule_data = f.read()
    
    url = f"https://{QRADAR_HOST}/api/analytics/rules"
    response = requests.post(url, data=rule_data, headers=HEADERS, verify=False)
    
    if response.status_code in [200, 201, 202]:
        print(f"✅ Uğurlu: {file_path}")
    else:
        print(f"❌ Xəta ({file_path}): {response.status_code} - {response.text}")

rule_files = glob.glob('detections/qradar/*.json')
for rule in rule_files:
    deploy_rule(rule)
