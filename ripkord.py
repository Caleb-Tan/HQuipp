from lomond import WebSocket
import ast

authorization = {"payload":{"build":2249,"phoneNumber":"16502507495","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2ZW5kb3JJZCI6Imo4NFRsNmRaTEciLCJwaG9uZU51bWJlciI6IjE2NTAyNTA3NDk1IiwiY29kZSI6Ijc5NDUiLCJpYXQiOjE1MzM3NjAzMjF9.3FMzqceNBeHZNyRpoCk0VFhnGQrDEkMxyYCSFXgrmnk","vendorId":"e553b6ce443dd4e8"},"type":"authenticate"}

websocket = WebSocket("ws://websockets.ripkord.tv/")

authorized = False
for msg in websocket:
    print(msg)
    if msg.name == "text":
        print(msg.text)
        if ast.literal_eval(msg.text)["type"] == "ping" and not authorized:
            websocket.send_json(authorization)
        else:
            print(msg.text)


   