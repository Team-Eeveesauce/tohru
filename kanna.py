import socket
import subprocess
import os
from eskcompro import server
from dotenv import load_dotenv
from win11toast import toast

# Define singular variable
load_dotenv()
PORT = int(os.getenv('PORT'))

# Define special commands
def runme(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        return(b"no")
    else:
        print(result.stdout)
        return(b"ok")

# Show toast ontifcations in Windows on certain occasions
def show_notification(title, message):
  toast(title, message)

def on_recv(data: dict, client:int):
    print(f'Connected to {s.get_client(client).getpeername()[0]}')

    print(f"Received: {data['data']}")

    # Message Handling Logic
    if data['data'] == 'connect':
        print("Was pinged! Sent a reply.")
        show_notification("Kanna", "You've been pinged!")
        reply = "ok"
    # elif data.decode() == 'gaming':
    #     print("Opening Epic Launcher...")
    #     reply = runme("\"C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe\"")
    #     conn.sendall(b"ok")
    elif data['data'] == 'emby':
        print("Restarting Emby... Probably.")
        reply = runme("\"E:\\Streamable - The Return\\Emby-Server\\system\\EmbyServer.exe\"")
        show_notification("Kanna", "Emby is restarting!")
    elif data.decode() == 'download_spigg':
        reply = "no"
        print("Downloading spigg... OR NOT!!")
    elif data['data'] == 'restart':
        reply = "no"
        print("Restarting bot... OR NOT!!")
    else:
        reply = "bad"
        print("Command failed!")
        show_notification("Kanna", "Recieved bad command from Tohru!")

    s.send(reply, 'b64', client)
    show_notification("Kanna", "Apparently we replied too...")

s = server(port=PORT)
s.on_receive = on_recv
print("Kanna active!")
show_notification("Kanna", "Kanna service is active!")
s.start()