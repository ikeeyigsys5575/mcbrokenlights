import requests

url = "https://mcbroken.com/markers.json"


response = requests.get(url)

if response.status_code == 200:
    print("Received!")
    print(response.json())
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")