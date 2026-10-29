import mcstatus

server = mcstatus.JavaServer("mc.mineberry.org", 25565)
try:
    status = server.query()
    print(f"MOTD: {status.motd}")
    print(f"Online Count: {status.players.online}/{status.players.max}")
    playerString = ""
    for player in status.players.list:
        playerString+=f"{player}\n"
    print(f"Players:\n{playerString}")
except Exception as e:
    print("Server is probably offline")
    print(f"RESPONSE: {e}")