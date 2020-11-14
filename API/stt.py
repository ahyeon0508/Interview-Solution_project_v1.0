import requests
import json
kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

rest_api_key = '3a27a613233efd4a36b3e1eea4d9580c'

headers = {
    "Content-Type": "application/octet-stream",
    "X-DSS-Service": "DICTATION",
    "Authorization": "KakaoAK " + rest_api_key,
}

with open('voice.wav', 'rb') as fp:
    audio = fp.read()

res = requests.post(kakao_speech_url, headers=headers, data=audio)

print(res.text)
result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
result = json.loads(result_json_string)
print(result)
print(result['value'])