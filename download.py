import json
import os
import random
import string
import time
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import requests



def listDWdirs():
    return [i for i in os.listdir() if os.path.isdir(i) and i not in ["venv", ".idea", ".git"]]

def getDWlinks(dir_name :str):
    with open(dir_name + "/links.txt", "r") as f:
        return [i.strip() for i in f.readlines() if "vip.linuxia.ir" in i]

def upload_folder(folder_name: str):
    gauth = GoogleAuth()
    # Try to load saved client credentials
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    drive = GoogleDrive(gauth)
    folder = drive.CreateFile({'title': folder_name, "mimeType": "application/vnd.google-apps.folder", "parents": [{"kind": "drive#fileLink", "id": "#TODO"}]}) ###TODO: add own gdrive folder
    folder.Upload()
    for i in os.listdir(folder_name):
        file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folder["id"]}], "title": i})
        file.SetContentFile(folder_name + "/" + i)
        file.Upload()


def addDWlink(folder: str, link: str):
    status = requests.head(link).status_code
    if status != 200:
        print("Link", link, "is dead")
        return
    data = json.dumps({
   "jsonrcp":"2.0",
   "id":"dw",
   "method":"aria2.addUri",
   "params":[
       [
         link
       ],
      {
         "dir":folder,
          "max-connection-per-server" : "16",
          "max-concurrent-downloads" : "16",
          "split" : "6",
      }
   ]
})
    response = requests.post('http://localhost:6800/jsonrpc', data=data)
    data = json.dumps({'jsonrpc':'2.0', 'id':"".join(random.choice(string.ascii_lowercase) for i in range(15)), 'method':'aria2.tellStatus', 'params':[json.loads(response.text)["result"]]})
    done = False
    while not done:
        response = requests.post('http://localhost:6800/jsonrpc', data=data)
        print(json.loads(response.text)["result"])
        if json.loads(response.text)["result"]["status"] == "complete":
            done = True
        time.sleep(1)

folders = listDWdirs()
print(folders)
for i in folders:
    dwlinks = getDWlinks(i)
    if len(dwlinks) == 0:
        print("No links found in", i)
        continue
    print("Downloading", i)
    print(dwlinks)
    print(i)
    for j in dwlinks:
        addDWlink(i, j)
    print("Done", i)
    upload_folder(i)
    print("Uploaded", i)
    input("TEST CHECK")
    print("Deleting", i)
    os.system("rm -rf " + i)