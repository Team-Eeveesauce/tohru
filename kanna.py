import socket
import subprocess
import os
from dotenv import load_dotenv
from win11toast import notify

# Define singular variable
load_dotenv()
PORT = int(os.getenv('PORT'))

# Define special command to run other commands on the machine.
def runme(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
        return(b"no")
    else:
        print(result.stdout)
        return(b"ok")

# Main loop
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(("0.0.0.0", PORT))
    s.listen()
    print("Kanna active!")
    notify("Kanna", "Kanna is now active!")

    while True:
        print("Waiting for something to do...")
        conn, addr = s.accept()
        with conn:
            print(f'Connected to {addr}')
            data = conn.recv(1024)
            if not data:
                break

            print(f"Received: {data.decode()}")

            # Message Handling Logic
            if data.decode() == 'connect':
                print("Was pinged! Sent a reply.")
                notify("Kanna", "You've been pinged!")
                reply = b"ok"
            # elif data.decode() == 'gaming':
            #     print("Opening Epic Launcher...")
            #     reply = runme("\"C:\\Program Files (x86)\\Epic Games\\Launcher\\Portal\\Binaries\\Win32\\EpicGamesLauncher.exe\"")
            #     conn.sendall(b"ok")
            elif data.decode() == 'emby':
                print("Restarting Emby... Probably.")
                reply = runme("\"E:\\Streamable - The Return\\Emby-Server\\system\\EmbyServer.exe\"")
                notify("Kanna", "Emby is restarting!")
            elif data.decode() == 'download_spigg':
                conn.sendall(b"no")
                print("Downloading spigg... OR NOT!!")
            elif data.decode() == 'restart':
                conn.sendall(b"no")
                print("Restarting bot... OR NOT!!")
            else:
                reply = b"bad"
                print("Command failed!")
                notify("Kanna", "Recieved bad command from Tohru!")

            conn.sendall(reply)
            notify("Kanna", "And... we replied back!")
