from lomond import WebSocket
from lomond.persist import persist
import ast

authorization = {"payload":{"build":2249,"phoneNumber":"16502507495","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZW5kb3JJZCI6Imo4NFRsNmRaTEciLCJwaG9uZU51bWJlciI6IjE2NTAyNTA3NDk1IiwiY29kZSI6Ijc5NDUiLCJpYXQiOjE1MzM3NjAzMjF9.3FMzqceNBeHZNyRpoCk0VFhnGQrDEkMxyYCSFXgrmnk","vendorId":"e553b6ce443dd4e8"},"type":"authenticate"}

websocket = WebSocket("ws://websockets.ripkord.tv/")
websocket_fngenius = WebSocket("wss://platform.fox.getplaytrivia.com/s/894/default/comm")

authorized = False
counter = 0

for msg in persist(websocket):
    counter += 1
    if msg.name == "poll" and not authorized:
        websocket.send_json(authorization)
        authorized = True
    else:
        try:
            q = ast.literal_eval(msg.text)
            print(q)
            if q["type"] == "incomingQuestion":
                print(q["payload"])
            elif q["type"] == "ping":
                websocket.send_json(authorization)
        except:
            pass



   