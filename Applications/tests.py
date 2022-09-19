import requests
import json
from datetime import datetime


def get_event_id():
    dd = datetime.now()
    time = dd.strftime("%d:%m:%Y,%H:%M:%S")
    url = "https://100003.pythonanywhere.com/event_creation"

    data = {
        "platformcode": "FB",
        "citycode": "101",
        "daycode": "0",
        "dbcode": "pfm",
        "ip_address": "192.168.0.41",
        "login_id": "lav",
        "session_id": "new",
        "processcode": "1",
        "regional_time": time,
        "dowell_time": time,
        "location": "22446576",
        "objectcode": "1",
        "instancecode": "100051",
        "context": "afdafa ",
        "document_id": "3004",
        "rules": "some rules",
        "status": "work",
        "data_type": "learn",
        "purpose_of_usage": "add",
        "colour": "color value",
        "hashtags": "hash tag alue",
        "mentions": "mentions value",
        "emojis": "emojis",

    }

    r = requests.post(url, json=data)
    return r.text


task_id = "63031112e91010402286fdd2"
task_object = {"user": "GeorgeTesting(Updated)", "title": "This is just an updated task",
               "description": "This is just an updated test description", "status": "Complete"}


def update_task(task_id: str, task_object: dict):
    url = "http://100002.pythonanywhere.com/"
    payload = json.dumps({
        "cluster": "hr_hiring",
        "database": "hr_hiring",
        "collection": "tasks",
        "document": "tasks_reports",
        "team_member_ID": "10005504",
        "function_ID": "ABCDE",
        "command": "update",
        "field": {"_id": task_id},
        "update_field": task_object,
        "platform": "bangalore"
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response


update_task(task_id, task_object)
