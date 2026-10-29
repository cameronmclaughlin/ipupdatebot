import mcstatus

try:
    server = mcstatus.JavaServer.lookup("hypixel.net")
    status = server.query()
    print(f"The server has {status.players.online} player(s) online and replied in {status.latency} ms")
except Exception as e:
    print(f"Couldn't reach the given server: {e}")