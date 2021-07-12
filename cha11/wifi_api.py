import urllib.request
import json

url = 'http://openapi.seoul.go.kr:8088/(인증키)/json/TbPublicWifiInfo/1/5'
response = urllib.request.urlopen(url)
json_str = response.read().decode('utf-8')
data = json.loads(json_str)
print(json.dumps(data, indent=4, ensure_ascii=False))

#for row in data['TbPublicWifiInfo']['row']:
#  print(row['GU_NM'])