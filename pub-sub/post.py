import requests

while True:
    message = input("Message for sending : ")
    res = requests.post('http://localhost:6666/pubsub/test', json={"data": message})
    if res.ok:
        print(res.json())
