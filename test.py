import requests
import json
import os
import time

URL = 'http://127.0.0.1:8000'

def color(text, color):
    colors = {
        'blue': '\033[94m',
        'red': '\033[91m',
        'green': '\033[92m',
        'reset': '\033[0m'
    }

    colored_text = f"{colors[color]}{text}{colors['reset']}"
    print(colored_text)

def login(username, password):
    json_data = {
        'username': username,
        'password': password,
    }

    response = requests.post(f'{URL}/api/token', json=json_data)
    if response.status_code == 200:
        color("[+] Login work !", "green")
    else:
        color("[-] Login dont work !", "red")

    return json.loads(response.text)["access"]

def register(username, password, age, shared, contacted):
    json_data = {
        "username": username, 
        "password": password,
        "age": age, 
        "can_be_contacted": shared, 
        "can_data_be_shared": contacted
    }

    response = requests.post(f'{URL}/api/register', json=json_data)
    if response.status_code == 201:
        color("[+] Registration work !", "green")
    elif "UNIQUE constraint failed: user_myuser.username" in response.text:
        color("[i] Registration fails because user already exist", "blue")
    else:
        color("[-] Error registration fails", "red")



def create_project(token):

    header = {
        "Authorization" : f"Bearer {token}"
    }

    json_data = {
        "name": "test", 
        "description": "porject 0 for test", 
        "type": "backend"
    }
    response = requests.post(f'{URL}/api/project', headers=header, json=json_data)
    if response.status_code == 201:
        color("[+] Project creation work !", "green")
    else:
        color("[-] Project creation dont work !", "red")
    # print(response.text)

def get_all_project(token):
    header = {
        "Authorization" : f"Bearer {token}"
    }
    response = requests.get(f'{URL}/api/project', headers=header)

    if response.status_code == 200:
        color("[+] Get all project work !", "green")
    else:
        color("[-] Get all project dont work !", "red")

    return json.loads(response.text)[-1]["id"]


def get_one_project(token, project, iscontributor):
    header = {
        "Authorization" : f"Bearer {token}"
    }
    response = requests.get(f'{URL}/api/project/{project}', headers=header)

    
    
    if response.status_code == 200 and iscontributor:
        color("[+] Get one project work !", "green")
    elif not iscontributor:
        color("[+] No broken access on get one project", "green")
    else:
        color("[-] Get one project dont work !", "red")

    if iscontributor:
        res = json.loads(response.text)["issues"]
        if res:
            return res[0]["id"]
    

def create_issue(token, project_id):

    header = {
        "Authorization" : f"Bearer {token}"
    }

    json_data = {
        "project_id" : project_id, 
        "name": "Example Issue", 
        "description": "This is a sample issue description.", 
        "priority": "MEDIUM", 
        "tag": "BUG", 
        "status": "To Do"
    }
    response = requests.post(f'{URL}/api/issue', headers=header, json=json_data)

    if response.status_code == 201:
        color("[+] Issue creation work !", "green")
    else:
        color("[-] Issue creation dont work !", "red")



def create_comment(token, issue_id):

    header = {
        "Authorization" : f"Bearer {token}"
    }

    json_data = {
        "issue_id" : issue_id, 
        "content": "first comment for testing"
    }

    response = requests.post(f'{URL}/api/comment', headers=header, json=json_data)

    if response.status_code == 201:
        color("[+] Comment creation work !", "green")
    else:
        color("[-] Comment creation dont work !", "red")


def get_one_issue(token, issue_id, iscontributor):
    header = {
        "Authorization" : f"Bearer {token}"
    }
    response = requests.get(f'{URL}/api/issue/{issue_id}', headers=header)
    

    if response.status_code == 200 and iscontributor:
        color("[+] Get one issue work !", "green")
    elif not iscontributor:
        color("[+] No broken access on get one issue", "green")
    else:
        color("[-] Get one issue dont work !", "red")

    if iscontributor:
        res = json.loads(response.text)["comments"]
        if res:
            return res[0]["id"]


def add_contributor(token, project_id):
    header = {
        "Authorization" : f"Bearer {token}"
    }
    response = requests.get(f'{URL}/api/contributor/del_add/{project_id}', headers=header)
    if response.status_code == 201:
        color("[+] Add contributor work !", "green")
    else:
        color("[-] Add contributor dont work !", "red")


if __name__ == "__main__":
    color("[i] Checking normal usage...\n", "blue")
    # test user login/register
    username1 = os.urandom(8).hex() 
    register(username1,"test", 18, False, False)
    register('test',"test", 18, False, False)
    
    user1 = login(username1, "test")
    user2 = login("test","test")
    
    # project test
    create_project(user1)
    project_user1 = get_all_project(user1)
    get_one_project(user1, int(project_user1), True)
    
    #issue test
    create_issue(user1, int(project_user1))
    issue_user1 = get_one_project(user1, int(project_user1), True)
    get_one_issue(user1, issue_user1, True)
    
    #comment test
    create_comment(user1, issue_user1)
    comment_user1 = get_one_issue(user1, issue_user1, True)
    

    color("\n[i] Checking for broken access...\n", "blue")
    get_all_project(user2)
    get_one_project(user2, project_user1, False)
    get_one_issue(user2, issue_user1, False)

    color("\nAdding user2 to contributor...\n", "blue")
    add_contributor(user2, project_user1)
    get_one_project(user2, project_user1, True)
    get_one_issue(user2, issue_user1, True)

