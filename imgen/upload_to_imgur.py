import base64
import requests
import sys

def upload_to_imgur(file_path):
    client_id = "546c25a59c58ad7"
    url = "https://api.imgur.com/3/image"
    
    with open(file_path, "rb") as f:
        img_data = f.read()
        
    headers = {"Authorization": f"Client-ID {client_id}"}
    payload = {
        "image": base64.b64encode(img_data),
        "type": "base64"
    }
    
    response = requests.post(url, headers=headers, data=payload)
    if response.status_code == 200:
        link = response.json()["data"]["link"]
        print(link)
    else:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)

if __name__ == "__main__":
    upload_to_imgur("linkedin_lobster_team_v3.png")
