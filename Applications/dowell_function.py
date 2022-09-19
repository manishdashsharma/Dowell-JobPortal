from asyncio import streams
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


def save_candidate(candidate):
    url = "http://100002.pythonanywhere.com/"
    # searchstring="ObjectId"+"("+"'"+"6139bd4969b0c91866e40551"+"'"+")"
    payload = json.dumps({
        "cluster": "hr_hiring",
        "database": "hr_hiring",
        "collection": "candidate_view",
        "document": "candidate_view",
        "team_member_ID": "1000553",
        "function_ID": "ABCDE",
        "command": "insert",
        "field": {
            "eventId": get_event_id(),
            "candidate_data": candidate
        },
        "update_field": {"order_nos": 21},
        "platform": "bangalore"
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def save_task(task):
    url = "http://100002.pythonanywhere.com/"
    payload = json.dumps({
        "cluster": "hr_hiring",
        "database": "hr_hiring",
        "collection": "tasks",
        "document": "tasks_reports",
        "team_member_ID": "10005504",
        "function_ID": "ABCDE",
        "command": "insert",
        "field": {
            "eventId": get_event_id(),
            "task_details": task
        },
        "update_field": {"order_nos": 21},
        "platform": "bangalore"
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    _id = response.text.split(" ")[3].strip("}").strip('"')
    # print(_id)
    return _id


def update_task_data(task_id: str, task_object: dict):
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
        "update_field": {"task": task_object},
        "platform": "bangalore"
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    return response


def save_application(document_name: str, member_id: str, application):
    url = "http://100002.pythonanywhere.com/"
    payload = json.dumps({
        "cluster": "hr_hiring",
        "database": "hr_hiring",
        "collection": document_name,
        "document": document_name,
        "team_member_ID": member_id,
        "function_ID": "ABCDE",
        "command": "insert",
        "field": {
            "eventId": get_event_id(),
            "application_details": application
        },
        "update_field": {"order_nos": 21},
        "platform": "bangalore"
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)


def save_to_teamleadview(application):
    url = "http://100002.pythonanywhere.com/"
    payload = json.dumps({
        "cluster": "hr_hiring",
        "database": "hr_hiring",
        "collection": "teamlead_view",
        "document": "teamelead_view",
        "team_member_ID": "1000552",
        "function_ID": "ABCDE",
        "command": "insert",
        "field": {
            "eventId": get_event_id(),
            "full_name": application
        },
        "update_field": {"order_nos": 21},
        "platform": "bangalore"
    })
    headers = {'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
