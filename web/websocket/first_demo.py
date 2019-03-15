import websocket

# https://github.com/websocket-client/websocket-client

ws = websocket.WebSocket()
ws.connect("ws://192.168.10.6:54435")
ws.send("hi")
