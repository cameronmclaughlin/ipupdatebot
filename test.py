import mcstatus

server = mcstatus.JavaServer("192.168.0.128", 25565)
try:
    status = server.status()
    print(f"MOTD: {status.motd.raw}")
    print(f"Online Count: {status.players.online}/{status.players.max}")
    print(f"Latency: {int(status.latency)}ms")
    playerString = ""
    if status.players.sample:
        for player in status.players.sample:
            playerString+=f"\n{player.name}"
    print(f"Players online:{playerString}")
except Exception as e:
    print("Server is probably offline")
    print(f"RESPONSE: {e}")