#coding=utf-8

'''
requires Python 3.6 or later
pip install requests
'''
import base64
import json
import os
import uuid
import requests

# 填写平台申请的appid, access_token以及cluster

def generate_voice(voice_gender,text,save_path):
    if voice_gender == "male":
        access_token = os.getenv("VOLCENGINE_TTS_MALE_ACCESS_TOKEN")
        cluster = "volcano_icl"
        appid = os.getenv("VOLCENGINE_TTS_MALE_APP_ID")
        spk_id = os.getenv("VOLCENGINE_TTS_MALE_SPK_ID")
        voice_type = spk_id
        uid = os.getenv("VOLCENGINE_TTS_MALE_UID")

    elif voice_gender == "female":
        access_token = os.getenv("VOLCENGINE_TTS_FEMALE_ACCESS_TOKEN")
        cluster = "volcano_icl"
        appid = os.getenv("VOLCENGINE_TTS_FEMALE_APP_ID")
        spk_id = os.getenv("VOLCENGINE_TTS_FEMALE_SPK_ID")
        voice_type = spk_id
        uid = os.getenv("VOLCENGINE_TTS_FEMALE_UID")
    else:
        raise ValueError("voice_gender must be 'male' or 'female'")

    if not all([access_token, appid, spk_id, uid]):
        raise ValueError(f"Missing Volcengine TTS environment variables for {voice_gender} voice")

    host = "openspeech.bytedance.com"
    api_url = f"https://{host}/api/v1/tts"
    
    header = {"Authorization": f"Bearer;{access_token}"}
    
    request_json = {
        "app": {
            "appid": appid,
            "token": "access_token",
            "cluster": cluster
        },
        "user": {
            "uid": uid
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.4,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"

        }
    }
    try:
        resp = requests.post(api_url, json.dumps(request_json), headers=header)
        print(resp)
        if "data" in resp.json():
            data = resp.json()["data"]
            file_to_save = open(save_path, "wb")
            file_to_save.write(base64.b64decode(data))
            return resp

    except Exception as e:
        e.with_traceback()

if __name__ == '__main__':
    generate_voice("male","我不认同", "male_submit.mp3")
    # try:

    #     resp = requests.post(api_url, json.dumps(request_json), headers=header)
    #     # print(f"resp body: \n{resp.json()}")
    #     if "data" in resp.json():
    #         data = resp.json()["data"]
    #         file_to_save = open("test_submit.mp3", "wb")
    #         file_to_save.write(base64.b64decode(data))
    # except Exception as e:
    #     e.with_traceback()
